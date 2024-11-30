# CMPU 2016 Object Oriented Programming
# TU857-2
# 2024/2025 Semester 1
#
# Group: Null Pointer
# Members: 1. Ryan Pitman 2. Qiu Xie 3. Andrew Cotter 4. Adam Pekalski 5. Erik Hansen Lopez 6. Daniel Smyth
#
# A mystery adventure game where the user must solve a puzzle on each level to be able to advance through the game
# During the game, the player will interact with NPCs, collect clues, and solve puzzles to progress through the levels
# The game consists of multiple levels, each with its own unique puzzle to solve
# The game is played in the terminal and the user must input their choices
# This project is a demonstration of object oriented programming and the use of object oriented concepts such as inheritance, encapsulation, and polymorphism
# The project also demonstrates the use of classes, objects, and methods in Python
#
# The game is saved and loaded using a JSON file to store the game state
# The game is automatically saved when the player completes a level
# The player will be prompted to load the game if a save file is found
# The player can also choose to start a new game if they wish


import time
import random
import json
from pathlib import Path
from abc import ABC, abstractmethod


class Game:
    def __init__(self):
        """Set up the game by creating the needed variables, this method is called when the game is created
        Also prepares a way of storing the current level of the user and the clues they have found"""

        self.is_running = False
        self.levels = [ # List of levels in the game
            MansionLevel(),
            StudyLevel(),
            KitchenLevel(),
            CellarLevel(),
            GardenLevel(),
            ObservatoryLevel(),
            FinalLevel()
        ] 
        self._current_level = 0 # The current level the player is on
        self._player_name = None

        self.clues = []  # List to store collected clues

        self.inventory = []  # List to store items the player has collected
        self.witness_statements = []  # List to store witness statements
        self.suspect_motives = []  # List to store suspects

    def start(self):
        """
        Checks for existing save files and loads the game if found, otherwise starts a new game.
        Sets `is_running` to True and creates the instances of the levels.
        Prompts the user with a welcome message and their name if starting a new game.
        """

        # Default save file location
        save_path = Path(__file__).parent / "save_game.json"

        # Check if the JSON save file exists
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
                print("2. View level clues")
                print("3. Look for clues")
                print("4. Solve the puzzle")
                print("5. View witness statements")
                print("6. View suspect motives")
                print("7. View inventory")
                print("8. Quit the game")

                # Get the user's choice
                choice = input("Enter your choice: ")

                if choice == "1":
                    current_level.introduce_npcs()
                elif choice == "2":
                    self.view_level_clues()
                elif choice == "3":
                    # Search the room for clues
                    current_level.search_room()
                elif choice == "4":
                    if current_level.solve_puzzle():
                        # Add a specific item to the inventory per level except the final level
                        if self._current_level < len(self.levels) - 1:
                            self.add_to_inventory(f"Broken Key Part {self._current_level + 1}")

                        # Move to the next level
                        self._current_level += 1
                        
                        # Save the game
                        self.save_game()
                        break  # Exit the input loop to move to the next level
                elif choice == "5":
                    self.view_witness_statements()
                elif choice == "6":
                    self.view_suspect_motives()
                elif choice == "7":
                    self.view_inventory()
                elif choice == "8":
                    self.quit_game()
                    break
                else:
                    print("Invalid choice. Please try again.")

        if self.is_running: # Check if the game is still running, this means the player has completed all levels
            print(f"\nCongratulations {self._player_name}! You completed the game.")
            print("\nThank you for playing!")

    def view_level_clues(self):
        """If the level has been searched, show the clue for the level here"""

        # Get the current level from the list of levels
        current_level = self.levels[self._current_level]

        # If the level has been searched, show the clue for the level
        if current_level.searched:
            print(f"\nClue for {current_level.name}:")
            print(f"- {current_level.clue}")
        else:
            print("\nYou have not found the clue for this level yet.")
        
    def view_inventory(self):
        """View the current items in the player's inventory"""

        # Check if the inventory is empty
        if not self.inventory:
            print("\nYou have not collected any items yet.")
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

    def view_witness_statements(self):
        """ View the witness statements collected so far"""

        if not self.witness_statements:
            print("\nYou have not collected any witness statements yet.")
        else:
            print("\nWitness Statements:")
            for statement in self.witness_statements:
                print(f"- {statement}")
    
    def view_suspect_motives(self):
        """View the motives of the suspects in the game"""

        if not self.suspect_motives:
            print("\nYou have not collected any suspect motives yet.")
        else:
            print("\nSuspect Motives:")
            for motive in self.suspect_motives:
                print(f"- {motive}")


    def save_game(self):
        """Saves the current game state to a JSON file."""

        save_path = Path(__file__).parent / "save_game.json"

        # Create a dictionary of the game state
        game_state = {
            "player_name": self._player_name,
            "current_level": self._current_level,
            "witness_statements": self.witness_statements,
            "suspect_motives": self.suspect_motives,
            "inventory": self.inventory
        }

        # Write the game state to a JSON file
        with open(save_path, "w") as file:
            json.dump(game_state, file, indent=4)
    
    def load_game(self, save_path):
        """Loads the game state from a JSON file."""

        # Check if the save file exists
        if not save_path.exists():
            print("No save file found.")
            return

        # Read the game state from the JSON file
        with open(save_path, "r") as file:
            game_state = json.load(file)

        # Set the game state variables
        self._player_name = game_state.get("player_name", "Unknown Player")
        self._current_level = game_state.get("current_level", 0)
        self.witness_statements = game_state.get("witness_statements", [])
        self.suspect_motives = game_state.get("suspect_motives", [])
        self.inventory = game_state.get("inventory", [])

        print(f"Game loaded successfully! Welcome back {self._player_name}!")
        print(f"You are currently on level {self._current_level + 1}.")

        # Continue the game loop
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
        self.witness_statement = None

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


