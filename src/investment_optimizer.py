"""
Investment Timing Optimizer Engine
===================================
Provides intelligent tax-saving investment recommendations including:
- Tax calculation and optimization under New Tax Regime
- ELSS SIP vs Lump Sum timing optimization
- Home Loan vs Rent decision analyzer
- Monthly investment planner
- What-if scenario simulations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, date
import json

# ======================================================
# TAX CONSTANTS (FY 2024-25)
# ======================================================

# Section limits
LIMIT_80C = 150000
LIMIT_80D_SELF = 25000
LIMIT_80D_PARENTS = 25000
LIMIT_80D_SENIOR = 50000
LIMIT_80CCD_1B = 50000
LIMIT_24B = 200000
LIMIT_80TTA = 10000
STANDARD_DEDUCTION = 50000

# Tax Slabs (New Regime - Mandatory from FY 2025-26)
TAX_SLABS = [
    (0, 300000, 0.0),
    (300000, 600000, 0.05),
    (600000, 900000, 0.10),
    (900000, 1200000, 0.15),
    (1200000, 1500000, 0.20),
    (1500000, float("inf"), 0.30),
]

# ELSS Historical Returns (for simulation)
ELSS_AVG_RETURN = 0.12  # 12% average
ELSS_STD_DEV = 0.18  # 18% standard deviation

# Home Loan Parameters
HOME_LOAN_RATE_RANGE = (0.08, 0.10)  # 8-10%
PROPERTY_APPRECIATION = 0.06  # 6% annual


@dataclass
class UserFinancialProfile:
    """Holds user's complete financial profile for optimization"""
    annual_salary: float
    hra_received: float = 0
    rent_paid: float = 0
    city_type: str = "metro"  # metro, non-metro
    investment_80c: float = 0
    medical_insurance_80d: float = 0
    parents_medical_80d: float = 0
    parents_senior: bool = False
    nps_80ccd: float = 0
    home_loan_interest: float = 0
    home_loan_principal: float = 0
    savings_interest: float = 0
    other_income: float = 0
    age: int = 30
    risk_appetite: str = "moderate"  # conservative, moderate, aggressive


# ======================================================
# TAX CALCULATION FUNCTIONS
# ======================================================

def calculate_hra_exemption(
    hra_received: float,
    rent_paid: float,
    basic_salary: float,
    city_type: str = "metro"
) -> float:
    """
    Calculate HRA exemption under Section 10(13A)
    Exemption is minimum of:
    1. Actual HRA received
    2. Rent paid - 10% of basic salary
    3. 50% of basic (metro) or 40% (non-metro)
    """
    if rent_paid == 0:
        return 0
    
    metro_percent = 0.50 if city_type == "metro" else 0.40
    
    option1 = hra_received
    option2 = max(0, rent_paid - (0.10 * basic_salary))
    option3 = metro_percent * basic_salary
    
    return min(option1, option2, option3)


def calculate_tax(taxable_income: float) -> float:
    """
    Calculate tax under New Tax Regime (Mandatory from FY 2025-26)
    This is now the only applicable regime for all Indian citizens.
    """
    tax = 0
    for lower, upper, rate in TAX_SLABS:
        if taxable_income > lower:
            taxable_amount = min(taxable_income, upper) - lower
            tax += taxable_amount * rate

    # Rebate under Section 87A (income ≤ ₹7 lakh)
    if taxable_income <= 700000:
        tax = 0

    # Add 4% Health & Education Cess
    tax *= 1.04

    return tax


def calculate_tax_liability(profile: UserFinancialProfile) -> Dict[str, Any]:
    """
    Calculate tax liability under the New Tax Regime
    """
    gross_income = profile.annual_salary + profile.other_income

    # New regime only allows standard deduction
    taxable_income = max(0, gross_income - STANDARD_DEDUCTION)
    tax_payable = calculate_tax(taxable_income)

    # Investment recommendations (for wealth creation, not tax savings)
    recommendations = generate_investment_recommendations(profile)

    return {
        "gross_income": gross_income,
        "standard_deduction": STANDARD_DEDUCTION,
        "taxable_income": taxable_income,
        "tax_payable": tax_payable,
        "effective_rate": (tax_payable / gross_income * 100) if gross_income > 0 else 0,
        "recommendations": recommendations
    }


