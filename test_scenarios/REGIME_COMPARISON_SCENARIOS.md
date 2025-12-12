# Regime Comparison Test Scenarios

## Overview
Test scenarios for Old vs New Tax Regime comparison calculator showing different outcomes based on salary, deductions, and circumstances.

---

## Scenario 1: Low Salary, No Deductions → NEW REGIME WINS ✅

**Inputs:**
- Annual Salary: **₹6,00,000**
- HRA Received: **₹0**
- Rent Paid: **₹0**
- City Type: **Metro**
- 80C: **₹0**
- 80D Self: **₹0**
- NPS 80CCD: **₹0**
- Home Loan Int: **₹0**

**Expected Output:**
- Old Regime Tax: **₹23,400**
- New Regime Tax: **₹5,200**
- **✅ NEW REGIME Recommended**
- Savings: **₹18,200**
- Break-even: **₹50,000** (minimal deductions needed)

**Why New Regime Wins:**
- Low salary, no deductions to claim
- New regime has higher basic exemption (₹3L vs ₹2.5L)
- Lower tax slabs benefit

---

## Scenario 2: High Salary, Maximum Deductions → OLD REGIME WINS ✅

**Inputs:**
- Annual Salary: **₹15,00,000**
- HRA Received: **₹3,00,000**
- Rent Paid: **₹3,60,000** (₹30K/month)
- City Type: **Metro**
- 80C: **₹1,50,000** (Max)
- 80D Self: **₹25,000**
- NPS 80CCD: **₹50,000** (Max)
- Home Loan Int: **₹2,00,000** (Max)

**Expected Output:**
- Old Regime Tax: **₹1,18,976**
- New Regime Tax: **₹1,95,000**
- **✅ OLD REGIME Recommended**
- Savings: **₹76,024**
- Break-even: **₹3,00,000** (already above)

**Why Old Regime Wins:**
- Maximum deductions claimed (₹6,25,000+)
- HRA exemption on ₹3L rent
- Home loan interest deduction
- High salary bracket benefits from deductions

---

## Scenario 3: Mid Salary, Partial Deductions → NEW REGIME WINS ✅

**Inputs:**
- Annual Salary: **₹10,00,000**
- HRA Received: **₹0**
- Rent Paid: **₹0**
- City Type: **Metro**
- 80C: **₹50,000** (Partial)
- 80D Self: **₹10,000**
- NPS 80CCD: **₹0**
- Home Loan Int: **₹0**

**Expected Output:**
- Old Regime Tax: **₹1,30,000**
- New Regime Tax: **₹46,800**
- **✅ NEW REGIME Recommended**
- Savings: **₹83,200**
- Break-even: **₹2,50,000**

**Why New Regime Wins:**
- Not enough deductions (only ₹1,10,000 total)
- Below break-even point
- New regime's lower slabs benefit

---

## Scenario 4: High HRA Exemption → OLD REGIME WINS ✅

**Inputs:**
- Annual Salary: **₹12,00,000**
- HRA Received: **₹4,80,000** (40% of salary)
- Rent Paid: **₹6,00,000** (₹50K/month)
- City Type: **Metro**
- 80C: **₹1,50,000**
- 80D Self: **₹15,000**
- NPS 80CCD: **₹50,000**
- Home Loan Int: **₹1,00,000**

**Expected Output:**
- Old Regime Tax: **₹84,656**
- New Regime Tax: **₹1,04,000**
- **✅ OLD REGIME Recommended**
- Savings: **₹19,344**
- HRA Exemption: **₹2,40,000** (metro 50% of basic)

**Why Old Regime Wins:**
- Large HRA exemption (₹2.4L)
- Combined with other deductions
- Total deductions exceed break-even

---

## Scenario 5: Exactly at Break-Even → BOTH EQUAL

**Inputs:**
- Annual Salary: **₹10,00,000**
- HRA Received: **₹63,000**
- Rent Paid: **₹0**
- City Type: **Metro**
- 80C: **₹1,50,000**
- 80D Self: **₹25,000**
- NPS 80CCD: **₹50,000**
- Home Loan Int: **₹0**

**Expected Output:**
- Old Regime Tax: **≈₹59,800**
- New Regime Tax: **≈₹46,800**
- **✅ NEW REGIME Recommended** (slightly better)
- Savings: **≈₹13,000**
- Break-even: **₹3,40,000**

**Note:** Close to break-even, minimal difference

---

## Scenario 6: Non-Metro City → Different HRA Calculation

**Inputs:**
- Annual Salary: **₹10,00,000**
- HRA Received: **₹2,00,000**
- Rent Paid: **₹2,40,000** (₹20K/month)
- City Type: **Non-Metro**
- 80C: **₹1,00,000**
- 80D Self: **₹10,000**
- NPS 80CCD: **₹25,000**
- Home Loan Int: **₹50,000**

**Expected Output:**
- Old Regime Tax: **≈₹1,01,920**
- New Regime Tax: **₹46,800**
- **✅ NEW REGIME Recommended**
- HRA Exemption: **₹1,60,000** (Non-metro 40% of basic)

**Why New Regime Wins:**
- Non-metro HRA exemption is lower (40% vs 50%)
- Moderate deductions
- Below break-even point

---

## Scenario 7: Home Loan Interest Benefit → OLD REGIME WINS ✅

**Inputs:**
- Annual Salary: **₹18,00,000**
- HRA Received: **₹0**
- Rent Paid: **₹0**
- City Type: **Metro**
- 80C: **₹1,50,000**
- 80D Self: **₹25,000**
- NPS 80CCD: **₹50,000**
- Home Loan Int: **₹2,00,000** (Max deduction)

