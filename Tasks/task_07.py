
from abc import ABC, abstractmethod


# Abstract parent class
class Employee(ABC):

    def __init__(self, employee_id, name):
        self.employee_id = employee_id
        self.name = name

    @abstractmethod
    def calculate_pay(self):
        pass


# Salaried employee
class SalariedEmployee(Employee):

    def __init__(self, employee_id, name, salary):
        super().__init__(employee_id, name)

        if salary < 0:
            raise ValueError("Salary cannot be negative")

        self.salary = salary

    def calculate_pay(self):
        return self.salary


# Hourly employee
class HourlyEmployee(Employee):

    def __init__(self, employee_id, name, hourly_rate, hours):
        super().__init__(employee_id, name)

        if hourly_rate < 0 or hours < 0:
            raise ValueError("Rate and hours cannot be negative")

        self.hourly_rate = hourly_rate
        self.hours = hours

    def calculate_pay(self):

        regular_hours = min(self.hours, 40)
        overtime_hours = max(self.hours - 40, 0)

        regular_pay = regular_hours * self.hourly_rate

        overtime_pay = overtime_hours * self.hourly_rate * 1.5

        return regular_pay + overtime_pay


# Commission employee
class CommissionEmployee(Employee):

    def __init__(self, employee_id, name, base_salary, sales, rate):
        super().__init__(employee_id, name)

        if base_salary < 0 or sales < 0:
            raise ValueError("Salary and sales cannot be negative")

        if not 0 <= rate <= 1:
            raise ValueError("Commission rate must be between 0 and 1")

        self.base_salary = base_salary
        self.sales = sales
        self.rate = rate

    def calculate_pay(self):

        commission = self.sales * self.rate

        return self.base_salary + commission


# Generate unified payroll summary
def payroll_summary(employees):

    summary = []
    total_payroll = 0

    for employee in employees:

        pay = employee.calculate_pay()

        summary.append({
            "employee_id": employee.employee_id,
            "name": employee.name,
            "employee_type": employee.__class__.__name__,
            "pay": pay
        })

        total_payroll += pay

    return summary, total_payroll


# MAIN PROGRAM

employees = [

    SalariedEmployee(
        101, "Ali", 50000
    ),

    HourlyEmployee(
        102, "Sara", 20, 45
    ),

    CommissionEmployee(
        103, "Ahmed", 500, 4000, 0.10
    )

]


# Generate payroll
summary, total_payroll = payroll_summary(employees)


# Display payroll report
print("EMPLOYEE PAYROLL SUMMARY")
print("-" * 60)

for employee in summary:

    print("Employee ID:", employee["employee_id"])
    print("Name:", employee["name"])
    print("Type:", employee["employee_type"])
    print("Pay:", employee["pay"])
    print("-" * 60)

print("TOTAL PAYROLL:", total_payroll)


# TEST CASES
print("\nTEST CASES")

hourly = HourlyEmployee(201, "Test Hourly", 20, 45)

commission = CommissionEmployee(
    202, "Test Commission", 500, 4000, 0.10
)

print("Hourly employee pay:", hourly.calculate_pay())
print("Commission employee pay:", commission.calculate_pay())


# ERROR HANDLING TESTS
print("\nERROR TESTS")

try:
    employee = Employee(301, "Test")
except TypeError:
    print("Cannot directly create Employee object")

try:
    HourlyEmployee(302, "Invalid", 20, -5)
except ValueError as error:
    print(error)

try:
    CommissionEmployee(303, "Invalid", 500, 4000, 1.5)
except ValueError as error:
    print(error)
