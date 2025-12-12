# Monthly Investment Planner Test Scenarios

## Overview
Test scenarios for Monthly Investment Planner showing different investment gaps, monthly targets, and tax savings based on current investments and start month.

---

## Scenario 1: Starting Early (April), Zero Investments

**Inputs:**
- Current 80C: **₹0**
- Current NPS: **₹0**
- Current 80D: **₹0**
- Annual Salary: **₹10,00,000**
- Start Planning From: **April**

**Expected Output:**
- **Gap to Invest**: ₹2,25,000
  - 80C Gap: ₹1,50,000
  - NPS Gap: ₹50,000
  - 80D Gap: ₹25,000
- **Monthly Target**: ₹18,750 (₹2,25,000 ÷ 12)
- **Tax Savings**: ₹70,200 (₹2,25,000 × 31.2%)
- **Months Left**: 12

**Why This Scenario:**
- Full year to invest
- Can spread out evenly
- Maximum tax benefit possible

---

## Scenario 2: Starting Mid-Year (October), Partial Investments

**Inputs:**
- Current 80C: **₹1,00,000**
- Current NPS: **₹25,000**
- Current 80D: **₹15,000**
- Annual Salary: **₹15,00,000**
- Start Planning From: **October**

**Expected Output:**
- **Gap to Invest**: ₹85,000
  - 80C Gap: ₹50,000
  - NPS Gap: ₹25,000
  - 80D Gap: ₹10,000
- **Monthly Target**: ₹14,167 (₹85,000 ÷ 6)
- **Tax Savings**: ₹26,520 (₹85,000 × 31.2%)
- **Months Left**: 6

**Why This Scenario:**
- Already invested ₹1,40,000
- Need to catch up quickly
- Higher monthly target needed

---

## Scenario 3: Starting Late (January), Low Investments

**Inputs:**
- Current 80C: **₹50,000**
- Current NPS: **₹0**
- Current 80D: **₹0**
- Annual Salary: **₹12,00,000**
- Start Planning From: **January**

**Expected Output:**
- **Gap to Invest**: ₹1,75,000
  - 80C Gap: ₹1,00,000
  - NPS Gap: ₹50,000
  - 80D Gap: ₹25,000
- **Monthly Target**: ₹58,333 (₹1,75,000 ÷ 3)
- **Tax Savings**: ₹54,600 (₹1,75,000 × 31.2%)
- **Months Left**: 3

**Why This Scenario:**
- Very late start
- High monthly burden
- Risk of missing tax savings

---

## Scenario 4: Already Maxed Out 80C

**Inputs:**
- Current 80C: **₹1,50,000** (Already maxed)
- Current NPS: **₹0**
- Current 80D: **₹0**
- Annual Salary: **₹18,00,000**
- Start Planning From: **July**

**Expected Output:**
- **Gap to Invest**: ₹75,000
  - 80C Gap: ₹0 (Already done!)
  - NPS Gap: ₹50,000
  - 80D Gap: ₹25,000
- **Monthly Target**: ₹8,333 (₹75,000 ÷ 9)
- **Tax Savings**: ₹23,400 (₹75,000 × 31.2%)
- **Months Left**: 9

**Why This Scenario:**
- 80C done via EPF/PPF
- Only NPS and 80D remain
- Manageable monthly target

---

## Scenario 5: Moderate Progress, Mid Start

**Inputs:**
- Current 80C: **₹80,000**
- Current NPS: **₹20,000**
- Current 80D: **₹10,000**
- Annual Salary: **₹14,00,000**
- Start Planning From: **August**

**Expected Output:**
- **Gap to Invest**: ₹1,15,000
  - 80C Gap: ₹70,000
  - NPS Gap: ₹30,000
  - 80D Gap: ₹15,000
- **Monthly Target**: ₹14,375 (₹1,15,000 ÷ 8)
- **Tax Savings**: ₹35,880 (₹1,15,000 × 31.2%)
- **Months Left**: 8

**Why This Scenario:**
- Half-way through year
- Moderate progress made
- Reasonable catch-up needed

---

## Scenario 6: Almost Complete, Just Top-Up

**Inputs:**
- Current 80C: **₹1,40,000**
- Current NPS: **₹45,000**
- Current 80D: **₹20,000**
- Annual Salary: **₹20,00,000**
- Start Planning From: **February**

**Expected Output:**
- **Gap to Invest**: ₹20,000
  - 80C Gap: ₹10,000
  - NPS Gap: ₹5,000
  - 80D Gap: ₹5,000
- **Monthly Target**: ₹10,000 (₹20,000 ÷ 2)
- **Tax Savings**: ₹6,240 (₹20,000 × 31.2%)
- **Months Left**: 2

**Why This Scenario:**
- Almost done with investments
- Small top-up needed
- Easy to complete

---

