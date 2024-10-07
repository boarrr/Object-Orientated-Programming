class Vehicle:
    def describe(self) -> None:
        return "This is a vehicle."
    
class Car(Vehicle):
    def __init__(self, brand) -> None:
        self.brand = brand

    def describe(self) -> None:
        return f"This is a {self.brand}"
    

car = Car("Toyota")
print(car.describe())