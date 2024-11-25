# CMPU 2016 Object-Oriented Programming
# TU857-2
# 2024-25, Semester 1: Python with Sunder Ali Khowaja
# Ryan Pitman | C23741429
#
# Composition and Dependency Management, based in the mystery adventure game
# Creation of a logger class and adding logs to the gase based on interactions and gameplay

from abc import ABC, abstractmethod

class Game:
    """The Game class interacts with the other objects to facilitate game
    play, handles user input, game flow, and interactions with characters
    and the crime scene."""

    def __init__(self):
        """Initializes the Game class with its state and creates the main 
        characters, crime scene, and NPCs."""

        # Initialise the logger using composition
        self.logger = Loggable()

        self.running = True
        self.game_started = False
        self.characters_interacted = False
        self.crime_scene = CrimeScene("Mansion's Drawing Room")

        # Main Characters
        self.suspect = Suspect("Mr. Smith", "I was in the library all evening.", "Confirmed by the butler.")
        self.witness = Witness("Ms. Parker", "I saw someone near the window at the time of the incident.", "Suspicious figure in dark clothing.")
        
        # List of NPCs with different traits for convenience
        self.npcs = [
            NPC("Old Man Jenkins", "Hello there, young one.\n", "friendly"),
            NPC("Mrs. Grumpy", "What do you want? Leave me alone!\n", "hostile"),
            NPC("The Gardener", "I'm just doing my job here...\n", "indifferent")
        ]

    def run(self):
        """Runs the main game loop, displays the welcome message, and handles 
        user input for starting or quitting the game."""

        print("Welcome to 'The Poirot Mystery'")
        print("You are about to embark on a thrilling adventure as a detective.")
        print("Your expertise is needed to solve a complex case and unveil "
              "the truth.")

        while self.running:
            self.update()

    def update(self):
        """Handles the game state updates and player interactions depending on
        the progress of the game. It handles user input for different game options."""

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
                                 "'r' to review your clues, 'l' to view dialogue logs "
                                 "or 'doors' to choose a door: ")
            if player_input.lower() == "q":
                self.logger.log("Player quit game")
                self.running = False
            elif player_input.lower() == "c":
                self.continue_game()
            elif player_input.lower() == "i":
                self.interact_with_characters()
            elif player_input.lower() == "e":
                self.examine_clues()
            elif player_input.lower() == "l":
                self.print_dialogue_log()
            elif player_input.lower() == "r":
                clues = self.crime_scene.review_clues()
                if clues:
                    print(clues)
                else:
                    print("You have not found any clues yet.")
            elif player_input.lower() == "doors":
                self.choose_door()

    def start_game(self):
        """Starts the game by allowing the player to choose their detective's name 
        and sets the initial game scenario."""

        # Log the game start
        self.logger.log("Game started by player")

        player_name = input("Enter your detective's name: ")
        print(f"Welcome, Detective {player_name}!")
        print("You find yourself in the opulent drawing room of a grand mansion.")
        print("As the famous detective, you're here to solve the mysterious case of...")
        print("'The Missing Diamond Necklace'.")
        print("Put your detective skills to the test and unveil the truth!")

    def interact_with_characters(self):
        """Allows the player to choose between interacting with the main characters
        (suspect/witness) or other NPCs. Based on the user's input, interactions 
        and actions are performed."""

        print("\nYou can choose to interact with the people in the room.")
        choice = input("Do you want to talk to the suspect/witness (s) or other NPCs (n)? ").lower()

        if choice == 's':
            self.logger.log("Player interacted with suspect and witness")

            # Interact with the suspect and witness
            sus_interact = self.suspect.interact()
            wit_interact = self.witness.interact()

            self.logger.log(f"NPC Dialogue: {sus_interact}")
            self.logger.log(f"NPC Dialogue: {wit_interact}")

            print(sus_interact)
            self.suspect.perform_action()  
            
            print(wit_interact)  
            self.witness.perform_action()   

            self.crime_scene.add_clue('A suspicious figure in dark clothing')
        elif choice == 'n':
            self.logger.log("Player interacted with NPCs")

            # Interact with NPCs
            print("\nYou choose to talk with other people in the room:\n")

            # Iterate through the NPCs to interact
            for npc in self.npcs:
                npc_interact = npc.interact()  
                self.logger.log(f"NPC Dialogue: {npc_interact}")

                print(npc_interact)     
                npc.perform_action()       
        else:
            print("\nInvalid choice. Please select either 's' for suspect/witness or 'n' for NPCs.\n")

    def examine_clues(self):
        """Allows the player to examine the clues at the crime scene. If the crime 
        scene has not been investigated, new clues are added, otherwise the scene 
        is marked as already investigated."""

        if not self.crime_scene.investigated:
            self.logger.log("Player investigated the clues")

            print("\nYou decide to examine the clues at the crime scene.")
            print("You find a torn piece of fabric near the window.")
            self.crime_scene.add_clue("Torn fabric")
            self.crime_scene.investigated = True
        else:
            print("\nYou've already examined the crime scene clues.")

    def choose_door(self):
        """Prompts the player to choose one of the three available doors. Based on the
        player's choice, different scenarios unfold."""

        print("\nYou stand in front of three doors. Which one would you like to choose?")
        print("1: The Front Door\n2: The Library\n3: The Kitchen\n")

        # Prompt the player to choose a door
        door_choice = int(input("Enter the number of the door you want to open (1, 2, or 3): "))

        self.inspect_door(door_choice)

    def inspect_door(self, door):
        """Allows the player to inspect one of three doors and provides different 
        scenarios depending on the choice.
        
        Args:
            door: The selected door number (1, 2, or 3).
        """

        if door == 1:
            self.logger.log("Player interacted with door 1")
            print("You open the Front Door. It's locked, and it seems it can only be opened from outside.")
        elif door == 2:
            self.logger.log("Player interacted with door 2")
            print("You enter the Library. The room is dimly lit, filled with old books. You notice a book slightly out of place...")
        elif door == 3:
            self.logger.log("Player interacted with door 3")
            print("You step into the Kitchen. The smell of spices lingers in the air. There are dirty dishes in the sink and a knife missing from the rack.")
            self.crime_scene.add_clue('Missing Knife')
        else:
            print("Invalid choice. Please choose a valid door number (1, 2, or 3).")

    def print_dialogue_log(self):
        """Prints the dialogue logs of all interacted NPCS throughout the game"""
        has_log = False

        for log in self.logger.logs:
                if log[0] == 'N':
                    print(log)
                    has_log = True
 
        # If no dialogue logs, default print
        if not has_log:
            print("\nNo dialogue logs to show!")
            
        
        

    def continue_game(self):
        """Prints a message indicating that the player is continuing the investigation."""

        print("You continue your investigation, determined to solve the mystery...")

    def end_game(self):
        """Ends the game when all clues are gathered, printing a winning message 
        with the outcome of the investigation."""
      
        print("\nYou were able to collect all the clues!")
        print("\nYou realized that Mr. Smith killed the Lady of the House with a knife from the kitchen, and climbed out the window to escape!")
        print("\nCongratulations!")

        game.logger.log("Game finished by player")

        # Print the game logs
        print("\nGame Logs:")    
        for log in game.logger.logs:
            print(log)

        exit(0)