## Scenario 7: Critical - Last Month

**Inputs:**
- Current 80C: **₹30,000**
- Current NPS: **₹10,000**
- Current 80D: **₹5,000**
- Annual Salary: **₹8,00,000**
- Start Planning From: **March**

**Expected Output:**
- **Gap to Invest**: ₹1,80,000
  - 80C Gap: ₹1,20,000
  - NPS Gap: ₹40,000
  - 80D Gap: ₹20,000
- **Monthly Target**: ₹1,80,000 (₹1,80,000 ÷ 1)
- **Tax Savings**: ₹56,160 (₹1,80,000 × 31.2%)
- **Months Left**: 1

**Why This Scenario:**
- Emergency situation
- Must invest huge amount immediately
- Risk losing major tax benefit

---

## Scenario 8: Balanced Approach, Mid-Year

**Inputs:**
- Current 80C: **₹75,000**
- Current NPS: **₹25,000**
- Current 80D: **₹12,500**
- Annual Salary: **₹16,00,000**
- Start Planning From: **September**

**Expected Output:**
- **Gap to Invest**: ₹1,12,500
  - 80C Gap: ₹75,000
  - NPS Gap: ₹25,000
  - 80D Gap: ₹12,500
- **Monthly Target**: ₹16,071 (₹1,12,500 ÷ 7)
- **Tax Savings**: ₹35,100 (₹1,12,500 × 31.2%)
- **Months Left**: 7

**Why This Scenario:**
- Balanced progress
- Half of each limit done
- Steady monthly commitment

---

## Scenario 9: Only 80D Pending

**Inputs:**
- Current 80C: **₹1,50,000** (Maxed)
- Current NPS: **₹50,000** (Maxed)
- Current 80D: **₹0**
- Annual Salary: **₹25,00,000**
- Start Planning From: **November**

**Expected Output:**
- **Gap to Invest**: ₹25,000
  - 80C Gap: ₹0
  - NPS Gap: ₹0
  - 80D Gap: ₹25,000
- **Monthly Target**: ₹6,250 (₹25,000 ÷ 4)
- **Tax Savings**: ₹7,800 (₹25,000 × 31.2%)
- **Months Left**: 4

**Why This Scenario:**
- Only health insurance pending
- Easy to complete
- Minimal monthly burden

---

## Scenario 10: Fresh Start Mid-Year

**Inputs:**
- Current 80C: **₹0**
- Current NPS: **₹0**
- Current 80D: **₹0**
- Annual Salary: **₹22,00,000**
- Start Planning From: **June**

**Expected Output:**
- **Gap to Invest**: ₹2,25,000
  - 80C Gap: ₹1,50,000
  - NPS Gap: ₹50,000
  - 80D Gap: ₹25,000
- **Monthly Target**: ₹22,500 (₹2,25,000 ÷ 10)
- **Tax Savings**: ₹70,200 (₹2,25,000 × 31.2%)
- **Months Left**: 10

**Why This Scenario:**
- No investments yet but still good time
- Manageable monthly amount
- Full benefits possible

---

## Quick Reference Table

| Scenario | Current Inv | Start Month | Gap | Monthly | Tax Saved | Months Left |
|----------|-------------|-------------|-----|---------|-----------|-------------|
| Early Start, Zero | ₹0 | April | ₹2.25L | ₹18,750 | ₹70,200 | 12 |
| Mid-Year, Partial | ₹1.4L | October | ₹85K | ₹14,167 | ₹26,520 | 6 |
| Late Start | ₹50K | January | ₹1.75L | ₹58,333 | ₹54,600 | 3 |
| 80C Maxed | ₹1.5L | July | ₹75K | ₹8,333 | ₹23,400 | 9 |
| Moderate Progress | ₹1.1L | August | ₹1.15L | ₹14,375 | ₹35,880 | 8 |
| Almost Complete | ₹2.05L | February | ₹20K | ₹10,000 | ₹6,240 | 2 |
| Last Month | ₹45K | March | ₹1.8L | ₹1,80,000 | ₹56,160 | 1 |
| Balanced | ₹1.125L | September | ₹1.125L | ₹16,071 | ₹35,100 | 7 |
| Only 80D | ₹2L | November | ₹25K | ₹6,250 | ₹7,800 | 4 |
| Fresh Mid-Year | ₹0 | June | ₹2.25L | ₹22,500 | ₹70,200 | 10 |

---

## Investment Limits (FY 2024-25)

### 80C - Maximum ₹1,50,000
**Eligible Investments:**
- PPF (Public Provident Fund)
- ELSS (Equity Linked Savings Scheme)
- EPF (Employee Provident Fund)
- Life Insurance Premium
- Home Loan Principal Repayment
- NSC (National Savings Certificate)
- Tax Saver FDs
- Sukanya Samriddhi Yojana
- Tuition Fees (2 children)

