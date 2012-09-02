# -*- coding: utf8
from math import *

start_salary = 25000
salary_factor_start = 1.10
salary_factor_decay = 0.9
start_age = 18
retire_age = 65
tax_start = 15000
tax_rate = 0.09
inflation = 1.03
loan_interest = 1.03
loan_amount = 9000 + 4950
loan_years = 3

age = start_age
loan_size = 0.0

inflation_adjust = 1.0
for y in range(0, loan_years):
	loan_size += loan_amount
	loan_size *= loan_interest
	age += 1
	inflation_adjust *= inflation

salary = start_salary
salary_factor = salary_factor_start
while age <= retire_age:
	print "At age %i, loan is £%0.0f and salary is £%0.0f (adjusted £%0.0f and £%0.0f)" % (
			age,
			loan_size,
			salary,
			loan_size / inflation_adjust,
			salary / inflation_adjust )
	for m in range(0,12):
		loan_size -= (salary / 12.0 - tax_start / 12.0) * tax_rate
		loan_size *= exp(log(loan_interest) / 12.0)
	tax_start *= inflation
	salary *= salary_factor
	salary_factor = (salary_factor-1.0) * salary_factor_decay + 1.0
	age += 1
	inflation_adjust *= inflation
	if loan_size < 0:
		tax_rate = 0
		loan_size = 0
