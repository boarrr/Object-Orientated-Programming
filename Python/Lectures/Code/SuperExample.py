class Vehicle:
    def __init__(self) -> None:
        self.wheels = 4

    def describe(self) -> None:
        return "This is a vehicle."
    
class Car(Vehicle):
    def __init__(self, brand: str) -> None:
        super().__init__()
        self.brand = brand

    def describe(self) -> None:
        return f"This is a {self.brand} and it has {self.wheels} wheels."
    
car = Car("Toyota")

print(car.describe())