### NPS (80CCD) - Maximum ₹50,000
**Additional Deduction:**
- Over and above ₹1.5L of 80C
- National Pension System contribution
- Lock-in till retirement (60 years)
- Additional ₹15,600 tax saving

### 80D - Maximum ₹25,000 (Self) + ₹25,000 (Parents)
**Health Insurance:**
- Self: Up to ₹25,000 (₹50,000 if senior)
- Parents: Up to ₹25,000 (₹50,000 if senior)
- Preventive health check-up: ₹5,000 (within limit)
- Max savings: ₹15,600 (self) + ₹15,600 (parents)

---

## Key Features of Planner

### Gap Analysis:
Shows exactly how much more you need to invest in each category to max out tax benefits.

### Monthly Targets:
Divides remaining gap by months left to give you a monthly investment target.

### Priority Allocation:
Suggests which instrument to prioritize:
1. **80C**: PPF, ELSS (highest limit)
2. **NPS**: Additional ₹50K (good returns + tax benefit)
3. **80D**: Health insurance (essential + tax saving)

### Visual Calendar:
Shows month-by-month investment plan with bars and targets.

### Progress Tracking:
Shows current vs target for each category visually.

---

## Expected Visual Output

When you click "Generate Investment Plan":

1. **Debug Banner**: Shows your current investments and start month
2. **Four Metric Cards**:
   - Total To Invest
   - Monthly Target
   - Tax Saved
   - Months Left
3. **Gap Analysis Chart**: Bar chart showing Current vs Gap vs Limit
4. **Monthly Timeline**: Calendar view of investments needed
5. **Investment Recommendations**: Priority order suggestions
6. **Instrument Suggestions**: Specific products for each category

---

## How to Test

1. Go to **"Monthly Planner"** tab
2. Enter current investments (80C, NPS, 80D)
3. Enter annual salary
4. Select start month
5. Click **"Generate Investment Plan"**
6. Check debug banner for inputs
7. Verify gaps, monthly targets, and tax savings match expectations

---

## Pro Tips

### Starting Early (April-June):
- ✅ Low monthly burden (₹15-20K)
- ✅ Time to research best instruments
- ✅ Can use SIP for ELSS
- ✅ Spread out cashflow impact

### Starting Mid-Year (July-September):
- ⚠️ Moderate monthly burden (₹20-30K)
- ⚠️ Need to decide quickly
- ✅ Still manageable
- ✅ Can use lump sum + SIP mix

### Starting Late (October-December):
- 🔴 High monthly burden (₹30-50K)
- 🔴 Limited time to research
- 🔴 May need lump sum investments
- ⚠️ Risk missing some limits

### Starting Very Late (January-March):
- 🔴 Extreme monthly burden (₹60K-2L)
- 🔴 Emergency mode
- 🔴 Forced to use whatever available
- 🔴 May miss tax benefits
- ⚠️ Plan better next year!

---

## Investment Strategy by Start Month

### April-May (Best Time):
```
Monthly: ₹18,750
Strategy:
- 80C: ₹12,500/month via ELSS SIP
- NPS: ₹4,200/month
- 80D: ₹2,100/month (or lump sum annual premium)
```

### October (Catchup Mode):
```
Monthly: ₹37,500
Strategy:
- 80C: Lump sum ₹1.5L (ELSS/PPF)
- NPS: ₹8,333/month for 6 months
- 80D: Lump sum premium (₹25K)
```

### March (Emergency):
```
Monthly: ₹2,25,000 (All at once!)
Strategy:
- 80C: ELSS ₹1.5L (instant investment)
- NPS: ₹50K (lump sum)
- 80D: ₹25K (annual premium)
Total: ₹2,25,000 in last month
```

---

## Common Mistakes to Avoid

❌ **Waiting till March** - Extreme cashflow pressure
❌ **Ignoring NPS** - Missing extra ₹50K deduction
❌ **No health insurance** - Missing ₹25K deduction + no coverage
❌ **Over-investing in one** - 80C maxed but NPS/80D ignored
❌ **Not tracking** - Forgetting what's invested where

✅ **Start in April** - Lowest monthly burden
✅ **Auto-invest via SIP** - Set and forget
✅ **Diversify** - Use 80C + NPS + 80D all
✅ **Track monthly** - Use this planner regularly
✅ **Have health insurance** - Protection + tax benefit

---

## Notes

- Financial year: April to March
- Tax filing deadline: July 31st
- But investments must be made BY March 31st
- Some instruments (like ELSS) need time to process
- Start early to avoid last-minute rush
- Salary parameter used for context (tax bracket assumed 30%)
- Tax savings calculated at 31.2% (30% + 4% cess)
- Planner assumes you want to maximize all limits
- Adjust based on your actual needs and risk appetite
