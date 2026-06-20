import datetime
import psutil
import math
import time

import translationchaos


from story import generate_story

from random import randint
from random import random
from random import seed
from random import gauss
from random import choice
from random import seed

# A global collection of available characters used to construct the final password string.
CHARACTERS: list[str] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '.', ':', '-', '_', ',', ';', '#', '\'', '+', '*', '’', '~', '´', '`', '<', '>', '|', '!', '"', '§', '$', '%', '&', '/', '(', ')',
    '=', '{', '}', '[', ']', '^', '°', '\\'
]

def choose_password_length() -> int:
    """
    Prompts the user via CLI to define the desired password length.
    Ensures safe fallbacks to default values if input is invalid or too short.

    Returns:
        int: The chosen password lengh

    """
    length_of_password: int = 20
    temp_length_of_password: int = 0

    user_input: str = input("How long should your password be? [Default=20; min=10]: ").strip()

    # If user presses enter without typing, return the default length of 20
    if user_input == "":
        return length_of_password
    
    try:
        temp_length_of_password = int(user_input)
        if temp_length_of_password < 10:
            print("The password must be at least 10 characters long. The password length will be the default length of 20.")
            return length_of_password
        else:
            return temp_length_of_password
    except:
        print("The password lengh has to be an integer. The password length will be the default length of 20.")
        return length_of_password

