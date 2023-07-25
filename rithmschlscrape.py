import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep

base_url="https://www.rithmschool.com"
url="/blog"

with open("rithmscrape.csv","w") as file:
    csv_writer=writer(file)
    csv_writer.writerow(["tittle","url","date"])

    while url:
        response=requests.get(f"{base_url}{url}")
        print(F"now scrapping{base_url}{url}")
        soup=BeautifulSoup(response.text ,"html.parser")
        articles=soup.find_all("article")

        for article in articles:
            tittle= article.find("a").text
            link=article.find("a")["href"]
            date=article.find("small").text
            csv_writer.writerow([tittle,link,date])
            
        next_page=soup.find(class_="next")
        url=next_page.find("a")["href"]  if next_page else None
        sleep(2)