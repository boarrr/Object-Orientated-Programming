class Circle:
    # Attributes
    radius = 0

    # Constructor
    def __init__(self, r):
        self.radius = r

    # Method to calculate area
    def calculate_area(self):
        return 3.14 * self.radius * self.radius
    

# Create an object
my_circle = Circle(5)

area = my_circle.calculate_area()

print(area)
