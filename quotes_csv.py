import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

#http://quotes.toscrape.com
base_url = "http://quotes.toscrape.com"

#target the class want to work with
def quote_scraping():
    all_quotes=[]
    page_url = "/page/1/"
    while page_url:
        content = requests.get(f"{base_url}{page_url}")
        #print(f"now scrapping:{page_url}")
        soup= BeautifulSoup(content.text,"html.parser")
        quotes=soup.find_all(class_="quote")

        #contents to get for each quote:qote,author,persons biolink-->list
        for quote in quotes:
            all_quotes.append({
                "quotes":quote.find(class_="text").get_text(),
                "author":quote.find(class_="author").get_text(),
                "bio_Link":quote.find("a")["href"]
            })
        next_page=soup.find(class_="next")
        page_url=next_page.find("a")["href"] if next_page else None
        sleep(1)
    return all_quotes

#storing the data in csv
def write_quotes(quotes):
    with open("quotes.csv","w",encoding='utf-8', newline ='') as file:
        headers=["quotes","author","bio_Link"]
        csv_writer=DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()

        for quote in all_quotes:
            csv_writer.writerow(quote)

all_quotes=quote_scraping()
write_quotes(all_quotes)