import os
from typing import Dict, List, Tuple, Any

import numpy as np
import pandas as pd
import joblib

# Current typical limits (adjust if law changes)
LIMIT_80C = 150000
LIMIT_80D = 25000
LIMIT_NPS = 50000

# Model path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "itr_risk_rf.pkl")


def _safe_div(num: float, den: float) -> float:
    den = den if den not in (0, None) else 1.0
    return float(num) / float(den)


def compute_engineered_features(row: pd.Series) -> Dict[str, float]:
    """
    Compute key ratios used for explainability and rule checks.
    """
    income = float(row.get("Annual_Salary", 0.0) or 0.0)
    total_deductions = float(row.get("Total_Deductions", 0.0) or 0.0)
    donations = float(row.get("Donations_80G", 0.0) or 0.0)
    rent = float(row.get("Rent_Paid", 0.0) or 0.0)
    groceries = float(row.get("Groceries", 0.0) or 0.0)
    utilities = float(row.get("Utilities", 0.0) or 0.0)
    entertainment = float(row.get("Entertainment", 0.0) or 0.0)
    healthcare = float(row.get("Healthcare", 0.0) or 0.0)

    total_expenses = rent + groceries + utilities + entertainment + healthcare

    return {
        "deduction_ratio": _safe_div(total_deductions, income),
        "donation_ratio": _safe_div(donations, income),
        "rent_ratio": _safe_div(rent, income),
        "expense_ratio": _safe_div(total_expenses, income),
        "total_deductions": total_deductions,
        "total_expenses": total_expenses,
    }


def apply_rule_checks(row: pd.Series) -> Tuple[List[str], int, Dict[str, float]]:
    """
    Apply rule-based checks and return:
      - flags (human readable messages)
      - rule-based risk score (0–40)
      - engineered features (ratios, totals)
    """
    flags: List[str] = []
    risk_score = 0

    feat = compute_engineered_features(row)

    income = float(row.get("Annual_Salary", 0.0) or 0.0)
    inv_80c = float(row.get("Investment_80C", 0.0) or 0.0)
    med_80d = float(row.get("Medical_Insurance_80D", 0.0) or 0.0)
    nps = float(row.get("NPS_Contribution_80CCD", 0.0) or 0.0)
    donations = float(row.get("Donations_80G", 0.0) or 0.0)

    # Hard limit checks
    if inv_80c > LIMIT_80C:
        excess = inv_80c - LIMIT_80C
        flags.append(f"Section 80C claimed ₹{inv_80c:.0f}, exceeds limit by ₹{excess:.0f}.")
        risk_score += 25

    if med_80d > LIMIT_80D:
        excess = med_80d - LIMIT_80D
        flags.append(f"Section 80D claimed ₹{med_80d:.0f}, exceeds typical limit by ₹{excess:.0f}.")
        risk_score += 20

    if nps > LIMIT_NPS:
        excess = nps - LIMIT_NPS
        flags.append(f"NPS (80CCD) claimed ₹{nps:.0f}, exceeds typical limit by ₹{excess:.0f}.")
        risk_score += 15

    # Ratio-based sanity checks
    if feat["deduction_ratio"] > 0.7:
        flags.append(
            f"Total deductions are {feat['deduction_ratio']*100:.1f}% of income — unusually high."
        )
        risk_score += 20

    if feat["donation_ratio"] > 0.3:
        flags.append(
            f"Donations are {feat['donation_ratio']*100:.1f}% of income — may draw scrutiny."
        )
        risk_score += 15

    if feat["expense_ratio"] > 0.8:
        flags.append(
            f"Key expenses are {feat['expense_ratio']*100:.1f}% of income — very high."
        )
        risk_score += 10

    if income > 0 and feat["rent_ratio"] > 0.6:
        flags.append(
            f"Rent is {feat['rent_ratio']*100:.1f}% of income — unusually high in most cases."
        )
        risk_score += 10

    # Cap rule-based contribution
    risk_score = int(max(0, min(40, risk_score)))
    return flags, risk_score, feat


def _load_rf_model():
    """
    Load the RandomForest risk model from disk.
    """
    if not os.path.exists(MODEL_PATH):
        return None, None
    try:
        data = joblib.load(MODEL_PATH)
        return data.get("model"), data.get("features")
    except Exception:
        return None, None


RF_MODEL, RF_FEATURES = _load_rf_model()


def compute_ml_risk_score(row: pd.Series) -> float:
    """
    Use trained RandomForest to predict probability of 'risky' (label=1).
    Map probability to a 0–60 risk contribution.
    """
    if RF_MODEL is None or RF_FEATURES is None:
        return 0.0

    x = []
    for col in RF_FEATURES:
        x.append(float(row.get(col, 0.0) or 0.0))
    X = np.array(x, dtype=float).reshape(1, -1)

    proba = RF_MODEL.predict_proba(X)[0, 1]  # probability of risky
    ml_score = float(proba * 60.0)  # 0–60
    return ml_score


def compute_risk_for_row(row: pd.Series) -> Dict[str, Any]:
    """
    High-level entry:
      - Run rule-based checks
      - Run ML model
      - Combine into final risk score
    """
    rule_flags, rule_score, feat = apply_rule_checks(row)
    ml_score = compute_ml_risk_score(row)

    total_risk = int(max(0, min(100, rule_score + ml_score)))

    if not rule_flags and total_risk < 20:
        rule_flags.append("Your return looks normal based on current checks and model.")

    return {
        "risk_score": total_risk,
        "rule_score": int(rule_score),
        "ml_score": float(round(ml_score, 2)),
        "flags": rule_flags,
        "features": feat,
    }


def compute_risk_for_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience wrapper to be used from Streamlit.
    """
    row = pd.Series(data)
    return compute_risk_for_row(row)
