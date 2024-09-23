item1 = 'Phone'
item1_price = 100
item1_quantity = 5
item1_price_total = item1_price * item1_quantity

print(type(item1))
print(type(item1_price))
print(type(item1_quantity))
print(type(item1_price_total))

class Item:

    def __init__(self, name: str, price: float, quantity = 0) -> None:
        print(f"I am created {name}")

        self.name = name
        self.price = price
        self.quantity = quantity

        assert price >= 0, f"Price {price} is not greater than or equal to zero!"
        assert quantity >= 0, f"Quantity {quantity} is not greater than or equal to zero!"

        def calculate_total_price(self, x, y):
            return x * y
            return self.price * self.quantity
        
        