def generate_investment_recommendations(profile: UserFinancialProfile) -> List[Dict[str, Any]]:
    """
    Generate personalized investment recommendations for wealth creation
    Note: Under new regime, investments don't provide tax deductions,
    but are still recommended for financial planning
    """
    recommendations = []

    # ELSS for wealth creation (no longer for tax saving)
    current_80c = profile.investment_80c + profile.home_loan_principal
    if current_80c < LIMIT_80C:
        gap = LIMIT_80C - current_80c
        recommendations.append({
            "section": "Equity Investment (ELSS)",
            "current": current_80c,
            "suggested_amount": LIMIT_80C,
            "gap": gap,
            "priority": "HIGH",
            "suggestions": [
                f"Invest ₹{gap:,.0f} in ELSS for wealth creation",
                "Build long-term wealth with equity exposure",
                "3-year lock-in ensures disciplined investing"
            ]
        })

    # NPS for retirement planning
    if profile.nps_80ccd < LIMIT_80CCD_1B:
        gap = LIMIT_80CCD_1B - profile.nps_80ccd
        recommendations.append({
            "section": "Retirement Planning (NPS)",
            "current": profile.nps_80ccd,
            "suggested_amount": LIMIT_80CCD_1B,
            "gap": gap,
            "priority": "HIGH",
            "suggestions": [
                f"Invest ₹{gap:,.0f} in NPS for retirement corpus",
                "Market-linked returns for long-term growth",
                "Choose aggressive allocation if young"
            ]
        })

    # Health Insurance
    self_limit = LIMIT_80D_SENIOR if profile.age >= 60 else LIMIT_80D_SELF
    if profile.medical_insurance_80d < self_limit:
        gap = self_limit - profile.medical_insurance_80d
        recommendations.append({
            "section": "Health Insurance",
            "current": profile.medical_insurance_80d,
            "suggested_amount": self_limit,
            "gap": gap,
            "priority": "CRITICAL",
            "suggestions": [
                "Adequate health coverage is essential",
                "Consider super top-up plans for better coverage",
                "Protect your savings from medical emergencies"
            ]
        })

    # Parents Health Insurance
    parent_limit = LIMIT_80D_SENIOR if profile.parents_senior else LIMIT_80D_PARENTS
    if profile.parents_medical_80d < parent_limit:
        gap = parent_limit - profile.parents_medical_80d
        recommendations.append({
            "section": "Parents Health Insurance",
            "current": profile.parents_medical_80d,
            "suggested_amount": parent_limit,
            "gap": gap,
            "priority": "HIGH",
            "suggestions": [
                f"Get health insurance for parents (up to ₹{parent_limit:,})",
                "Senior citizen parents need comprehensive coverage",
                "Higher coverage limits for senior citizens"
            ]
        })

    return recommendations


# ======================================================
# ELSS SIP VS LUMP SUM OPTIMIZER
# ======================================================

