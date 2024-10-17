# CMPU 2016 Object-Oriented Programming
# TU857-2
# 2024-25, Semester 1: Python with Sunder Ali Khowaja
# SunderAli.Khowaja@tudublin.ie
#
# Mystery Adventure Game - Week 4 Lab Starter File
# Please refer to the lab sheet to understand this week's exercise.
#
# Inheritance and Method Overriding
#
# Learning objectives lab week 4:
# 1. Inheritance:
#    - Understand the concept of inheritance in object-oriented programming,
#      where a new class (subclass) can inherit attributes and methods from an
#      existing class (superclass).
#    - Recognize the benefits of code reuse, extensibility, and organization
#      that inheritance offers.
# 2. Method Overriding:
#    - Learn how to override methods in a subclass to provide specialized
#      behavior while retaining the method signature from the superclass.
#    - Comprehend that method overriding allows for polymorphism, where objects
#      of different classes can be treated uniformly through a common
#      interface.
# 3. Superclass and Subclass Relationship:
#    - Grasp the hierarchical relationship between a superclass and its
#      subclasses.
#    - Understand that subclasses inherit attributes and methods from the
#      superclass, and they can add new attributes and behaviors or modify
#      existing ones.
# 4. Polymorphism:
#    - Explore the concept of polymorphism, which allows objects of different
#      classes to be used interchangeably when they share a common superclass.
#    - Recognize how method overriding contributes to achieving polymorphic
#      behavior.
# 5. Code Modularity and Reusability:
#    - Realize the importance of code modularity and reusability through
#      inheritance.
#    - Discover how designing classes hierarchically can promote the reuse of
#      existing code while allowing for specific customizations when necessary.
# 6. Method Overriding Guidelines:
#    - Understand the guidelines and best practices for method overriding,
#      including maintaining the method signature, providing a meaningful
#      and relevant implementation, and adhering to the
#      Liskov Substitution Principle to ensure the correctness of subclass
#      behavior.
# 7. Encapsulation Preservation:
#    - Recognize the importance of preserving encapsulation while designing
#      subclasses.
#    - Learn how to use access modifiers and property methods to control access
#      to attributes and methods in both superclasses and subclasses.
# 8. Object Interaction:
#    - Realize the implications of method overriding on object interaction.
#    - Understand how the choice of which overridden method to call is
#      determined by the runtime type of the object, enabling dynamic
#      behavior based on the actual object being used.
# 9. Class Hierarchy Design:
#    - Gain experience in designing class hierarchies that effectively
#      represent the relationships between classes.
#    - Consider the "is-a" relationship and use inheritance to model
#      commonalities and differences between classes.

