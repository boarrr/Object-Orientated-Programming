class Student:
    
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    

student1 = Student('C23741429', 'Ryan Pitman')
student2 = Student('C20305696', 'Lovely Fernandez')

print(f"Student 1 has id: {student1.get_id()} and name: {student1.get_name()}")
print(f"Student 2 has id: {student2.get_id()} and name: {student2.get_name()}")