def optimize_elss_investment(
    annual_amount: float,
    investment_month: int = 4,  # April = start of FY
    expected_return: float = ELSS_AVG_RETURN,
    risk_tolerance: str = "moderate"
) -> Dict[str, Any]:
    """
    Compare ELSS SIP vs Lump Sum strategies with timing optimization
    """
    monthly_sip = annual_amount / 12
    
    # Simulate both strategies
    sip_results = simulate_elss_sip(monthly_sip, expected_return)
    lumpsum_results = simulate_elss_lumpsum(annual_amount, investment_month, expected_return)
    
    # Calculate tax benefits timing
    tax_benefit = annual_amount * 0.312  # Max tax bracket
    
    # Determine optimal strategy based on risk tolerance
    if risk_tolerance == "conservative":
        recommendation = "SIP"
        reason = "Rupee cost averaging reduces timing risk"
    elif risk_tolerance == "aggressive":
        recommendation = "Lump Sum (April)"
        reason = "Maximizes time in market for higher expected returns"
    else:
        recommendation = "SIP" if sip_results['risk_adjusted_return'] > lumpsum_results['risk_adjusted_return'] else "Lump Sum"
        reason = "Balanced approach based on risk-adjusted returns"
    
    # Monthly investment calendar
    calendar = generate_investment_calendar(annual_amount, recommendation)
    
    return {
        "annual_investment": annual_amount,
        "tax_benefit": tax_benefit,
        "sip_strategy": {
            "monthly_amount": monthly_sip,
            "expected_value_3yr": sip_results['expected_value'],
            "risk_score": sip_results['risk_score'],
            "pros": ["Rupee cost averaging", "Disciplined investing", "Lower timing risk"],
            "cons": ["Slightly lower expected returns", "Need to remember monthly"]
        },
        "lumpsum_strategy": {
            "amount": annual_amount,
            "best_month": "April",
            "expected_value_3yr": lumpsum_results['expected_value'],
            "risk_score": lumpsum_results['risk_score'],
            "pros": ["Maximum time in market", "One-time effort", "Higher expected returns"],
            "cons": ["Timing risk", "Requires lump sum availability"]
        },
        "recommendation": recommendation,
        "reason": reason,
        "investment_calendar": calendar,
        "lock_in_end_dates": calculate_lockin_dates(recommendation)
    }


def simulate_elss_sip(
    monthly_amount: float,
    annual_return: float,
    years: int = 3
) -> Dict[str, float]:
    """Simulate SIP returns with Monte Carlo"""
    monthly_return = (1 + annual_return) ** (1/12) - 1
    months = years * 12
    
    # Simple projection
    future_value = 0
    for month in range(months):
        months_remaining = months - month
        future_value += monthly_amount * ((1 + monthly_return) ** months_remaining)
    
    total_invested = monthly_amount * months
    
    return {
        "expected_value": future_value,
        "total_invested": total_invested,
        "expected_gain": future_value - total_invested,
        "cagr": ((future_value / total_invested) ** (1/years) - 1) * 100,
        "risk_score": 6,  # Medium risk due to averaging
        "risk_adjusted_return": (future_value - total_invested) / total_invested * 0.85
    }


def simulate_elss_lumpsum(
    amount: float,
    investment_month: int,
    annual_return: float,
    years: int = 3
) -> Dict[str, float]:
    """Simulate lump sum returns"""
    # Adjust for partial first year
    effective_years = years + (12 - investment_month) / 12
    
    future_value = amount * ((1 + annual_return) ** effective_years)
    
    return {
        "expected_value": future_value,
        "total_invested": amount,
        "expected_gain": future_value - amount,
        "cagr": annual_return * 100,
        "risk_score": 8,  # Higher risk due to timing
        "risk_adjusted_return": (future_value - amount) / amount * 0.75
    }


def generate_investment_calendar(annual_amount: float, strategy: str) -> List[Dict]:
    """Generate month-by-month investment calendar"""
    calendar = []
    months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    
    if "SIP" in strategy:
        monthly = annual_amount / 12
        for i, month in enumerate(months):
            calendar.append({
                "month": month,
                "amount": monthly,
                "cumulative": monthly * (i + 1),
                "action": "SIP Investment",
                "tax_proof_ready": i >= 9  # Jan onwards for proof submission
            })
    else:
        calendar.append({
            "month": "Apr",
            "amount": annual_amount,
            "cumulative": annual_amount,
            "action": "Lump Sum Investment",
            "tax_proof_ready": True
        })
        for month in months[1:]:
            calendar.append({
                "month": month,
                "amount": 0,
                "cumulative": annual_amount,
                "action": "No action needed",
                "tax_proof_ready": True
            })
    
    return calendar