class Game:
    """The Game class interacts with the other objects to facilitate game
    play. It handles the main game loop, user input, and interactions with 
    the crime scene and characters."""

    def __init__(self):
        """Initializes the Game instance with game state attributes such as 
        running, game_started, and characters_interacted. It also sets up the 
        crime scene and character objects (suspect and witness)."""
        
        super().__init__()

        self.running = True
        self.game_started = False
        self.characters_interacted = False
        self.crime_scene = CrimeScene("Mansion's Drawing Room")

        # new from here:
        self.suspect = Suspect("Mr. Smith", "I was in the library "
                                            " all evening.", "Confirmed by "
                                                             "the butler.")
        self.witness = Witness("Ms. Parker", "I saw someone near "
                                             "the window at the time of the "
                                             "incident.", "Suspicious figure in "
                                                          "dark clothing.")

    def inspect_door(self, door) -> None:
        """Handles door options based on user input.
        
        Args:
            door: The door number selected by the user (1, 2, or 3).
        """

        if door == 1:
            print("You open the Front Door. It's locked, and it seems it can only be opened from outside.")
        elif door == 2:
            print("You enter the Library. The room is dimly lit, filled with old books. You notice a book slightly out of place...")
        elif door == 3:
            print("You step into the Kitchen. The smell of spices lingers in the air. There are dirty dishes in the sink and a knife missing from the rack.")
            self.crime_scene.add_clue('Missing Knife')
        else:
            # Handle invalid input
            print("Invalid choice. Please choose a valid door number (1, 2, or 3).")

    def run(self):
        """Runs the main game loop. Displays the welcome message and waits 
        for user input to start or quit the game."""

        print("Welcome to 'The Poirot Mystery'")
        print("You are about to embark on a thrilling adventure as a detective.")
        print("Your expertise is needed to solve a complex case and unveil "
              "the truth.")

        while self.running:
            self.update()

    def update(self):
        """Handles the game state and user input during the game loop. It 
        updates the game based on whether the player has started the game or 
        is in the process of interacting with the environment."""

        if not self.game_started:
            player_input = input("Press 'q' to quit or 's' to start: ")
            if player_input.lower() == "q":
                self.running = False
            elif player_input.lower() == "s":
                self.game_started = True
                self.start_game()
        else:
            player_input = input("Press 'q' to quit, 'c' to continue, "
                                 "'i' to interact, 'e' to examine clues, "
                                 "'r' to review your clues, "
                                 "or 'doors' to choose a door: ")
            if player_input.lower() == "q":
                self.running = False
            elif player_input.lower() == "c":
                self.continue_game()
            elif player_input.lower() == "i":
                self.interact_with_characters()
            elif player_input.lower() == "e":
                self.examine_clues()
            elif player_input.lower() == "r":
                clues = self.crime_scene.review_clues()
                if clues:
                    print(clues)
                else:
                    print("You have not found any clues yet.")
            elif player_input.lower() == "doors":
                self.choose_door()

    def start_game(self):
        """Starts the game and sets up the initial scenario where the player 
        is introduced to the mystery."""

        player_name = input("Enter your detective's name: ")
        print(f"Welcome, Detective {player_name}!")
        print("You find yourself in the opulent drawing room of a grand "
              "mansion.")
        print("As the famous detective, you're here to solve the mysterious "
              "case of...")
        print("'The Missing Diamond Necklace'.")
        print("Put your detective skills to the test and unveil the truth!")

    def interact_with_characters(self):
        """Handles interaction with both the suspect and witness. Displays
        dialogue and unique actions for both characters, and adds clues to 
        the crime scene based on interaction."""

        print("\nYou find two people to talk with, and you ask them about the necklace.\n")
        print(self.suspect.interact())  # Print the interaction with the suspect
        print(self.witness.interact())  # Print the interaction with the witness

        self.crime_scene.add_clue('A suspicious figure in dark clothing')

    def examine_clues(self):
        """Allows the player to examine the clues at the crime scene. If the 
        crime scene hasn't been examined yet, it adds new clues to the scene."""

        if not self.crime_scene.investigated:
            print("\nYou decide to examine the clues at the crime scene.")
            print("You find a torn piece of fabric near the window.")
            self.crime_scene.add_clue("Torn fabric")
            self.crime_scene.investigated = True
        else:
            print("\nYou've already examined the crime scene clues.")

    def choose_door(self):
        """Handles door selection and provides different scenarios based on 
        the door choice (1, 2, or 3)."""

        print("\nYou stand in front of three doors. Which one would you like to choose?")
        print("1: The Front Door\n2: The Library\n3: The Kitchen\n")

        # Prompt the player to choose a door
        door_choice = int(input("Enter the number of the door you want to open (1, 2, or 3): "))

        self.inspect_door(door_choice)

    def continue_game(self):
        """Prints a message to indicate the player is continuing their 
        investigation."""

        print("You continue your investigation, determined to solve the mystery...")

    def end_game(self):
        """Ends the game when all clues are found and prints a winning 
        message."""

        print("\nYou were able to collect all the clues!")
        print("\nYou realized that Mr. Smith killed the Lady of the House with a knife from the kitchen, and climbed out the window to escape!")
        print("\nCongratulations!")

        exit(0)


