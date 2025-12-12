"""
Enhanced ITR Risk Prediction with Detailed SHAP Explanations
==============================================================
Provides clear, visual explanations of WHY AI predicted a certain risk score
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shap
from typing import Dict, Tuple, List
import io
import base64

# Get project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "itr_risk_rf.pkl")


class EnhancedITRRiskAnalyzer:
    """Enhanced ITR Risk Analyzer with Detailed SHAP Explanations"""

    def __init__(self):
        """Initialize the analyzer"""
        self.model = None
        self.feature_names = [
            'Annual_Salary',
            'Investment_80C',
            'Medical_Insurance_80D',
            'Home_Loan_Interest_24b',
            'Donations_80G',
            'Rent_Paid',
            'Deduction_Ratio',
            'Donation_Ratio',
            'Rent_Ratio'
        ]
        self.load_model()

    def load_model(self):
        """Load or create the Random Forest model"""
        try:
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            print(f"Model loaded from {MODEL_PATH}")
        except:
            print("Warning: Creating dummy model for demonstration...")
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            X_dummy = np.random.rand(100, len(self.feature_names))
            y_dummy = np.random.randint(0, 2, 100)
            self.model.fit(X_dummy, y_dummy)

    def calculate_derived_features(self, data: Dict) -> Dict:
        """Calculate derived ratios"""
        salary = data.get('Annual_Salary', 0)

        if salary > 0:
            total_deductions = (
                data.get('Investment_80C', 0) +
                data.get('Medical_Insurance_80D', 0) +
                data.get('Home_Loan_Interest_24b', 0) +
                data.get('Donations_80G', 0)
            )
            data['Deduction_Ratio'] = total_deductions / salary
            data['Donation_Ratio'] = data.get('Donations_80G', 0) / salary
            data['Rent_Ratio'] = data.get('Rent_Paid', 0) / salary
        else:
            data['Deduction_Ratio'] = 0
            data['Donation_Ratio'] = 0
            data['Rent_Ratio'] = 0

        return data

    def prepare_features(self, data: Dict) -> np.ndarray:
        """Prepare feature vector"""
        data = self.calculate_derived_features(data)

        features = np.array([
            data.get('Annual_Salary', 0),
            data.get('Investment_80C', 0),
            data.get('Medical_Insurance_80D', 0),
            data.get('Home_Loan_Interest_24b', 0),
            data.get('Donations_80G', 0),
            data.get('Rent_Paid', 0),
            data.get('Deduction_Ratio', 0),
            data.get('Donation_Ratio', 0),
            data.get('Rent_Ratio', 0)
        ]).reshape(1, -1)

        return features

    def predict_risk(self, data: Dict) -> Dict:
        """Predict ITR risk score"""
        try:
            features = self.prepare_features(data)

            risk_prob = self.model.predict_proba(features)[0][1]
            risk_score = int(risk_prob * 100)

            if risk_score < 30:
                risk_level = "LOW"
                risk_color = "#10b981"
                risk_emoji = "✅"
            elif risk_score < 60:
                risk_level = "MEDIUM"
                risk_color = "#f59e0b"
                risk_emoji = "⚠️"
            else:
                risk_level = "HIGH"
                risk_color = "#ef4444"
                risk_emoji = "🚨"

            return {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_color": risk_color,
                "risk_emoji": risk_emoji,
                "risk_probability": float(risk_prob),
                "features": features
            }

        except Exception as e:
            return {
                "risk_score": 0,
                "risk_level": "ERROR",
                "risk_color": "#94a3b8",
                "risk_emoji": "❓",
                "risk_probability": 0.0,
                "features": None
            }

    def generate_detailed_shap_explanation(self, data: Dict) -> Dict:
        """Generate detailed SHAP explanations with clear interpretations"""
        try:
            features = self.prepare_features(data)

            # Create SHAP explainer
            explainer = shap.TreeExplainer(self.model)
            shap_values = explainer.shap_values(features)

            # Get SHAP values for high risk class
            if isinstance(shap_values, list):
                shap_values_risk = shap_values[1][0]
            else:
                shap_values_risk = shap_values[0]

            # Base value
            base_value = explainer.expected_value
            if isinstance(base_value, list):
                base_value = base_value[1]

            # Create feature importance dataframe
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'value': features[0],
                'shap_value': shap_values_risk
            })

            # Sort by absolute SHAP value
            feature_importance['abs_shap'] = np.abs(feature_importance['shap_value'])
            feature_importance = feature_importance.sort_values('abs_shap', ascending=False)

            # Generate detailed explanations
            explanations = []
            for _, row in feature_importance.head(5).iterrows():
                feature = row['feature']
                value = row['value']
                shap_val = row['shap_value']

                # Determine impact
                if shap_val > 0:
                    impact = "INCREASES"
                    direction = "↑"
                    impact_color = "#ef4444"
                else:
                    impact = "DECREASES"
                    direction = "↓"
                    impact_color = "#10b981"

                # Generate human-readable explanation
                explanation_text = self._generate_feature_explanation(feature, value, shap_val, data)

                explanation = {
                    "feature": self._format_feature_name(feature),
                    "feature_key": feature,
                    "value": float(value),
                    "shap_value": float(shap_val),
                    "abs_shap_value": float(abs(shap_val)),
                    "impact": impact,
                    "direction": direction,
                    "impact_color": impact_color,
                    "importance_percentage": float(abs(shap_val) / feature_importance['abs_shap'].sum() * 100),
                    "explanation": explanation_text
                }
                explanations.append(explanation)

            # Overall interpretation
            total_positive_impact = sum([exp['shap_value'] for exp in explanations if exp['shap_value'] > 0])
            total_negative_impact = sum([exp['shap_value'] for exp in explanations if exp['shap_value'] < 0])

            overall_interpretation = self._generate_overall_interpretation(
                explanations, total_positive_impact, total_negative_impact
            )

            return {
                "explanations": explanations,
                "base_value": float(base_value),
                "total_positive_impact": float(total_positive_impact),
                "total_negative_impact": float(total_negative_impact),
                "overall_interpretation": overall_interpretation,
                "feature_importance_df": feature_importance,
                "success": True
            }

        except Exception as e:
            print(f"Error generating SHAP explanation: {e}")
            return {
                "explanations": [],
                "base_value": 0.0,
                "total_positive_impact": 0.0,
                "total_negative_impact": 0.0,
                "overall_interpretation": "Unable to generate explanation. Model needs retraining.",
                "feature_importance_df": None,
                "success": False,
                "error": str(e)
            }

    def _format_feature_name(self, feature: str) -> str:
        """Format feature name for display"""
        name_map = {
            'Annual_Salary': 'Annual Salary',
            'Investment_80C': '80C Investments',
            'Medical_Insurance_80D': 'Health Insurance (80D)',
            'Home_Loan_Interest_24b': 'Home Loan Interest',
            'Donations_80G': 'Donations (80G)',
            'Rent_Paid': 'Rent Paid',
            'Deduction_Ratio': 'Total Deductions / Salary',
            'Donation_Ratio': 'Donations / Salary',
            'Rent_Ratio': 'Rent / Salary'
        }
        return name_map.get(feature, feature)

    def _generate_feature_explanation(self, feature: str, value: float, shap_val: float, data: Dict) -> str:
        """Generate human-readable explanation for each feature"""
        salary = data.get('Annual_Salary', 0)

        if feature == 'Annual_Salary':
            if shap_val > 0:
                return f"Your salary of ₹{value:,.0f} is in a bracket that slightly increases scrutiny risk."
            else:
                return f"Your salary of ₹{value:,.0f} is normal and doesn't raise concerns."

        elif feature == 'Investment_80C':
            if value > 150000:
                return f"Your 80C investments of ₹{value:,.0f} exceed the limit of ₹1.5L, which is a red flag."
            elif shap_val > 0:
                return f"Your 80C investments of ₹{value:,.0f} are high relative to income, raising minor concerns."
            else:
                return f"Your 80C investments of ₹{value:,.0f} are within normal limits."

        elif feature == 'Medical_Insurance_80D':
            limit = 50000 if data.get('age', 30) >= 60 else 25000
            if value > limit:
                return f"Your health insurance of ₹{value:,.0f} exceeds the limit of ₹{limit:,.0f}."
            elif shap_val > 0:
                return f"Your health insurance of ₹{value:,.0f} is on the higher side."
            else:
                return f"Your health insurance of ₹{value:,.0f} is reasonable."

        elif feature == 'Home_Loan_Interest_24b':
            if value > 200000:
                return f"Your home loan interest of ₹{value:,.0f} exceeds the ₹2L limit for self-occupied property."
            elif shap_val > 0:
                return f"Your home loan interest of ₹{value:,.0f} is high but within limits."
            else:
                return f"Your home loan interest of ₹{value:,.0f} is normal."

        elif feature == 'Donations_80G':
            if shap_val > 0:
                return f"Your donations of ₹{value:,.0f} are unusually high compared to your income, which may draw attention."
            else:
                return f"Your donations of ₹{value:,.0f} are reasonable."

        elif feature == 'Rent_Paid':
            if shap_val > 0:
                return f"Your rent of ₹{value:,.0f}/year is very high relative to income. Ensure HRA calculation is correct."
            else:
                return f"Your rent of ₹{value:,.0f}/year seems reasonable."

        elif feature == 'Deduction_Ratio':
            percentage = value * 100
            if percentage > 70:
                return f"Your total deductions are {percentage:.1f}% of income - this is unusually high and may trigger scrutiny."
            elif percentage > 50:
                return f"Your deductions are {percentage:.1f}% of income - on the higher side but explainable."
            else:
                return f"Your deductions are {percentage:.1f}% of income - within normal range."

        elif feature == 'Donation_Ratio':
            percentage = value * 100
            if percentage > 30:
                return f"Donations are {percentage:.1f}% of income - very high proportion may be questioned."
            elif percentage > 15:
                return f"Donations are {percentage:.1f}% of income - ensure proper documentation."
            else:
                return f"Donations are {percentage:.1f}% of income - reasonable amount."

        elif feature == 'Rent_Ratio':
            percentage = value * 100
            if percentage > 50:
                return f"Rent is {percentage:.1f}% of income - very high. Verify HRA exemption calculation."
            elif percentage > 30:
                return f"Rent is {percentage:.1f}% of income - on the higher side but acceptable."
            else:
                return f"Rent is {percentage:.1f}% of income - normal for most cities."

        return f"Value: ₹{value:,.0f}"

    def _generate_overall_interpretation(self, explanations: List[Dict], positive_impact: float, negative_impact: float) -> str:
        """Generate overall interpretation of SHAP analysis"""
        interpretation = "## 📊 Overall Risk Assessment\n\n"

        if len(explanations) == 0:
            return interpretation + "Unable to generate detailed analysis. Please check your inputs."

        # Dominant factors
        if abs(positive_impact) > abs(negative_impact):
            interpretation += f"### ⚠️ Risk-Increasing Factors Dominate\n\n"
            interpretation += f"The AI model identified **{len([e for e in explanations if e['shap_value'] > 0])} factors** that increase your ITR scrutiny risk.\n\n"

            interpretation += "**Top Concerns:**\n"
            for exp in [e for e in explanations if e['shap_value'] > 0][:3]:
                interpretation += f"- **{exp['feature']}**: {exp['explanation']}\n"

        else:
            interpretation += f"### ✅ Low Risk Profile\n\n"
            interpretation += f"Most factors work in your favor. Your return appears normal.\n\n"

        interpretation += f"\n**Risk Balance:**\n"
        interpretation += f"- Factors Increasing Risk: Impact score {positive_impact:.3f}\n"
        interpretation += f"- Factors Decreasing Risk: Impact score {abs(negative_impact):.3f}\n"

        # Recommendations
        interpretation += f"\n### 💡 Recommendations:\n\n"

        high_risk_features = [e for e in explanations if e['shap_value'] > 0.1]
        if high_risk_features:
            interpretation += "**To Reduce Risk:**\n"
            for exp in high_risk_features[:2]:
                if 'exceed' in exp['explanation'].lower():
                    interpretation += f"- {exp['feature']}: Exceeds limits. Review and correct this deduction.\n"
                elif 'high' in exp['explanation'].lower() or 'unusual' in exp['explanation'].lower():
                    interpretation += f"- {exp['feature']}: Ensure proper documentation and receipts.\n"
        else:
            interpretation += "- Your return looks well-balanced. Maintain proper documentation for all deductions.\n"

        interpretation += "- Keep all receipts, certificates, and proof of investments.\n"
        interpretation += "- Consider consulting a CA before filing for complex cases.\n"

        return interpretation

    def analyze(self, data: Dict) -> Dict:
        """Complete analysis with risk prediction and SHAP explanation"""
        # Get risk prediction
        prediction = self.predict_risk(data)

        # Generate SHAP explanation
        shap_result = self.generate_detailed_shap_explanation(data)

        # Generate flags
        flags = self._generate_flags(data, prediction['risk_score'])

        return {
            "risk_score": prediction['risk_score'],
            "risk_level": prediction['risk_level'],
            "risk_color": prediction['risk_color'],
            "risk_emoji": prediction['risk_emoji'],
            "shap_explanations": shap_result['explanations'],
            "overall_interpretation": shap_result.get('overall_interpretation', ''),
            "total_positive_impact": shap_result.get('total_positive_impact', 0),
            "total_negative_impact": shap_result.get('total_negative_impact', 0),
            "flags": flags,
            "success": shap_result['success']
        }

    def _generate_flags(self, data: Dict, risk_score: int) -> List[str]:
        """Generate specific risk flags"""
        flags = []
        salary = data.get('Annual_Salary', 0)

        if salary == 0:
            return ["No income data provided"]

        if data.get('Investment_80C', 0) > 150000:
            flags.append("🚨 Section 80C exceeds Rs.1.5L limit - major red flag")

        if data.get('Medical_Insurance_80D', 0) > 50000:
            flags.append("⚠️  Health insurance exceeds Rs.50K limit (senior citizen)")

        deduction_ratio = (
            data.get('Investment_80C', 0) +
            data.get('Medical_Insurance_80D', 0) +
            data.get('Home_Loan_Interest_24b', 0) +
            data.get('Donations_80G', 0)
        ) / salary if salary > 0 else 0

        if deduction_ratio > 0.7:
            flags.append(f"⚠️  Total deductions are {deduction_ratio*100:.1f}% of income - unusually high")

        if risk_score < 30:
            if not flags:
                flags.append("✅ Your return looks normal - low scrutiny risk")
        elif risk_score >= 60:
            flags.append("🚨 HIGH RISK: Strongly recommend CA review before filing")

        return flags


# DEMO
if __name__ == "__main__":
    print("Initializing Enhanced ITR Risk Analyzer...")

    analyzer = EnhancedITRRiskAnalyzer()

    test_data = {
        'Annual_Salary': 1200000,
        'Investment_80C': 150000,
        'Medical_Insurance_80D': 25000,
        'Home_Loan_Interest_24b': 200000,
        'Donations_80G': 50000,
        'Rent_Paid': 240000
    }

    print("\n" + "="*70)
    print("TESTING ENHANCED ITR RISK ANALYZER WITH SHAP")
    print("="*70 + "\n")

    result = analyzer.analyze(test_data)

    print(f"Risk Score: {result['risk_score']}/100 [{result['risk_level']}]")
    print(f"Risk Level: {result['risk_level']}\n")

    print("SHAP Explanations (Top 5 Features):\n")
    for i, exp in enumerate(result['shap_explanations'], 1):
        print(f"{i}. {exp['feature']}: Rs.{exp['value']:,.0f}")
        print(f"   {exp['direction']} {exp['impact']} risk by {exp['importance_percentage']:.1f}%")
        print(f"   Explanation: {exp['explanation']}\n")

    print(result['overall_interpretation'])

    print("\nEnhanced ITR Risk Analyzer initialized successfully!")