def password(story: str, runden: int, genre: str, words: str, passwordlength: int = 20) -> str:
    """
    Generates a random password by combining text-mutation entropy, 
    user-input seed values, and complex mathematical manipulations.

    Features intentional inefficiencies, hardware jitter, network latency simulation, 
    and highly chaotic mathematical state rolling to maximize entropy (and CPU and GPU cycles).

    Args:
        story (str): Base text used as the primary source for character mutation.
        runden (int): Number of translation iterations to run the story through.
        genre (str): User-defined category to influence initial seed calculation.
        words (str): Supplementary seed words provided by the user.
        passwordlength (int): Target password length (minimum 10, defaults to 20 if lower).

    Returns:
        str: The generated password string.
    """
    translated_story: str = ""
    password: str = ""
    number: complex = 0.0
    old_number: complex = 0.0
    check_val: float = 0.0
    iterations: int = 0

    # Temporary registers used to dynamic-sort dynamic random ranges.
    # CRITICAL: Prevents ValueError (empty range) from chaotic Unicode/ASCII index mismatches from languages with a different writing system, like Mandarin.
    val1: int = 0
    val2: int = 0
    val3: int = 0
    val4: int = 0
    
    # Enforce a minimum password length of 10
    if passwordlength < 10:
        length_of_password: int = 20
    else:
        length_of_password: int = passwordlength
    
    # Generate baseline entropy by running the story through multi-language translation loops
    translated_story = translationchaos.randimasation_through_translation(story, runden)
    
    # Incorporate 'genre' into the seed by accumulating character ASCII values
    for i in range(len(genre)):
        number += ord(genre[i]) 

    # Compound 'words' into the seed via character ASCII multiplication
    for j in range(len(words)):
        number *= ord(words[j])
    
    # Store initial user-input seed calculation to keep multi-line equations readable
    old_number = number 

    # Loop until the generated password reaches the target length
    while len(password) < length_of_password:
        iterations += 1

        for i in range(len(translated_story)-1):
            # Theoretical possibility that the requested length is longer than the text, 
            # so we keep track of the iteration depth.
            print(f"Generating character: {i+iterations}") 
            
            # Compiles a pseudo-random seed by combining epoch time and system boot time.
            # The resulting value relies on hardware-level non-determinism:
            # - CPU/GPU process scheduling fluctuations.
            # - Dynamic thermal throttling and cooling system latency.
            # - Microarchitectural variances (Silicon Lottery).
            seed(2*time.time() - datetime.datetime.fromtimestamp(psutil.boot_time()).timestamp())

            # Translate this short sentence. The network/inference latency (local network stack) and the reasons beforehand introduces
            # additional timing jitter, further shifting the state for subsequent iterations.
            # a short sentence was chosen because otherwice it would have taken too long 
            translationchaos.translation_saveguard("This is the most inefficent password generator", "Hindi")
            
            # Index boundary safeguard for processing string character pairs
            # It got split for better readability
            if i < len(translated_story)-1:
                val1 = ord(translated_story[randint(0, (len(translated_story)-1))])
                val2 = (len(translated_story)+ord(translated_story[randint(0, (len(translated_story)-1))]))
                
                # Polynomial algebraic manipulation mixing neighbor characters and random bounds
                number -= (old_number*(ord(translated_story[randint(0, (len(translated_story)-1))])**3))
                number += (ord(translated_story[randint(0, (len(translated_story)-1))])**2)
                
                # Enforce min/max to prevent ValueError if a rare Unicode char (val1) > length-bound (val2)
                number += (randint(min(val1, val2), max(val1, val2))**3)
                number = (old_number)**(1/3) - old_number
                
                # Feed previous result back into the rolling calculation
                old_number = number 
                
                val1 = (-ord(translated_story[randint(0, (len(translated_story)-1))]))
                val2 = ord(translated_story[randint(0, (len(translated_story)-1))])

                # Safe range sorting for the negative/positive transition bounds to prevent ValueError
                number = -randint(min(val1, val2), max(val1, val2))*old_number**2
                number += gauss(ord(translated_story[randint(0, (len(translated_story)-1))]), (ord(translated_story[randint(0, (len(translated_story)-1))])/(30*math.pi)))*old_number

                val1 = ord(translated_story[randint(0,len(translated_story)-1)])
                val2 = ord(translated_story[randint(0,len(translated_story)-1)-1])**2

                val3 = randint(0, ord(translated_story[randint(0,len(translated_story)-1)]))
                val4 = randint(min(val1, val2), max(val1, val2))**2
                
                # Multi-stage sorted bounds logic ensuring stability during entropy reduction
                number -= randint(min(val3, val4), max(val3, val4))
            else:
                # Alternative fallback logic handling the string boundary edges
                number += ord(translated_story[randint(0, (len(translated_story)-1))])**3
                number += ord(translated_story[i-1])**3
                val1 = ord(translated_story[randint(0, (len(translated_story)-1))])
                val2 = ord(translated_story[i-1])**2
                number += randint(min(val1, val2), max(val1, val2))**3
                number += old_number**(1/3)
                
                # Feed previous result back into the rolling calculation
                old_number = number 
                
                val1 = ord(translated_story[randint(0, (len(translated_story)-1))])
                val2 = ord(translated_story[randint(0, (len(translated_story)-1))])
                
                # Sorting inverse character boundaries safely
                number = randint(min(-val1, val2), max(-val1, val2))*old_number**2
                number -= gauss(ord(translated_story[i-1]), ord(translated_story[i-1])/(30*math.pi))*old_number

                val1 = ord(translated_story[randint(0,len(translated_story)-1)])
                val2 = 2*ord(translated_story[randint(0,len(translated_story)-1)])
                val3 = randint(0,ord(translated_story[randint(0,len(translated_story)-1)]))
                val4 = randint(min(val1, val2), max(val1, val2))
                number -= randint(min(val3, val4), max(val3, val4))

            # Extract the real part since fractional exponents (cubic roots) can cast the state into a complex number
            if isinstance(number, complex):
                check_val = number.real 
            else:
                check_val = number

            old_number = number
            
            # Prevent 'Numerical result out of range' (float overflow) and TypeError (complex comparison).
            # If the mathematical state escalates, we hard-reset it to a chaotic but safe baseline.
            if check_val > 1e150 or check_val < -1e150:
                number = random()*randint(randint((-300),(-20)), randint(20, 300))
            else:
                number = check_val

            # Seed Python's RNG with the accumulated mathematical entropy to select the next character
            seed(old_number.real) 
            password += choice(CHARACTERS)

            # Sync calculations for the next loop cycle
            old_number = number 

            # Break early if target length is met within the inner loop
            if len(password) == length_of_password:
                break

        iterations += len(story)
                
    return password

if __name__ == "__main__":
    # Test if the passwordgenerator works as intended
    print(f"password 1: {password("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "Slice of Life", "Supermarkt; frisches Gemüse; Abendessen; morgen; kaufen", 10)}")
    print(f"password 2: {password("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "Slice of Life", "Supermarkt; frisches Gemüse; Abendessen; morgen; kaufen")}")
    print(f"password 3: {password("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "Slice of Life", "Supermarkt; frisches Gemüse; Abendessen; morgen; kaufen", 30)}")
    print(f"password 4: {password("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "Slice of Life", "Supermarkt; frisches Gemüse; Abendessen; morgen; kaufen", 1)}")
    print(f"password 5: {password("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "Slice of Life", "Supermarkt; frisches Gemüse; Abendessen; morgen; kaufen", -2)}")
    print(f"password 6: {password("Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen.", 1, "Slice of Life", "Supermarkt; frisches Gemüse; Abendessen; morgen; kaufen", 0)}")
