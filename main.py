import streamlit as st
import pandas as pd
import datetime
from db import create_table, db_path,select_from_table,insert_record

create_table(db_path, "kakeibo")

st.set_page_config( layout= "wide")

today=datetime.datetime.now()
year = today.year
month = today.month
day = today.day
time= today.strftime("%H:%M:%S")

#income decorator

@st.dialog("test")
def add_income():
    with st.form("add income"):
        col1,col2,col3 = st.columns(3)

        with col2:
            amount = st.text_input("Amount")
        with col1:
            description = st.text_input("Description")
        with col3:
            date_time = st.datetime_input("Date Time", value=datetime.datetime.now())
        
        #submit
        submit = st.form_submit_button("add income")
        if submit:
            insert_record(db_path, "kakeibo", description, amount , "incomes", date_time)
            st.rerun()
            

# fix expense decorator

@st.dialog("test")
def add_expense():
    with st.form("add expense"):
        col1,col2,col3 = st.columns(3)

        with col2:
            amount = st.text_input("Amount")
        with col1:
            description = st.text_input("Description")
        with col3:
            date_time = st.datetime_input("Date Time", value=datetime.datetime.now())

        #submit
        submit = st.form_submit_button("add expense")
        if submit:
            expenses = {"Description":description, "Amount":amount, "timestamp":date_time}
            st.session_state.dict_fix_expenses.append(expenses)
            st.rerun()


#daily expenses decorator

@st.dialog("test")
def add_daily_expense():
    with st.form("add daily expenses"):
        col1,col2,col3 = st.columns(3)

        with col2:
            amount = st.text_input("Amount")
        with col1:
            description = st.text_input("Description")
        with col3:
            date_time = st.datetime_input("Date Time", value=datetime.datetime.now())

        #submit
        submit = st.form_submit_button("add daily expense")
        if submit:
            daily_expenses = {"Description":description, "Amount":amount, "timestamp":date_time}
            st.session_state.dict_daily_expenses.append(daily_expenses)
            st.rerun()

if st.session_state.get("dict_incomes") is None:
    st.session_state.dict_incomes = []

if st.session_state.get("dict_fix_expenses") is None:
    st.session_state.dict_fix_expenses = []

if st.session_state.get("dict_daily_expenses") is None:
    st.session_state.dict_daily_expenses = []


col1, col2, col3= st.columns(3)
with col2:
    st.subheader(":red[Fixed Expenses]", text_alignment="center")
    fix_expenses = pd.DataFrame(st.session_state.dict_fix_expenses)
    st.dataframe(fix_expenses, hide_index=True)
    info_submit = st.button("Add expense")
    if info_submit:
        add_expense()


with col3:
    st.subheader(":orange[Daily Expenses]", text_alignment="center")
    daily_expenses = pd.DataFrame(st.session_state.dict_daily_expenses )
    st.dataframe(daily_expenses, hide_index=True)
    income_submit = st.button ("Add daily expense")
    if income_submit:
        add_daily_expense()

with col1:
    st.subheader(":green[Incomes]", text_alignment="center")
    incomes = pd.DataFrame(st.session_state.dict_incomes)
    st.dataframe(incomes, hide_index=True)
    income_submit = st.button ("Add income")
    if income_submit:
        add_income()

fix_expenses = pd.DataFrame(st.session_state.dict_fix_expenses)
incomes = pd.DataFrame(st.session_state.dict_incomes)

month = "month"
week = "week"
week_budget="weekb"
week_spent="weeks"
total_money= "total money"
result_table = { "month budget":[month], "month spent":[week], "this week budget": week_budget, "this week spent": week_spent, "total money": total_money}
st.table(result_table)

st.dataframe(select_from_table(db_path, "kakeibo"))