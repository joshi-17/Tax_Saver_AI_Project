import pandas as pd
import numpy as np
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

print("🤖 Starting Recommendation Engine...")

# ======================================================
# Load tax results dataset
# ======================================================
TAX_RESULTS_PATH = os.path.join(DATASETS_DIR, "final_tax_results.csv")

try:
    df = pd.read_csv(TAX_RESULTS_PATH)
    print("✅ Loaded tax results successfully!")
except Exception as e:
    raise SystemExit(f"❌ Error loading tax results: {e}")


# ======================================================
# Recommendation Functions
# ======================================================

def suggest_investments(row):
    """
    Suggest investments for wealth creation.
    Note: Under New Tax Regime, investments don't provide tax deductions,
    but are still recommended for financial planning.
    """
    suggestions = []

    max_elss = 150000
    current_80c = row["Investment_80C"]
    if current_80c < max_elss:
        deficit = max_elss - current_80c
        suggestions.append(f"Consider investing ₹{deficit:.0f} more in ELSS for wealth creation.")

    max_nps = 50000
    current_nps = row["NPS_Contribution_80CCD"]
    if current_nps < max_nps:
        deficit = max_nps - current_nps
        suggestions.append(f"Invest ₹{deficit:.0f} in NPS for retirement planning.")

    max_health = 25000
    current_health = row["Medical_Insurance_80D"]
    if current_health < max_health:
        deficit = max_health - current_health
        suggestions.append(f"Increase health insurance by ₹{deficit:.0f} for better coverage.")

    if len(suggestions) == 0:
        return "Your investment portfolio looks good. Continue with current strategy."

    return " ".join(suggestions)


def suggest_expenses(row):
    suggestions = []

    if row["Expense_Ratio"] > 0.7:
        suggestions.append("Your expenses exceed 70% of your salary. Try reducing lifestyle expenses.")

    # Check overspending categories:
    if row["Entertainment"] > 0.15 * row["Annual_Salary"]:
        suggestions.append("Reduce entertainment expenses by 15–20% to save more.")

    if row["Groceries"] > 0.25 * row["Annual_Salary"]:
        suggestions.append("Your grocery expenses are high; consider budgeting strategies.")

    if len(suggestions) == 0:
        return "Your spending pattern is balanced."

    return " ".join(suggestions)


def suggest_tax_planning(row):
    """Provide general tax planning advice for New Tax Regime"""
    tax_amount = row["Tax_Amount"]
    taxable_income = row["Taxable_Income"]

    if taxable_income <= 700000:
        return "Great! You qualify for the rebate under Section 87A. No tax payable."
    elif tax_amount > 0:
        effective_rate = (tax_amount / row["Annual_Salary"] * 100) if row["Annual_Salary"] > 0 else 0
        return f"Your effective tax rate is {effective_rate:.1f}%. Focus on wealth creation through investments."
    return "Continue with current financial planning."


# ======================================================
# Generate All Recommendations
# ======================================================
df["Recommendation_Investments"] = df.apply(suggest_investments, axis=1)
df["Recommendation_Expenses"] = df.apply(suggest_expenses, axis=1)
df["Recommendation_Tax_Planning"] = df.apply(suggest_tax_planning, axis=1)


# ======================================================
# Save Recommendations
# ======================================================
OUTPUT_PATH = os.path.join(DATASETS_DIR, "tax_recommendations.csv")
df.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Recommendations generated successfully! Saved at: {OUTPUT_PATH}")
print("🤖 Recommendation Engine Complete!")