**Expected Output:**
- Old Regime Tax: **≈₹2,27,760**
- New Regime Tax: **≈₹3,19,500**
- **✅ OLD REGIME Recommended**
- Savings: **≈₹91,740**
- Total Deductions: **₹4,75,000**

**Why Old Regime Wins:**
- Maximum home loan interest (₹2L)
- High deductions (₹4.75L total)
- Well above break-even

---

## Scenario 8: Senior Citizen → Higher 80D Limit

**Inputs:**
- Annual Salary: **₹8,00,000**
- HRA Received: **₹0**
- Rent Paid: **₹0**
- City Type: **Metro**
- 80C: **₹1,50,000**
- 80D Self: **₹50,000** (Senior citizen limit)
- NPS 80CCD: **₹50,000**
- Home Loan Int: **₹0**

**Expected Output:**
- Old Regime Tax: **≈₹46,800**
- New Regime Tax: **≈₹23,400**
- **✅ NEW REGIME Recommended** (depends on exact calculation)
- Total Deductions: **₹3,00,000**

**Note:** Senior citizens can claim up to ₹50K in 80D vs ₹25K for others

---

## Scenario 9: Very High Salary, No Deductions → NEW REGIME WINS ✅

**Inputs:**
- Annual Salary: **₹25,00,000**
- HRA Received: **₹0**
- Rent Paid: **₹0**
- City Type: **Metro**
- 80C: **₹0**
- 80D Self: **₹0**
- NPS 80CCD: **₹0**
- Home Loan Int: **₹0**

**Expected Output:**
- Old Regime Tax: **≈₹7,28,000**
- New Regime Tax: **≈₹6,19,500**
- **✅ NEW REGIME Recommended**
- Savings: **≈₹1,08,500**

**Why New Regime Wins:**
- No deductions to offset in old regime
- New regime's lower top slabs benefit
- Simplicity wins

---

## Scenario 10: Maximum Everything → OLD REGIME WINS ✅

**Inputs:**
- Annual Salary: **₹20,00,000**
- HRA Received: **₹8,00,000** (40% of salary)
- Rent Paid: **₹12,00,000** (₹1L/month)
- City Type: **Metro**
- 80C: **₹1,50,000**
- 80D Self: **₹25,000**
- NPS 80CCD: **₹50,000**
- Home Loan Int: **₹2,00,000**

**Expected Output:**
- Old Regime Tax: **≈₹1,87,200**
- New Regime Tax: **≈₹4,39,500**
- **✅ OLD REGIME Recommended**
- Savings: **≈₹2,52,300**
- HRA Exemption: **₹4,00,000** (50% of basic ₹8L)
- Total Deductions: **≈₹8,75,000**

**Why Old Regime Wins:**
- Maximum HRA exemption (₹4L)
- Maximum all other deductions
- Massive deduction benefit
- Far above break-even

---

## Quick Reference Table

| Scenario | Salary | Total Deductions | Old Tax | New Tax | Winner | Savings |
|----------|--------|------------------|---------|---------|--------|---------|
| Low, No Deductions | ₹6L | ₹50K | ₹23.4K | ₹5.2K | **NEW** | ₹18.2K |
| High, Max Deductions | ₹15L | ₹6.25L+ | ₹1.19L | ₹1.95L | **OLD** | ₹76K |
| Mid, Partial Deductions | ₹10L | ₹1.1L | ₹1.3L | ₹46.8K | **NEW** | ₹83.2K |
| High HRA | ₹12L | ₹5.55L | ₹84.7K | ₹1.04L | **OLD** | ₹19.3K |
| Break-even | ₹10L | ₹2.75L | ₹59.8K | ₹46.8K | **NEW** | ₹13K |
| Non-Metro | ₹10L | ₹3.45L | ₹1.02L | ₹46.8K | **NEW** | ₹55.2K |
| Home Loan | ₹18L | ₹4.75L | ₹2.28L | ₹3.20L | **OLD** | ₹91.7K |
| Very High, No Ded | ₹25L | ₹50K | ₹7.28L | ₹6.20L | **NEW** | ₹1.08L |
| Max Everything | ₹20L | ₹8.75L+ | ₹1.87L | ₹4.40L | **OLD** | ₹2.52L |

---

## Key Insights

### When OLD REGIME Wins:
- ✅ Total deductions > ₹3,00,000
- ✅ High HRA exemption (₹2L+)
- ✅ Home loan interest (₹1L+)
- ✅ Maximum 80C + NPS + 80D utilized
- ✅ High salary + high deductions combination

### When NEW REGIME Wins:
- ✅ Low deductions (< ₹2,50,000)
- ✅ No HRA exemption
- ✅ Simplicity preferred
- ✅ Low to mid salary with minimal investments
- ✅ No home loan

### Break-Even Point:
- Typically around **₹2,50,000 - ₹3,50,000** total deductions
- Varies by salary level
- Calculator shows exact break-even for each case

---

## How to Test

1. Go to **"Tax Calculator"** → **"Regime Comparison"** tab
2. Enter values from any scenario above
3. Click **"Analyze Best Regime"**
4. Verify debug banner shows correct inputs
5. Check recommendation matches expected output

---

## Notes

- Standard deduction (₹50K) automatically included in both regimes
- HRA exemption = minimum of:
  - Actual HRA received
  - Rent paid - 10% of basic salary
  - 50% of basic (metro) or 40% (non-metro)
- Tax rates subject to surcharge and cess (4%)
- All scenarios assume rebate u/s 87A not applicable (income > ₹7L for new regime, > ₹5L for old)
