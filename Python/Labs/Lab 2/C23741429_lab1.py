# CMPU 2016 Object-Oriented Programming TU857-2
# Ryan Pitman C23741429
# 26/09/2024
#
# Mystery Adventure Game - Week 1 Lab Template
# Introduction to Mystery Adventure Game Development
# Setting up the initial game environment and introduction scene
#
# Learning objectives lab week 1:
# 1. Understand Basic Python Programming:
#    - Familiarize yourself with the structure of a Python script.
#    - Identify the role of classes and methods in Python code.
# 2. Handle User Input:
#    - Learn to use the input() function to receive user input.
#    - Practice capturing and processing user choices and responses.
# 3. Apply If-Else Statements:
#    - Understand the concept of conditional statements.
#    - Learn to use if-else statements to control program flow based on
#    conditions.
# 4. Enhance User Experience:
#    - Explore techniques to make user interactions more engaging and immersive.
#    - Learn to incorporate descriptive text and narrative elements into your
#    program.
# 5. Modify Menu Options Dynamically:
#    - Understand how to change menu options based on the game's state.
#    - Learn to dynamically adjust user choices to match the game's progression.

class Game:
    """The Game class is set up to manage the game's behavior."""

    def __init__(self):
        # self.running is an instance variable within the Game class
        # This means that when an instance of the Game class is created,
        # the game loop will start running by default as it is set to True.
        self.running = True

    def run(self):
        """The run method starts the game loop and provides an introduction to
        the game."""

        print("Welcome to 'The Poirot Mystery'")
        print("You are about to embark on a thrilling adventure as a "
              "detective.")
        print("Your expertise is needed to solve a complex case and unveil "
              "the truth.")

        while self.running:
            self.update()

    def update(self):
        """The update method waits for player input and responds to their
        choice to start the game or quit."""

        player_input = input("Press 'q' to quit or 's' to start: ")
        if player_input.lower() == "q":
            # we exit the game running loop by setting this flag variable
            # to False
            self.running = False
        elif player_input.lower() == "s":
            self.start_game()

    def check_door(self, door):
        """Check the door inputted by the user to return a segment of the story for them, only valid options are door 1 or door 2"""

        try:
            if door not in [1, 2]:
                raise ValueError(f"{door} is not a valid door choice!\n")
        except ValueError as e:
            print(e)
            self.check_door(self.choose_door())

        if door == 1:
            print("\nBehind door 1 you find a bedroom, with a large dresser covered in shiny jewellery")
            print("In the center of the dresser is an open jewellery box, lined with a velvet interior")
            print("On the floor you see footprints leading from the box, left by traces of a mysterious white powder")
            print("You close the door and go back to the dining room")
            return
        elif door == 2:
            print("\nBehind door 2, you see a shiny and clean kitchen along with all the counters and ingredients used")
            print("This is where all the meals are prepared by the houses staff for the owners of this mansion")
            print("You notice a dough on the counter, it appears to have been being rolled into bread for dinner")
            print("Beside the dough you notice flour over the counter and floor, probably used to help roll the dough")
            print("You leave the room and return to the dining room")

    def choose_door(self):
        """The user can choose a door out of 1 or two, and then that value gets returned"""
        player_door = int(input("Please choose a door to peek behind! '1' or '2'? "))

        return player_door
    
    def choose_option(self):
        """The player can choose to accuse a suspect or peek again behind a door"""

        try:
            player_choice = int(input("\nWould you like to (1) Accuse a Suspect or (2) Peek behind another door?: "))

            if player_choice not in [1, 2]:
                raise ValueError(f"{player_choice} is not a valid choice, try again!\n")
        except ValueError as e:
            print(e)
            self.choose_option()

        return player_choice

    def accuse_suspect(self):
        """The player is guessing the correct suspect, possible cases are the player being right, which triggers a game end, or the user being wrong
        Returns a boolean on if the guess was correct or not"""

        print("You are about to guess who stole to necklace")
        print("Who do you think stole the necklace?")
        
        try:
            player_guess = int(input("(1) The Valet\n(2) The Chef\n(3) The Maid\n"))

            if player_guess not in [1, 2, 3]:
                raise ValueError(f"{player_guess} is not a valid choice! Try again!\n")
        except ValueError as e:
            print(e)
            self.accuse_suspect()
        
        match player_guess:
            case 1:
                print("The Valet did not steal the necklace, and was very upset at being accused of it!")
                return False
            case 2:
                print("The Chef looked guilty, and pulled the necklace out of his apron, it was his footprints left by flour on the floor! Congrats!")
                return True
            case 3:
                print("The Maid did not steal the necklace, and was outraged at being accused")
                return False

    def game_loop(self):
        """Main game loop logic, show some context text and loop the users choices between checking doors or making a guess
        When the user guesses correctly, the game will go back to the main menu"""
        
        self.check_door(self.choose_door())

        print("In the dining room, you have three suspects of who stole the necklace")
        print("The valet, who drives the madam of the house whenever she needs, and carries her expensive shopping")
        print("The chef, who cooks all the meals for the house, and spends his time in the kitchen")
        print("Or the maid, who cleans all the rooms in the house, and polishes the madams jewellery")

        guess = False
    
        while not guess:
            if self.choose_option() == 1:
                guess = self.accuse_suspect()
            else:
                self.check_door(self.choose_door())

    def start_game(self):
        """The start_game method introduces the player to the mystery case and
        sets the scene."""

        print("\nYou find yourself in the opulent drawing room of a grand "
              "mansion.")
        print("As the famous detective, you're here to solve the mysterious"
              " case of...")
        print("'The Missing Diamond Necklace'.")
        print("Put your detective skills to the test and unveil the truth!")
        print("In front of you you see a large table, adorned with a lavish dinner set")
        print("Behind the table, are two doors of equal grandiour")

        self.game_loop()


if __name__ == "__main__":
    game = Game()
    game.run()
