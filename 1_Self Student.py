class Student:
    def _init_(self, name, marks ):
        self.name = name
        self.marks = marks

        def display(self):
            print(f"Name: {self.name}Marks: {self.marks}")

s1 = Student("Sarim", 100)
s1.display()
