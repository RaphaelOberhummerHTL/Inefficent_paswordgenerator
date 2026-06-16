import passwordgenerator
import time

def get_user_mode() -> str:
    print("\nWhat would you like to do?")
    print("[1] Story: See the chaotic/wrong translations of a random story")
    print("[2] Password: Generate the final password directly")
    
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Your choice (1 or 2): ").strip()
        if choice not in ["1", "2"]:
            print("Invalid input. Please type '1' or '2'.")
            
    # Rückgabewert als klarer String für deine Weiterverarbeitung
    return "story" if choice == "1" else "password"

if __name__ =="__main__":
    start:float = time.time()
    story: str = ""
    output_choice: str
    translations_rounds: int

    output_choice = get_user_mode()
    print(output_choice)
    translations_rounds = int(input("How often do you want the translations_rounds to happen? "))
    if translations_rounds < 1:
        print("The translation rounds is too low. It will get set to the default of 40 rounds")
        translations_rounds = 40

    if output_choice == "story":
        output_language = passwordgenerator.translationchaos.choose_language()
    story = passwordgenerator.translationchaos.story.generate_story()
    if output_choice == "story":
        passwordgenerator.translationchaos.translation_chaos(story, translations_rounds, output_language)
    else:
        print(f"Your password is: {passwordgenerator.password(story, translations_rounds)}")
    end:float = time.time()
    print(f"The script worked for{end-start}")