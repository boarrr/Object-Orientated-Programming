# Base class for Shapes
class Shape:
    def area(self) -> float:
        pass # Placeholder Method

# Circle inherits Shpae
class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

	# Overrides area placeholder
    def area(self) -> float:
        return 3.14 * self.radius * self.radius

# Rectangle inherits Shape
class Rectangle(Shape):
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

	# Overrides area placeholder
    def area(self) -> float:
        return self.width * self.height
    

shapes = [Circle(5), Rectangle(4, 6)]

for shape in shapes:
    print(f"Area: {shape.area()}")