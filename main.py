import time

from passwordgenerator import password
from passwordgenerator import choose_password_length
from translationchaos import choose_language
from translationchaos import translation_chaos
from translationchaos import translate_lokal

from story import choose_genre
from story import choose_startingwords
from story import generate_story
from story import LANGUAGES

def get_user_mode() -> str:
    """
    Prompts the user via CLI to choose between exploring the story translation chaos 
    or directly generating a chaotic password.

    Variables:
    - choice (str): Holds the user's raw menu selection string. Used for validation checking.
    """
    print("\nWhat would you like to do?")
    print("[1] Story: See the chaotic/wrong translations of a random story")
    print("[2] Password: Generate the final password directly")
    
    choice: str = ""
    # Loop until a valid numeric choice corresponding to a menu mode is submitted
    while choice not in ["1", "2"]:
        choice = input("Your choice (1 or 2): ").strip()
        if choice not in ["1", "2"]:
            print("Invalid input. Please type '1' or '2'.")
            
    # Return a clean string keyword reflecting the chosen engine path
    return "story" if choice == "1" else "password"

if __name__ =="__main__":
    # Track performance entry point metrics
    start: float = time.time()
    story: str = ""
    translations_rounds: int = 0
    final_password: str = ""

    # Sequence of interactive user configuration inputs
    password_length: int = choose_password_length()
    output_choice: str = get_user_mode()
    words: str = choose_startingwords()
    genre: str = choose_genre()

    # Capture and safeguard the number of translation iterations
    translations_rounds = int(input("How often do you want the translations_rounds to happen? To see real entropy through the translations, you should use something higher than 10."))
    if not translations_rounds:
            print("No input detected. Using the default of 40 rounds.")
            translations_rounds = 40
    
    if translations_rounds < 1:
        print("The translation rounds is too low. It will get set to the default of 40 rounds")
        translations_rounds = 40

    # Conditional step: Only ask for a target language if the user actually wants to read the final story text
    if output_choice == "story":
        output_language = choose_language()

    # Core generation step: Create the baseline story context using the chosen options
    story = generate_story(genre, words)
    
    # Direct execution branch based on user selection mode
    if output_choice == "story":
        # Mode 1: Walk the user through the dynamic translation breakdown step by step
        translation_chaos(story, translations_rounds, output_language)
    else:
        # Mode 2: Run the full entropy equation routine behind the scenes to yield a strong password string
        final_password = password(story, translations_rounds, genre, words, password_length)
        print(f"Your password is: {final_password}")

    # Track performance exit point metrics and report total elapsed runtime logic
    end: float = time.time()
    print(f"The script worked for {end - start:.2f} seconds")