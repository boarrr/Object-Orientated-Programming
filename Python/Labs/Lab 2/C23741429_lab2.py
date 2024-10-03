# CMPU 2016 Object-Oriented Programming TU857-2
# Ryan Pitman C23741429
# 26/09/2024
#
# A mystery game concept to teach the fundamentals of Object-Oriented Programming
# Involves a basic murder mystery concept

class CrimeScene:
    def __init__(self, location: str) -> None:
        self.location = location
        self.__clues = []  # Private attribute to store clues
        self.__investigated = False  # Private attribute to track if scene is investigated

    # Add a new clue to the private clues list
    def add_clue(self, clue: str) -> None:
        self.__clues.append(clue)

    # Review clues collected so far
    def review_clues(self) -> list:
        return self.__clues

    # Property to get or set the investigated status
    @property
    def investigated(self) -> bool:
        return self.__investigated

    @investigated.setter
    def investigated(self, value: bool) -> None:
        self.__investigated = value


class Game:
    username = ""

    def __init__(self) -> None:
        self.running = True
        self.start = False
        self.crime_scene = CrimeScene("Drawing Room")
        self.door1 = False  # Track whether the left door has been investigated
        self.door2 = False  # Track whether the right door has been investigated

    def run(self):
        """The run method starts the game loop and provides an introduction to the game."""

        print("Welcome to 'The Poirot Mystery'")
        print("You are about to embark on a thrilling adventure as a detective.")
        print("Your expertise is needed to solve a complex case and unveil the truth.")

        while self.running:
            self.update()

    def update(self) -> None:
        """The update method waits for player input and responds to their choices within the game."""

        if not self.start:
            player_input = input("Press 'q' to quit or 's' to start: ")

            if player_input.lower() == "q":
                self.running = False
            elif player_input.lower() == "s":
                self.start = self.start_game()
        else:
            print("\nWhat would you like to do?")
            print("Enter 'q' to quit.")
            print("Enter 'i' to investigate.")
            print("Enter 'r' to review your clues.")
            print("Enter 'f' to finish the case.")
            player_input = input("Your choice: ")

            # Main game logic for choices
            if player_input.lower() == "q":
                self.running = False
            elif player_input.lower() == "i":
                self.investigate_scene()
            elif player_input.lower() == "r":
                self.review_clues()
            elif player_input.lower() == "f":
                self.finish_case()
            else:
                print("Invalid input. Please try again.")

    def start_game(self) -> bool:
        """The start_game method introduces the player to the mystery case and sets the scene."""

        print("\nYou find yourself in the opulent drawing room of a grand mansion.")
        print("As the famous detective, you're here to solve the mysterious case of...")
        print("'The Missing Diamond Necklace'.")
        print("Put your detective skills to the test and unveil the truth!")
        print("In front of you, you see a large table, adorned with a lavish dinner set.")
        print("Behind the table are two doors of equal grandeur.")
        print("You can investigate the scene, the left door, or the right door to find clues.")

        self.username = input("\nEnter your detective's name: ")

        print(f"\nHello Detective {self.username}, let's begin!\n")
        print("At any time, you can:")
        print("- Enter 'i' to investigate different areas.")
        print("- Enter 'r' to review your collected clues.")
        print("- Enter 'f' to attempt to solve the case.")
        print("- Enter 'q' to quit the game.\n")

        return True

    def investigate_scene(self) -> None:
        """Investigate different parts of the scene and gather new clues."""

        print("\nWhat would you like to investigate?")
        print("Enter 'scene' to investigate the crime scene.")
        print("Enter 'left door' to investigate the left door.")
        print("Enter 'right door' to investigate the right door.")
        choice = input("Your choice: ").lower()

        if choice == 'scene':
            if self.crime_scene.investigated:
                print("The scene has already been investigated. No new clues found.")
            else:
                print("\nYou step into the dimly lit crime scene. Broken glass lies near the window, and a table is overturned.")
                print("There's a distinct smell of perfume lingering in the air. The mystery deepens.\n")
                self.crime_scene.add_clue("broken glass near window")
                self.crime_scene.add_clue("an overturned table at crime scene")
                self.crime_scene.add_clue("smell of perfume")
                self.crime_scene.investigated = True

        elif choice == 'left door':
            if self.door1:
                print("You've already investigated the left door.")
            else:
                print("\nAs you approach the left door, you hear a faint whisper... The plot thickens!")

                self.crime_scene.add_clue("faint whisper")
                self.door1 = True
        elif choice == 'right door':
            if self.door2:
                print("You've already investigated the right door.")
            else:
                print("\nYou hear the sound of a piano playing softly behind the right door. Something is amiss.")

                self.crime_scene.add_clue("sound of a piano")
                self.door2 = True
        else:
            print("Invalid choice. Please select 'scene', 'left door', or 'right door'.")

    def review_clues(self) -> None:
        """Review the clues gathered so far."""

        clues = self.crime_scene.review_clues()

        # If any clues exist, print them
        if clues:
            print("\nYour clues so far:")
            for clue in clues:
                print(f"- {clue}")
            print()
        else:
            print("You have not collected any clues yet.")

    def finish_case(self) -> None:
        """Attempt to conclude the case based on collected clues."""
        clues = self.crime_scene.review_clues()

        # Check if all essential clues are gathered to solve the case
        required_clues = {"faint whisper", "broken glass near window", "smell of perfume", "sound of a piano"}

        # If the clues required are in the set of the users clues, they solved the case
        if required_clues <= set(clues):
            print("\nCongratulations, Detective! You have solved the case of 'The Missing Diamond Necklace'.")
            print("It turns out the faint whisper was a maid hiding in the next room, who witnessed everything!")
            print("The smell of perfume led to Lady Vanishing, who was trying to frame the butler by knocking over the table.")
            print("The sound of the piano was a distraction orchestrated by the butler.")
            print("With your skills, you have brought justice to the mansion. Well done!\n")
            self.running = False  # End the game
        else:
            print("\nYou don't have enough evidence yet to make a conclusive decision. Keep investigating to gather more clues.\n")


if __name__ == "__main__":
    game = Game()
    game.run()
