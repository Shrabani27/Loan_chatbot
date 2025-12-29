import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Loan Credibility AI Chatbot"
)

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2-flash")

st.title("Loan Credibility AI Chatbot")
st.write("AI-powered loan eligibility analysis with explanation.")

st.divider()

st.subheader("Personal Details")
age = st.slider("Age", 21, 60, 30)
marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
dependents = st.selectbox("Number of Dependents", [0, 1, 2, 3, "3+"])

st.subheader("Employment & Income")
employment_type = st.selectbox(
    "Employment Type", ["Salaried", "Self-employed", "Business", "Unemployed", "Retired"]
)

monthly_income = st.selectbox(
    "Monthly Income (₹)",
    ["< 20,000", "20,000 – 40,000", "40,000 – 75,000", "75,000 – 1,00,000", "> 1,00,000"]
)

work_experience = st.slider("Work Experience (Years)", 0, 40, 3)

st.subheader("Credit History")
credit_score = st.selectbox(
    "Credit Score Range",
    ["< 550 (Poor)", "550 – 649 (Fair)", "650 – 749 (Good)", "750+ (Excellent)"]
)

existing_loans = st.selectbox(
    "Existing Loans", ["None", "1 Loan", "2 Loans", "3+ Loans"]
)

emi_income_ratio = st.selectbox(
    "EMI to Income Ratio", ["< 30%", "30% – 40%", "40% – 50%", "> 50%"]
)

st.subheader("Loan Details")
loan_amount = st.selectbox(
    "Loan Amount", ["< 1 Lakh", "1 – 5 Lakhs", "5 – 10 Lakhs", "10 – 25 Lakhs", "> 25 Lakhs"]
)

loan_tenure = st.selectbox("Loan Tenure (Years)", [1, 2, 3, 5, 10, 15, 20])
loan_purpose = st.selectbox(
    "Loan Purpose", ["Home", "Education", "Personal", "Business", "Medical", "Vehicle"]
)

st.divider()

def calculate_score():
    score = 0

    if credit_score == "750+ (Excellent)":
        score += 30
    elif credit_score == "650 – 749 (Good)":
        score += 20
    elif credit_score == "550 – 649 (Fair)":
        score += 10

    if monthly_income in ["75,000 – 1,00,000", "> 1,00,000"]:
        score += 20
    elif monthly_income == "40,000 – 75,000":
        score += 15
    elif monthly_income == "20,000 – 40,000":
        score += 10

    if employment_type == "Salaried":
        score += 15
    elif employment_type in ["Self-employed", "Business"]:
        score += 10
    elif employment_type == "Unemployed":
        score -= 20

    if emi_income_ratio == "< 30%":
        score += 15
    elif emi_income_ratio == "30% – 40%":
        score += 10
    elif emi_income_ratio == "40% – 50%":
        score += 5

    if existing_loans == "None":
        score += 10
    elif existing_loans == "1 Loan":
        score += 5

    if 25 <= age <= 45:
        score += 5

    return max(score, 0)

if st.button("Check Loan Credibility"):
    score = calculate_score()

    st.subheader("Evaluation Result")

    if score >= 70:
        status = "High Loan Approval Probability"
        st.success(status)
    elif score >= 50:
        status = "Medium Loan Approval Probability"
        st.warning(status)
    else:
        status = "Low Loan Approval Probability"
        st.error(status)

    st.progress(score / 100)
    st.info(f"Credibility Score: {score} / 100")

    prompt = f"""
    You are a financial loan advisor AI.

    Applicant details:
    Age: {age}
    Employment Type: {employment_type}
    Monthly Income: {monthly_income}
    Credit Score: {credit_score}
    EMI Ratio: {emi_income_ratio}
    Existing Loans: {existing_loans}
    Loan Amount: {loan_amount}
    Loan Purpose: {loan_purpose}
    Calculated Score: {score}/100
    Result: {status}

    Explain:
    1. Why this score was given
    2. Key strengths in profile
    3. Weaknesses or risks
    4. 3 clear improvement suggestions

    Keep it simple and professional.
    """

    with st.spinner("Generating AI explanation..."):
        response = model.generate_content(prompt)
        st.subheader("AI Loan Advisor Explanation")
        st.write("Gemini says:",response.text)

st.divider()
st.caption("Demo AI-based loan credibility checker using Google Generative AI.")