class CrimeScene(Game):
    """Represents a crime scene where clues are gathered. It manages the
    location of the crime scene and tracks clues found during the game."""

    def __init__(self, location):
        """Initializes the CrimeScene with a location and an empty list of 
        clues. It also tracks whether the scene has been investigated.
        
        Args:
            location: The location of the crime scene.
        """
        self.location = location
        self.__clues = []
        self.__investigated = False

    @property
    def investigated(self):
        """Gets the investigated status of the crime scene."""
        return self.__investigated

    @investigated.setter
    def investigated(self, value):
        """Sets the investigated status of the crime scene. Ensures that 
        only boolean values can be set.
        
        Args:
            value: The new investigated status.
        """
        if isinstance(value, bool):
            self.__investigated = value
        else:
            print("investigated is expected to be a boolean.")

    def add_clue(self, clue):
        """Adds a clue to the crime scene.
        
        Args:
            clue: The clue to be added to the crime scene.
        """
        self.__clues.append(clue)

    def review_clues(self):
        """Allows the player to review the clues found at the crime scene. 
        If three clues are found, the game ends.
        
        Returns:
            list: The list of clues found at the crime scene.
        """
        if len(self.__clues) == 3:
            super().end_game()
        else:
            return self.__clues


class Character:
    """The Character class serves as the base class, providing common
    attributes and methods for characters. The Suspect and Witness classes
    are subclasses that inherit from Character and introduce their unique
    attributes and methods."""

    def __init__(self, name, dialogue):
        """Initializes the character with a name and a dialogue.
        
        Args:
            name: The name of the character.
            dialogue: The dialogue the character will say during interaction.
        """
        self._name = name
        self._dialogue = dialogue
        self._interacted = False

    def interact(self):
        """Handles the interaction with the character, displaying their 
        dialogue. If the character has already interacted, a different 
        response is shown.
        
        Returns:
            string: The interaction dialogue of the character.
        """
        if not self.has_interacted():
            interaction = f"{self._name}: {self._dialogue}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction

    def has_interacted(self):
        """Checks whether the character has interacted already.
        
        Returns:
            bool: True if the character has interacted, False otherwise.
        """
        return self._interacted


class Suspect(Character):
    """Represents a suspect in the crime investigation, a specific type of 
    character that has an alibi and a confirmation of that alibi."""

    def __init__(self, name, alibi, confirmation):
        """Initializes the suspect with a name, an alibi, and confirmation of the alibi.
        
        Args:
            name: The name of the suspect.
            alibi: The suspect's alibi.
            confirmation: The confirmation of the alibi.
        """
        super().__init__(name, "I don't have anything to say to you.")
        self.alibi = alibi
        self.confirmation = confirmation

    def interact(self):
        """Overrides the interact method to provide the suspect's alibi and 
        confirmation if they haven't interacted yet.
        
        Returns:
            string: The interaction dialogue of the suspect.
        """
        if not self.has_interacted():
            interaction = f"{self._name}: I was {self.alibi}. {self.confirmation}"
            self._interacted = True
        else:
            interaction = f"{self._name}: You've already asked me! Go away!"

        return interaction


class Witness(Character):
    """Represents a witness in the crime investigation, a specific type of 
    character that has witnessed something related to the crime."""

    def __init__(self, name, witness, suspect):
        """Initializes the witness with a name, witness statement, and a 
        suspect they saw.
        
        Args:
            name: The name of the witness.
            witness: The witness's statement about what they saw.
            suspect: The suspect they observed.
        """
        super().__init__(name, "I'm scared!")
        self.name = name
        self.witness = witness
        self.suspect = suspect

    def interact(self):
        """Overrides the interact method to provide the witness's statement 
        about what they saw.
        
        Returns:
            string: The interaction dialogue of the witness.
        """
        if not self.has_interacted():
            interaction = f"{self._name}: {self.witness}. It was a {self.suspect}\n"
            self._interacted = True
        else:
            interaction = f"{self._name}: Please catch him!\n"

        return interaction


if __name__ == "__main__":
    game = Game()
    game.run()
