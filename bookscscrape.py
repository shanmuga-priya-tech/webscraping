import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import writer

base_url="https://books.toscrape.com/catalogue/"
page_url="page-1.html"


with open("booksscrape.csv","w",newline="",encoding="utf-8") as file:
    csv_writer=writer(file)
    csv_writer.writerow(["title","price","star_rating","image_url"])

    while page_url:
        response=requests.get(f"{base_url}{page_url}")
        print(f"now scraping:{base_url}{page_url}")
        soup=BeautifulSoup(response.text,"html.parser")
        articles=soup.find_all("article",class_="product_pod")
        
        for article in articles:
                title=article.find("img")["alt"]
                price=article.find("p",class_="price_color").get_text()
                star=article.find("p")["class"][1]
                image_link=article.find("a")["href"]
                csv_writer.writerow([title,price,star,image_link])

        next_page=soup.find(class_="next")
        page_url=next_page.find("a")["href"]if next_page else None
        sleep(1)