# Ryan Pitman - Level 1: The Mansion
class MansionLevel(Level):
    def __init__(self):
        super().__init__("The Mansion") # Level name
        self.npcs = [
            NPC("Butler", "Please do not disturb the master of the house, he is very busy at the moment."),
            NPC("Maid", "I can't believe a murder happened right here in this house!")
        ]
        self.witness = Witness("Groundskeeper Smith", "All I know is, I saw Lady Rosalind enter the house shortly before we found the body! It could not have been her!")
        self.suspect = Suspect("Miss Ivy", "Miss Ivy was loyal to the mansion owner but feared being fired due to recent accusations of theft.\nThe victim had also been unusually harsh toward her, fueling resentment.")
        self.clue = "Text on the wall that states, 'Every good house master leaves behind a Le...."
        self.searched = False

    def start(self):
        """Introduces the mansion level"""

        print(f"\nWelcome to {self.name}!")
        print("You have entered the mansion and find yourself in a grand foyer.")
        print("You must find the clue to move on to the next level.")
        print("Try to find the butler and maid in the room to help you!")

    def introduce_npcs(self):
        """Introduces the maid and butler in the mansion foyer, along with the groundskeeper"""

        print("\nIn the foyer you see the following NPCs:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")
        
        print(f"\nThere is also {self.witness} near the staircase")
        
        # Allow the user to interact with these NPCs
        choice = input("Who would you like to speak to? (Butler / Maid / Groundskeeper): ").lower()

        # Find the witness and interact
        if choice == "groundskeeper":
            statement = self.witness.provide_statement()
            print(f"\n{statement}")

            if statement not in game.witness_statements:
                game.witness_statements.append(statement)

            # Mark the suspect
            motive = self.suspect.reveal_motive()

            print("\nYou also learn that Miss Ivy has a motive to commit the crime.")
            print(f"{motive}")

            if motive not in game.suspect_motives:
                game.suspect_motives.append(motive)
    
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
        

