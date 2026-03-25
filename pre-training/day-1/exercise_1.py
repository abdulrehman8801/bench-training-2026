name = "Abdul-Rehman"
age = 26
drinks_coffee = True
salary = 1000.5
retirement_age = 60
coffee_cups_per_day = 3
coffee_price_per_cup = 150
days_in_week = 7

years_until_retirement = retirement_age - age
weekly_coffee_budget = (
    days_in_week * coffee_price_per_cup * coffee_cups_per_day if drinks_coffee else 0
)

print(
    f"My name is {name} and I am {age} years old. "
    f"Do I drink coffee? {drinks_coffee}. My salary is {salary}."
)
print(f"Years until retirement (at {retirement_age}): {years_until_retirement}")
print(f"Weekly coffee budget: {weekly_coffee_budget}")