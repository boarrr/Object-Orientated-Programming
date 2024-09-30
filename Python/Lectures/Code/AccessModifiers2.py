class Payment:
    def __init__(self, price) -> None:
        self.__final_price = price + price * 0.05

    def get_final_price(self):
        return self.__final_price
    
book = Payment(10)

book._Payment__final_price = 0

print(book.get_final_price())