#Adam Pekalski - Level 2: The Study
class StudyLevel(Level):
    def __init__(self):
        super().__init__("The Study")  # Level name
        self.npcs = [
            NPC("Professor", "Ah, a visitor! Perhaps you can solve this conundrum for me?"),
            NPC("Librarian", "Hello! Knowledge is the key to all mysteries, you know."),
        ]
        self.witness = Witness("Librarian Euclidia", "I sent Miss Ivy out to buy some chalk and scrolls, she was out at the time of the incident.")
        self.suspect = Suspect("Professor Alabaster", "Professor Alabaster believed the victim had stolen valuable artifacts and withheld them from public display.\nHe may have wanted to recover them or silence the victim.")
        self.clue = "X is found by finding the inverse of 3 mod 7, modular equations are key."
        self.searched = False  # Indicates if the room has been searched

    def start(self):
        """Introduce the Study level."""

        print(f"\nWelcome to {self.name}!")
        print(
            "You enter the Study. The room is dimly lit, with bookshelves lining the walls. "
            "A small desk with scattered papers sits near the center. "
            "Two figures are here, looking at you curiously."
        )
        print("A strange puzzle glistens on the chalkboard in the corner.")

    def introduce_npcs(self):
        """Introduce the NPCs in the Study."""

        print("\nIn the Study, you see the following NPCs:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")

        # Allow interaction with NPCs
        choice = input("Who would you like to interact with? (Professor / Librarian): ").lower()

        if choice == "professor":
            self.interact_with_professor()
        elif choice == "librarian":
            self.interact_with_librarian()
        else:
            print("\nYou couldn't find that NPC in the room.")

    def interact_with_professor(self):
        """Interact with the Professor NPC."""
        print("\nProfessor Algebrus: 'This mysterious puzzle appeared on my chalkboard, and I have not been able to solve it.'")
        print("Professor Algebrus: 'Can you help me solve it?'")


    def interact_with_librarian(self):
        """Interact with the Librarian NPC."""
        print("\nLibrarian Euclidia: 'I don’t have puzzles, but I can share some wisdom.'")
        statment = self.witness.provide_statement()
        print(f"\n{statment}")

        if statment not in game.witness_statements:
            game.witness_statements.append(statment)
        
        motive = self.suspect.reveal_motive()
        print("\nYou also learn that another professor, Professor Alabaster, has a motive to commit the crime.")
        print(f"{motive}")

        if motive not in game.suspect_motives:
            game.suspect_motives.append(motive)

    def search_room(self):
        """Search the Study for clues."""
        if self.searched:
            print("\nYou already found the clue for this level.")
            return

        print("\nYou search the Study for anything unusual.")
        print("You find a book on mathematics, with a note on the page.")
        print(f"The note reads: {self.clue}")
        print("You take the note with you.")
        self.searched = True

    def solve_puzzle(self):
        """Solve the puzzle in the Study level."""
        print("\nThe puzzle is still on the chalkboard: 3x ≡ 1 (mod 7).")
        print("Enter the correct value of x to proceed.")

        answer = input("Enter your answer: ")
        if answer.isdigit() and int(answer) == 5:
            print("\nCorrect! You solved the puzzle.")
            return True
        else:
            print("\nIncorrect answer, try again.")
            return False

