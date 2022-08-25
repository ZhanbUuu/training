import requests
from bs4 import BeautifulSoup
from time import sleep
import lxml

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

# the function takes the URL of the image as input and writes it to the specified folder
def download_img(url):
    resp = requests.get(url, stream=True)
    r = open("C:\\Users\\User\\Desktop\\image\\" + url.split("/")[-1], "wb")
    for v in resp.iter_content(1024*1024):
        r.write(v)
    r.close()

# generator function outputs each product page
def get_url():
    for i in range(1, 8):
        url = "https://scrapingclub.com/exercise/list_basic/?page=" + str(i)
        src = requests.get(url, headers=headers)
        soup = BeautifulSoup(src.text, "lxml")
        card_links = soup.find_all("h4", class_="card-title")
        for value in card_links:
            links = "https://scrapingclub.com" + value.find("a").get("href")
            yield links
            
# the generator function takes as input a link for each category page and outputs everything about the product
def get_data():
    for links in get_url():
        src = requests.get(links, headers=headers)
        sleep(1)
        soup = BeautifulSoup(src.text, "lxml")
        card_url = soup.find("div", class_="card mt-4 my-4")
        name = card_url.find("h3", class_="card-title").text
        price = card_url.find("h4").text
        text = card_url.find("p", class_="card-text").text
        img = "https://scrapingclub.com" + card_url.find("img", class_="card-img-top img-fluid").get("src")
        download_img(img)
        yield name, price, text, img