class CrimeScene(Game):
    """Represents the crime scene where clues are collected. It tracks whether 
    the scene has been investigated and stores the clues found."""

    def __init__(self, location):
        """Initializes the crime scene with a specific location and prepares an empty 
        list of clues.
        
        Args:
            location (str): The location of the crime scene.
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
        """Sets the investigated status of the crime scene.
        
        Args:
            value: The boolean value indicating if the scene has been investigated.
        """

        if isinstance(value, bool):
            self.__investigated = value
        else:
            print("investigated is expected to be a boolean.")

    def add_clue(self, clue):
        """Adds a clue to the crime scene's list of clues.
        
        Args:
            clue: The clue to add to the crime scene.
        """

        self.__clues.append(clue)

    def review_clues(self):
        """Allows the player to review the clues gathered from the crime scene. 
        If three clues are found, the game ends.
        
        Returns:
            list: The list of clues gathered so far.
        """
        if len(self.__clues) >= 3:
            super().end_game()
        else:
            return self.__clues


class Character(ABC):
    """The abstract Character class serves as the base class for all characters in
    the game. It provides common attributes and methods that are inherited by its 
    subclasses (e.g., Suspect, Witness, NPC)."""

    def __init__(self, name, dialogue):
        """Initializes the character with a name and a dialogue.
        
        Args:
            name: The name of the character.
            dialogue: The dialogue the character will say.
        """
        self._name = name
        self._dialogue = dialogue
        self._interacted = False

    def interact(self):
        """Handles the interaction with the character. If the character has already
        been interacted with, a different response is returned.
        
        Returns:
            str: The dialogue of the character during interaction.
        """
        if not self.has_interacted():
            interaction = f"{self._name}: {self._dialogue}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction

    def has_interacted(self):
        """Checks whether the character has already been interacted with.
        
        Returns:
            bool: True if the character has interacted, False otherwise.
        """
        return self._interacted
    
    @abstractmethod
    def perform_action(self):
        """An abstract method that must be implemented by subclasses to 
        define character-specific actions."""
        pass


class Suspect(Character):
    """Represents the suspect in the crime investigation. A special type of character
    that has an alibi and confirmation of that alibi."""

    def __init__(self, name, alibi, confirmation):
        """Initializes the suspect with a name, an alibi, and confirmation of the alibi.
        
        Args:
            name: The name of the suspect.
            alibi: The suspect's alibi during the crime.
            confirmation: The confirmation of the suspect's alibi.
        """
        super().__init__(name, "I don't have anything to say to you.")
        self.alibi = alibi
        self.confirmation = confirmation

    def interact(self):
        """Handles the interaction with the suspect, displaying their alibi and confirmation 
        if they haven't been interacted with already.
        
        Returns:
            str: The suspect's dialogue during interaction.
        """
        if not self.has_interacted():
            interaction = f"\n{self._name}: I was {self.alibi}. {self.confirmation}\n"
            self._interacted = True
        else:
            interaction = f"{self._name}: You've already asked me! Go away!"

        return interaction
    
    def perform_action(self):
        """Defines the specific action the suspect performs during interaction."""

        print(f"{self._name} nervously looks around and fidgets with their fingers\n")


class Witness(Character):
    """Represents a witness in the crime investigation. A special type of character
    that has witnessed an event related to the crime."""

    def __init__(self, name, witness, suspect):
        """Initializes the witness with a name, their witness statement, and the 
        suspect they saw.
        
        Args:
            name: The name of the witness.
            witness: The witness's statement about what they saw.
            suspect: The suspect the witness observed.
        """
        super().__init__(name, "I'm scared!")
        self.witness = witness
        self.suspect = suspect

    def interact(self):
        """Handles the interaction with the witness, providing the details of what they 
        witnessed.
        
        Returns:
            str: The witness's dialogue during interaction.
        """
        if not self.has_interacted():
            interaction = f"{self._name}: {self.witness}. It was a {self.suspect}\n"
            self._interacted = True
        else:
            interaction = f"{self._name}: Please catch him!\n"

        return interaction
    
    def perform_action(self):
        """Defines the specific action the witness performs during interaction."""
        print(f"{self._name} trembles and points at the window\n")


class NPC(Character):
    """Represents a non-playable character (NPC) in the game with different traits 
    (friendly, hostile, indifferent)."""

    def __init__(self, name, dialogue, trait):
        """Initializes the NPC with a name, dialogue, and trait that defines their
        behavior during interaction.
        
        Args:
            name: The name of the NPC.
            dialogue The NPC's dialogue.
            trait: The personality trait of the NPC (friendly, hostile, indifferent).
        """
        super().__init__(name, dialogue)
        self.trait = trait

    def perform_action(self):
        """Defines the action performed by the NPC depending on their trait."""

        if self.trait == 'friendly':
            print(f"{self._name} smiles at you gently\n")
        elif self.trait == 'angry':
            print(f"{self._name} glares and refuses to cooperate with you\n")
        elif self.trait == 'neutral':
            print(f"{self._name} shrugs at you and seems to not care\n")


class Loggable:
    def __init__(self):
        self.__logs = []

    def log(self, message: str):
        """ Takes a message and appends it to the logs array which is private
        Args:
            message: The message to be logged
        """
        self.__logs.append(message)

    @property
    def logs(self):
        """Getter method to show all logs"""
        return self.__logs
    


if __name__ == "__main__":
    game = Game()
    game.run()