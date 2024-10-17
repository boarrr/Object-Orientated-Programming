# Import the ABC
from abc import ABC, abstractmethod

# Abstract base class SuperHero
class SuperHero(ABC):
    
    def __init__(self, name) -> None:
        self.name = name
    
    @abstractmethod
    def suit_up(self) -> None:
        pass

    @abstractmethod
    def rescue_world(self) -> None:
        pass


class BatMan(SuperHero):
    def suit_up(self) -> None:
        return f"{self.name} suits up as Batman" 

    def rescue_world(self) -> None:
        return f"{self.name} saves the world as Batman"


class SuperMan(SuperHero):
    def suit_up(self) -> None:
        return f"{self.name} suits up as Superman"
    
    def rescue_world(self) -> None:
        return f"{self.name} saves the world as Superman"
    

batman = BatMan("Bruce Wayne")
superman = SuperMan("Clark Kent")

print(batman.suit_up())
print(batman.rescue_world())
print(superman.suit_up())
print(superman.rescue_world())

