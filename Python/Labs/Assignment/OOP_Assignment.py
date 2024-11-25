# CMPU 2016 Object Oriented Programming
# TU857-2
# 2024/2025 Semester 1
#
# Group: Null Pointer
# Members: 1. Ryan Pitman 2. Qiu Xie 3. Andrew Cotter 4. Adam Pekalski 5. Erik Hansen Lopez 6. Daniel Smyth
#
# A mystery adventure game where the user must solve a puzzle on each level to gather the clue for that level
# The clues are used to solve the final puzzle and win the game
# The game is played in the terminal and the user must input their choices
# This project is a demonstration of object oriented programming and the use of object oriented concepts such as inheritance, encapsulation, and polymorphism
# The project also demonstrates the use of classes, objects, and methods in Python

import random
from abc import ABC, abstractmethod


class Game:
    def __init__(self):
        """Set up the game by creating the needed variables, this method is called when the game is created
        Also prepares a way of storing the current level of the user and the clues they have found"""

        self.is_running = False
        self.levels = [ # List of levels in the game
            MansionLevel(),
        ] 
        self._current_level = 0 # The current level the player is on
        self._player_name = None
        self.clues = []  # List to store collected clues

    def start(self):
        """Start the game by setting is_running to True and creating the instances of the levels
        also prompts the user with a welcome message, and for the user to input their name."""

        print("Welcome to the mystery adventure game created by Null Pointer!\n")
        print("You need to gather clues throughout the adventure!")
        print("The clues are used to solve the final puzzle and win the game!")
        print("Good luck!\n")

        # Prompt the user to input their name
        self._player_name = input("Please enter your name to continue: ")
        print(f"\nHello {self._player_name}!\n")

        self.is_running = True
        self.game_loop()

    def game_loop(self):
        """The main game loop that runs while the game is running
        This loop facilitates user input and choices throughout the game"""

        # Run while the game is running and the current level is less than the total number of levels
        while self.is_running and self._current_level < len(self.levels):

            # Get the current level from the list of levels and start the level
            current_level = self.levels[self._current_level]
            current_level.start()
        
            while True:
                # Display the options for the user
                print("\nWhat would you like to do?")
                print("1. Interact with the NPCs")
                print("2. Review your clues")
                print("3. Solve the puzzle")
                print("4. Look for clues")
                print("5. Quit the game")

                # Get the user's choice
                choice = input("Enter your choice: ")

                if choice == "1":
                    current_level.introduce_npcs()
                elif choice == "2":
                    self.review_clues()
                elif choice == "3":
                    if current_level.solve_puzzle():
                        # If the puzzle is solved without searching the room, add the clue to the list
                        if not current_level.clue in self.clues:
                            self.clues.append(current_level.clue)
                        break  # Exit the input loop to move to the next level
                elif choice == "4":
                    if not current_level.searched:
                        self.clues.append(current_level.clue)
                    current_level.search_room()
                elif choice == "5":
                    self.quit_game()
                    return
                else:
                    print("Invalid choice. Please try again.")

            self._current_level += 1

        if self.is_running: # Check if the game is still running, this means the player has completed all levels
            print(f"\nCongratulations {self._player_name}! You completed the game.")
            print("\nClues you collected:")
            for clue in self.clues:
                print(f"- {clue}")
            print("\nThank you for playing!")

    def review_clues(self):
        """Review the clues collected so far"""
        print("\nClues collected so far:")
        if not self.clues:
            print("You have not collected any clues yet.")
        else:
            for clue in self.clues:
                print(f"- {clue}")

    def quit_game(self):
        """Quit the game"""
        print("Thanks for playing! Goodbye.")
        self.is_running = False

# Base class for all NPCs
class NPC:
    def __init__(self, role, dialogue):
        self.name = self.generate_name()
        self.role = role
        self.dialogue = dialogue
    
    def generate_name(self):
        """This method generates a random name and prefix for each NPC instance"""

        prefixes = ["Mr.", "Mrs.", "Miss", "Dr."]
        names = [
            "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", 
            "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", 
            "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", 
            "Robinson", "Clark", "Rodriguez", "Lewis", "Lee"
        ]

        return f"{random.choice(prefixes)} {random.choice(names)}"
    
    def interact(self):
        """Allows the player to interact with the NPCs"""
        return f"{self.name} ({self.role}): {self.dialogue}"

# Base abstract class for all levels
class Level(ABC):
    def __init__(self, name):
        self.name = name
        self.npcs = []
        self.clue = None

    @abstractmethod
    def start(self):
        """Starts the level"""
        pass

    @abstractmethod
    def introduce_npcs(self):
        """Introduce the NPCs in the level"""
        pass

    @abstractmethod
    def search_room(self):
        """Search the room for clues"""
        pass

    @abstractmethod
    def solve_puzzle(self):
        """Attempt to solve the puzzle in the level"""
        pass


# Level 1: The Mansion
class MansionLevel(Level):
    def __init__(self):
        super().__init__("The Mansion") # Level name
        self.npcs = [
            NPC("Butler", "Please do not disturb the master of the house, he is very busy at the moment."),
            NPC("Maid", "I can't believe a murder happened right here in this house!")
        ]
        self.clue = "Text on the wall that states, 'Every good house master leaves behind a Le...."
        self.searched = False

    def start(self):
        """Introduces the mansion level"""

        print(f"Welcome to {self.name}!")
        print("You have entered the mansion and find yourself in a grand foyer.")
        print("You must find the clue to move on to the next level.")
        print("Try to find the butler and maid in the room to help you!")

    def introduce_npcs(self):
        """Introduces the maid and butler in the mansion foyer"""

        print("\nIn the foyer you see the following NPCs:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")

        # Allow the user to interact with these NPCs
        choice = input("Who would you like to speak to? (Butler / Maid): ").lower()

        # Find the NPC with that role and interact
        for npc in self.npcs:
            if npc.role.lower() == choice:
                print(f"\n{npc.interact()}")
                return
        
        # The NPC entered was not found
        print("\nYou were unable to find that NPC in the room.")

    def search_room(self):
        """Search the mansion foyer for clues"""
        if self.searched:
            print("\nYou have already searched the foyer.")
            return

        print("\nYou search the mansion foyer for clues.")
        print("You find a note on the wall with a missing word.")
        print(f"The notes says: {self.clue}")
        print("You put the note in your pocket for later.")
        self.searched = True


    def solve_puzzle(self):
        """Solve the puzzle in the mansion level to collect the clue"""

        print("\nYou see door with a keypad lock.")
        print("You need to input a word to unlock the door.")
        print("It appears to be a 6 letter word.")

        answer = input("What word would you like to enter?: ").strip().lower()
        if answer == "legacy":
            print("Correct! You found the clue.")
            return True
        else:
            print("Incorrect word, try again.")
            return False

if __name__ == "__main__":
    # Create a game instance
    game = Game()

    # Start the game
    game.start()
