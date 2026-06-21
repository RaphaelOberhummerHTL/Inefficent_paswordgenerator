import ollama

# --- GLOBAL CONFIGURATION VARIABLES ---

# MODEL (str): The specific local LLM checkpoint identifier to execute via Ollama.
# Note: 'gemma4:12b' balances inference speed and linguistic accuracy on higher midrange gaming hardware or higher.
# 
# OPEN SOURCE NOTE ON MODEL SWAPPING:
# If you change this model identifier (e.g., to a different generation or a model from another company),
# please manually verify that your chosen model supports the languages listed in the `LANGUAGES` list.
# Unsupported languages may result in incoherent translations or hallucinations.
MODEL = 'gemma4:12b' 

# LANGUAGES (list[str]): A curated collection of global target languages categorized by region.
# Used by the translation engine to introduce semantic variations and structural linguistic changes.
#
# EXTENSIBILITY NOTE:
# This list is completely open to modification. If your chosen MODEL supports additional regional 
# languages, dialects, or historical scripts not listed below, you can freely append them directly 
# to this list (e.g., "Esperanto", "Latin"). Conversely, feel free to remove any languages that 
# your custom model struggles to process accurately.
LANGUAGES: list[str] = [
    # --- CENTRAL & WESTERN EUROPE ---
    "German", "English", "French", "Dutch", "Romansh",
    # Comment: Romansh is a minority language that yields wonderful translation glitches.

    # --- NORTHERN EUROPE & SCANDINAVIA ---
    "Swedish", "Norwegian", "Finnish", "Icelandic",
    # Comment: Finnish is non-Indo-European; Icelandic is extremely close to Old Norse.

    # --- EASTERN EUROPE & BALTICS ---
    "Russian", "Polish", "Czech", "Romanian", "Hungarian", "Lithuanian", "Estonian",
    # Comment: Hungarian and Estonian break sentence structures due to their Finno-Ugric grammar.

    # --- SOUTHERN EUROPE ---
    "Italian", "Spanish", "Portuguese", "Greek", "Catalan", "Basque",
    # Comment: Basque is a language isolate – perfect for creating maximum chaos!

    # --- CELTIC REGION ---
    "Irish", "Welsh",
    # Comment: Excellent for "Telephone Game" effects, as LLMs often translate these poetically but inaccurately.

    # --- MIDDLE EAST & NORTH AFRICA ---
    "Arabic", "Hebrew", "Persian", "Turkish", "Egyptian Arabic",
    # Comment: Shifts the logic to Semitic writing systems and agglutinative grammar (Turkish).

    # --- CAUCASUS & CENTRAL ASIA ---
    "Georgian", "Armenian", "Kazakh", "Uzbek",
    # Comment: Kazakh and Uzbek introduce Central Asian structural patterns.

    # --- SOUTH ASIA (Indian Subcontinent) ---
    "Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Urdu", "Nepali", "Sinhala",
    # Comment: Heavy mix of Indo-Aryan (Northern) and Dravidian (Southern) languages. Gemma 4 is highly capable here.

    # --- EAST ASIA ---
    "Mandarin", "Cantonese", "Japanese", "Korean", "Tibetan",
    # Comment: Entirely different sentence structures (e.g., Subject-Object-Verb in Japanese/Korean).

    # --- SOUTHEAST ASIA ---
    "Thai", "Vietnamese", "Indonesian", "Tagalog", "Burmese", "Khmer", "Malay",
    # Comment: Tonal languages (Thai/Vietnamese) vs. Malayo-Polynesian languages (Indonesian) cause great semantic shifts.

    # --- SUB-SAHARAN AFRICA ---
    "Swahili", "Amharic", "Yoruba", "Zulu", "Xhosa", "Hausa", "Igbo", "Somali", "Oromo", "Shona",
    # Comment: Massive diversity. Swahili and Zulu use complex noun class systems that easily confuse Western-centric LLM logics.

    # --- PACIFIC & OCEANIA ---
    "Maori", "Samoan", "Hawaiian",
    # Comment: Polynesian languages often have a very small phoneme inventory, heavily distorting words.

    # --- INDIGENOUS LANGUAGES OF THE AMERICAS ---
    "Quechua", "Guarani", "Nahuatl", "Mayan"
    # Comment: Nahuatl (Aztec) and Mayan are included as Gemma 4 possesses an impressive historical text corpus for them.
]

# GENRE (dict[str, str]): A map linking structural numerical strings to story genres.
GENRE: dict[str, str] = {
    "1": "Science Fiction",
    "2": "Fantasy",
    "3": "Thriller",
    "4": "Comedy",
    "5": "Everyday Horror",
    "6": "Romance",
    "7": "Cyberpunk",
    "8": "Fairytale",
    "9": "Mystery",
    "10": "Absurd",
    "11": "Young Adult",
    "12": "Coming of Age",
    "13": "Slice of Life",
    "14": "Cosmic Horror"
}


