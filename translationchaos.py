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

    Args:
        text (str): The input string/sentence that needs to be translated.
        output_language (str): The target language for the translation.

    Returns:
        str: The cleaned, translated text from the model, stripped of leading 
            and trailing whitespaces.
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

    Args:
        text (str): The original text to be translated.
        language (str, optional): The target language. If left empty, a random 
            language from the supported list will be chosen. Defaults to "".

    Returns:
        str: The successfully translated text.
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

def randimasation_through_translation(start_text: str, translation_rounds: int) -> str:
    """
    Passes a word through multiple rounds of random translations (like a game of Telephone)
    to intentionally introduce semantic drift and randomization.

    Args:
        start_text (str): The initial word or sentence to begin the chain with.
        translation_rounds (int): The total number of translation cycles to perform.

    Raises:
        ValueError: If `translation_rounds` is less than 1 or `start_text` is empty/whitespaces only.

    Returns:
        str: The final mutated text after all translation rounds are completed.
    """

    if translation_rounds < 1:
        raise ValueError("The number of translation rounds must be at least 1.")
    
    if start_text.strip() == "":
        raise ValueError("The input text can't contain only whitespaces or be empty.")
    
    new_text: str = start_text
    
    # Iteratively translate the text 'translation_rounds' times using random languages
    for i in range(translation_rounds):
        new_text = translation_saveguard(new_text)
        print(f"Translation {i+1} out of {translation_rounds} finished")

    return new_text

def translation_chaos(start_text: str, translation_rounds: int = 5, outputlanguage: str = "English") -> str:
    """
    Executes the 'Telephone game' translation process, prints the intermediate 
    language steps, and translates the final chaotic result back to the user's chosen language.

    Args:
        start_text (str): The initial user input string to be translated.
        translation_rounds (int, optional): The number of chaotic translation iterations. 
            Defaults to 5.
        outputlanguage (str, optional): The final target language the user wants to read. 
            Defaults to "English".

    Raises:
        ValueError: If `translation_rounds` is less than 1 or `start_text` is empty/whitespaces only.

    Returns:
        str: The final output string translated back to the user's chosen outputlanguage.
    """
    if translation_rounds < 1:
        raise ValueError("The number of translation rounds must be at least 1.")
    
    if outputlanguage.strip() == "" or outputlanguage not in story.LANGUAGES:
        outputlanguage = "English"
    
    if start_text.strip() == "":
        raise ValueError("The input text can't contain only whitespaces or be empty.")

    text: str = start_text
    final_text: str = ""

    print(f"Start: {text}\n" + "-"*30)
    
    # Multi-round random translation loop. The last translation round is into the outputlanguage.
    for i in range(translation_rounds-1):

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
    while final_text == "":
        final_text = translation_saveguard(text, outputlanguage)
        
    return final_text

# Test how different languages in the input texts will get translated
if __name__ == "__main__":
    # Test if the translation of the Input text will be somewhat coherent in different input languages
    print("Only German")
    print("-"*30 + f"\nThe final result in German: {translation_chaos("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "German")}")

    print("Only English")
    print("-"*30 + f"\nThe final result in German: {translation_chaos("I am going to the supermarket tomorrow and buying some fresh vegetables for dinner.", 1, "German")}")

    # Test how the model handle a text with different languages, where the differnt languages are nearly 50/50 of the text.
    print("Mixed")
    print("-"*30 + f"\nThe final result in German: {translation_chaos("Ich gehe morgen to the supermarket und kaufe some fresh vegetables für das Abendessen.", 1, "German")}")


    # Test if the translation of the Input text will be somewhat coherent in different input languages, even with an higher translation count
    print("Only German")
    print("-"*30 + f"\nThe final result in German: {translation_chaos("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 20, "German")}")

    print("Only English")
    print("-"*30 + f"\nThe final result in German: {translation_chaos("I am going to the supermarket tomorrow and buying some fresh vegetables for dinner.", 20, "German")}")

    # Test how the model handle a text with different languages, where the differnt languages are nearly 50/50 of the text.
    print("Mixed")
    print("-"*30 + f"\nThe final result in German: {translation_chaos("Ich gehe morgen to the supermarket und kaufe some fresh vegetables für das Abendessen.", 20, "German")}")