# 💰 Tax Saver AI - Advanced Tax Intelligence Platform

AI-powered personal tax optimization system with RAG-based advisor, explainable AI for risk assessment, and predictive analytics for Indian taxpayers.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![AI](https://img.shields.io/badge/AI-Powered-10b981?style=for-the-badge&logo=robot&logoColor=white)

**Version 4.0** | Production-Ready | Advanced AI Features | Explainable AI | Predictive Analytics

## ✨ Features

### 🤖 1. RAG-based Tax Advisor (NEW!)
**Conversational AI powered by Gemini LLM**
- Ask natural language questions about Indian taxation
- Retrieval-Augmented Generation for accurate responses
- 15+ tax topics covered (80C, 80D, HRA, ITR filing, etc.)
- Shows source documents with relevance scores
- Browse by category: deductions, exemptions, compliance
- Context-aware responses using knowledge base

**Example Questions:**
- "What is Section 80C?"
- "How to claim HRA exemption?"
- "When is the ITR filing deadline?"

### 📊 2. ELSS Investment Optimizer
- **SIP vs Lump Sum** strategy recommendations
- Real market data (Nifty PE ratio)
- Risk-based recommendations (Conservative/Moderate/Aggressive)
- Expected returns calculator
- Investment calendar with best timing

### 🏠 3. Buy vs Rent Analyzer
- **Data-driven decision** calculator
- 8 major Indian cities covered
- Year-by-year tax benefit calculation
- Opportunity cost analysis
- EMI calculator with loan amortization
- Property appreciation projections

### 📅 4. Monthly Investment Planner
- Investment gap analysis (80C, NPS, 80D)
- Month-by-month targets from any starting month
- Tax savings calculator
- Priority recommendations
- Deadline tracking

### 🔄 5. What-If Simulator
- **Real-time tax impact** analysis
- Base vs Modified scenario comparison
- Instant updates (no button needed)
- Progressive tax visualization
- Financial decision modeling

### 🚨 6. Enhanced ITR Risk Check with SHAP (NEW!)
**Explainable AI for risk assessment**
- AI-powered risk prediction using Random Forest
- **SHAP explanations** showing WHY a score was assigned
- Top 5 feature impacts visualized
- Color-coded impact indicators (↑ increases / ↓ decreases risk)
- Horizontal bar chart showing feature contributions
- Risk flags with detailed warnings
- Transparency in AI decision-making

**Key Innovation:** Unlike black-box models, this shows exactly which factors contribute to your risk score and by how much.

### 📈 7. LSTM Tax Liability Prediction (NEW!)
**Deep learning for future tax forecasting**
- Input 4+ years of historical income data
- LSTM neural network predicts next 3-10 years
- Trend visualization (historical vs predicted)
- Year-wise breakdown: income, tax, effective rate
- Method indicator (LSTM vs Linear fallback)
- Tax planning recommendations
- Helps with long-term financial planning

**Use Case:** Plan ahead for major life events (home purchase, career change, retirement) by forecasting tax liability.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API (Optional for RAG Advisor)
```bash
# Set environment variable for Gemini API
export GEMINI_API_KEY="your_api_key_here"

# Or use .env file
echo "GEMINI_API_KEY=your_api_key" > .env
```

### 3. Run the Application
```bash
streamlit run app/streamlit_app.py
```

### 4. Open Browser
Navigate to `http://localhost:8501`

## 📁 Project Structure

```
Tax_Saver_AI_Project/
├── app/
│   └── streamlit_app.py              # Main application (New v4.0)
├── src/
│   ├── rag_tax_advisor.py            # RAG-based Tax Advisor (NEW)
│   ├── itr_risk_shap.py              # ITR Risk with SHAP explanations (NEW)
│   ├── lstm_tax_predictor.py         # LSTM Tax Liability Predictor (NEW)
│   ├── investment_optimizer.py       # ELSS, Buy vs Rent, Planner
│   ├── itr_risk_engine.py            # Original ITR Risk model
│   ├── tax_engine.py                 # Tax calculations
│   └── recommendation_engine.py       # Investment recommendations
├── models/
│   └── itr_risk_rf.pkl               # Trained Random Forest model
├── datasets/
│   ├── investment_data.json          # Real market data
│   ├── itr_risk_training_data.csv    # ITR risk training data
│   └── [other datasets...]
└── requirements.txt                   # All dependencies
```

## 🧠 AI/ML Technologies Used

### 1. **Retrieval-Augmented Generation (RAG)**
- **Model**: Google Gemini Pro LLM
- **Technique**: Vector-based document retrieval + LLM generation
- **Use Case**: Conversational tax advisor
- **Accuracy**: Context-aware responses based on curated knowledge base

### 2. **SHAP (SHapley Additive exPlanations)**
- **Model**: Random Forest Classifier
- **Technique**: TreeExplainer for feature importance
- **Use Case**: Explainable ITR risk prediction
- **Benefit**: Shows which factors increase/decrease risk and by how much

### 3. **LSTM (Long Short-Term Memory)**
- **Model**: Sequential neural network
- **Architecture**: 2 LSTM layers (50 units each) + Dense layers
- **Use Case**: Tax liability forecasting
- **Fallback**: Linear regression for insufficient data
- **Training**: On historical income trends with early stopping

### 4. **Random Forest**
- **Use Case**: ITR risk classification
- **Features**: 9 features including income, deductions, ratios
- **Performance**: Trained on synthetic + real data

## 📊 Key Innovations

### 🎯 Explainability (SHAP)
**Problem Solved:** Most AI models are "black boxes" - they predict but don't explain.

**Our Solution:** SHAP values show:
- Which features matter most
- How each feature impacts the prediction
- Direction of impact (positive/negative)

**Example:**
```
Feature: Donation Ratio (30% of income)
SHAP Value: +0.25
Impact: ↑ Increases risk by 25%
Reason: Unusually high donation ratio may draw scrutiny
```

### 🔮 Predictive Analytics (LSTM)
**Problem Solved:** People don't plan taxes proactively.

**Our Solution:** LSTM predicts future tax liability based on:
- Historical income trends
- Expected growth rates
- Tax law changes

**Benefit:** Make informed decisions about:
- When to buy a house
- When to change jobs
- Retirement planning

### 💬 Conversational AI (RAG)
**Problem Solved:** Tax laws are complex and confusing.

**Our Solution:** Ask questions in plain English:
- "What is Section 80C?" → Detailed explanation
- "Should I choose old or new regime?" → Context-aware advice
- "How to claim HRA?" → Step-by-step guidance

**Accuracy:** Retrieves relevant context before generating response, ensuring accuracy.

## 📈 Use Cases

### 1. **Tax Planning (RAG Advisor)**
- Ask: "What deductions can I claim for my home loan?"
- Get: Detailed explanation of Section 24(b), limits, and documentation

### 2. **Risk Assessment (SHAP)**
- Input: Your financial data
- Get: Risk score + explanation showing exactly why
- Action: Fix issues before filing ITR

### 3. **Future Planning (LSTM)**
- Input: Last 4 years' income
- Get: Next 5 years' tax prediction
- Action: Plan major expenses based on forecasted tax

### 4. **Investment Timing (ELSS Optimizer)**
- Input: Investment amount, risk appetite
- Get: SIP vs Lump Sum recommendation based on market PE ratio

### 5. **Buy vs Rent Decision**
- Input: City, property price, loan details
- Get: Year-wise analysis showing which option saves more

## 🔬 Technical Details

### RAG Tax Advisor
- **Knowledge Base**: 15 curated tax FAQs with keywords
- **Retrieval**: Cosine similarity on TF-IDF vectors
- **Top-K**: Retrieves 3 most relevant documents
- **LLM**: Gemini Pro generates context-aware response
- **Fallback**: Returns best match if LLM unavailable

### SHAP Explanations
- **Explainer**: TreeExplainer (optimized for Random Forest)
- **Values**: Per-feature SHAP values for class 1 (high risk)
- **Visualization**: Horizontal bar chart + impact indicators
- **Interpretation**: Positive SHAP = increases risk, Negative = decreases risk

### LSTM Predictor
- **Input Sequence**: 3 years of historical income
- **Layers**: LSTM(50) → Dropout(0.2) → LSTM(50) → Dropout(0.2) → Dense(25) → Dense(1)
- **Scaler**: MinMaxScaler for normalization
- **Training**: 100 epochs with early stopping (patience=10)
- **Prediction**: Recursive forecasting for multiple years ahead

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.51.0+ with custom CSS
- **Visualization**: Plotly interactive charts
- **ML Framework**: scikit-learn (Random Forest)
- **Deep Learning**: TensorFlow/Keras (LSTM)
- **Explainability**: SHAP
- **LLM**: Google Gemini Pro
- **Data**: Pandas, NumPy

## ⚠️ Disclaimer

**For Educational Purposes Only**

This tool provides estimates based on FY 2024-25 tax laws. Tax laws change frequently. Please consult a qualified Chartered Accountant or tax professional for accurate advice.

**Not Financial Advice**: All recommendations and predictions are indicative. Actual results may vary.

## 📞 Support

- 📖 Check documentation in `src/` modules
- 🐛 Review error logs if issues occur
- 🎯 All features have built-in error handling

---

**Built with ❤️ | Tax Saver AI v4.0 | Production-Ready** © 2025

**Changelog v4.0 (Major Overhaul):**
- ⭐ **NEW: RAG-based Tax Advisor** with Gemini LLM
- ⭐ **NEW: SHAP Explainability** for ITR Risk (shows WHY)
- ⭐ **NEW: LSTM Tax Liability Prediction** (future forecasting)
- ❌ Removed Tax Calculator (standalone feature)
- ❌ Removed Smart Expense Tracker (separate module)
- ✅ Enhanced ITR Risk with explainable AI
- ✅ Kept all Investment Optimizer features
- ✅ Modern UI with better visualizations
- ✅ Comprehensive error handling

**Changelog v3.0:**
- Added Smart Expense Tracker with AI categorization
- Updated to New Tax Regime (Mandatory FY 2025-26)
- Removed old regime comparison

**Changelog v2.0:**
- Added 4 new calculators (ELSS, Buy vs Rent, Monthly Planner, What-If)
- Fixed buy vs rent calculations
- Created 70+ test scenarios
