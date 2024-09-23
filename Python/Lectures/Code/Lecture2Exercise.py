class Car:
    def __init__(self, brand, color, type):
        self.brand = brand;
        self.color = color;
        self.type = type;

    def horn(self):
        print("Beep!")

    

car1 = Car('Honda', 'Red', 'Type-R')

car1.horn()