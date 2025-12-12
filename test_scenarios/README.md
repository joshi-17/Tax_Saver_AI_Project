# Tax Saver AI - Test Scenarios Master Index

## Overview
This folder contains comprehensive test scenarios for all features of the Tax Saver AI application. Each file contains multiple scenarios with expected inputs and outputs to verify functionality.

---

## Quick Navigation

### By Calculator Type

| Calculator | File | Scenarios | Use Cases |
|------------|------|-----------|-----------|
| **Tax Calculator** | [TAX_CALCULATOR_SCENARIOS.md](TAX_CALCULATOR_SCENARIOS.md) | 10 | Entry-level to executive salaries |
| **Regime Comparison** | [REGIME_COMPARISON_SCENARIOS.md](REGIME_COMPARISON_SCENARIOS.md) | 10 | Old vs New regime comparison |
| **ELSS Optimizer** | [ELSS_OPTIMIZER_SCENARIOS.md](ELSS_OPTIMIZER_SCENARIOS.md) | 10 | SIP vs Lump Sum recommendations |
| **Buy vs Rent** | [BUY_VS_RENT_ALL_CITIES.md](BUY_VS_RENT_ALL_CITIES.md) | 16 | All major cities, both outcomes |
| **Monthly Planner** | [MONTHLY_PLANNER_SCENARIOS.md](MONTHLY_PLANNER_SCENARIOS.md) | 10 | Investment gap analysis |
| **What-If Simulator** | [WHAT_IF_SIMULATOR_SCENARIOS.md](WHAT_IF_SIMULATOR_SCENARIOS.md) | 10 | Tax impact comparisons |

### Quick Start Guides

| Guide | File | Purpose |
|-------|------|---------|
| **SIP Quick Test** | [QUICK_SIP_TEST.md](QUICK_SIP_TEST.md) | Get SIP recommendation in 30 seconds |
| **SIP Scenarios** | [SIP_RECOMMENDATION_SCENARIOS.md](SIP_RECOMMENDATION_SCENARIOS.md) | When SIP is recommended |
| **Bangalore Rent** | [BANGALORE_RENT_SCENARIOS.md](BANGALORE_RENT_SCENARIOS.md) | Rent recommendations for Bangalore |

---

## Scenario Count by Outcome

### Tax Calculator (10 scenarios)
- Various salary ranges: ₹4.5L to ₹25L
- Different deduction combinations
- Metro vs Non-Metro
- With/without home loan

### Regime Comparison (10 scenarios)
- **Old Regime Wins**: 4 scenarios
- **New Regime Wins**: 5 scenarios
- **Equal/Close**: 1 scenario

### ELSS Optimizer (10 scenarios)
- **SIP Recommended**: 7 scenarios
- **Lump Sum Recommended**: 3 scenarios

### Buy vs Rent (16 scenarios)
- **BUY Recommended**: 8 scenarios
- **RENT Recommended**: 8 scenarios
- Covers: Bangalore, Mumbai, Delhi, Hyderabad, Pune, Chennai, Kolkata, Ahmedabad

### Monthly Planner (10 scenarios)
- Start months: April to March
- Investment gaps: ₹20K to ₹2.25L
- Monthly targets: ₹6K to ₹1.8L

### What-If Simulator (10 scenarios)
- Tax savings: ₹7K to ₹1.32L
- Salary ranges: ₹8L to ₹25L
- Various investment combinations

---

## How to Use These Scenarios

### For Testing:
1. Open the relevant scenario file
2. Go to corresponding tab in Streamlit app
3. Enter exact inputs from scenario
4. Click calculation button
5. Verify output matches expected result
6. Check debug banner shows correct inputs

### For Learning:
1. Read scenario descriptions
2. Understand why certain recommendations are made
3. Compare similar scenarios with different outcomes
4. Learn key factors that influence decisions

### For Demonstration:
1. Pick scenario that matches your audience
2. Show inputs and calculation process
3. Explain recommendation logic
4. Demonstrate debug banner transparency

---

## Detailed File Descriptions

### 1. TAX_CALCULATOR_SCENARIOS.md
**Purpose**: Basic tax calculation with deductions

**Covers:**
- Entry-level professional (₹6L)
- Mid-career (₹12L)
- Senior manager (₹18L)
- High earners (₹25L)
- Different HRA situations
- Home loan scenarios
- Metro vs non-metro
- With/without investments

**Key Learning**: How salary, deductions, and HRA impact tax

**Best For**: Understanding basic tax calculation

---

### 2. REGIME_COMPARISON_SCENARIOS.md
**Purpose**: Compare Old vs New tax regime

**Covers:**
- Low salary, no deductions → New wins
- High salary, max deductions → Old wins
- Mid salary, partial deductions
- High HRA exemption impact
- Home loan interest benefit
- Break-even analysis
- Senior citizen scenarios

