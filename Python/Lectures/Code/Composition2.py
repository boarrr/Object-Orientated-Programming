class Salary:
    def __init__(self, pay):
        self.pay = pay

    def annual_salary(self):
        return (self.pay * 12)

class Employee:
    def __init__(self, name, age, pay, bonus):
        self.name = name
        self.age = age
        self.bonus = bonus
        self.salary_obj = Salary(pay)

    def total_salary(self):
        return self.salary_obj.annual_salary() + self.bonus
    
emp = Employee("Anna", 20, 2500, 10000)

print(emp.total_salary())