# --- UTILITY AND GENERATION FUNCTIONS ---

def choose_genre() -> str:
    """
    Displays the mapped dictionary of genres and prompts the user via CLI to choose one.

    Returns:
        str: The name of the genre corresponding to the user's validated selection.
    """
    choice: str = ""
    # Continue looping until the user submits a valid numeric index present in the GENRE dictionary
    while choice not in GENRE:
        # Loop through and present all menu configuration options cleanly to the user
        for nummer, genre in GENRE.items():
            print(f"{nummer}: {genre}")
            
        choice = input(f"Please select a genre (1-{len(GENRE)}): ").strip()
        
        # Validation feedback step
        if choice not in GENRE:
            print("Invalid choice. Please type a number from the list.")

    return GENRE[choice]

def choose_startingwords() -> str:
    """
    Collects a set of 5 seed words from the user via CLI prompts.

    Returns:
        str: A single string containing the 5 collected words, separated by semicolons.
    """
    word_list = []
    print("With which random words should the story get generated?")
    
    # Loop strictly 5 times to gather exactly 5 distinct words
    for i in range(5):
        while True:
            # Read input and instantly clear out leading or trailing whitespaces
            user_input = input(f"Please input the word {i+1}: ").strip()
            
            # Reject inputs that contain empty string blocks or spaces entirely
            if user_input == "":
                print("An empty string or a string containing only spaces doesn't carry any meaning.")
                continue  # Force the loop to ask for this word index again
            
            # Append valid word entry and break out of inner validation loop
            word_list.append(user_input)
            break
            
    # Combine the collected word list entries into a single semicolon-delimited string
    return "; ".join(word_list)

def generate_story(genre: str, words: str) -> str:
    """
    Interfaces with the local Ollama instance to construct a narrative context 
    based on the selected genre and starting keywords.

    Args:
        genre (str): The chosen structural thematic style for the story.
        words (str): The semicolon-separated string containing the 5 required 
            narrative seed words.

    Returns:
        str: The clean generated story from the model, stripped of leading 
            and trailing whitespaces.
    """
    # Construct a highly specialized prompt to force linguistic matching to seed words and block introductory fluff
    prompt = (
        f"You are a multilingual author who writes brilliant stories worldwide.\n"
        f"TASK:\n"
        f"Write a creative story in the genre '{genre}' incorporating these 5 words: {words}\n\n"
        f"SAFETY & LANGUAGE RULES:\n"
        f"1. IDENTIFY THE DOMINANT LANGUAGE: Analyze the 5 input words. Determine which language they primarily belong to (e.g., German, Japanese, Mandarin, Zulu, English).\n"
        f"2. OUTPUT LANGUAGE: You MUST write the entire story in that identified language. Do NOT write the story in English unless English is the dominant language.\n"
        f"3. MIXED LANGUAGES & TRANSLATION LOGIC: If the input words are a mix of languages, you must integrate them into the dominant language based on these strict rules:\n"
        f"   - TRANSLATE basic vocabulary: If an input word is a basic, common word in a foreign language, you MUST translate it into the dominant language so the story flows naturally.\n"
        f"   - DO NOT TRANSLATE loanwords/slang: If a foreign word is commonly used as a loanword or modern slang in the dominant language (e.g., 'weird', 'cool', 'chill' in German), keep it exactly as it is.\n"
        f"   - POETIC/EXOTIC INTEGRATION: If a word is in a completely different script or language that cannot be directly translated without losing its flair, integrate it grammatically into the sentence structure of the dominant language.\n"
        f"4. NO EXTRA TEXT: Output ONLY the story. No introduction, no explanations, no 'Here is your story:'.\n\n"
        f"Story:"
    )
    safeguard: str = ""

    while safeguard == "":
        # Dispatch request payload configurations directly to the active Ollama container engine
        story = ollama.generate(
            model=MODEL,
            prompt=prompt,
            options={
                # Temperature balanced at 0.8 to provide creative phrase variety while maintaining readable narrative logic
                'temperature': 0.8 
            }
        )
        safeguard = story['response'].strip()

    # Return the clean generation string, stripping accidental outer whitespace artifacts
    return safeguard

def choose_language() -> str:
    """
    Prompts the user via CLI to choose a valid output language from the available list.

    Returns:
        str: The validated, capitalized target language chosen by the user.
    """
    output_language: str = ""
    # Loop until the user provides a language that exists in story.LANGUAGES
    while output_language.strip().title() not in LANGUAGES:
        print("In which language do you want the output to be?")
        
        # Format and display the available languages in a clean grid (8 columns)
        languages_grid = "".join(f"{lang:<15}" + ("\n" if (i+1) % 8 == 0 else "") for i, lang in enumerate(LANGUAGES))
        
        output_language = input(f"Here are the available languages:\n{languages_grid}\n\nYour input: ").capitalize()
    return output_language