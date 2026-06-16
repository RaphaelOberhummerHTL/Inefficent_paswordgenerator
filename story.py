import ollama

MODEL = 'gemma4:12b'

LANGUAGES: list[str] = [
    #"Zentraleuropa / Westeuropa": 
    "German", "English", "French", "Dutch", "Romansh",
    # Comment: This group includes Germanic (German, English, Dutch) 
    # and Romance languages (French, Romansh). Romansh is a 
    # minority language, mainly spoken in the Swiss canton of Grisons (Graubünden).
    
    # "Nordeuropa / Skandinavien": [
    "Swedish", "Norwegian", "Danish", "Icelandic", "Finnish",
    # Comment: Swedish, Norwegian, Danish, and Icelandic belong to the 
    # North Germanic languages (with Icelandic being closest to Old Norse). 
    # Finnish, however, is not a Germanic language; it belongs to the Finno-Ugric 
    # language family and is therefore more closely related to Hungarian.

    #"Osteuropa": [
    "Russian", "Ukrainian", "Polish", "Czech", "Romanian", 
    "Bulgarian", "Croatian", "Hungarian",
    # Comment: The majority here are Slavic languages (Russian, Ukrainian, Polish, 
    # Czech, Bulgarian, Croatian). Romanian is an interesting exception, as it is a 
    # Romance language with strong Slavic influences. Hungarian—like Finnish—is 
    # a non-Indo-European, Finno-Ugric language in the middle of Eastern Europe.

    #"Südeuropa / Südwesteuropa": [
    "Italian", "Spanish", "Portuguese", "Greek", "Latin", "Catalan", "Basque",
    # Comment: Shaped by the Roman Empire, we find here the major Romance 
    # languages as well as Latin as their common root and Catalan as a regional language. 
    # Greek forms its own, very ancient branch of the Indo-European family. 
    # Basque (in the Spain/France border region) is an absolute mystery: it is an 
    # isolated language that is unrelated to any other known living language.

    # "Baltikum": 
    "Latvian", "Lithuanian", "Estonian",
    # Comment: Latvian and Lithuanian form the Baltic branch of the Indo-European 
    # languages and are considered linguistically very archaic (conservative). 
    # Estonian belongs to this group geographically, but linguistically it is closely related to Finnish.

    # "Keltischer Raum (Britische Inseln)": [
    "Irish", "Welsh", "Gaelic",
    # Comment: These languages originate from the indigenous Celtic peoples of the 
    # British Isles (Ireland, Wales, Scotland) and have survived as living cultural 
    # languages to this day, despite the dominant influence of English.

    # "Naher Osten / Nordafrika": 
    "Arabic", "Hebrew", "Persian", "Turkish", "Urdu",
    # Comment: Arabic and Hebrew are Semitic languages from the Afroasiatic 
    # family. Persian (Iran) and Urdu (Pakistan) are Indo-Iranian languages and thus 
    # Indo-European (related to European languages). Turkish belongs to an entirely 
    # different family, the Turkic languages, but uses the Latin alphabet today.

    #"Kaukasus"
    "Georgian", "Armenian",
    # Comment: A region of extreme linguistic diversity. Armenian is an 
    # independent branch of the Indo-European languages. Georgian belongs to the South Caucasian 
    # (Kartvelian) language family and uses its own unique, beautiful alphabet.

    #"Zentralasien"
    "Kazakh", "Uzbek", "Azerbaijani", "Mongolian",
    # Comment: Kazakh, Uzbek, and Azerbaijani are closely related Turkic languages 
    # spoken across a vast territory from Eastern Europe to Western China. Mongolian 
    # forms its own language family in the east of this region.

    # "Südasien (Indischer Subkontinent)"
    "Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Punjabi",
    # Comment: India is linguistically divided. The north speaks Indo-Iranian languages 
    # (Hindi, Bengali, Marathi, Punjabi), which are distant cousins of European languages. 
    # The south speaks Dravidian languages (Tamil, Telugu), which form a completely independent 
    # language family with no connection to Indo-European.

    # "Ostasien": 
    "Mandarin", "Cantonese", "Japanese", "Korean", "Tibetan",
    # Comment: Mandarin and Cantonese are Sinitic languages from China; Tibetan is 
    # closely related to them. Japanese and Korean, on the other hand, are grammatically structured 
    # completely differently, and their exact origin or relationship remains controversial in 
    # linguistic research to this day (often classified as isolated language families).

    # "Südostasien"
    "Thai", "Vietnamese", "Indonesian", "Malay", "Tagalog", "Burmese", "Khmer", "Lao",
    # Comment: A melting pot of language families. Thai and Lao belong together, just like 
    # Vietnamese and Khmer (Austroasiatic). Indonesian, Malay, and Tagalog (Philippines) 
    # belong to the Austronesian language family, which stretches across the entire archipelago.

    # "Subsahara-Afrika": [
    "Swahili", "Amharic", "Yoruba", "Zulu", "Xhosa", "Afrikaans", "Hausa", "Igbo", "Somali",
    # Comment: Swahili, Yoruba, Zulu, Igbo, and Xhosa (known for its click sounds) belong 
    # to the massive Niger-Congo language family. Amharic (Ethiopia) and Somali are Afroasiatic. 
    # Afrikaans is a European peculiarity: it developed in the 17th century from Dutch, 
    # which was brought to South Africa by settlers.

    # "Pazifik / Ozeanien": [
    "Maori", "Samoan", "Hawaiian",
    # Comment: These languages all belong to the Polynesian subgroup of the Austronesian 
    # languages. They show the fascinating historical migration by boat across thousands 
    # of kilometers in the Pacific Ocean (from New Zealand to Hawaii).

    # "Indigene Sprachen Amerikas": [
    "Quechua", "Guarani"
    # Comment: Remnants of the great pre-Columbian civilizations. Quechua was the 
    # language of the Inca Empire in the Andes of South America. Today, Guarani is an 
    # official language in Paraguay alongside Spanish and is spoken by the majority of the population there.
]

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

