class Employee:
    def __init__(self, name):
        self.name = name 
class Department:
    def __init__(self, employee):
        self.empolyee = employee
        
emp = Employee("Sarim developer")   
dept = Department(emp)

print(dept.empolyee.name)