def calculate_lockin_dates(strategy: str) -> List[Dict]:
    """Calculate ELSS 3-year lock-in end dates"""
    today = date.today()
    fy_start = date(today.year if today.month >= 4 else today.year - 1, 4, 1)
    
    dates = []
    if "SIP" in strategy:
        for i in range(12):
            invest_date = date(fy_start.year + (i // 12), ((fy_start.month - 1 + i) % 12) + 1, 1)
            unlock_date = date(invest_date.year + 3, invest_date.month, invest_date.day)
            dates.append({
                "investment_month": invest_date.strftime("%b %Y"),
                "unlock_date": unlock_date.strftime("%b %Y"),
                "days_remaining": (unlock_date - today).days
            })
    else:
        unlock_date = date(fy_start.year + 3, 4, 1)
        dates.append({
            "investment_month": fy_start.strftime("%b %Y"),
            "unlock_date": unlock_date.strftime("%b %Y"),
            "days_remaining": (unlock_date - today).days
        })
    
    return dates


# ======================================================
# HOME LOAN VS RENT ANALYZER
# ======================================================

def analyze_home_loan_vs_rent(
    monthly_rent: float,
    property_value: float,
    loan_amount: float,
    loan_tenure_years: int,
    interest_rate: float,
    annual_salary: float,
    expected_rent_increase: float = 0.05,
    property_appreciation: float = PROPERTY_APPRECIATION
) -> Dict[str, Any]:
    """
    Comprehensive analysis of Home Loan vs Rent decision
    including tax implications
    """
    # Calculate EMI
    monthly_rate = interest_rate / 12
    num_payments = loan_tenure_years * 12
    emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** num_payments) / \
          (((1 + monthly_rate) ** num_payments) - 1)
    
    # Generate amortization schedule
    amortization = generate_amortization_schedule(loan_amount, interest_rate, loan_tenure_years)
    
    # Calculate tax benefits
    tax_benefits = calculate_home_loan_tax_benefits(amortization, annual_salary)
    
    # Calculate rent projection
    rent_projection = project_rent_costs(monthly_rent, loan_tenure_years, expected_rent_increase)
    
    # Calculate property value projection
    property_projection = project_property_value(property_value, loan_tenure_years, property_appreciation)
    
    # Net cost comparison
    total_loan_cost = emi * num_payments
    total_interest = total_loan_cost - loan_amount
    down_payment = property_value - loan_amount
    
    # Opportunity cost of down payment
    opportunity_cost = down_payment * ((1 + 0.10) ** loan_tenure_years - 1)  # 10% alternative investment
    
    # Net position after tenure
    home_net_position = property_projection['final_value'] - total_loan_cost - down_payment + tax_benefits['total_benefit']
    rent_net_position = -rent_projection['total_rent'] + opportunity_cost
    
    # Break-even analysis
    break_even_years = calculate_break_even_years(
        monthly_rent, emi, property_value, loan_amount,
        interest_rate, expected_rent_increase, property_appreciation
    )
    
    # Recommendation
    if home_net_position > rent_net_position:
        recommendation = "BUY"
        reason = f"Buying builds ₹{home_net_position - rent_net_position:,.0f} more wealth over {loan_tenure_years} years"
    else:
        recommendation = "RENT"
        reason = f"Renting + investing saves ₹{rent_net_position - home_net_position:,.0f} over {loan_tenure_years} years"
    
    return {
        "loan_details": {
            "property_value": property_value,
            "loan_amount": loan_amount,
            "down_payment": down_payment,
            "interest_rate": interest_rate * 100,
            "tenure_years": loan_tenure_years,
            "emi": emi,
            "total_payment": total_loan_cost,
            "total_interest": total_interest
        },
        "tax_benefits": tax_benefits,
        "rent_projection": rent_projection,
        "property_projection": property_projection,
        "comparison": {
            "home_net_position": home_net_position,
            "rent_net_position": rent_net_position,
            "break_even_years": break_even_years,
            "recommendation": recommendation,
            "reason": reason
        },
        "year_wise_comparison": generate_yearly_comparison(
            emi, monthly_rent, property_value, loan_amount,
            interest_rate, expected_rent_increase, property_appreciation,
            loan_tenure_years, amortization, annual_salary
        )
    }


def generate_amortization_schedule(
    principal: float,
    annual_rate: float,
    tenure_years: int
) -> List[Dict]:
    """Generate year-wise amortization schedule"""
    monthly_rate = annual_rate / 12
    num_payments = tenure_years * 12
    emi = principal * monthly_rate * ((1 + monthly_rate) ** num_payments) / \
          (((1 + monthly_rate) ** num_payments) - 1)
    
    balance = principal
    schedule = []
    
    for year in range(1, tenure_years + 1):
        year_interest = 0
        year_principal = 0
        
        for month in range(12):
            if balance <= 0:
                break
            interest_payment = balance * monthly_rate
            principal_payment = emi - interest_payment
            year_interest += interest_payment
            year_principal += principal_payment
            balance -= principal_payment
        
        schedule.append({
            "year": year,
            "principal_paid": year_principal,
            "interest_paid": year_interest,
            "total_paid": year_principal + year_interest,
            "balance": max(0, balance)
        })
    
    return schedule


def calculate_home_loan_tax_benefits(
    amortization: List[Dict],
    annual_salary: float
) -> Dict[str, Any]:
    """Calculate tax benefits from home loan"""
    yearly_benefits = []
    total_80c_benefit = 0
    total_24b_benefit = 0
    
    for year_data in amortization:
        # Section 80C - Principal repayment (max 1.5L, shared with other 80C)
        principal_deduction = min(year_data['principal_paid'], LIMIT_80C * 0.5)  # Assume 50% of 80C available
        
        # Section 24(b) - Interest deduction (max 2L for self-occupied)
        interest_deduction = min(year_data['interest_paid'], LIMIT_24B)
        
        # Tax saving (assuming 30% bracket)
        tax_rate = 0.312  # 30% + 4% cess
        year_benefit = (principal_deduction + interest_deduction) * tax_rate
        
        yearly_benefits.append({
            "year": year_data['year'],
            "principal_deduction": principal_deduction,
            "interest_deduction": interest_deduction,
            "tax_saved": year_benefit
        })
        
        total_80c_benefit += principal_deduction * tax_rate
        total_24b_benefit += interest_deduction * tax_rate
    
    return {
        "yearly_benefits": yearly_benefits,
        "total_80c_benefit": total_80c_benefit,
        "total_24b_benefit": total_24b_benefit,
        "total_benefit": total_80c_benefit + total_24b_benefit
    }


def project_rent_costs(
    monthly_rent: float,
    years: int,
    annual_increase: float
) -> Dict[str, Any]:
    """Project rent costs over time"""
    yearly_rents = []
    total = 0
    current_rent = monthly_rent
    
    for year in range(1, years + 1):
        annual_rent = current_rent * 12
        total += annual_rent
        yearly_rents.append({
            "year": year,
            "monthly_rent": current_rent,
            "annual_rent": annual_rent,
            "cumulative": total
        })
        current_rent *= (1 + annual_increase)
    
    return {
        "starting_rent": monthly_rent,
        "ending_rent": current_rent / (1 + annual_increase),
        "total_rent": total,
        "yearly_breakdown": yearly_rents
    }


def project_property_value(
    current_value: float,
    years: int,
    appreciation_rate: float
) -> Dict[str, Any]:
    """Project property value appreciation"""
    yearly_values = []
    value = current_value
    
    for year in range(1, years + 1):
        value *= (1 + appreciation_rate)
        yearly_values.append({
            "year": year,
            "value": value,
            "appreciation": value - current_value
        })
    
    return {
        "initial_value": current_value,
        "final_value": value,
        "total_appreciation": value - current_value,
        "cagr": appreciation_rate * 100,
        "yearly_values": yearly_values
    }


def calculate_break_even_years(
    monthly_rent: float,
    emi: float,
    property_value: float,
    loan_amount: float,
    interest_rate: float,
    rent_increase: float,
    property_appreciation: float
) -> float:
    """Calculate years to break even on home purchase vs rent"""
    down_payment = property_value - loan_amount
    
    cumulative_rent = 0
    cumulative_home_cost = down_payment
    current_rent = monthly_rent
    property_val = property_value
    
    for year in range(1, 31):
        # Rent cost for year
        cumulative_rent += current_rent * 12
        current_rent *= (1 + rent_increase)
        
        # Home cost (EMI) - already paid down payment
        cumulative_home_cost += emi * 12
        
        # Property appreciation
        property_val *= (1 + property_appreciation)
        
        # Net position
        home_equity = property_val - cumulative_home_cost
        rent_savings = -cumulative_rent + down_payment * ((1 + 0.10) ** year)  # Opportunity cost
        
        if home_equity > rent_savings:
            return year
    
    return 30  # Max years if never breaks even


def generate_yearly_comparison(
    emi: float,
    monthly_rent: float,
    property_value: float,
    loan_amount: float,
    interest_rate: float,
    rent_increase: float,
    property_appreciation: float,
    years: int,
    amortization: List[Dict],
    annual_salary: float
) -> List[Dict]:
    """Generate year-by-year comparison of buy vs rent"""
    comparison = []
    down_payment = property_value - loan_amount
    
    cumulative_emi = down_payment
    cumulative_rent = 0
    current_rent = monthly_rent
    property_val = property_value
    
    for year in range(1, min(years + 1, len(amortization) + 1)):
        year_data = amortization[year - 1]
        
        # EMI outflow
        year_emi = emi * 12
        cumulative_emi += year_emi
        
        # Tax benefit
        interest_deduction = min(year_data['interest_paid'], LIMIT_24B)
        tax_benefit = interest_deduction * 0.312
        
        # Rent outflow
        year_rent = current_rent * 12
        cumulative_rent += year_rent
        
        # Property value
        property_val *= (1 + property_appreciation)
        
        # Net positions
        home_net = property_val - cumulative_emi + tax_benefit
        rent_net = -cumulative_rent + down_payment * ((1 + 0.10) ** year)
        
        comparison.append({
            "year": year,
            "emi_outflow": year_emi,
            "rent_outflow": year_rent,
            "tax_benefit": tax_benefit,
            "property_value": property_val,
            "home_net_position": home_net,
            "rent_net_position": rent_net,
            "buy_advantage": home_net - rent_net
        })
        
        current_rent *= (1 + rent_increase)
    
    return comparison


# ======================================================
# WHAT-IF SCENARIO SIMULATOR
# ======================================================

def simulate_scenario(
    base_profile: UserFinancialProfile,
    changes: Dict[str, float]
) -> Dict[str, Any]:
    """
    Simulate tax impact of financial changes under New Tax Regime
    """
    # Create modified profile
    modified_profile = UserFinancialProfile(
        annual_salary=changes.get('annual_salary', base_profile.annual_salary),
        hra_received=changes.get('hra_received', base_profile.hra_received),
        rent_paid=changes.get('rent_paid', base_profile.rent_paid),
        city_type=changes.get('city_type', base_profile.city_type),
        investment_80c=changes.get('investment_80c', base_profile.investment_80c),
        medical_insurance_80d=changes.get('medical_insurance_80d', base_profile.medical_insurance_80d),
        parents_medical_80d=changes.get('parents_medical_80d', base_profile.parents_medical_80d),
        parents_senior=changes.get('parents_senior', base_profile.parents_senior),
        nps_80ccd=changes.get('nps_80ccd', base_profile.nps_80ccd),
        home_loan_interest=changes.get('home_loan_interest', base_profile.home_loan_interest),
        home_loan_principal=changes.get('home_loan_principal', base_profile.home_loan_principal),
        savings_interest=changes.get('savings_interest', base_profile.savings_interest),
        other_income=changes.get('other_income', base_profile.other_income),
        age=changes.get('age', base_profile.age),
        risk_appetite=changes.get('risk_appetite', base_profile.risk_appetite)
    )

    # Calculate both scenarios
    base_result = calculate_tax_liability(base_profile)
    modified_result = calculate_tax_liability(modified_profile)

    # Calculate impact
    base_tax = base_result['tax_payable']
    modified_tax = modified_result['tax_payable']

    return {
        "base_scenario": base_result,
        "modified_scenario": modified_result,
        "impact": {
            "tax_change": modified_tax - base_tax,
            "percentage_change": ((modified_tax - base_tax) / base_tax * 100) if base_tax > 0 else 0,
            "recommendation": "Beneficial" if modified_tax < base_tax else "Not Recommended"
        }
    }


# ======================================================
# MONTHLY INVESTMENT PLANNER
# ======================================================

def create_monthly_investment_plan(
    annual_salary: float,
    current_investments: Dict[str, float],
    target_deductions: float = None
) -> Dict[str, Any]:
    """
    Create a month-by-month investment plan to maximize tax savings
    """
    if target_deductions is None:
        target_deductions = LIMIT_80C + LIMIT_80CCD_1B + LIMIT_80D_SELF
    
    # Calculate gaps
    gaps = {
        "80C": max(0, LIMIT_80C - current_investments.get('80c', 0)),
        "80CCD": max(0, LIMIT_80CCD_1B - current_investments.get('nps', 0)),
        "80D": max(0, LIMIT_80D_SELF - current_investments.get('health_insurance', 0))
    }
    
    total_gap = sum(gaps.values())
    monthly_target = total_gap / 12
    
    # Generate monthly plan
    monthly_plan = []
    months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    
    remaining_80c = gaps["80C"]
    remaining_nps = gaps["80CCD"]
    
    for i, month in enumerate(months):
        month_investments = []
        month_total = 0
        
        # ELSS SIP (spread throughout year)
        if remaining_80c > 0:
            elss_amount = min(remaining_80c / (12 - i), remaining_80c)
            month_investments.append({
                "type": "ELSS SIP",
                "amount": elss_amount,
                "section": "80C"
            })
            month_total += elss_amount
            remaining_80c -= elss_amount
        
        # NPS (can be quarterly)
        if remaining_nps > 0 and i % 3 == 0:
            nps_amount = min(remaining_nps / ((12 - i) // 3 + 1), remaining_nps)
            month_investments.append({
                "type": "NPS Contribution",
                "amount": nps_amount,
                "section": "80CCD(1B)"
            })
            month_total += nps_amount
            remaining_nps -= nps_amount
        
        # Health insurance (annual, pay in April)
        if i == 0 and gaps["80D"] > 0:
            month_investments.append({
                "type": "Health Insurance Premium",
                "amount": gaps["80D"],
                "section": "80D"
            })
            month_total += gaps["80D"]
        
        monthly_plan.append({
            "month": month,
            "investments": month_investments,
            "total": month_total,
            "cumulative_tax_saved": sum(m['total'] for m in monthly_plan[:i]) * 0.312 + month_total * 0.312
        })
    
    return {
        "gaps_identified": gaps,
        "total_investment_needed": total_gap,
        "monthly_target": monthly_target,
        "plan": monthly_plan,
        "total_tax_savings": total_gap * 0.312,
        "effective_monthly_saving": total_gap * 0.312 / 12
    }
