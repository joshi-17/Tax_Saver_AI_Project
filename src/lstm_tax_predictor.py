"""
LSTM-based Personal Tax Liability Prediction
=============================================
Predicts future tax liability based on historical income trends
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.preprocessing import MinMaxScaler
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("TensorFlow not available. Using fallback linear prediction.")
    TENSORFLOW_AVAILABLE = False


class LSTMTaxPredictor:
    """LSTM-based Tax Liability Predictor"""

    def __init__(self):
        """Initialize the LSTM predictor"""
        self.model = None
        self.scaler_income = MinMaxScaler() if TENSORFLOW_AVAILABLE else None
        self.scaler_tax = MinMaxScaler() if TENSORFLOW_AVAILABLE else None
        self.sequence_length = 3  # Use 3 years of history
        self.tensorflow_available = TENSORFLOW_AVAILABLE

        # Tax slabs (New Regime)
        self.tax_slabs = [
            (0, 300000, 0.0),
            (300000, 600000, 0.05),
            (600000, 900000, 0.10),
            (900000, 1200000, 0.15),
            (1200000, 1500000, 0.20),
            (1500000, float("inf"), 0.30),
        ]

    def calculate_tax(self, income: float) -> float:
        """Calculate tax under New Tax Regime"""
        tax = 0
        for lower, upper, rate in self.tax_slabs:
            if income > lower:
                taxable_amount = min(income, upper) - lower
                tax += taxable_amount * rate

        # Rebate under Section 87A
        if income <= 700000:
            tax = 0

        # Add 4% cess
        tax *= 1.04

        return tax

    def generate_training_data(self, base_salary: float, years: int = 10, growth_rate: float = 0.08) -> Tuple[List, List]:
        """Generate synthetic training data with salary growth"""
        incomes = []
        taxes = []

        current_salary = base_salary

        for year in range(years):
            # Add some randomness
            noise = np.random.normal(0, 0.02)  # 2% noise
            salary = current_salary * (1 + noise)
            tax = self.calculate_tax(salary)

            incomes.append(salary)
            taxes.append(tax)

            # Growth for next year
            current_salary *= (1 + growth_rate)

        return incomes, taxes

    def prepare_sequences(self, data: np.ndarray, sequence_length: int) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare sequences for LSTM training"""
        X, y = [], []

        for i in range(len(data) - sequence_length):
            X.append(data[i:i+sequence_length])
            y.append(data[i+sequence_length])

        return np.array(X), np.array(y)

    def build_lstm_model(self, input_shape: Tuple) -> Sequential:
        """Build LSTM model architecture"""
        model = Sequential([
            LSTM(50, activation='relu', return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, activation='relu'),
            Dropout(0.2),
            Dense(25, activation='relu'),
            Dense(1)
        ])

        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train_model(self, historical_incomes: List[float], retrain: bool = False):
        """Train the LSTM model on historical data"""
        if not self.tensorflow_available:
            print("TensorFlow not available. Using simple linear projection.")
            return

        if self.model is not None and not retrain:
            print("Model already trained. Use retrain=True to retrain.")
            return

        try:
            # Ensure we have enough data
            if len(historical_incomes) < self.sequence_length + 1:
                print(f"Not enough historical data. Need at least {self.sequence_length + 1} years.")
                print("Generating synthetic data for training...")
                # Use the last income or a default to generate synthetic data
                base_income = historical_incomes[-1] if historical_incomes else 800000
                historical_incomes, _ = self.generate_training_data(base_income, years=20)

            # Calculate taxes for historical incomes
            historical_taxes = [self.calculate_tax(income) for income in historical_incomes]

            # Scale data
            incomes_scaled = self.scaler_income.fit_transform(np.array(historical_incomes).reshape(-1, 1))
            taxes_scaled = self.scaler_tax.fit_transform(np.array(historical_taxes).reshape(-1, 1))

            # Prepare sequences
            X_income, y_income = self.prepare_sequences(incomes_scaled, self.sequence_length)
            X_tax, y_tax = self.prepare_sequences(taxes_scaled, self.sequence_length)

            # Reshape for LSTM [samples, time steps, features]
            X_income = X_income.reshape((X_income.shape[0], X_income.shape[1], 1))
            X_tax = X_tax.reshape((X_tax.shape[0], X_tax.shape[1], 1))

            # Build model
            self.model = self.build_lstm_model((self.sequence_length, 1))

            # Train on income -> income prediction first
            early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
            self.model.fit(X_income, y_income, epochs=100, batch_size=16, verbose=0, callbacks=[early_stop])

            print("LSTM model trained successfully!")

        except Exception as e:
            print(f"Error training LSTM model: {e}")
            self.tensorflow_available = False

    def predict_future_tax(self, historical_incomes: List[float], years_ahead: int = 3, growth_rate: float = 0.08) -> Dict:
        """Predict future tax liability"""
        try:
            if not self.tensorflow_available or self.model is None:
                # Fallback: simple linear projection
                return self._predict_simple(historical_incomes, years_ahead, growth_rate)

            # Ensure we have enough data
            if len(historical_incomes) < self.sequence_length:
                print(f"Not enough historical data. Need at least {self.sequence_length} years.")
                return self._predict_simple(historical_incomes, years_ahead, growth_rate)

            # Train model if not already trained
            if self.model is None:
                self.train_model(historical_incomes)

            # Get last sequence
            recent_incomes = historical_incomes[-self.sequence_length:]
            incomes_scaled = self.scaler_income.transform(np.array(recent_incomes).reshape(-1, 1))

            # Predict future incomes
            future_incomes = []
            current_sequence = incomes_scaled.reshape(1, self.sequence_length, 1)

            for _ in range(years_ahead):
                # Predict next income
                next_income_scaled = self.model.predict(current_sequence, verbose=0)[0][0]

                # Inverse scale
                next_income = self.scaler_income.inverse_transform([[next_income_scaled]])[0][0]
                future_incomes.append(next_income)

                # Update sequence
                current_sequence = np.roll(current_sequence, -1, axis=1)
                current_sequence[0, -1, 0] = next_income_scaled

            # Calculate taxes for predicted incomes
            future_taxes = [self.calculate_tax(income) for income in future_incomes]

            # Calculate effective tax rates
            effective_rates = [
                (tax / income * 100) if income > 0 else 0
                for income, tax in zip(future_incomes, future_taxes)
            ]

            return {
                "historical_incomes": historical_incomes,
                "future_incomes": future_incomes,
                "future_taxes": future_taxes,
                "effective_rates": effective_rates,
                "years_ahead": years_ahead,
                "method": "LSTM",
                "success": True
            }

        except Exception as e:
            print(f"Error in LSTM prediction: {e}")
            return self._predict_simple(historical_incomes, years_ahead, growth_rate)

    def _predict_simple(self, historical_incomes: List[float], years_ahead: int, growth_rate: float) -> Dict:
        """Fallback: Simple linear projection"""
        if not historical_incomes:
            historical_incomes = [800000]  # Default

        # Use simple growth rate
        last_income = historical_incomes[-1]
        future_incomes = []

        for year in range(1, years_ahead + 1):
            future_income = last_income * ((1 + growth_rate) ** year)
            future_incomes.append(future_income)

        # Calculate taxes
        future_taxes = [self.calculate_tax(income) for income in future_incomes]

        # Calculate effective rates
        effective_rates = [
            (tax / income * 100) if income > 0 else 0
            for income, tax in zip(future_incomes, future_taxes)
        ]

        return {
            "historical_incomes": historical_incomes,
            "future_incomes": future_incomes,
            "future_taxes": future_taxes,
            "effective_rates": effective_rates,
            "years_ahead": years_ahead,
            "method": "Linear Projection",
            "success": True
        }

    def generate_prediction_report(self, prediction: Dict) -> str:
        """Generate a textual report of the prediction"""
        report = []
        report.append(f"Tax Liability Forecast ({prediction['years_ahead']} years)")
        report.append(f"Method: {prediction['method']}")
        report.append("")

        for i, (income, tax, rate) in enumerate(zip(
            prediction['future_incomes'],
            prediction['future_taxes'],
            prediction['effective_rates']
        ), 1):
            report.append(f"Year {i}:")
            report.append(f"  Predicted Income: Rs.{income:,.0f}")
            report.append(f"  Estimated Tax: Rs.{tax:,.0f}")
            report.append(f"  Effective Rate: {rate:.2f}%")
            report.append("")

        # Calculate totals
        total_income = sum(prediction['future_incomes'])
        total_tax = sum(prediction['future_taxes'])
        avg_rate = (total_tax / total_income * 100) if total_income > 0 else 0

        report.append("Summary:")
        report.append(f"  Total Income (forecast): Rs.{total_income:,.0f}")
        report.append(f"  Total Tax (forecast): Rs.{total_tax:,.0f}")
        report.append(f"  Average Effective Rate: {avg_rate:.2f}%")

        return "\n".join(report)


# ======================================================
# DEMO / TESTING
# ======================================================
if __name__ == "__main__":
    print("Initializing LSTM Tax Liability Predictor...")

    predictor = LSTMTaxPredictor()

    # Test with historical income data
    historical_incomes = [
        800000,   # 3 years ago
        850000,   # 2 years ago
        920000,   # Last year
        1000000   # Current year
    ]

    print("\n" + "="*60)
    print("TESTING LSTM TAX PREDICTOR")
    print("="*60 + "\n")

    print("Historical Income Data:")
    for i, income in enumerate(historical_incomes, 1):
        print(f"  Year -{len(historical_incomes)-i}: Rs.{income:,}")

    print("\nTraining model...")
    predictor.train_model(historical_incomes)

    print("\nPredicting next 3 years...")
    prediction = predictor.predict_future_tax(historical_incomes, years_ahead=3, growth_rate=0.10)

    print("\n" + predictor.generate_prediction_report(prediction))

    print("\n" + "="*60)
    print("LSTM Tax Predictor initialized successfully!")
