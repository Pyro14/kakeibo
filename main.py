import streamlit as st
import pandas as pd
import datetime
import calendar
from db import create_table, db_path, select_from_table, insert_record

# Initialize database
create_table(db_path, "kakeibo")

st.set_page_config(layout="wide", page_title="Kakeibo Professional")

# --- DATE & CALENDAR LOGIC ---
today = datetime.datetime.now()
year = today.year
month = today.month
current_month_str = today.strftime("%Y-%m")

# Get days in the current month
days_in_month = calendar.monthrange(year, month)[1]
month_cal = calendar.monthcalendar(year, month)

# Calculate days in first and last week (ignoring zeros from other months)
first_week_days = sum(1 for d in month_cal[0] if d != 0)
last_week_days = sum(1 for d in month_cal[-1] if d != 0)

# --- SIDEBAR GOALS ---
st.sidebar.header("🎯 Monthly Targets")
savings_goal = st.sidebar.number_input("How much to save this month?", min_value=0.0, value=200.0, step=50.0)
past_last_week_carryover = st.sidebar.number_input("Carryover from last month", min_value=0.0, value=0.0)

# --- DIALOGS ---
@st.dialog("Add Entry")
def add_entry(entry_type):
    label = "Income" if entry_type == "incomes" else "Expense"
    with st.form("entry_form"):
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        date_time = st.datetime_input("Date", value=datetime.datetime.now())
        if st.form_submit_button("Save"):
            insert_record(db_path, "kakeibo", description, amount, entry_type, date_time.strftime("%Y-%m-%d %H:%M:%S"))
            st.rerun()

# --- DATA PROCESSING ---
df = select_from_table(db_path, "kakeibo")

if not df.empty:
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Filter only for this month
    month_df = df[df['timestamp'].dt.strftime("%Y-%m") == current_month_str].copy()
else:
    month_df = pd.DataFrame(columns=['description', 'amount', 'type', 'timestamp'])

# Totals for Math
total_income = month_df[month_df['type'] == 'incomes']['amount'].sum()
total_fixed = month_df[month_df['type'] == 'fixed']['amount'].sum()
total_daily_spent = month_df[month_df['type'] == 'daily']['amount'].sum()

# --- THE FRANKENSTEIN CALCULATIONS ---
# 1. Monthly Daily Allowance
# (Income - Fixed Expenses - Savings) / Days in month
money_for_daily_use = total_income - total_fixed - savings_goal
daily_money = money_for_daily_use / days_in_month if money_for_daily_use > 0 else 0

# 2. Week Breakdowns
first_week_money = (first_week_days * daily_money) + past_last_week_carryover
middle_week_money = 7 * daily_money
last_week_money = last_week_days * daily_money

# --- UI LAYOUT ---
st.title(f"💴 Kakeibo Budget: {calendar.month_name[month]} {year}")

# Top Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Daily Allowance", f"${daily_money:,.2f}")
m2.metric("First Week Cap", f"${first_week_money:,.2f}")
m3.metric("Normal Week Cap", f"${middle_week_money:,.2f}")
m4.metric("Last Week Cap", f"${last_week_money:,.2f}")

st.divider()

# Main Display Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(":green[Incomes]")
    st.dataframe(month_df[month_df['type'] == 'incomes'][['description', 'amount', 'timestamp']], hide_index=True, use_container_width=True)
    if st.button("Add Income"): add_entry("incomes")

with col2:
    st.subheader(":red[Fixed Expenses]")
    st.dataframe(month_df[month_df['type'] == 'fixed'][['description', 'amount', 'timestamp']], hide_index=True, use_container_width=True)
    if st.button("Add Fixed"): add_entry("fixed")

with col3:
    st.subheader(":orange[Daily Expenses]")
    st.dataframe(month_df[month_df['type'] == 'daily'][['description', 'amount', 'timestamp']], hide_index=True, use_container_width=True)
    if st.button("Add Daily"): add_entry("daily")

st.divider()

# Monthly Summary Table
st.subheader("Monthly Reflection")
remaining_money = money_for_daily_use - total_daily_spent

# Visual Alert
if remaining_money < 0:
    st.error(f"You are over budget by ${abs(remaining_money):,.2f}!")
else:
    st.success(f"You still have ${remaining_money:,.2f} available for daily spending this month.")

res_table = {
    "Description": ["Days in Month", "Income Total", "Fixed Costs Total", "Savings Goal", "Daily Use Budget (Total)"],
    "Value": [days_in_month, f"${total_income:,.2f}", f"${total_fixed:,.2f}", f"${savings_goal:,.2f}", f"${money_for_daily_use:,.2f}"]
}
st.table(pd.DataFrame(res_table))