import translationchaos

from random import randint
from random import random
from random import seed
from random import gauss
from random import choice

import math
import time

CHARACTERS: list[str] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '.', ':', '-', '_', ',', ';', '#', '\'', '+', '*', '’', '~', '´', '`', '<', '>', '|', '!', '"', '§', '$', '%', '&', '/', '(', ')',
    '=', '{', '}', '[', ']', '^', '°', '\\'
]

def password(story: str, runden: int, genre:str, words:str) -> str:
    translated_story:str = ""
    number:float = 0.0
    length_of_password: int = 20
    password: str = ""

    while length_of_password < 10:
        user_input:str = input("How long should your password be? [Default=20; min=10]: ")

        if user_input == "":
            length_of_password = 20
            break
        
        length_of_password = int(user_input)
        
        if length_of_password < 10:
            print("The password must be at least 10 characters long. Try again.")
    
    translated_story:str = translationchaos.randimasation_through_translation(story, runden) # This function call will stay here because I built the idea of this password generator around the loss of information through translations
    for i in range(len(genre)):
        number += ord(genre[i])

    for j in range(len(words)):
        number *= ord(words[j])

    while len(password) < length_of_password:
        for i in range(len(translated_story)-1):
            seed(time.time())
            if i < len(translated_story)-1:
                number = (ord(translated_story[i])**3 + ord(translated_story[i+1])**3 + randint(ord(translated_story[i]), ord(translated_story[i+1])**2)**3)**(1/3) - number
                number = random()*(number**3)+randint((-ord(translated_story[i])), ord(translated_story[i]))*number**2-gauss(ord(translated_story[i+1]), (ord(translated_story[i+1])/(30*math.pi)))*number-randint(randint(0,ord(translated_story[randint(0,len(translated_story)-1)])),randint(ord(translated_story[randint(0,len(translated_story)-1)])%5,ord(translated_story[randint(0,len(translated_story)-1)-1])**2)**2)
            else:
                number = (ord(translated_story[i])**3 + ord(translated_story[i-1])**3 + randint(ord(translated_story[i]), ord(translated_story[i-1])**2)**3)**(1/3)
                number = random()*(number**3)+randint((-ord(translated_story[i])), ord(translated_story[i]))*number**2-gauss(ord(translated_story[i-1]), ord(translated_story[i-1])/(30*math.pi))*number-randint(randint(0,ord(translated_story[randint(0,len(translated_story)-1)])),randint(ord(translated_story[randint(0,len(translated_story)-1)]),2*ord(translated_story[randint(0,len(translated_story)-1)])))
            seed(number)
            password += choice(CHARACTERS)
            if len(password) == length_of_password:
                break
    return password