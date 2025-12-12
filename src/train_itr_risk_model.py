import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import joblib

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
MODEL_DIR = os.path.join(BASE_DIR, "models")

DATA_PATH = os.path.join(DATASETS_DIR, "final_preprocessed_dataset.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "itr_risk_rf.pkl")

# Legal/typical limits (change when law changes)
LIMIT_80C = 150000
LIMIT_80D = 25000
LIMIT_NPS = 50000


def load_base_data():
    """
    Load the cleaned dataset and keep only the numeric columns
    needed for risk modelling.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run data_preprocessing.py first.")

    df = pd.read_csv(DATA_PATH)

    required_cols = [
        "Annual_Salary",
        "Total_Deductions",
        "Taxable_Income",
        "Rent_Paid",
        "Investment_80C",
        "Medical_Insurance_80D",
        "NPS_Contribution_80CCD",
        "Home_Loan_Interest_24b",
        "Donations_80G",
        "Groceries",
        "Utilities",
        "Entertainment",
        "Healthcare",
    ]
    for c in required_cols:
        if c not in df.columns:
            df[c] = 0

    df[required_cols] = df[required_cols].fillna(0).astype(float)
    return df[required_cols]


def generate_synthetic_anomalies(base_df: pd.DataFrame, frac: float = 0.4) -> pd.DataFrame:
    """
    Generate synthetic 'risky' ITR-like cases by corrupting some rows:
      - Overclaim 80C
      - Extreme donations vs income
      - Very high rent vs salary
      - Overall deductions too high
    """
    n = len(base_df)
    n_anom = max(1, int(frac * n))
    rng = np.random.default_rng(42)

    sample = base_df.sample(n_anom, random_state=42).copy()

    for idx in sample.index:
        row = sample.loc[idx]
        anomaly_type = rng.integers(0, 4)  # 0,1,2,3

        # Ensure a reasonable base income
        base_income = max(row["Annual_Salary"], 200000)

        # 1) Over-claim 80C
        if anomaly_type == 0:
            row["Investment_80C"] = LIMIT_80C * rng.uniform(1.3, 2.0)
            row["Total_Deductions"] = row["Total_Deductions"] + (row["Investment_80C"] - LIMIT_80C)

        # 2) Extreme donations vs income
        elif anomaly_type == 1:
            row["Donations_80G"] = base_income * rng.uniform(0.4, 0.8)
            row["Total_Deductions"] = row["Total_Deductions"] + row["Donations_80G"]

        # 3) Very high rent vs salary
        elif anomaly_type == 2:
            row["Rent_Paid"] = base_income * rng.uniform(0.7, 1.2)

        # 4) Overall deductions too high
        elif anomaly_type == 3:
            row["Total_Deductions"] = base_income * rng.uniform(0.8, 1.2)

        # Recompute taxable income approx
        row["Taxable_Income"] = max(
            0.0, row["Annual_Salary"] - (row["Total_Deductions"] + 50000.0)
        )

        sample.loc[idx] = row

    sample["label"] = 1  # risky/anomalous
    return sample


def build_training_data():
    """
    Build labelled training data:
      - base data labelled 0 (normal)
      - synthetic anomalies labelled 1 (risky)
    """
    base = load_base_data()
    base = base.copy()
    base["label"] = 0  # normal

    anomalies = generate_synthetic_anomalies(base.drop(columns=["label"]))

    training_df = pd.concat([base, anomalies], ignore_index=True)
    training_df = shuffle(training_df, random_state=42).reset_index(drop=True)

    # Save for inspection
    out_path = os.path.join(DATASETS_DIR, "itr_risk_training_data.csv")
    training_df.to_csv(out_path, index=False)
    print(f"📝 Training data saved to {out_path}")

    feature_cols = [
        "Annual_Salary",
        "Total_Deductions",
        "Taxable_Income",
        "Rent_Paid",
        "Investment_80C",
        "Medical_Insurance_80D",
        "NPS_Contribution_80CCD",
        "Home_Loan_Interest_24b",
        "Donations_80G",
        "Groceries",
        "Utilities",
        "Entertainment",
        "Healthcare",
    ]
    X = training_df[feature_cols].values
    y = training_df["label"].values

    return X, y, feature_cols


def train_and_save_model():
    X, y, feature_cols = build_training_data()
    print("📊 Training shape:", X.shape, "labels:", np.bincount(y))

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({"model": model, "features": feature_cols}, MODEL_PATH)
    print("✅ Risk model saved to:", MODEL_PATH)


if __name__ == "__main__":
    train_and_save_model()
