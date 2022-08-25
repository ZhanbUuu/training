import requests
from bs4 import BeautifulSoup
from time import sleep

# get a request and check
url = "https://pc-1.ru/i_shop"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

# looking for a class with categories
soup = BeautifulSoup(src, "lxml")
all_items = soup.find_all(class_="object_announcement block_02")

# the generator function takes a link to a category as input and returns a link to each page in that category
def get_category_url():
    for item in all_items:
        catalog_name = item.text
        location = item.get("onclick")
        page_link = "https://pc-1.ru" + location.split("'")[1]
        page_number = requests.get(page_link, headers=headers)
        soup_page = BeautifulSoup(page_number.text, "lxml")
        count = len(soup_page.find_all("a", class_="pseudo_button"))
        for i in range(1, count - 1):
            try:
                page_url = "https://pc-1.ru" + location.split("'")[
                    1] + "?rid=29654&isSearched=1&act=1&currentRid=29654&page=" + str(i)
                yield page_url, catalog_name
            except:
                page_url = "https://pc-1.ru" + location.split("'")[1]
                yield page_url, catalog_name

# the generator function takes as input a link for each category page and outputs everything about the product
def all_products():
    for page_url, catalog_name in get_category_url():
        sleep(2)
        product = requests.get(page_url, headers=headers)
        soup_product = BeautifulSoup(product.text, "lxml")
        product_inf = soup_product.find_all("div", class_="object_goods block_02")
        for inf in product_inf:
            href = "https://pc-1.ru" + inf.find("a").get("href")
            name = inf.find("h3", class_="object_goods_header").find("a").text
            price = inf.find("span", class_="imp_01").text
            description = inf.find("span").text
            yield name, price, description, href, catalog_name
