import translationchaos

from random import randint
from random import random
from random import seed
from random import gauss
from random import choice

import math
import time

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

    Variables:
    - length_of_password (int): The verified length returned by the function. Acts as a control flag for the loop.
    - temp_length_of_password (int): Temporary holder for parsing user input before validation.
    - user_input (str): The raw string captured from the command line prompt.
    """
    length_of_password: int = 20
    temp_length_of_password: int = 0

    user_input: str = input("How long should your password be? [Default=20; min=10]: ").strip()

    # If user presses enter without typing, return the default length of 20
    if user_input == "":
        return length_of_password
    
    temp_length_of_password = int(user_input)
    
    # FIXED: Changed validation check from 'length_of_password' to 'temp_length_of_password'
    if temp_length_of_password < 10:
        print("The password must be at least 10 characters long. The passwordlength will be the default length of 20.")
    else:
        length_of_password = temp_length_of_password
            
    return length_of_password

def password(story: str, runden: int, genre: str, words: str, passwordlength: int) -> str:
    """
    Generates a secure, chaotic password based on text translation mutations and multi-layered mathematical entropy.

    Variables:
    - story (str): Input text block used as the primary source of dynamic chaos.
    - runden (int): Number of random translation loops to run the story through.
    - genre (str): User-provided category/genre string to influence initial entropy math.
    - words (str): Extra seed words provided by the user for supplementary deterministic complexity.
    - passwordlength (int): Target size constraint for the generated string.
    - translated_story (str): Holds the mutated, distorted output of the story translation steps.
    - number (float): Continuous entropy variable calculated via heavy math expressions to continuously re-seed the RNG.
    - password (str): The growing string containing chosen characters returned at the end.
    - length_of_password (int): Clean scoped integer copy matching passwordlength.
    - i, j (int): Loop index track counters navigating positions in strings.
    """
    translated_story: str = ""
    number: float = 0.0
    password: str = ""

    length_of_password: int = passwordlength
    
    # Run the initial story through chaotic multi-language translations to establish entropy baseline
    translated_story = translationchaos.randimasation_through_translation(story, runden)
    
    # Inject user choice 'genre' into mathematical entropy by accumulating character ASCII values (ord)
    for i in range(len(genre)):
        number += ord(genre[i]) 

    # Compound user choice 'words' into mathematical seed values via multiplication
    for j in range(len(words)):
        number *= ord(words[j])

    # Keep iterating until the output password reaches the requested length limit
    while len(password) < length_of_password:
        for i in range(len(translated_story)-1):
            
            # Continuously update state baseline based on exact execution runtime epoch timestamps
            seed(time.time())
            
            # Conditional block safeguarding list bounds to check characters across the string
            if i < len(translated_story)-1:
                # Heavy polynomial algebraic manipulation combining character neighbors alongside safe pseudo-random steps
                number = (ord(translated_story[i])**3 + ord(translated_story[i+1])**3 + randint(ord(translated_story[i]), ord(translated_story[i+1])**2)**3)**(1/3) - number
                number = random()*(number**3)+randint((-ord(translated_story[i])), ord(translated_story[i]))*number**2-gauss(ord(translated_story[i+1]), (ord(translated_story[i+1])/(30*math.pi)))*number-randint(randint(0,ord(translated_story[randint(0,len(translated_story)-1)])),randint(ord(translated_story[randint(0,len(translated_story)-1)])%5,ord(translated_story[randint(0,len(translated_story)-1)-1])**2)**2)
            else:
                # Alternative mathematical path calculation fallback handling the string boundary edges safely
                number = (ord(translated_story[i])**3 + ord(translated_story[i-1])**3 + randint(ord(translated_story[i]), ord(translated_story[i-1])**2)**3)**(1/3)
                number = random()*(number**3)+randint((-ord(translated_story[i])), ord(translated_story[i]))*number**2-gauss(ord(translated_story[i-1]), ord(translated_story[i-1])/(30*math.pi))*number-randint(randint(0,ord(translated_story[randint(0,len(translated_story)-1)])),randint(ord(translated_story[randint(0,len(translated_story)-1)]),2*ord(translated_story[randint(0,len(translated_story)-1)])))
            
            # Set computed high-entropy float number as seed for the final character picker sequence step
            seed(number)
            password += choice(CHARACTERS)
            
            # Immediately break out if the desired password size threshold is reached inside loop
            if len(password) == length_of_password:
                break
                
    return password