**Key Learning**: When to choose which regime

**Best For**: Regime selection decision

---

### 3. ELSS_OPTIMIZER_SCENARIOS.md
**Purpose**: SIP vs Lump Sum investment strategy

**Covers:**
- Conservative risk (always SIP)
- Moderate risk (depends on market)
- Aggressive risk (often lump sum)
- Short-term (3Y) to long-term (10Y)
- Low investment (₹50K) to max (₹1.5L)
- Different return expectations (12-20%)

**Key Learning**: Risk tolerance and market timing impact

**Best For**: ELSS investment decisions

---

### 4. BUY_VS_RENT_ALL_CITIES.md
**Purpose**: Property buying vs renting analysis

**Covers:**
- 8 major Indian cities
- 2 scenarios per city (1 buy, 1 rent)
- Property prices: ₹50L to ₹2Cr
- Different interest rates
- Various property appreciation rates
- Opportunity cost calculations

**Key Learning**: When buying makes sense vs renting

**Best For**: Home purchase decisions

---

### 5. MONTHLY_PLANNER_SCENARIOS.md
**Purpose**: Investment gap and monthly target planning

**Covers:**
- Starting early (April) vs late (March)
- Zero investments vs partial progress
- Different investment gaps (₹20K to ₹2.25L)
- Monthly targets (₹6K to ₹1.8L)
- Tax savings potential
- Priority allocation strategies

**Key Learning**: Importance of early tax planning

**Best For**: Year-round investment planning

---

### 6. WHAT_IF_SIMULATOR_SCENARIOS.md
**Purpose**: Real-time tax impact simulation

**Covers:**
- Salary increase impact
- Investment increase impact
- Home loan benefit analysis
- Incremental deduction testing
- Maximum vs minimum scenarios
- Progressive tax system understanding

**Key Learning**: How changes affect tax liability

**Best For**: Planning and optimization

---

### 7. QUICK_SIP_TEST.md
**Purpose**: Fast SIP recommendation test (30 seconds)

**Covers:**
- Guaranteed SIP scenario
- Step-by-step instructions
- Expected visual output
- Alternative quick tests
- Troubleshooting tips

**Key Learning**: Conservative = SIP always

**Best For**: Quick demos and verification

---

### 8. SIP_RECOMMENDATION_SCENARIOS.md
**Purpose**: Detailed SIP recommendation logic

**Covers:**
- When SIP is recommended
- When Lump Sum is recommended
- Market PE ratio impact
- Risk tolerance importance
- Complete test matrix

**Key Learning**: SIP vs Lump Sum decision factors

**Best For**: Understanding recommendation engine

---

### 9. BANGALORE_RENT_SCENARIOS.md
**Purpose**: Bangalore-specific rent recommendations

**Covers:**
- 6 scenarios where RENT wins
- Property prices: ₹60L to ₹1.5Cr
- Different rent amounts
- Interest rate variations
- Appreciation scenarios

**Key Learning**: When renting beats buying in Bangalore

**Best For**: Bangalore real estate decisions

---

## Scenario Selection Guide

### "I want to see..."

#### "...Old Regime recommended"
→ **REGIME_COMPARISON_SCENARIOS.md** - Scenarios 2, 4, 7, 10

#### "...New Regime recommended"
→ **REGIME_COMPARISON_SCENARIOS.md** - Scenarios 1, 3, 6, 9

#### "...SIP recommended"
→ **ELSS_OPTIMIZER_SCENARIOS.md** - Scenarios 1, 2, 3, 5, 6, 8, 9
→ **QUICK_SIP_TEST.md** - Any conservative scenario

#### "...Lump Sum recommended"
→ **ELSS_OPTIMIZER_SCENARIOS.md** - Scenarios 4, 7, 10

#### "...BUY recommended"
→ **BUY_VS_RENT_ALL_CITIES.md** - Affordable scenarios (see table)

#### "...RENT recommended"
→ **BUY_VS_RENT_ALL_CITIES.md** - Expensive/high rate scenarios
→ **BANGALORE_RENT_SCENARIOS.md** - All scenarios

#### "...Low tax liability"
→ **TAX_CALCULATOR_SCENARIOS.md** - Scenarios 1, 7, 9

#### "...High tax savings"
→ **WHAT_IF_SIMULATOR_SCENARIOS.md** - Scenario 6 (59% reduction)

#### "...Emergency planning"
→ **MONTHLY_PLANNER_SCENARIOS.md** - Scenario 7 (March start)

#### "...Early planning"
→ **MONTHLY_PLANNER_SCENARIOS.md** - Scenarios 1, 10 (April start)

---

## Testing Workflow

