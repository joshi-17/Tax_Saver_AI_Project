# Basic Tax Calculator Test Scenarios

## Overview
Test scenarios for the basic tax calculator showing tax calculation, deductions breakdown, and tax-saving recommendations for different income levels and investments.

---

## Scenario 1: Entry-Level Professional

**Inputs:**
- Annual Salary: **₹6,00,000**
- HRA Received: **₹1,20,000** (20% of salary)
- Rent Paid: **₹1,50,000** (₹12,500/month)
- City: **Metro**
- 80C Investments: **₹50,000**
- 80D Medical: **₹10,000**
- NPS 80CCD: **₹0**
- Home Loan Interest: **₹0**

**Expected Output:**
- **Gross Income**: ₹6,00,000
- **HRA Exemption**: ₹92,000
- **Total Deductions**: ₹2,02,000
- **Taxable Income**: ₹3,98,000
- **Tax Payable**: **₹7,904**
- **Monthly Tax**: ₹659

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-3.98L: ₹7,904 (@ 5% + cess)

**Key Insight**: Low income with HRA benefit = minimal tax

---

## Scenario 2: Mid-Career Professional

**Inputs:**
- Annual Salary: **₹12,00,000**
- HRA Received: **₹2,40,000**
- Rent Paid: **₹3,00,000** (₹25K/month)
- City: **Metro**
- 80C Investments: **₹1,50,000**
- 80D Medical: **₹25,000**
- NPS 80CCD: **₹50,000**
- Home Loan Interest: **₹1,50,000**

**Expected Output:**
- **Gross Income**: ₹12,00,000
- **HRA Exemption**: ₹2,40,000
- **Total Deductions**: ₹6,15,000
- **Taxable Income**: ₹5,85,000
- **Tax Payable**: **₹35,152**
- **Monthly Tax**: ₹2,929

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-5.85L: ₹17,680

**Key Insight**: Maximum deductions significantly reduce tax

---

## Scenario 3: Senior Manager

**Inputs:**
- Annual Salary: **₹18,00,000**
- HRA Received: **₹0** (Company accommodation)
- Rent Paid: **₹0**
- City: **Metro**
- 80C Investments: **₹1,50,000**
- 80D Medical: **₹25,000**
- NPS 80CCD: **₹50,000**
- Home Loan Interest: **₹2,00,000**

**Expected Output:**
- **Gross Income**: ₹18,00,000
- **HRA Exemption**: ₹0
- **Total Deductions**: ₹4,75,000
- **Taxable Income**: ₹13,25,000
- **Tax Payable**: **₹1,91,360**
- **Monthly Tax**: ₹15,947

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-10L: ₹1,04,000
- ₹10L-13.25L: ₹67,600

**Key Insight**: High salary, no HRA = substantial tax

---

## Scenario 4: Startup Employee (No Investments)

**Inputs:**
- Annual Salary: **₹10,00,000**
- HRA Received: **₹0**
- Rent Paid: **₹0**
- City: **Metro**
- 80C Investments: **₹0**
- 80D Medical: **₹0**
- NPS 80CCD: **₹0**
- Home Loan Interest: **₹0**

**Expected Output:**
- **Gross Income**: ₹10,00,000
- **HRA Exemption**: ₹0
- **Total Deductions**: ₹50,000 (Std deduction only)
- **Taxable Income**: ₹9,50,000
- **Tax Payable**: **₹1,19,600**
- **Monthly Tax**: ₹9,967

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-9.5L: ₹93,600

**Key Insight**: No tax planning = maximum tax!

---

## Scenario 5: Homeowner with Loan

**Inputs:**
- Annual Salary: **₹15,00,000**
- HRA Received: **₹0** (Own house)
- Rent Paid: **₹0**
- City: **Metro**
- 80C Investments: **₹1,50,000** (Includes principal)
- 80D Medical: **₹15,000**
- NPS 80CCD: **₹30,000**
- Home Loan Interest: **₹2,00,000**

**Expected Output:**
- **Gross Income**: ₹15,00,000
- **HRA Exemption**: ₹0
- **Total Deductions**: ₹4,45,000
- **Taxable Income**: ₹10,55,000
- **Tax Payable**: **₹1,43,040**
- **Monthly Tax**: ₹11,920

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-10L: ₹1,04,000
- ₹10L-10.55L: ₹17,160

**Key Insight**: Home loan interest major deduction

---

## Scenario 6: Rented Accommodation, Metro

**Inputs:**
- Annual Salary: **₹14,00,000**
- HRA Received: **₹4,20,000** (30% of salary)
- Rent Paid: **₹4,80,000** (₹40K/month)
- City: **Metro**
- 80C Investments: **₹1,00,000**
- 80D Medical: **₹20,000**
- NPS 80CCD: **₹40,000**
- Home Loan Interest: **₹0**

