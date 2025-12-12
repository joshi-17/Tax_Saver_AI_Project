import pandas as pd
import numpy as np
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

print("🧮 Starting Tax Engine...")

# ======================================================
# 1️⃣ Load preprocessed dataset
# ======================================================
DATA_PATH = os.path.join(DATASETS_DIR, "final_preprocessed_dataset.csv")

try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Loaded preprocessed dataset successfully!")
except Exception as e:
    raise SystemExit(f"❌ Error loading cleaned dataset: {e}")


# ======================================================
# 2️⃣ NEW REGIME TAX CALCULATION (Mandatory from FY 2025-26)
# ======================================================
def compute_tax(taxable_income):
    """
    Calculate tax as per New Tax Regime (Post-Budget 2023)
    This is now the only applicable regime for all Indian citizens.
    """
    tax = 0

    slabs = [
        (0, 300000, 0),
        (300000, 600000, 0.05),
        (600000, 900000, 0.10),
        (900000, 1200000, 0.15),
        (1200000, 1500000, 0.20),
        (1500000, float("inf"), 0.30),
    ]

    for lower, upper, rate in slabs:
        if taxable_income > lower:
            taxable_amount = min(taxable_income, upper) - lower
            tax += taxable_amount * rate

    # Rebate under Section 87A (income ≤ ₹7 lakh)
    if taxable_income <= 700000:
        return 0

    return tax


# ======================================================
# 3️⃣ Apply tax calculation for every user
# ======================================================
df["Tax_Amount"] = df["Taxable_Income"].apply(compute_tax)


# ======================================================
# 5️⃣ Save final results
# ======================================================
OUTPUT_FILE = os.path.join(DATASETS_DIR, "final_tax_results.csv")
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Tax calculations complete! Results saved to: {OUTPUT_FILE}")
print(f"🧾 Rows processed: {len(df)}")
print(f"📊 Columns available: {len(df.columns)}")
print("Tax Engine complete!")
