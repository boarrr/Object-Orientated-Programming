# ABC = Abstract Base Classes
from abc import ABC, abstractmethod

class Computer(ABC):
    @abstractmethod
    def process(self) -> None:
        pass


class Laptop(Computer):
    def process(self) -> None:
        print("Its running")

    
class Programmer:
    def work(self, com) -> None:
        print("Solving Bugs")
        com.process()

class Whiteboard:
    def Write(self) -> None:
        print("Its writing")


# Can not instantiate abstract class Computer with abstract method process
#com = Computer()
#com.process()

com1 = Laptop()
com1.process()

prog1 = Programmer()
prog1.work(com1)

com2 = Whiteboard()