# Qiu Xie - Level 3: The Kitchen
class KitchenLevel(Level):
    def __init__(self):
        super().__init__("The Kitchen")
        self.npcs = [
            NPC("Head Chef", "Hello. I cook the meals for the mansion."),
            NPC("Sous Chef", "I am the sous chef, I assist the head chef in the kitchen.")
        ]
        # Clue for the kitchen level
        self.clue = "A old tattered recipe, with some words faded, it says 'Bread: 2 Eggs, 500ml Milk, 50 Grams Sugar, 30 Grams Yeast, ...\nIt has poorly written handwriting at the bottom that says 'The flour weight is 10 times the sugar"
        self.suspect = Suspect("Lady Rosalind", "Lady Rosalind had a complicated relationship with the victim. They recently quarreled, and she was concerned about her reputation.")
        self.witness = Witness("Chef De Cuisine", "During the incident, I was preparing a meal alongside the Colonel.\nHe wished to learn more about cooking.")
        self.searched = False

    def start(self):
        # Introduce the kitchen level
        print("\nYou have now entered the kitchen")
        print("Along the counters are lavish ingredients and cooking utensils.")
        print("Inside the kitchen there are the two main chefs of the house, along with all the kitchen staff")

    def introduce_npcs(self):
        # Introduce the NPCs in the kitchen
        print("\nIn the Kitchen you see the following NPCs:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")

        # Allow the user to interact with these NPCs
        choice = input("Who would you like to speak to? (Head Chef / Sous Chef): ").lower()

        # Find the NPC with that role and interact
        for npc in self.npcs:
            if npc.role.lower() == choice:
                print(f"\n{npc.interact()}")
                break
        

    def search_room(self):
        """Search the kitchen for clues"""

        if self.searched:
            print("\nYou have already searched the kitchen.")
            return
        
        # Search the kitchen for clues
        print("\nYou search the kitchen for clues.")
        print("You find a cup of coffee on the table.")
        print("'It just a cup of coffee, nothing else.'")
        print("\nYou continue to search the kitchen.")
        print("You find a piece of paper on the kitchen table.")
        # Print the clue found in the kitchen
        print(f"It is: {self.clue}")
        print("You put the note in your pocket for later.")
        self.searched = True

        print(f"\nThe {self.witness} approaches you as you search the kitchen.")
        statement = self.witness.provide_statement()
        print(f"\n{statement}")

        if statement not in game.witness_statements:
            game.witness_statements.append(statement)

        # Mark the suspect
        motive = self.suspect.reveal_motive()
        print("\nYou also learn from the chef that Lady Rosalind has a motive to commit the crime.")
        print(f"{motive}")

        if motive not in game.suspect_motives:
            game.suspect_motives.append(motive)

    def solve_puzzle(self):
        """Solve the puzzle in the kitchen level to collect the clue"""

        # Solve the puzzle to unlock the door
        print("\nYou see a scale attached to the door.")
        print("You need to balance the scale to unlock the door.")
        print("The scale is currently unbalanced.")
        print("You need to add the correct weight to the scale to balance it.")
        print("It appears as though there is a white powder on the table.")

        # Get the user's input for the weight
        weight = input("What weight would you like to add to the scale?: ").strip().lower()
        if weight == '500':
            print("\nCorrect! The door clicks open.")
            return True
        else:
            print("\nIncorrect weight, try again.")
            return False
        

