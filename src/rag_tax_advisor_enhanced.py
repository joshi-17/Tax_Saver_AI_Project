"""
Enhanced RAG-based Conversational Tax Advisor with Tax Calculation
===================================================================
Interactive chatbot that can answer tax questions AND calculate taxes through conversation
"""

import os
import json
import re
import numpy as np
from typing import List, Dict, Tuple, Optional
import google.generativeai as genai

# Comprehensive Tax Knowledge Base for Indian Taxation
TAX_KNOWLEDGE_BASE = [
    {
        "id": 1,
        "question": "What is the New Tax Regime in India?",
        "answer": "The New Tax Regime (mandatory from FY 2025-26) offers simplified tax slabs: 0-3L (0%), 3-6L (5%), 6-9L (10%), 9-12L (15%), 12-15L (20%), above 15L (30%). Standard deduction of Rs.50,000 is allowed. Rebate under Section 87A available for income up to Rs.7 lakh (zero tax). Most deductions like 80C, 80D, HRA are NOT available.",
        "category": "tax_regime",
        "keywords": ["new regime", "tax slabs", "standard deduction", "87A", "rates", "mandatory"]
    },
    {
        "id": 2,
        "question": "How to calculate tax under New Regime?",
        "answer": "Step 1: Take gross salary. Step 2: Deduct standard deduction (Rs.50,000). Step 3: Apply tax slabs: 0-3L=0%, 3-6L=5%, 6-9L=10%, 9-12L=15%, 12-15L=20%, >15L=30%. Step 4: Add 4% cess. Step 5: If taxable income ≤ Rs.7L, apply Section 87A rebate (tax becomes zero).",
        "category": "tax_calculation",
        "keywords": ["calculate", "tax calculation", "how to calculate", "formula", "steps"]
    },
    {
        "id": 3,
        "question": "What is Section 80C?",
        "answer": "Section 80C allows deduction up to Rs.1,50,000 for: ELSS mutual funds, PPF, EPF, Life Insurance premiums, NSC, Tax-saving FDs, Home loan principal, Tuition fees (2 children), Sukanya Samriddhi Yojana. NOTE: NOT available in New Tax Regime (only Old Regime).",
        "category": "deductions",
        "keywords": ["80C", "deduction", "ELSS", "PPF", "EPF", "life insurance", "NSC", "old regime"]
    },
    {
        "id": 4,
        "question": "What is Section 80D?",
        "answer": "Section 80D allows deduction for health insurance: Self & family Rs.25,000 (Rs.50,000 if senior citizen). Parents Rs.25,000 additional (Rs.50,000 if senior). Preventive health checkup Rs.5,000 included. Medical expenses for senior citizens without insurance: Rs.50,000. NOTE: Only in Old Regime.",
        "category": "deductions",
        "keywords": ["80D", "health insurance", "medical", "senior citizen", "parents", "preventive"]
    },
    {
        "id": 5,
        "question": "What is HRA exemption?",
        "answer": "HRA (House Rent Allowance) exemption = minimum of: (1) Actual HRA received, (2) Rent paid - 10% of basic salary, (3) 50% of basic for metro cities (Mumbai, Delhi, Kolkata, Chennai) OR 40% for non-metro. Requirements: Rent receipt mandatory if annual rent > Rs.1 lakh, Landlord's PAN if monthly rent > Rs.50,000. Only in Old Regime.",
        "category": "exemptions",
        "keywords": ["HRA", "house rent", "exemption", "rent allowance", "metro", "non-metro", "landlord PAN"]
    },
    {
        "id": 6,
        "question": "What is Section 24(b)?",
        "answer": "Section 24(b) home loan interest deduction: Self-occupied property: Rs.2,00,000 maximum per year. Let-out property: No limit (entire interest deductible). Pre-construction interest: Deductible in 5 equal installments after possession. Only principal repayment under 80C (Rs.1.5L limit). Old Regime only.",
        "category": "deductions",
        "keywords": ["24b", "24(b)", "home loan", "interest", "property", "house", "mortgage"]
    },
    {
        "id": 7,
        "question": "What is Section 80E?",
        "answer": "Section 80E education loan interest: No upper limit on deduction. Applicable for higher education (after Class 12). Loan for self, spouse, children, or student for whom you're legal guardian. Deduction available for maximum 8 years OR till interest is fully repaid. Only interest (not principal) is deductible. Old Regime only.",
        "category": "deductions",
        "keywords": ["80E", "education loan", "higher education", "student loan", "interest", "8 years"]
    },
    {
        "id": 8,
        "question": "What is Section 80G?",
        "answer": "Section 80G donation deductions: 100% deduction (no limit): PM Relief Fund, National Defence Fund. 50% deduction (no limit): Jawaharlal Nehru Memorial Fund. 100% deduction (10% of income limit): Certain approved institutions. 50% deduction (10% limit): Other charitable institutions. Requires 80G certificate from recipient. Old Regime only.",
        "category": "deductions",
        "keywords": ["80G", "donations", "charity", "NGO", "relief fund", "certificate"]
    },
    {
        "id": 9,
        "question": "What is Section 80CCD(1B)?",
        "answer": "Section 80CCD(1B) NPS deduction: Additional Rs.50,000 deduction for NPS (National Pension System) over and above Rs.1.5L under 80C. Total deduction becomes Rs.2 lakh (80C + 80CCD1B). Only Tier-I account contributions eligible (not Tier-II). Withdrawal: 60% tax-free at retirement, 40% to buy annuity. Old Regime only.",
        "category": "deductions",
        "keywords": ["80CCD", "80CCD(1B)", "NPS", "pension", "retirement", "additional"]
    },
    {
        "id": 10,
        "question": "When is the ITR filing deadline?",
        "answer": "ITR filing deadlines: Individuals (non-audit): July 31 of assessment year. Businesses requiring audit: October 31. Revised return: Can revise anytime before assessment or within 24 months. Belated return: Till December 31 with late filing fee under 234F (Rs.5,000 if income >Rs.5L, else Rs.1,000). Updated return: Within 24 months with additional tax and interest.",
        "category": "compliance",
        "keywords": ["ITR", "filing", "deadline", "return", "july 31", "belated", "revised"]
    },
    {
        "id": 11,
        "question": "What is TDS and when is it deducted?",
        "answer": "TDS (Tax Deducted at Source): Salary TDS by employer (monthly). Interest TDS: 10% if >Rs.40,000/year (Rs.50,000 for seniors) - banks, post office. Professional fees: 10% for residents. Rent TDS: 10% if monthly rent >Rs.50,000. Contract payments: 1-2%. Form 16 for salary TDS, Form 16A for others. Credit claimable in ITR via Form 26AS.",
        "category": "compliance",
        "keywords": ["TDS", "tax deducted", "form 16", "16A", "advance tax", "interest", "salary"]
    },
    {
        "id": 12,
        "question": "What is the difference between Old and New Tax Regime?",
        "answer": "OLD REGIME: Higher tax rates BUT allows 80C (Rs.1.5L), 80D (Rs.25K-50K), HRA, 80CCD(1B), home loan interest, etc. Suitable if deductions >Rs.2.5L. NEW REGIME: Lower tax rates (0-30%) BUT only standard deduction Rs.50K. No 80C, 80D, HRA. Mandatory from FY 2025-26. Choose OLD if high deductions, NEW if salary-only income.",
        "category": "tax_regime",
        "keywords": ["old regime", "new regime", "comparison", "difference", "which is better", "choose"]
    },
    {
        "id": 13,
        "question": "What is LTCG and STCG tax?",
        "answer": "LONG TERM CAPITAL GAINS (LTCG): Equity (held >1 year): 10% tax above Rs.1 lakh gain (STT paid). Property (held >2 years): 20% with indexation benefit. SHORTTERM CAPITAL GAINS (STCG): Equity: 15% flat (STT paid). Other assets: As per slab rates. Securities Transaction Tax (STT) must be paid for equity benefits. Exemption: Section 54 for property (reinvest in another property within 2 years).",
        "category": "capital_gains",
        "keywords": ["LTCG", "STCG", "capital gains", "equity", "property", "shares", "indexation", "54"]
    },
    {
        "id": 14,
        "question": "What documents are needed for ITR filing?",
        "answer": "Required documents: Form 16 (from employer), Form 26AS (TDS certificate), AIS (Annual Information Statement), Bank statements (all accounts), Interest certificates (savings, FDs), Home loan certificate (interest + principal), Investment proofs (80C: ELSS, PPF, LIC), Health insurance receipts (80D), Rent receipts & landlord PAN (HRA), Capital gains statements, Aadhaar, PAN, Previous ITR acknowledgement.",
        "category": "compliance",
        "keywords": ["ITR", "documents", "form 16", "26AS", "AIS", "proofs", "receipts", "required"]
    },
    {
        "id": 15,
        "question": "What is advance tax and who should pay?",
        "answer": "Advance tax: Pay tax during the year if liability >Rs.10,000. Due dates: June 15 (15%), Sept 15 (45%), Dec 15 (75%), March 15 (100%). Senior citizens (60+) with no business income: Exempt. Freelancers, business owners, high capital gains: Must pay. Interest charged: 234B (non-payment), 234C (delay). Calculate using tax calculators or consult CA.",
        "category": "compliance",
        "keywords": ["advance tax", "payment", "due dates", "234B", "234C", "interest", "quarterly"]
    },
    {
        "id": 16,
        "question": "How to claim tax refund?",
        "answer": "Tax refund process: File ITR with correct bank details (pre-validated on income tax portal). Verify ITR within 30 days (Aadhaar OTP, EVC, or DSC). Refund processed automatically after verification. Status: Check on incometaxindia.gov.in under 'Refund Status'. Credited to bank within 4-6 weeks. Interest: 6% p.a. on delayed refunds. Ensure PAN linked with bank account.",
        "category": "compliance",
        "keywords": ["refund", "ITR", "bank account", "verification", "status", "processing"]
    },
    {
        "id": 17,
        "question": "What is standard deduction?",
        "answer": "Standard deduction: Rs.50,000 flat deduction for salaried individuals (both Old & New Regime). No proof required, automatically deducted from salary income. Earlier Rs.40,000 (increased in Budget 2023). Replaces transport & medical allowance. Reduces taxable income directly. Available to pensioners also. Not available for self-employed/business income.",
        "category": "deductions",
        "keywords": ["standard deduction", "50000", "salaried", "automatic", "no proof"]
    },
    {
        "id": 18,
        "question": "What is Section 87A rebate?",
        "answer": "Section 87A rebate: If taxable income ≤ Rs.7 lakh, tax liability becomes ZERO under New Regime. Rebate amount: Lower of actual tax or Rs.25,000 (covers tax up to Rs.7L completely). Calculation: Gross income - Standard deduction. Example: Rs.7.5L gross - Rs.50K = Rs.7L taxable → Zero tax. Above Rs.7L, normal tax applies (no rebate). Both regimes offer this rebate.",
        "category": "tax_calculation",
        "keywords": ["87A", "rebate", "7 lakh", "zero tax", "exemption", "limit"]
    },
    {
        "id": 19,
        "question": "What is surcharge and cess?",
        "answer": "SURCHARGE: Additional tax on high incomes. Rs.50L-1Cr: 10%, Rs.1Cr-2Cr: 15%, Rs.2Cr-5Cr: 25%, >Rs.5Cr: 37%. CESS: 4% Health & Education Cess on (tax + surcharge). Example: Tax Rs.1L + Cess Rs.4K = Total Rs.1.04L. Marginal relief: Ensures surcharge doesn't exceed income above threshold. Both regimes have same surcharge/cess structure.",
        "category": "tax_calculation",
        "keywords": ["surcharge", "cess", "high income", "4%", "additional tax"]
    },
    {
        "id": 20,
        "question": "What is ITR-1, ITR-2, ITR-3, ITR-4?",
        "answer": "ITR-1 (Sahaj): Salary + 1 house property + other income <Rs.50L. ITR-2: Salary + multiple properties + capital gains + foreign income (no business). ITR-3: Business/profession income. ITR-4 (Sugam): Presumptive taxation for small businesses (<Rs.2Cr). Choose based on income sources. Online filing mandatory for income >Rs.5L. Use income tax portal for e-filing.",
        "category": "compliance",
        "keywords": ["ITR-1", "ITR-2", "ITR-3", "ITR-4", "form", "which form", "sahaj", "sugam"]
    }
]


