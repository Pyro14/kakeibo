import calendar 
import streamlit as st


past_last_week_money = 34

#date
year= 2026
month = 1
days_in_month = calendar.monthrange(year, month)[1]
print(days_in_month,"days in month")

#incomes
income = 670
extra_income = 430

#expenses
total_expenses=0
expenses = {"Draco":100, "Papa":50, "Limpieza facial":90}
for value in expenses.values():
    total_expenses += value

#calculations
daily_money = income + extra_income - total_expenses
print(daily_money,"for this month")
savings = int(input("how much do you want to save this month"))
daily_money -= savings
daily_money /= days_in_month
print(round(daily_money,2))

#first and last week calculations
first_last_calculation = (0, -1)
for i in first_last_calculation:
    week = calendar.monthcalendar(year, month)[i]
    days = sum(1 for day in week if day != 0)
    if i == 0:
        first_week_days = days
    else:
        last_week_days = days
print("first week",first_week_days, "last week", last_week_days)

first_week_money = first_week_days * daily_money
last_week_money = last_week_days * daily_money

print("fist week money", round(past_last_week_money + first_week_money,2))
print("middle weeks money", round(daily_money*7,2))