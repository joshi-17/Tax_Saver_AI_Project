# Deployment Guide - Tax Saver AI v4.5

## Free Deployment on Streamlit Community Cloud

### Step 1: Push Latest Changes to GitHub

All changes are already tracked in your repository:
**GitHub URL:** https://github.com/joshi-17/Tax_Saver_AI_Project

### Step 2: Deploy on Streamlit Community Cloud

1. **Go to Streamlit Community Cloud:**
   - Visit: https://streamlit.io/cloud
   - Click "Sign up" or "Sign in" with your GitHub account

2. **Create New App:**
   - Click "New app" button
   - Select your repository: `joshi-17/Tax_Saver_AI_Project`
   - Main file path: `app/streamlit_app.py`
   - Branch: `main`

3. **Configure Secrets (Important!):**
   - Before clicking "Deploy", click "Advanced settings"
   - In the "Secrets" section, add your Gemini API key:
   ```toml
   [gemini]
   api_key = "YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY"
   ```
   - Replace `YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY` with your real API key

4. **Click "Deploy":**
   - Streamlit will automatically install all dependencies from `requirements.txt`
   - Initial deployment takes 5-10 minutes
   - You'll get a free URL like: `https://your-app-name.streamlit.app`

### Step 3: Get Your Gemini API Key (If You Don't Have One)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key and paste it in Streamlit secrets

### Step 4: Test Your Deployment

Once deployed, test all features:
- ✅ Tax Calculator (New Regime)
- ✅ Investment Optimizer (ELSS, Buy vs Rent, Monthly Planner, What-If)
- ✅ ITR Risk Check (with SHAP explanations)
- ✅ RAG Tax Advisor (conversational chatbot)
- ✅ Tax Forecasting (LSTM predictions)

### Free Tier Limits

Streamlit Community Cloud is **completely free** with:
- ✅ Unlimited apps
- ✅ No credit card required
- ✅ 1GB RAM per app
- ✅ Custom domain support
- ✅ Automatic updates from GitHub
- ❌ No GPU (CPU only)

**Note:** Your app has TensorFlow (for LSTM), which might take longer to load initially (~30-60 seconds). This is normal for ML apps on free tier.

### Alternative Free Deployment Options

If Streamlit Cloud doesn't work:

#### Option 2: Hugging Face Spaces
1. Create account: https://huggingface.co/spaces
2. Create new Space → Select "Streamlit"
3. Upload your files or connect GitHub
4. Add API key in Space settings → Secrets

#### Option 3: Render (Free Tier)
1. Sign up: https://render.com
2. Create "Web Service"
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app/streamlit_app.py --server.port $PORT`
6. Add environment variable: `GEMINI_API_KEY`

### Troubleshooting

**Problem:** App crashes on startup
- **Solution:** Check logs in Streamlit dashboard, likely missing API key

**Problem:** "Module not found" error
- **Solution:** Verify all dependencies in `requirements.txt` are installed

**Problem:** LSTM takes too long to load
- **Solution:** This is normal for TensorFlow on free tier, consider lazy loading

**Problem:** Out of memory
- **Solution:** Reduce batch size in LSTM or disable TensorFlow features

### Updating Your Deployed App

1. Make changes locally
2. Commit and push to GitHub: `git push origin main`
3. Streamlit Cloud **auto-updates** within 1-2 minutes!

### Monitoring

- **View logs:** Streamlit dashboard → Your app → Logs
- **Analytics:** Built-in viewer stats
- **Errors:** Real-time error tracking in dashboard

---

## Project Structure for Deployment

```
Tax_Saver_AI_Project/
├── app/
│   └── streamlit_app.py          # Main entry point
├── src/
│   ├── tax_calculator.py
│   ├── investment_optimizer.py
│   ├── itr_risk_shap_enhanced.py
│   ├── rag_tax_advisor_enhanced.py
│   ├── lstm_tax_forecaster.py
│   └── knowledge_base/
│       └── tax_knowledge.json
├── models/
│   ├── itr_risk_model.pkl
│   ├── scaler.pkl
│   └── lstm_tax_model.h5
├── .streamlit/
│   ├── config.toml                # Theme configuration
│   └── secrets.toml.example       # API key template
├── requirements.txt               # Python dependencies
└── README.md

```

---

## Cost Estimate

**Streamlit Community Cloud:** $0/month (100% FREE)
**Gemini API:** $0/month (Free tier: 60 requests/minute)
**GitHub:** $0/month (Free for public repos)

**Total Cost: $0 per month** 🎉

---

## Support

If you encounter issues during deployment:
1. Check Streamlit Community Docs: https://docs.streamlit.io/streamlit-community-cloud
2. GitHub Issues: https://github.com/joshi-17/Tax_Saver_AI_Project/issues
3. Streamlit Forum: https://discuss.streamlit.io

---

**Deployed By:** Tax Saver AI Team
**Last Updated:** January 3, 2026
**Version:** 4.5 (Production Ready)
