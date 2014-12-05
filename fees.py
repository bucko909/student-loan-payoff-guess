#!/usr/bin/python
# -*- coding: utf8
from math import *

import cgi

form = cgi.FieldStorage()

start_salary = int(form.getfirst("start_salary", 22000))
salary_factor_start = float(form.getfirst("salary_factor_start", 1.30))
salary_factor_decay = float(form.getfirst("salary_factor_decay", 0.7))
salary_factor_decay_to = float(form.getfirst("salary_factor_decay_to", 1.01))
start_age = max(int(form.getfirst("start_age", 18)), 16)
retire_age = min(int(form.getfirst("retire_age", 65)), 100)
tax_start = int(form.getfirst("tax_start", 15000))
tax_rate = float(form.getfirst("tax_rate", 0.09))
inflation = float(form.getfirst("inflation", 1.03))
loan_interest = float(form.getfirst("loan_interest", 1.03))
loan_amount = int(form.getfirst("loan_amount", 9000 + 4950))
course_years = min(int(form.getfirst("course_years", 3)), 10)

print "Content-type: text/html; charset=utf8"
print
print '''<html><head><title>Tuition fees/loan repayments</title></head><body><h1>Fees/Loans</h1><h2>Tweak values</h2><p>For the non-mathematitions, factors are in decimal and represent what'd happen to £1 after the change, so a 3%% decrease is 0.97 and 3%% increase is 1.03.</p><p>Values aren't meant to represent anything real: they're the result of applying a simple model to salaries and repayments. They should give a reasonable idea of what gets repaid and when, though.</p><form>
<input type="text" name="start_salary" value="%i" /> &lt;-- salary when you leave university; will be adjusted for inflation <br/>
<input type="text" name="salary_factor_start" value="%0.3f" /> &lt;-- payrise in first year <br/>
<input type="text" name="salary_factor_decay" value="%0.3f" /> &lt;-- payrise factor, year on year ("how much does the payrise change each year?")<br/>
<input type="text" name="salary_factor_decay_to" value="%0.3f" /> &lt;-- limiting (lowest) payrise ("what's the lowest payrise I can expect, when I'm ancient?")<br />
<input type="text" name="start_age" value="%i" /> &lt;-- start age <br />
<input type="text" name="retire_age" value="%i" /> &lt;-- retirement age <br />
<input type="text" name="tax_start" value="%i" /> &lt;-- tax payment threshold; will be adjusted for inflation <br />
<input type="text" name="tax_rate" value="%0.3f" /> &lt;-- tax rate after threshold <br />
<input type="text" name="inflation" value="%0.3f" /> &lt;-- assumed inflation <br />
<input type="text" name="loan_interest" value="%0.3f" /> &lt;-- loan interest rate (if you don't trust the government, set this above inflation) <br />
<input type="text" name="loan_amount" value="%i" /> &lt;-- loan taken per year of course; will be adjusted for inflation <br />
<input type="text" name="course_years" value="%i" /> &lt;-- years of course <br />
<input type="submit"/>
</form>

<h2>Simulation</h2>''' % (start_salary, salary_factor_start, salary_factor_decay, salary_factor_decay_to, start_age, retire_age, tax_start, tax_rate, inflation, loan_interest, loan_amount, course_years)

age = start_age
loan_size = 0.0

inflation_adjust = 1.0
salary = start_salary
for y in range(0, course_years):
	loan_size += loan_amount
	loan_size *= loan_interest
	salary *= inflation
	loan_amount *= inflation
	age += 1
	inflation_adjust *= inflation
	print "After age %i, loan is £%0.0f (adjusted £%0.0f) <br/>" % (
			age,
			loan_size,
			loan_size / inflation_adjust )

salary_factor = salary_factor_start
repaid = 0.0
while age <= retire_age:
	print "At age %i, loan is £%0.0f and salary is £%0.0f (adjusted £%0.0f and £%0.0f) <br/>" % (
			age,
			loan_size,
			salary,
			loan_size / inflation_adjust,
			salary / inflation_adjust )
	for m in range(0,12):
		repayment_size = min(loan_size, (salary / 12.0 - tax_start / 12.0) * tax_rate)
		repaid += repayment_size
		repaid *= exp(log(inflation) / 12.0)
		loan_size -= repayment_size
		loan_size *= exp(log(loan_interest) / 12.0)
	tax_start *= inflation
	salary *= salary_factor
	salary_factor = (salary_factor-salary_factor_decay_to) * salary_factor_decay + salary_factor_decay_to
	age += 1
	inflation_adjust *= inflation
	if loan_size <= 0 and tax_rate > 0:
		tax_rate = 0
		loan_size = 0

print "Total repayments: £%0.2f (adjusted £%0.2f) <br/>" % (repaid, repaid / inflation_adjust)

print "</body></html>"