### Complete Testing (All Features):
1. ✅ Tax Calculator - Try Scenario 2 (mid-career)
2. ✅ Regime Comparison - Try Scenarios 2 & 3 (both outcomes)
3. ✅ ELSS Optimizer - Try Scenarios 2 & 4 (both recommendations)
4. ✅ Buy vs Rent - Try Bangalore Scenarios 1 & 2 (both outcomes)
5. ✅ Monthly Planner - Try Scenarios 1 & 3 (early & late)
6. ✅ What-If - Try Scenario 6 (maximum impact)

**Total Time**: ~20-30 minutes

### Quick Smoke Test (Core Features):
1. ✅ Regime Comparison - Scenario 2 (high deductions)
2. ✅ ELSS Optimizer - Use QUICK_SIP_TEST
3. ✅ Buy vs Rent - Bangalore Scenario 1 (rent recommended)

**Total Time**: ~5 minutes

---

## Verification Checklist

For each scenario tested:

- [ ] Inputs entered exactly as specified
- [ ] Calculation button clicked
- [ ] Debug banner appears
- [ ] Debug banner shows correct inputs
- [ ] Output matches expected result
- [ ] Recommendation (if any) matches expected
- [ ] Visual indicators (badges, highlights) correct
- [ ] Charts/graphs display properly

---

## Common Issues and Solutions

### Issue: Output doesn't match expected
**Solution**:
1. Check debug banner - are inputs correct?
2. Verify you clicked the button
3. Try refreshing page (press R)
4. Clear browser cache

### Issue: Same output for different inputs
**Solution**:
1. Look at debug banner
2. If banner shows new inputs but output is same → report bug
3. If banner shows old inputs → refresh page

### Issue: Scenario file says "guaranteed" but different outcome
**Solution**:
1. Verify EXACT inputs (check decimals, zeros)
2. Check if market data changed (for ELSS PE-based recommendations)
3. Ensure using correct calculator tab

---

## Contributing New Scenarios

If you want to add new test scenarios:

1. **Choose appropriate file** based on calculator
2. **Follow existing format**:
   - Scenario number and title
   - Clear inputs section
   - Expected output section
   - "Why" explanation
3. **Test the scenario** yourself first
4. **Document edge cases** if any
5. **Add to quick reference table**

---

## Statistics

**Total Scenario Files**: 9
**Total Scenarios**: 70+
**Calculators Covered**: 6
**Cities Covered**: 8
**Outcome Combinations**: All major permutations

**Coverage**:
- ✅ All calculator features
- ✅ All possible recommendations
- ✅ Edge cases
- ✅ Common use cases
- ✅ Quick tests
- ✅ Comprehensive tests

---

## Related Documentation

### In `error_logs/` folder:
- **ERROR_LOG_AND_FIXES.md** - All bugs and fixes

### In project root:
- **TESTING_GUIDE.md** - How to test the app
- **DEBUG_INSTRUCTIONS.md** - Using debug banners
- **COMPLETE_FIX_SUMMARY.md** - Summary of all fixes
- **WHAT_YOU_WILL_SEE.md** - Visual guide

---

## Support

### Need Help?
1. Read the relevant scenario file thoroughly
2. Follow inputs exactly as specified
3. Check debug banner for verification
4. Refer to TESTING_GUIDE.md
5. Check ERROR_LOG_AND_FIXES.md

### Found a Bug?
1. Document exact inputs used
2. Screenshot showing debug banner
3. Note expected vs actual output
4. Check if scenario file is outdated
5. Report with all details

---

## Updates

**Last Updated**: 2025-12-09

**Recent Changes**:
- ✅ Added debug banner verification to all scenarios
- ✅ Created separate city-specific files
- ✅ Added quick start guides
- ✅ Organized by outcome types
- ✅ Added master index (this file)

**Future Plans**:
- Additional niche scenarios
- Video walkthroughs
- Interactive scenario selector
- Automated test runner

---

## Quick Reference Card

**FASTEST TESTS:**
- Tax: Scenario 2 (₹12L salary)
- Regime: Scenario 3 (mid-salary)
- ELSS: QUICK_SIP_TEST
- Buy/Rent: Bangalore #1
- Planner: Scenario 1 (April)
- What-If: Scenario 1

**MOST INTERESTING:**
- Regime: Scenario 10 (max everything)
- ELSS: Scenario 7 (aggressive 20% returns)
- Buy/Rent: Mumbai #1 (₹2Cr property)
- Planner: Scenario 7 (emergency March)
- What-If: Scenario 6 (59% tax reduction)

**EDGE CASES:**
- Regime: Scenario 5 (break-even)
- ELSS: Scenario 10 (10-year horizon)
- Buy/Rent: Scenario with 10.5% interest
- Planner: Scenario 7 (last month)
- What-If: Scenario 5 (low vs high salary)

---

Happy Testing! 🎯

All scenarios have been verified to work correctly with the current version of Tax Saver AI.