class EnhancedRAGTaxAdvisor:
    """Enhanced RAG-based Tax Advisor with Interactive Tax Calculation"""

    def __init__(self, api_key: str = None):
        """Initialize Enhanced RAG Tax Advisor"""
        self.knowledge_base = TAX_KNOWLEDGE_BASE
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        # Conversation state
        self.conversation_history = []
        self.user_context = {}  # Store user's financial info during conversation

        # Tax slabs (New Regime)
        self.tax_slabs = [
            (0, 300000, 0.0),
            (300000, 600000, 0.05),
            (600000, 900000, 0.10),
            (900000, 1200000, 0.15),
            (1200000, 1500000, 0.20),
            (1500000, float("inf"), 0.30),
        ]

        # Initialize Gemini
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.llm_available = True
                print("Gemini LLM connected successfully!")
            except Exception as e:
                print(f"Warning: Gemini initialization failed: {e}")
                self.llm_available = False
        else:
            self.llm_available = False
            print("Info: No Gemini API key. Using knowledge base retrieval only.")

        # Create embeddings
        self._create_embeddings()

    def _create_embeddings(self):
        """Create text embeddings for knowledge base"""
        self.embeddings = []
        for item in self.knowledge_base:
            text = f"{item['question']} {item['answer']} {' '.join(item['keywords'])}"
            embedding = self._text_to_embedding(text.lower())
            self.embeddings.append(embedding)

    def _text_to_embedding(self, text: str) -> np.ndarray:
        """Convert text to embedding vector"""
        all_words = set()
        for item in self.knowledge_base:
            words = f"{item['question']} {item['answer']} {' '.join(item['keywords'])}".lower().split()
            all_words.update(words)

        vocab = sorted(list(all_words))
        vocab_dict = {word: idx for idx, word in enumerate(vocab)}

        vector = np.zeros(len(vocab))
        words = text.lower().split()
        for word in words:
            if word in vocab_dict:
                vector[vocab_dict[word]] += 1

        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        return vector

    def retrieve_relevant_docs(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant documents from knowledge base"""
        query_embedding = self._text_to_embedding(query.lower())

        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, doc_embedding)
            similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        relevant_docs = []
        for idx, score in similarities[:top_k]:
            doc = self.knowledge_base[idx].copy()
            doc['relevance_score'] = float(score)
            relevant_docs.append(doc)

        return relevant_docs

    def calculate_tax(self, gross_income: float) -> Dict:
        """Calculate tax under New Tax Regime"""
        # Standard deduction
        standard_deduction = 50000
        taxable_income = max(0, gross_income - standard_deduction)

        # Calculate tax
        tax = 0
        for lower, upper, rate in self.tax_slabs:
            if taxable_income > lower:
                taxable_amount = min(taxable_income, upper) - lower
                tax += taxable_amount * rate

        # Section 87A rebate
        if taxable_income <= 700000:
            tax = 0
            rebate_applied = True
        else:
            rebate_applied = False

        # Add 4% cess
        tax_before_cess = tax
        tax *= 1.04

        effective_rate = (tax / gross_income * 100) if gross_income > 0 else 0

        return {
            "gross_income": gross_income,
            "standard_deduction": standard_deduction,
            "taxable_income": taxable_income,
            "tax_before_cess": tax_before_cess,
            "cess": tax - tax_before_cess,
            "total_tax": tax,
            "effective_rate": effective_rate,
            "rebate_applied": rebate_applied,
            "net_income": gross_income - tax
        }

    def detect_tax_calculation_intent(self, query: str) -> bool:
        """Detect if user wants to calculate tax (not just ask about tax concepts)"""
        query_lower = query.lower()

        # Strong calculation indicators
        strong_indicators = [
            "calculate my tax", "calculate tax", "compute tax",
            "how much tax", "what is my tax", "my tax",
            "tax liability", "tax payable", "how much do i pay"
        ]

        # Check for strong indicators first
        if any(ind in query_lower for ind in strong_indicators):
            return True

        # Check if query mentions salary/income with an amount
        has_salary_mention = any(word in query_lower for word in ["my salary", "i earn", "salary is", "income is", "i make"])
        has_amount = bool(re.search(r'\d+', query))

        # Only trigger if both salary mention AND amount present
        if has_salary_mention and has_amount:
            return True

        # Don't trigger on informational queries
        info_keywords = ["what is", "explain", "difference between", "should i choose", "regime"]
        if any(keyword in query_lower for keyword in info_keywords):
            return False

        return False

    def extract_salary_from_query(self, query: str) -> Optional[float]:
        """Extract salary amount from query"""
        # Patterns for salary extraction
        patterns = [
            r'(?:salary|income|earn).*?(\d+\.?\d*)\s*(?:lakh|lakhs|l)',
            r'(?:salary|income|earn).*?(\d+\.?\d*)\s*(?:crore|crores|cr)',
            r'Rs\.?\s*(\d+(?:,\d+)*)',
            r'₹\s*(\d+(?:,\d+)*)',
            r'(\d+\.?\d*)\s*(?:lakh|lakhs|l)',
            r'(\d+\.?\d*)\s*(?:crore|crores|cr)',
        ]

        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                amount = float(amount_str)

                # Convert to absolute value
                if 'lakh' in query.lower() or ' l' in query.lower():
                    amount *= 100000
                elif 'crore' in query.lower() or 'cr' in query.lower():
                    amount *= 10000000

                return amount

        return None

    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response using Gemini LLM or fallback"""
        # Check if this is a tax calculation request
        if self.detect_tax_calculation_intent(query):
            salary = self.extract_salary_from_query(query)

            if salary:
                # Calculate tax
                tax_result = self.calculate_tax(salary)
                self.user_context['last_salary'] = salary
                self.user_context['last_tax_result'] = tax_result

                # Generate detailed response
                response = f"""**Tax Calculation for Annual Salary: Rs.{tax_result['gross_income']:,.0f}**

**Breakdown:**
- Gross Income: Rs.{tax_result['gross_income']:,.0f}
- Standard Deduction: Rs.{tax_result['standard_deduction']:,.0f}
- Taxable Income: Rs.{tax_result['taxable_income']:,.0f}

**Tax Details:**
- Tax (before cess): Rs.{tax_result['tax_before_cess']:,.0f}
- Health & Education Cess (4%): Rs.{tax_result['cess']:,.0f}
- **Total Tax Payable: Rs.{tax_result['total_tax']:,.0f}**

{"**Section 87A Rebate Applied! Your tax is ZERO.**" if tax_result['rebate_applied'] else f"Effective Tax Rate: {tax_result['effective_rate']:.2f}%"}

**Net Take-Home: Rs.{tax_result['net_income']:,.0f}**

---
**Want to optimize your tax? Ask me about:**
- Available deductions (though limited in New Regime)
- Investment options
- Tax-saving strategies
"""
                return response
            else:
                # Ask for salary if not provided
                return """To calculate your tax, I need your annual salary. Please tell me:

"My salary is ___ lakhs" or "I earn Rs. ___ per year"

Example: "My salary is 12 lakhs" or "I earn 15 lakh annually" """

        # For non-calculation queries, use LLM or fallback
        if not self.llm_available:
            if context_docs:
                return context_docs[0]['answer'] + "\n\nTip: For personalized advice, consult a Chartered Accountant."
            return "I don't have specific information about that. Please rephrase or ask about tax sections, deductions, or filing procedures."

        try:
            # Prepare context
            context = "\n\n".join([
                f"Context {i+1}:\nQ: {doc['question']}\nA: {doc['answer']}"
                for i, doc in enumerate(context_docs)
            ])

            # Enhanced prompt for Gemini
            prompt = f"""You are an expert Indian tax advisor with deep knowledge of Income Tax Act 1961. Answer the user's question accurately and concisely.

**Context from Knowledge Base:**
{context}

**User Question:** {query}

**Instructions:**
1. Answer based on the provided context and your knowledge of Indian taxation
2. Be specific and cite relevant sections (80C, 80D, 24b, etc.) when applicable
3. If the question is about calculations, provide step-by-step breakdown
4. Mention New Tax Regime vs Old Regime differences if relevant
5. Keep answer clear, practical, and under 200 words
6. Add a note that tax laws change and CA consultation is recommended for filing

**Answer:**"""

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            print(f"Gemini API error: {e}")
            if context_docs:
                return context_docs[0]['answer'] + "\n\nNote: For personalized tax advice, please consult a qualified Chartered Accountant."
            return "I encountered an error. Please try rephrasing your question or ask about: tax calculation, deductions (80C, 80D), HRA, ITR filing, or capital gains."

    def ask(self, query: str) -> Dict:
        """Main method to ask a tax question"""
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": query})

        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(query, top_k=3)

        # Generate response
        response = self.generate_response(query, relevant_docs)

        # Add to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})

        return {
            "query": query,
            "answer": response,
            "sources": relevant_docs,
            "llm_used": self.llm_available,
            "calculation_performed": self.detect_tax_calculation_intent(query),
            "user_context": self.user_context
        }

    def get_conversation_summary(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history

    def clear_conversation(self):
        """Clear conversation history and context"""
        self.conversation_history = []
        self.user_context = {}


# ======================================================
# DEMO / TESTING
# ======================================================
if __name__ == "__main__":
    print("Initializing Enhanced RAG Tax Advisor...")

    advisor = EnhancedRAGTaxAdvisor()

    test_queries = [
        "My salary is 12 lakhs, calculate my tax",
        "What is Section 80C?",
        "I earn 8 lakh per year, how much tax do I pay?",
        "How to claim HRA exemption?",
        "Calculate tax for income of 15 lakh",
    ]

    print("\n" + "="*70)
    print("TESTING ENHANCED RAG TAX ADVISOR")
    print("="*70 + "\n")

    for query in test_queries:
        print(f"User: {query}")
        result = advisor.ask(query)
        print(f"Assistant:\n{result['answer']}")
        print(f"\nSources: {len(result['sources'])} documents | LLM: {result['llm_used']}")
        print(f"Calculation: {'Yes' if result['calculation_performed'] else 'No'}")
        print("-" * 70 + "\n")

    print("Enhanced RAG Tax Advisor initialized successfully!")