**Expected Output:**
- **Gross Income**: ₹14,00,000
- **HRA Exemption**: ₹2,80,000** (50% of basic ₹5.6L)
- **Total Deductions**: ₹4,90,000
- **Taxable Income**: ₹9,10,000
- **Tax Payable**: **₹1,06,080**
- **Monthly Tax**: ₹8,840

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-9.1L: ₹85,280

**Key Insight**: High rent = good HRA exemption

---

## Scenario 7: Non-Metro City

**Inputs:**
- Annual Salary: **₹10,00,000**
- HRA Received: **₹2,00,000**
- Rent Paid: **₹2,40,000** (₹20K/month)
- City: **Non-Metro**
- 80C Investments: **₹1,50,000**
- 80D Medical: **₹15,000**
- NPS 80CCD: **₹50,000**
- Home Loan Interest: **₹50,000**

**Expected Output:**
- **Gross Income**: ₹10,00,000
- **HRA Exemption**: ₹1,60,000** (40% of basic in non-metro)
- **Total Deductions**: ₹4,75,000
- **Taxable Income**: ₹5,25,000
- **Tax Payable**: **₹28,600**
- **Monthly Tax**: ₹2,383

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-5.25L: ₹5,200

**Key Insight**: Non-metro HRA exemption lower (40% vs 50%)

---

## Scenario 8: Freelancer/Consultant

**Inputs:**
- Annual Salary: **₹20,00,000**
- HRA Received: **₹0** (Self-employed)
- Rent Paid: **₹0**
- City: **Metro**
- 80C Investments: **₹1,50,000**
- 80D Medical: **₹25,000**
- NPS 80CCD: **₹50,000**
- Home Loan Interest: **₹0**

**Expected Output:**
- **Gross Income**: ₹20,00,000
- **HRA Exemption**: ₹0
- **Total Deductions**: ₹2,75,000
- **Taxable Income**: ₹17,25,000
- **Tax Payable**: **₹3,43,360**
- **Monthly Tax**: ₹28,613

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-10L: ₹1,04,000
- ₹10L-17.25L: ₹1,87,200

**Key Insight**: High income without HRA = high tax

---

## Scenario 9: Fresh Graduate

**Inputs:**
- Annual Salary: **₹4,50,000**
- HRA Received: **₹90,000**
- Rent Paid: **₹1,08,000** (₹9K/month)
- City: **Non-Metro**
- 80C Investments: **₹20,000**
- 80D Medical: **₹5,000**
- NPS 80CCD: **₹0**
- Home Loan Interest: **₹0**

**Expected Output:**
- **Gross Income**: ₹4,50,000
- **HRA Exemption**: ₹72,000
- **Total Deductions**: ₹1,47,000
- **Taxable Income**: ₹3,03,000
- **Tax Payable**: **₹2,756**
- **Monthly Tax**: ₹230

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-3.03L: ₹2,756 (@ 5% + cess)

**Key Insight**: Below ₹5L = eligible for rebate in new regime

---

## Scenario 10: Dual Home Loan

**Inputs:**
- Annual Salary: **₹25,00,000**
- HRA Received: **₹0**
- Rent Paid: **₹0**
- City: **Metro**
- 80C Investments: **₹1,50,000** (Max)
- 80D Medical: **₹25,000**
- NPS 80CCD: **₹50,000**
- Home Loan Interest: **₹2,00,000** (Capped at max)

**Expected Output:**
- **Gross Income**: ₹25,00,000
- **HRA Exemption**: ₹0
- **Total Deductions**: ₹4,75,000
- **Taxable Income**: ₹20,25,000
- **Tax Payable**: **₹5,26,960**
- **Monthly Tax**: ₹43,913

**Tax Breakdown:**
- ₹0-2.5L: ₹0
- ₹2.5L-5L: ₹13,000
- ₹5L-10L: ₹1,04,000
- ₹10L-20.25L: ₹3,33,800

**Key Insight**: Very high income = very high tax even with max deductions

---

## Quick Reference Table

| Scenario | Salary | HRA Exempt | Total Deductions | Taxable Income | Tax | Monthly Tax |
|----------|--------|------------|------------------|----------------|-----|-------------|
| Entry-Level | ₹6L | ₹92K | ₹2.02L | ₹3.98L | ₹7.9K | ₹659 |
| Mid-Career | ₹12L | ₹2.4L | ₹6.15L | ₹5.85L | ₹35.2K | ₹2,929 |
| Senior Manager | ₹18L | ₹0 | ₹4.75L | ₹13.25L | ₹1.91L | ₹15,947 |
| No Investments | ₹10L | ₹0 | ₹50K | ₹9.5L | ₹1.20L | ₹9,967 |
| Homeowner | ₹15L | ₹0 | ₹4.45L | ₹10.55L | ₹1.43L | ₹11,920 |
| High Rent | ₹14L | ₹2.8L | ₹4.9L | ₹9.1L | ₹1.06L | ₹8,840 |
| Non-Metro | ₹10L | ₹1.6L | ₹4.75L | ₹5.25L | ₹28.6K | ₹2,383 |
| Freelancer | ₹20L | ₹0 | ₹2.75L | ₹17.25L | ₹3.43L | ₹28,613 |
| Fresh Grad | ₹4.5L | ₹72K | ₹1.47L | ₹3.03L | ₹2.8K | ₹230 |
| Very High | ₹25L | ₹0 | ₹4.75L | ₹20.25L | ₹5.27L | ₹43,913 |

