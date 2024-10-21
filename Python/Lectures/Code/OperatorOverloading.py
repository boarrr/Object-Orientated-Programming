class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        sum_x = self.x + other.x
        sum_y = self.y + other.y
        return Vector2D(sum_x, sum_y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
vector1 = Vector2D(3, 2)
vector2 = Vector2D(1, 7)

resulting_vector = vector1 + vector2

print("Result:", resulting_vector)
