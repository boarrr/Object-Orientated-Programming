class Vehicle:
    def describe(self) -> None:
        return "This is a vehicle."
    
class Car(Vehicle):
    def __init__(self, brand) -> None:
        self.brand = brand

car = Car("Toyota")

print(car.describe())