# Daniel Smyth - Level 4: The Cellar
class CellarLevel(Level):
    def __init__(self):
        super().__init__("The Cellar")
        self.Detective = {"health": 35, "damage": 8, "charge": False, "user": "Detective"}
        self.Skeleton = {"health": 25, "damage": 7, "charge": False, "user": "Skeleton"}
        self.movelist = ["attack", "defend", "charge"]  # Possible moves for the Skeleton
        self.npcs = [
            NPC("Groundskeeper", "I saw someone come down here with a clinking sack. After the murder, I've come down here to investigate, but something's clattering and rattling inside.")
        ]
        self.suspect = Suspect(
            "Mr. Blackthorn",
            "Mr. Blackthorn was in massive debt to the mansion owner. He stood to gain financially from stealing the deeds of the manor."
        )
        self.witness = Witness("Artifacts", "You do not find Professor Alabasters prints on the artifacts as you expected.\nYou found Mr. Blackthorns prints on the chest.")
        self.clue = "It appears as though someone was trying to hide something in the cellar, maybe inside this chest?"
        self.searched = False

    def start(self):
        """Introduce the cellar level."""
        print("\nWelcome to The Cellar!")
        print("The cellar is damp, cold, and cloaked in darkness.")
        print("A Groundskeeper stands near the door, his lantern casting flickering shadows.")

    def introduce_npcs(self):
        """Introduce the NPCs in the Cellar."""
        print("\nIn the Cellar, you see:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")
        choice = input("Would you like to speak to the Groundskeeper? (yes/no): ").lower()
        if choice == "yes":
            print(f"\n{self.npcs[0].interact()}")
            print("You learn that Mr. Blackthorn has a motive to commit the crime.")
            motive = self.suspect.reveal_motive()
            print(f"{motive}")
            if motive not in game.suspect_motives:
                game.suspect_motives.append(motive)
        else:
            print("\nYou decide not to speak to the Groundskeeper.")

    def search_room(self):
        """Search the room for clues."""
        if self.searched:
            print("\nYou have already found the chest.")
        else:
            print("\nYou cautiously search the cellar. The faint sound of rattling echoes in the darkness.")
            print("You find a locked chest, but something seems to be guarding it.")
            self.searched = True

    def solve_puzzle(self):
        """Engage in combat with the Skeleton to obtain the clue."""
        if not self.searched:
            print("\nYou haven't found the chest yet. Explore the cellar first!")
            return False

        print("\nYou approach the chest, but a Skeleton emerges from the shadows!")
        print("To retrieve the key around its neck, you must defeat it in combat.")
        
        # Combat loop
        while self.Detective["health"] > 0 and self.Skeleton["health"] > 0:
            print(f"\nDetective's Health: {self.Detective['health']}, Charge: {self.Detective['charge']}")
            print(f"Skeleton's Health: {self.Skeleton['health']}, Charge: {self.Skeleton['charge']}")

            # Get the Detective's move
            input1 = input("Detective | Choose your move (attack/charge/defend): ").strip().lower()

            # Skeleton randomly selects a move
            input2 = random.choice(self.movelist)

            print(f"\nDetective chose: {input1}")
            print(f"Skeleton chose: {input2}")

            # Perform the moves
            self.move(input1, input2, self.Detective, self.Skeleton)
            self.move(input2, input1, self.Skeleton, self.Detective)

        # Determine combat outcome
        if self.Detective["health"] <= 0 and self.Skeleton["health"] <= 0:
            print("\nBoth the Skeleton and the Detective collapse!")
            print("You wake up at the top of the cellar stairs, unsure of what happened.")
            return False
        elif self.Detective["health"] <= 0:
            print("\nThe Skeleton defeats you! You stumble upstairs in defeat.")
            return False
        elif self.Skeleton["health"] <= 0:
            print("\nThe Skeleton crumbles to dust, dropping the key!")
            print("You unlock the chest and discover artifacts hidden inside.")
            print("You dust the artifacts for fingerprints.")

            # Add the witness statement to the game
            statement = self.witness.provide_statement()

            if statement not in game.witness_statements:
                game.witness_statements.append(statement)
            
            print(f"\n{statement}")

            return True

    def move(self, main_move, other_move, main_stats, other_stats):
        """Perform the chosen move."""
        if main_move in ["attack", "atk"]:
            self.attack(main_stats, other_move, other_stats)
        elif main_move in ["defend", "def"]:
            self.defend(main_stats)
        elif main_move in ["charge", "chg"]:
            self.charge(main_stats)
        else:
            print(f"Invalid move: {main_move}. {main_stats['user']} wastes their turn.")

    def attack(self, main_stats, other_move, other_stats):
        """Handle attack logic."""
        damage = main_stats["damage"] * 2 if main_stats["charge"] else main_stats["damage"]
        main_stats["charge"] = False  # Reset charge after attack
        if other_move in ["defend", "def"]:
            reduced_damage = int(damage * 0.25)
            print(f"{other_stats['user']} defends and reduces damage by {damage - reduced_damage}.")
            damage = reduced_damage
        other_stats["health"] -= damage
        print(f"{main_stats['user']} deals {damage} damage to {other_stats['user']}.")

    def charge(self, main_stats):
        """Handle charge logic."""
        main_stats["charge"] = not main_stats["charge"]
        status = "charged" if main_stats["charge"] else "uncharged"
        print(f"{main_stats['user']} has {status} their attack.")

    def defend(self, main_stats):
        """Handle defend logic."""
        print(f"{main_stats['user']} takes a defensive stance.")

