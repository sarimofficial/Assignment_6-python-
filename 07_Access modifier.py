class Employee:
    def __init__(self, name, salary, ssn):
        self.name = name #public
        self._salary = salary #protected
        self.__ssn = ssn #private

emp = Employee("Sarim", 500000, "03120013034")

print(emp.name)
print(emp._salary)
print(emp._Employee__ssn)





