import requests
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import datetime
import pytz

base_url="https://books.toscrape.com/catalogue/"
page_url="page-1.html"

client=MongoClient(" ") #mongodb connection string
db=client.scrape
collection=db.product

while page_url:
        response=requests.get(f"{base_url}{page_url}")
        # print(f"now scraping:{base_url}{page_url}")
        soup=BeautifulSoup(response.text,"html.parser")
        articles=soup.find_all("article",class_="product_pod")

                
        for article in articles:
                        title=article.find("img")["alt"]
                        price=article.find("p",class_="price_color").get_text()
                        rating = {      "One": 1,
                                        "Two": 2,
                                        "Three": 3,
                                        "Four": 4,
                                        "Five": 5
                                        }

                        star=article.find("p")["class"][1]
                        rating_value = rating.get(star)
                        if rating_value is None:
                                rating_value = 0
                            
                        stock_availability=article.find("p",class_="instock availability").get_text()
                        is_stock_available ="In stock" in stock_availability
            
                        image_link=article.find("a")["href"]
                        product_link=article.find("h3").find("a")["href"]
                        

                        product_page =requests.get( f"{base_url}{product_link}")
                        product = BeautifulSoup(product_page.text, "html.parser")

                        product_description=product.find("div",id="product_description")
                        para=product_description.find_next("p").get_text()

                        upc=product.find_all("td")[0].get_text()
                        product_type=product.find_all("td")[1].get_text()
                        price_excl_tax=product.find_all("td")[2].get_text()
                        price_incl_tax=product.find_all("td")[3].get_text()
                        tax=product.find_all("td")[4].get_text()

                        availability=product.find_all("td")[5].get_text()#"In stock (22 available)"
                        split_res= availability.split("(")[1]#['22 available)']
                        availability=split_res.split(" ")[0]#22

                        reviews=product.find_all("td")[6].get_text()
                        
                        categories=product.find("ul",class_="breadcrumb").find_all("li")
                        category_list=[]
                        for category in categories:
                                if category.find("a"):
                                        cat_text= category.find("a").get_text()
                                if cat_text !="Home":
                                        category_list.append(cat_text)
                        category_list.append(categories[-1].get_text())

                        imgs=article.find_all("img")
                        for img in imgs:
                                img_link=f"{base_url}{img.attrs.get('src')}"
                                image=requests.get(img_link).content
                                filename=f"books_img/{title}.jpg"
                                with open(filename,"wb") as file:
                                        file.write(image)
                                        
                        epoch_time=datetime.datetime.utcnow()
                        ist_timezone = pytz.timezone('Asia/Kolkata')
                        current_ist_time = epoch_time.astimezone(ist_timezone)
                        iso_time=current_ist_time.strftime('%Y-%m-%d %H:%M:%S.%fZ')

                        data={"product_name":title,
                        "product_price":price,
                        "product_rating":rating_value,
                        "stock_availability":is_stock_available,
                        "image_link":image_link,
                        "product_link":product_link,
                        "product_description":para,
                        "product_info":{
                                "UPC":upc,
                                "product_type":product_type,
                                "price_excluding_tax":price_excl_tax,
                                "price_including_tax":price_incl_tax,
                                "tax":tax,
                                "availability":availability,
                                "No.of.Reviews":reviews
                        },
                        "category":category_list,
                        "image_path_local":filename,
                        "scrapped_timestamp_epoch":epoch_time,
                        "Scrapped_timestamp_iso":iso_time            
                        }
                        collection.insert_one(data)

        next_page=soup.find(class_="next")
        page_url=next_page.find("a")["href"]if next_page else None
        sleep(1)