---

## HRA Exemption Calculation

### Formula:
Minimum of:
1. Actual HRA received
2. Rent paid - 10% of basic salary
3. 50% of basic (Metro) or 40% of basic (Non-Metro)

### Example (Scenario 6):
- Salary: ₹14,00,000
- Basic (40%): ₹5,60,000
- HRA Received: ₹4,20,000
- Rent Paid: ₹4,80,000

**Calculation:**
1. Actual HRA: ₹4,20,000
2. Rent - 10% basic: ₹4,80,000 - ₹56,000 = ₹4,24,000
3. 50% of basic: ₹2,80,000 ✅ **Minimum**

**HRA Exemption: ₹2,80,000**

---

## Deduction Limits Summary

| Section | Description | Limit | Tax Saved (30% bracket) |
|---------|-------------|-------|-------------------------|
| Standard | Automatic | ₹50,000 | ₹15,600 |
| 80C | Investments | ₹1,50,000 | ₹46,800 |
| 80CCD(1B) | NPS | ₹50,000 | ₹15,600 |
| 80D | Health Insurance (Self) | ₹25,000 | ₹7,800 |
| 80D | Health Insurance (Parents) | ₹25,000 | ₹7,800 |
| 24(b) | Home Loan Interest | ₹2,00,000 | ₹62,400 |
| **Total** | | **₹5,00,000** | **₹1,56,000** |

---

## Tax Slab (Old Regime)

| Income Range | Rate | Tax on Max |
|--------------|------|------------|
| ₹0 - ₹2.5L | 0% | ₹0 |
| ₹2.5L - ₹5L | 5% | ₹13,000 |
| ₹5L - ₹10L | 20% | ₹1,04,000 |
| Above ₹10L | 30% | (varies) |

**Plus**: 4% Health & Education Cess

**Effective Rates**: 5.2%, 20.8%, 31.2%

---

## Expected Visual Output

When you click "Calculate Tax":

1. **Income Summary Card**:
   - Gross Income
   - HRA Exemption
   - Total Deductions
   - Taxable Income

2. **Tax Calculation Card**:
   - Tax Amount (large display)
   - Monthly tax
   - Effective tax rate

3. **Deductions Breakdown Chart**:
   - Pie chart showing 80C, NPS, 80D, HRA, etc.

4. **Tax-Saving Recommendations**:
   - If gap in 80C: "Invest ₹XX,XXX more to save ₹YY,YYY"
   - If no NPS: "Add NPS ₹50K to save ₹15,600"
   - If no 80D: "Get health insurance to save ₹7,800"

---

## How to Test

1. Go to **"Tax Calculator"** tab (first tab)
2. Enter salary and deduction details
3. Click **"Calculate Tax"**
4. Verify:
   - Debug banner shows inputs
   - Tax amount calculated correctly
   - Recommendations shown for gaps

---

## Common Patterns

### High Tax Scenarios:
- ❌ No investments (₹0 in 80C)
- ❌ No HRA benefit
- ❌ High salary without planning
- ❌ Ignoring NPS and 80D

### Low Tax Scenarios:
- ✅ Maximum 80C (₹1.5L)
- ✅ NPS contribution (₹50K)
- ✅ Health insurance (₹25K+)
- ✅ Home loan (₹2L interest)
- ✅ High HRA exemption

---

## Pro Tips

### 💡 Maximize HRA:
- Pay market rent (to family also allowed)
- Keep rent receipts
- HRA can be largest deduction

### 💡 Home Loan Strategy:
- Interest deduction u/s 24(b): ₹2L
- Principal in 80C: ₹1.5L (combined limit)
- Total benefit: ₹62,400 tax saved

### 💡 Don't Forget:
- Standard deduction: Automatic ₹50K
- 80D: Even ₹5K premium helps
- NPS: Extra ₹50K over 80C

### 💡 Compare Regimes:
- Use Regime Comparison tab
- New regime may be better if low deductions
- Old regime better if high deductions

---

## Notes

- All calculations for Old Regime
- Standard deduction automatically included
- HRA exemption based on basic salary (typically 40-50% of gross)
- Tax rates include 4% cess
- Rebate u/s 87A: ₹12,500 if income < ₹5L (not shown separately)
- Surcharge applicable if income > ₹50L (not covered here)
- This is indicative - actual may vary based on Form 16, TDS, etc.
- Always consult a CA for accurate filing