#Erik Hansen Lopez - Level 5: The Garden
class GardenLevel(Level):
    def __init__(self):
        super().__init__("The Garden")  # Level name
        # Set NPCs in the Garden level
        self.npcs = [
            NPC("Gardener", "I've been trying to identify this mysterious plant in the note. Can you help me solve this puzzle?"),
            NPC("Lobotomist", "If I may, I think the puzzle refers to a poisonous plant. Something with 'shade,' perhaps?")
        ]
        self.witness = Witness("Gardener", "Dr. Steele was with me at the time of the murder.\nAnd look, the footprints in the Nightshade patch are too small for Dr. Steele's foot size.")
        self.suspect = Suspect("Colonel Hawthorne", "The victim has recently threatened to reveal a scandal from Hawthrones past, which would ruin is reputation")
        self.clue = "A poisonous plant, that might be something to do with 'shade'"
        self.searched = False  # Track whether the level's puzzle has been solved

    def start(self):
        """Start the Garden level"""
        print(f"\nWelcome to the {self.name}!")
        print(
            "You enter the Garden. The room is bright, with vibrant-colored flowers and plants growing everywhere. "
            "Right in the center of the room stands a beautiful fountain where two figures can be spotted. "
            "One is staring at a note in confusion, while the other is examining the flowers."
        )

    def introduce_npcs(self):
        """Introduce the gardener and lobotomist in the garden."""
        print("\nIn the Garden, you see the following NPCs:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")

        # Allow the user to interact with these NPCs
        choice = input("\nWho would you like to speak to? (Gardener / Lobotomist): ").strip().lower()
        if choice == "gardener":
            self.interact_with_gardener()
        elif choice == "lobotomist":
            self.interact_with_lobotomist()
        else:
            print("\nInvalid choice. Please try again.")

    def interact_with_gardener(self):
        """Interact with the gardener NPC"""
        print(f"\n{self.npcs[0].interact()}")
        print("I swear I've seen this plant before, but I can't remember the name.")

    def interact_with_lobotomist(self):
        """Interact with the Lobotomist NPC"""
        print(f"\n{self.npcs[1].interact()}")
        print("The Lobotomist continues: 'The answer might be a poisonous plant. But which one? Something with 'shade,' perhaps?'")
        print("You also learn that Colonel Hawthorne has a motive to commit the crime.")
        motive = self.suspect.reveal_motive()
        print(f"{motive}")

        if motive not in game.suspect_motives:
            game.suspect_motives.append
        

    def solve_puzzle(self):
        """Solve the puzzle in the Garden level"""

        print("\nThe note reads:")
        print("'I am a plant with dark purple or black berries and a reputation for being highly toxic.'")
        print("'My leaves are broad and oval-shaped, and I am often associated with witchcraft and dark magic. What am I?'")
        
        # Correct answer to the puzzle
        correct_answer = "nightshade"
        user_answer = input("Enter your answer: ").strip().lower()

        if user_answer == correct_answer:
            print("\nYou identify the plant as Nightshade.")
            print("Looking around the patches, you realize there are footprints nearby.")
            print("The footprints are too small for Dr. Steele's foot size.")

            # Add the witness statement to the game
            statement = self.witness.provide_statement()

            if statement not in game.witness_statements:
                game.witness_statements.append(statement)

            return True
        else:
            print("\nHmm, that’s not quite right. Keep thinking!")

    def search_room(self):
        """Search the room for clues."""
        if self.searched:
            print("\nYou have already solved the puzzle and found the clue in this level.")
        else:
            print("\nYou search the garden carefully, noticing a note held by the Gardener.")
            print("Perhaps solving the puzzle on the note will lead to more information.")
            print("You think about what the Lobotomist said about a poisonous plant.")

