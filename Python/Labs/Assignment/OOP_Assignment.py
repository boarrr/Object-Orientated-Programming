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
from pathlib import Path
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
        self.inventory = []  # List to store items the player has collected

    def start(self):
        """
        Checks for existing save files and loads the game if found, otherwise starts a new game.
        Sets `is_running` to True and creates the instances of the levels.
        Prompts the user with a welcome message and their name if starting a new game.
        """

        # Default save file location
        save_path = Path(__file__).parent / "save.txt"

        # Does the save file exist?
        if save_path.exists():
            # Prompt user to load the game
            while True:
                user_load = input("Save game found! Would you like to load? (yes/no): ").strip().lower()
                if user_load in ["yes", "no"]:
                    break
                print("Invalid input. Please enter 'yes' or 'no'.")

            if user_load == "yes":
                self.load_game(save_path)
                return

        # New game setup
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
                print("3. Look for clues")
                print("4. Solve the puzzle")
                print("5. View the inventory")
                print("6. Quit the game")

                # Get the user's choice
                choice = input("Enter your choice: ")

                if choice == "1":
                    current_level.introduce_npcs()
                elif choice == "2":
                    self.review_clues()
                elif choice == "3":
                    # if the room has not been searched, add the clue to the list and save the game
                    if not current_level.searched:
                        self.add_clue(current_level.clue)
                        self.save_game()
                    # Search the room for clues
                    current_level.search_room()
                elif choice == "4":
                    if current_level.solve_puzzle():
                        # If the puzzle is solved without searching the room, ensure the rooms clue is in the list
                        self.add_clue(current_level.clue)
        
                        # Add a specific item to the inventory per level
                        self.add_to_inventory(f"Broken Key Part {self._current_level + 1}")

                        # Move to the next level
                        self._current_level += 1
                        
                        # Save the game
                        self.save_game()
                        break  # Exit the input loop to move to the next level
                elif choice == "5":
                    self.view_inventory()
                elif choice == "6":
                    self.quit_game()
                    break
                else:
                    print("Invalid choice. Please try again.")

            

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
    
    def add_clue(self, clue):
        """Add a clue to the player's list of clues"""

        # Check if the clue is already in the list
        if clue in self.clues:
            return
        
        self.clues.append(clue)
        
    def view_inventory(self):
        """View the current items in the player's inventory"""

        # Check if the inventory is empty
        if not self.inventory:
            print("You have not collected any items yet.")
        else: # Print each item in the inventory
            print("\nInventory:")
            for item in self.inventory:
                print(f"- {item}")

    def add_to_inventory(self, item):
        """Add an item to the player's inventory"""

        # Check if the item is already in the inventory
        if item in self.inventory:
            print(f"You already have the {item} in your inventory.")
        else:
            self.inventory.append(item)
            print(f"{item} has been added to your inventory.")

    def save_game(self):
        """Saves the current game state to a file. Data saved includes the current level, player name, and clues collected"""

        save_path = Path(__file__).parent / "save.txt"

        # Write the game data to a file, creating a new file if it does not exist
        with open(save_path, "w") as file:
            # Store the player name and current level
            file.write(f"{self._player_name}\n")
            file.write(f"{self._current_level}\n")

            # Store the clues collected as as string
            file.write("\n".join(self.clues))

            # Add a new line for the inventory 
            file.write("\n--Inventory--\n")
            file.write("\n".join(self.inventory))
    
    def load_game(self, save_path):
        """Loads a saved game from a file, as long as that file exists"""

        # Redundant error checking
        if not save_path.exists():
            print("No save file found.")
            return
    
        # Read the game data from the file
        with open(save_path, "r") as file:
           file_data = file.readlines()

        # Set the player name, current level, and clues from the file data
        # Strip is used to ensure no whitespace from the start and end of the string
        self._player_name = file_data[0].strip()
        self._current_level = int(file_data[1].strip())

       # Check if the --Inventory-- marker is present in the file 
        try:
            inventory_index = file_data.index("--Inventory--\n")

            # Clues are all lines before the --Inventory-- marker
            self.clues = [line.strip() for line in file_data[2:inventory_index] if line.strip()]

            # Inventory items are all lines after the --Inventory-- marker
            self.inventory = [line.strip() for line in file_data[inventory_index + 1:] if line.strip()]
        except ValueError:
            # If --Inventory-- is not found, assume all remaining lines are clues
            self.clues = [line.strip() for line in file_data[2:] if line.strip()]
            self.inventory = []  # Initialize an empty inventory if no marker is found

        print(f"\nGame loaded successfully! Welcome back {self._player_name}!")
        print(f"\nYou are currently on level {self._current_level + 1}: {self.levels[self._current_level].name}")
        print("You have collected the following clues:")
        for clue in self.clues:
            print(f"- {clue}")
        
        print("\nYou have the following items in your inventory:")
        for item in self.inventory:
            print(f"- {item}")

        self.is_running = True
        self.game_loop()

    def quit_game(self):
        """Quit the game"""
        print("\nThanks for playing! Goodbye.")
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

# Base class for main game characters
class Character:
    def __init__(self, name, role):
        self.name = name
        self.role = role
    
    def introduce(self):
        """Introduce the character"""
        return f"{self.role}: {self.name}"

# Subclasses of the Character class
class Suspect(Character):
    def __init__(self, name, motive):
        super().__init__(name, "Suspect")
        self.motive = motive
    
    def reveal_motive(self):
        """Reveal the suspect's motive"""
        return f"{self.name}'s motive: {self.motive}"

class Witness(Character):
    def __init__(self, name, statement):
        super().__init__(name, "Witness")
        self.statement = statement
    
    def provide_statement(self):
        """Provide the witness's statement"""
        return f"{self.name}'s statement: {self.statement}"
    
    # Override the __str__ method to return the name of the witness
    def __str__(self):
        return self.name


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
        self.witness = Witness("Groundskeeper Smith", "I saw Lady Rosalind enter the house shortly before we found the body!")
        self.clue = "Text on the wall that states, 'Every good house master leaves behind a Le...."
        self.searched = False

    def start(self):
        """Introduces the mansion level"""

        print(f"\nWelcome to {self.name}!")
        print("You have entered the mansion and find yourself in a grand foyer.")
        print("You must find the clue to move on to the next level.")
        print("Try to find the butler and maid in the room to help you!")

    def introduce_npcs(self):
        """Introduces the maid and butler in the mansion foyer"""

        print("\nIn the foyer you see the following NPCs:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")
        
        print(f"\nThere is also {self.witness} near the staircase")
        
        # Allow the user to interact with these NPCs
        choice = input("Who would you like to speak to? (Butler / Maid / Groundskeeper): ").lower()

        # Find the witness and interact
        if choice == "groundskeeper":
            print(f"\n{self.witness.provide_statement()}")
            return

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
            print("\nCorrect! You found the clue.")
            return True
        else:
            print("\nIncorrect word, try again.")
            return False

if __name__ == "__main__":
    # Create a game instance
    game = Game()

    # Start the game
    game.start()