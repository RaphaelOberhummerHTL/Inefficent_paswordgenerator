import ollama
import random
import psutil
import datetime
import time

import story

def translate_lokal(text, output_language) -> str:
    """
    Translates a given text into the target language using a local Ollama model.
    Enforces strict output rules via prompting.

    Variables:
    - text (str): The input string/sentence that needs to be translated.
    - output_language (str): The target language for the translation.
    - prompt (str): The structured instruction sent to Ollama to enforce strict output formatting.
    - response (dict): The raw JSON/dictionary payload returned by the Ollama API.
    """
    # Construct a strict system prompt to ensure the model only returns the raw translation
    prompt = (
        f"You are a pure translation module. Translate the following text into the language: {output_language}.\n"
        f"RULES:\n"
        f"- Output ONLY the translation.\n"
        f"- No quotation marks, no explanations, no 'Here is the translation'.\n"
        f"- If you do not know the language, transliterate the sound.\n\n"
        f"Text:\n{text}"
    )

    # Call the Ollama API with the configured model
    response = ollama.generate(
        model=story.MODEL,
        prompt=prompt,
        options={
            # High temperature (0.9) increases creativity/entropy, 
            # allowing for diverse translations without breaking sentence structure.
            'temperature': 0.9 
        }
    )
    # Return the cleaned response, stripping any accidental leading/trailing whitespace
    return response['response'].strip()

def translation_saveguard(text: str, language: str = "") -> str:
    """
    Ensures a valid translation is received. If Ollama returns an empty string,
    it retries until a successful translation is generated.

    Variables:
    - text (str): The original text to be translated.
    - language (str): The optional target language. Defaults to an empty string.
    - new_text (str): Stores the translation result; acts as the safety check variable.
    - given_language (bool): Flag indicating if a specific language was forced by the caller.
    """
    new_text: str = ""
    given_language: bool = False

    # Check if a specific target language was requested
    if language != "":
        given_language = True
    
    # Loop guarantees a successful translation if the model occasionally returns empty outputs
    while new_text == "":
        # If no language was predefined, pick a random one from the supported list for this iteration
        if not given_language:
            # Seed = current_time + uptime 
            #      = time.time() + (time.time() - boot_time)
            #      = 2 * time.time() - boot_time
            # This combination leverages the current time and translation time from your system for a more unpredictable seed.
            random.seed(2*time.time() - datetime.datetime.fromtimestamp(psutil.boot_time()).timestamp())
            language = random.choice(story.LANGUAGES)
        new_text = translate_lokal(text, language)

    return new_text

def randimasation_through_translation(start_wort: str, runden: int) -> str:
    """
    Passes a word through multiple rounds of random translations (like a game of Telephone)
    to intentionally introduce semantic drift and randomization.

    Variables:
    - start_wort (str): The initial word or sentence to begin the chain with.
    - runden (int): The total number of translation cycles to perform.
    - new_text (str): Tracks the mutating text across the loop iterations.
    - i (int): Loop index counter for the current round.
    """
    new_text: str = start_wort
    
    # Iteratively translate the text 'runden' times using random languages
    for i in range(runden):
        new_text = translation_saveguard(new_text)

    return new_text

def choose_language() -> str:
    """
    Prompts the user via CLI to choose a valid output language from the available list.

    Variables:
    - output_language (str): The user's input choice, formatted to capitalized text.
    - languages_grid (str): A dynamically generated string displaying the language list in an 8-column grid.
    - lang (str): Iterator variable for individual languages during string formatting.
    - i (int): Iterator index used to calculate line breaks for the grid layout.
    """
    output_language: str = ""
    # Loop until the user provides a language that exists in story.LANGUAGES
    while output_language.capitalize() not in story.LANGUAGES:
        print("In which language do you want the output to be?")
        
        # Format and display the available languages in a clean grid (8 columns)
        languages_grid = "".join(f"{lang:<15}" + ("\n" if (i+1) % 8 == 0 else "") for i, lang in enumerate(story.LANGUAGES))
        
        output_language = input(f"Here are the available languages:\n{languages_grid}\n\nDeine Auswahl: ").capitalize()
    return output_language

def translation_chaos(start_wort: str, runden: int, outputlanguage: str) -> None:
    """
    Executes the 'Telephone game' translation process, prints the intermediate 
    language steps, and translates the final chaotic result back to the user's chosen language.

    Variables:
    - start_wort (str): The initial user input string.
    - runden (int): The number of chaotic translation iterations.
    - outputlanguage (str): The final target language the user wants to read.
    - text (str): Holds and updates the progressively chaotic text through the loop.
    - i (int): Loop index tracking the current round number.
    - language (str): Stores the randomly selected language for the current loop cycle.
    - final_text (str): The final output string translated back to the user's chosen outputlanguage.
    """
    text: str = start_wort
    print(f"Start: {text}\n" + "-"*30)
    
    # Multi-round random translation loop
    for i in range(runden):

        # Seed = current_time + uptime 
        #      = time.time() + (time.time() - boot_time)
        #      = 2 * time.time() - boot_time
        # This combination leverages the current time and translation time from your system for a more unpredictable seed.
        random.seed(2*time.time() - datetime.datetime.fromtimestamp(psutil.boot_time()).timestamp())

        # Select a random language and track it for the print statement
        language = random.choice(story.LANGUAGES) 
        
        # Fixed logic step: text updates dynamically each round
        text = translation_saveguard(text, language)
        
        print(f"Runde {i+1}: Übersetzt nach [{language}] -> {text}")
        
    # Final step: Translate the completely randomized text back to the desired output language
    final_text: str = ""
    while final_text == "":
        final_text = translate_lokal(text, outputlanguage)
        
    print("-"*30 + f"\nThe final result in {outputlanguage}: {final_text}")

# Test how different languages in the input texts will get translated
if __name__ == "__main__":
    # Test if the translation of the Input text will be somewhat coherent in different input languages
    print("Only German")
    translation_chaos("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "German")

    print("Only English")
    translation_chaos("I am going to the supermarket tomorrow and buying some fresh vegetables for dinner.", 1, "German")

    # Test how the model handle a text with different languages, where the differnt languages are nearly 50/50 of the text.
    print("Mixed")
    translation_chaos("Ich gehe morgen to the supermarket und kaufe some fresh vegetables für das Abendessen.", 1, "German")


    # Test if the translation of the Input text will be somewhat coherent in different input languages, even with an higher translation count
    print("Only German")
    translation_chaos("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 20, "German")

    print("Only English")
    translation_chaos("I am going to the supermarket tomorrow and buying some fresh vegetables for dinner.", 20, "German")

    # Test how the model handle a text with different languages, where the differnt languages are nearly 50/50 of the text.
    print("Mixed")
    translation_chaos("Ich gehe morgen to the supermarket und kaufe some fresh vegetables für das Abendessen.", 20, "German")