def choose_genre() -> str:
    while choice not in GENRE:
        for nummer, genre in GENRE.items():
            print(f"{nummer}: {genre}")
        choice = input(f"Please select a genre (1-{len(GENRE)}): ").strip()
        if choice not in GENRE:
            print("Invalid choice. Please type a number from the list.")

    return GENRE[choice]

def choose_startingwords() -> str:
    word_list = []
    print("With which random words should the story get generated?")
    
    for i in range(5):
        while True:
            # Eingabe einlesen und direkt die Leerzeichen am Anfang/Ende wegschneiden
            user_input = input(f"Please input the word {i+1}: ").strip()
            
            if user_input == "":
                print("An empty string or a string containing only spaces doesn't carry any meaning.")
                # Die Schleife läuft weiter, bis eine gültige Eingabe kommt
                continue  
            
            # Wenn das Wort gültig ist, fügen wir es der Liste hinzu und brechen die while-Schleife ab
            word_list.append(user_input)
            break
            
    return "; ".join(word_list)

def generate_story(genre:str, words:str) -> str:
    
    prompt = (
        f"You are a multilingual author who writes brilliant stories worldwide.\n"
        f"TASK:\n"
        f"Write a creative story in the genre '{genre}' incorporating these 5 words: {words}\n\n"
        f"SAFETY & LANGUAGE RULES:\n"
        f"1. IDENTIFY THE DOMINANT LANGUAGE: Analyze the 5 input words. Determine which language they primarily belong to (e.g., German, Japanese, Mandarin, Zulu, English).\n"
        f"2. OUTPUT LANGUAGE: You MUST write the entire story in that identified language. If the words are in Zulu, the story must be in Zulu. Do NOT translate the user's words into English.\n"
        f"3. MIXED LANGUAGES: If the words are a mix of languages (e.g., Denglish), default to the language of the majority of the words, or the language that makes the most sense for a cohesive narrative.\n"
        f"4. NO EXTRA TEXT: Output ONLY the story. No introduction, no explanations, no 'Here is your story in German:'.\n\n"
        f"Story:"
    )

    story = ollama.generate(
        model=MODEL,
        prompt=prompt,
        options={
            'temperature': 0.9
        }
    )
    return story['response'].strip()
    