# Andrew Cotter - Level 6: The Observatory
class ObservatoryLevel(Level):
    def __init__(self):
        super().__init__("The Observatory") # Level name
        self.npcs = [
            NPC("Professor", "Hmm? You say that somebody was murdered?"),
            NPC("Colonel", "What? A murder? How could that have happened?")
        ]
        self.suspect = Suspect("Dr. Victor Steele", "The mansion ownder funded Dr. Steeles Experiments but recently withdrew support, jeapordizing his career")
        self.clue = "After looking through the telescope you discover that it is aimed at the constellation 'ursa major'"
        self.searched = False

    def start(self):
        """Introduces the observatory level"""

        print(f"Welcome to {self.name}!")
        print("You enter the observatory, a large telescope dominates the middle of the room, star charts cover the walls.")
        print("In the room stands a colonel and professor")

    def introduce_npcs(self):
        """Introduces the colonel and professor in the observatory"""

        print("\nIn the observatory you see the following NPCs:")
        for npc in self.npcs:
            print(f"- {npc.name}, the {npc.role}")

        # Allow the user to interact with these NPCs
        choice = input("Who would you like to speak to? (Professor / Colonel): ").lower()

        # Find the NPC with that role and interact
        for npc in self.npcs:
            if npc.role.lower() == choice:
                print(f"\n{npc.interact()}")
                return
        
        # The NPC entered was not found
        print("\nYou were unable to find that NPC in the room.")

    def search_room(self):
        """Search the observatory for clues"""

        if self.searched:
            print("\nYou have already searched the observatory.")
            return

        print("\nYou search the observatory for clues.")
        print("You find star charts covering the walls depicting a number of constellations, you note what constellations you see.")
        print(f"You decide to check the telescope. {self.clue}")
        print("You put the note in your pocket for later.")
        self.searched = True

        # Add the suspect motive to the game
        motive = self.suspect.reveal_motive()
        print("\nThe colonel approaches you, and informs you that Dr. Victor Steele has a motive to commit the crime.")
        print(f"{motive}")

        if motive not in game.suspect_motives:
            game.suspect_motives.append(motive)


    def solve_puzzle(self):
        """Solve the puzzle in the mansion level to collect the clue"""

        print("\nYou see a lockbox with a constellation on it.")
        print("You need to input the name of the constellation to unlock it.")

        answer = input("What word would you like to enter?: ").strip().lower()
        if answer == "ursa major":
            print("Correct! You found the clue.")
            return True
        else:
            print("Incorrect word, try again.")
            return False

class FinalLevel(Level):
    def __init__(self):
        super().__init__("The Final Level")
        self.searched = False
        self.in_chamber = False

    def start(self):
        print("\nYou have found a doorway that leads to a hidden chamber.")
        print("The door is locked with a complex mechanism.")
        print("You check your inventory and find the broken key parts you collected.")
        print("It seems that you need to assemble the key to unlock the door.")
        print("You carefully assemble the key and insert it into the lock.")
        print("The door clicks open, revealing a hidden chamber.")


    def introduce_npcs(self):

        if not self.in_chamber:
            print("\nYou have not entered the hidden chamber yet.")
            return
        
        print("\nYou enter the hidden chamber.")
        time.sleep(1)
        print("In the center of the room, you see a figure standing in the shadows.")
        time.sleep(1)
        print("As you approach, the figure steps forward into the light.")
        time.sleep(1)
        print("It is the entrepreneur, Mr. Blackthorn.")
        time.sleep(1)
        print("He looks at you with a cold, calculating gaze.")
        time.sleep(1)
        print("You realize that he is the mastermind behind the murder")

    def search_room(self):
        if self.searched:
            print("You have already searched the hidden chamber")
            return
        self.in_chamber = True
        self.introduce_npcs()
        self.searched = True

    def solve_puzzle(self):
        print("\nYou successfully found the truth of the murder in this mansion")
        print("By collecting witness statements and clues, you were able to eliminate possibilities of the suspects")
        print("You arrest Mr. Blackthorn in his hidden chamber for the murder")
        print("He used nightshade from the garden to poison the food of the victim")
        
        return True

# Main method to run the game
if __name__ == "__main__":
    # Create a game instance
    game = Game()

    # Start the game
    game.start()