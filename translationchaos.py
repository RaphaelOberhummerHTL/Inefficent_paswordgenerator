import ollama
import random

import story

def translate_lokal(text, output_language) -> str:
    prompt = (
        f"You are a pure translation module. Translate the following text into the language: {output_language}.\n"
        f"RULES:\n"
        f"- Output ONLY the translation.\n"
        f"- No quotation marks, no explanations, no 'Here is the translation'.\n"
        f"- If you do not know the language, transliterate the sound.\n\n"
        f"Text:\n{text}"
    )

    response = ollama.generate(
        model=story.MODEL,
        prompt=prompt,
        options={
            'temperature': 0.9
        }
    )
    return response['response'].strip()

def randimasation_through_translation(start_wort: str, runden: int) -> str:
    old_text:str = start_wort
    
    for i in range(runden):
        # Wichtig: Für jede Runde neu initialisieren!
        new_text:str = ""
        language:str = ""
        
        # Sicherheitsnetz: Wiederholen, bis Ollama eine Antwort liefert
        while new_text == "":
            language = random.choice(story.LANGUAGES)
            new_text = translate_lokal(old_text, language)
        
        # The new 
        old_text = new_text

    return new_text

def choose_language() -> str:
    output_language: str = ""
    while output_language.capitalize() not in story.LANGUAGES:
        print("In wich language do you want the output to be?")
        output_language = input("Here are the available languages:\n" + "".join(f"{lang:<15}" + ("\n" if (i+1) % 8 == 0 else "") for i, lang in enumerate(story.LANGUAGES)) + "\n\nDeine Auswahl: ").capitalize()
    return output_language

def translation_chaos(start_wort: str, runden: int, outputlanguage:str) -> None:
    old_text:str = start_wort
    print(f"Start: {old_text}\n" + "-"*30)
    
    for i in range(runden):
        # Wichtig: Für jede Runde neu initialisieren!
        new_text:str = ""
        language:str = ""
        
        # Sicherheitsnetz: Wiederholen, bis Ollama eine Antwort liefert
        while new_text == "":
            language = random.choice(story.LANGUAGES)
            new_text = translate_lokal(old_text, language)
        
        print(f"Runde {i+1}: Übersetzt nach [{language}] -> {new_text}")
        
        # The new 
        old_text = new_text
        
    final_text:str = ""
    while final_text == "":
        final_text = translate_lokal(old_text, outputlanguage)
        
    print("-"*30 + f"\nThe final result in {outputlanguage}: {final_text}")