class Payment:
    def __init__(self, price) -> None:
        self.__final_price = price + price * 0.05

book = Payment(10)


# book.__final_price = 0
print(book.__final_price)
