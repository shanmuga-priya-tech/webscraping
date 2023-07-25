import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

base_url = "http://quotes.toscrape.com"

def read_quotes(filename):
    with open(filename,"r",encoding='utf-8') as file:
        csv_reader=DictReader(file)
        return list(csv_reader)

#contents to display:who said this quote and remaining guess
def start_game(quotes):
    choosen_quote = choice(all_quotes)
    print("Here is Your Quote:")
    print(choosen_quote["quotes"])
    
    #initializing the remaining guess to 4 and decrementing it if author name is wrong ans and quit the game when its zero
    remaining_guess = 4 
    guess=""

    while guess.lower() != choosen_quote["author"].lower() and remaining_guess > 0:
        guess = input("who said this quotes ?  ")
        
        if guess.lower() == choosen_quote["author"].lower() :
            print("CONGRATS!!!....YOU GOT IT CORRECT")
            break
        remaining_guess -=1
        print(f"The remaining guesses is {remaining_guess}")

    #sec hint to display author birthdate and place by again scrapping through biolink
        if remaining_guess == 3:
            res = requests.get(f"{base_url}{choosen_quote['bio_Link']}")
            soup = BeautifulSoup(res.text,"html.parser")

            date = soup.find(class_="author-born-date").get_text()
            place = soup.find(class_="author-born-location").get_text()
            print("Here is the 2nd hint:")
            print(f"The author was born on {date} {place}")
            
    #3rd hint 1st letter in author 1st name
        elif remaining_guess == 2:
            first_letter=choosen_quote["author"][0]
            print("Here is the 3rd hint:")
            print(f"The author's first name starts with {first_letter}")

    #4th hint 1st letter in author last name
        elif remaining_guess == 1:
            last_letter=choosen_quote["author"].split(" ")[1][0]
            print("Here is the last  hint:")
            print(f"The author's last name starts with {last_letter}")

        else:
            print(f"SORRY:)...BETTER LUCK NEXT TIME.The answer is {choosen_quote['author']}")

    #ask to play again if s start again
    play_again=" "
    while play_again not in ("yes","y","no","n"):
        play_again=input("Do you want to play again (y/n) ?  ").lower()
    if play_again in ("yes","y"):
         return start_game(quotes)
    else:
        print("Ok..Have a good day")

all_quotes=read_quotes("quotes.csv")
start_game(all_quotes)



