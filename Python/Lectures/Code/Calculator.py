class Calculator:
    def __init__(self, x, y, o):
        self.x = x
        self.y = y
        self.operator = o

    def calculate(self) -> float:
        match self.operator:
            case '+':
                return self.x + self.y
            case '-':
                return self.x - self.y
            case '/':
                return self.x / self.y
            case '*':
                return self.x * self.y
            case _:
                return 0
            
test = Calculator(420, 69, '*')

print(test.calculate())