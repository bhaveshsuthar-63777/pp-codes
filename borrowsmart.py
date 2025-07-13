import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import pandas as pd
import requests
import urllib

st.set_page_config(page_title="Smart Loan Advisor v3", layout="centered")
st.title("💼 BorrowSmart AI")
st.subheader("Your AI-Powered Loan Eligibility & Advisory Tool")

name = st.text_input("👤 Enter your name:")
if name:
    st.write(f"Welcome, {name}! Let's explore realistic loan options.")

salary = st.number_input("💰 Enter your monthly salary (₹):", min_value=0)
age = st.number_input("🎂 Enter your age:", min_value=18, max_value=65)
employment = st.selectbox("🏢 Employment Type:", ["Salaried", "Self-Employed"])
loan_type = st.selectbox("📄 Loan Type:", ["Personal Loan", "Home Loan", "Car Loan", "Education Loan"])

bank_offers = {
    "Personal Loan": {"HDFC Bank": 10.5, "ICICI Bank": 11.2, "Bajaj Finserv": 12.0},
    "Home Loan": {"LIC Housing": 8.5, "SBI": 9.2, "Axis Bank": 9.8},
    "Car Loan": {"Tata Capital": 9.0, "Mahindra Finance": 9.5, "HDFC Bank": 10.1},
    "Education Loan": {"SBI Edu Loan": 8.2, "Axis Bank": 9.0, "PNB": 8.7}
}

st.subheader("🏦 Live Bank Loan Offers")
for bank, rate in bank_offers[loan_type].items():
    st.markdown(f"🔹 {bank}: {rate}% Interest Rate")

if st.button("🔍 Check Eligibility"):
    credit_score = random.randint(650, 850)
    st.info(f"📊 Estimated Credit Score: {credit_score}")

    if credit_score < 700:
        st.warning("📉 Your credit score is moderate. Improve it by paying dues on time, lowering existing EMIs, and avoiding frequent loan applications.")

    factors = {"Personal Loan": 12, "Home Loan": 60, "Car Loan": 36, "Education Loan": 48}
    max_loan = salary * factors[loan_type]
    tenure_years = 5
    bank_interest = list(bank_offers[loan_type].values())[0]
    monthly_interest = bank_interest / (12 * 100)
    num_months = tenure_years * 12

    emi = (max_loan * monthly_interest * (1 + monthly_interest) ** num_months) / ((1 + monthly_interest) ** num_months - 1)
    
    st.success(f"✅ Eligible Loan: ₹{max_loan:,.0f} ({loan_type})")
    st.write(f"📊 Estimated EMI: ₹{emi:,.0f} per month")

    st.subheader("📤 Share Your Loan Eligibility")
    share_text = f"{name}, you are eligible for a ₹{max_loan:,} {loan_type} with an EMI of ₹{emi:,.0f}/month."
    share_link = f"https://wa.me/?text={urllib.parse.quote(share_text)}"
    st.markdown(f"[👉 Share on WhatsApp]({share_link})")

st.subheader("🚀 Apply Now")
for bank in bank_offers[loan_type].keys():
    st.markdown(f"[Apply with {bank}](https://www.examplebank.com)")

st.markdown("---")
st.header("🧾 I Want a Loan – EMI & Interest Calculator")

desired_loan = st.number_input("📌 Enter desired loan amount (₹):", min_value=10000)
desired_tenure = st.slider("📆 Choose loan tenure (years):", 1, 30, 5)
desired_interest = st.slider("📈 Interest rate (annual %):", 5.0, 20.0, 10.0)

if desired_loan > 0:
    months = desired_tenure * 12
    r = desired_interest / (12 * 100)
    emi_user = (desired_loan * r * (1 + r) ** months) / ((1 + r) ** months - 1)
    total_payment = emi_user * months
    total_interest = total_payment - desired_loan

    st.success(f"💸 Monthly EMI: ₹{emi_user:,.0f}")
    st.info(f"🧾 Total Interest Paid: ₹{total_interest:,.0f} over {desired_tenure} years")
    st.info(f"💰 Total Payment (Loan + Interest): ₹{total_payment:,.0f}")


# **Angel Money Provider Section**
st.subheader("Meet your angel EMI fund provider")

# Define EMI amount (Make sure this input is correctly handled)
emi = st.number_input("Enter your EMI amount (₹):", min_value=0)

# Define user's available funds
user_funds = st.number_input("💳 Available funds for EMI (₹):", min_value=0)

# Validate user input
if user_funds < emi:
    st.warning(f"⚠️ Your current funds ({user_funds:,.0f}) are insufficient for EMI ({emi:,.0f}). Consider angel money providers.")
    
    # Define angel money interest rate
    angel_interest = 1.5  # Example interest rate
    repayment_amount = emi + (emi * (angel_interest / 100))
    
    st.info(f"🕊️ Angel Money EMI Support: Your new repayment amount will be ₹{repayment_amount:,.0f} per month.")

    st.button("📩 Apply for Angel Money Support")


    share_text_loan = f"{name} wants a ₹{desired_loan:,} loan with an EMI of ₹{emi_user:,.0f}/month. Tenure: {desired_tenure} years, Interest: {desired_interest}%."
    share_link_loan = f"https://wa.me/?text={urllib.parse.quote(share_text_loan)}"
    st.markdown(f"[👉 Share Loan Details on WhatsApp]({share_link_loan})")

st.markdown("---")
st.caption("🔒 This is a simulation. Final loan approval depends on official credit reports and lender criteria.")