# material taken fror  here: https://www.youtube.com/watch?v=ks64MvZJe0w
# slightly modified for Windows
import random
import lxml
from bs4 import BeautifulSoup
import requests
import json
from time import sleep
import csv


# получил код страницы
# url = "https://health-diet.ru/table_calorie/"
#
headers = {
     "accept": "*/*",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
#
# req = requests.get(url, headers=headers)
# src = req.text
# # print(src)

# записал код страницы в файл
# with open("my_pars_education.html", "w", encoding='UTF-8-sig') as file:
#     file.write(src)

# теперь использую этот файл для поиска категорий продуктов
with open("my_pars_education.html", encoding='UTF-8-sig') as file:
    src = file.read()

# ищу в этом файле класс категорий
soup = BeautifulSoup(src, "lxml")
all_items = soup.find_all(class_="mzr-tc-group-item-href")
# print(all_items)

# а тут упорядочиваю
all_catigories_dict = {}
for item in all_items:
    item_text = item.text
    item_location = "https://health-diet.ru" + item.get("href")
    all_catigories_dict[item_text] = item_location
# print(all_catigories_dict)

# записываю что получилось в файл json
# with open("all_catigories_dict.json", "w", encoding='UTF-8-sig') as file:
#     json.dump(all_catigories_dict, file, indent=4, ensure_ascii=False)

# далее буду использовать этот файл
with open("all_catigories_dict.json", encoding='UTF-8-sig') as file:
    all_catigories = json.load(file)
# print(all_catigories)

# создал счетик итераций и убрал ненужные знаки препинания
iteration_count = int(len(all_catigories)) - 1
print("Всего итераций", iteration_count)
count = 0
for category_name, category_location in all_catigories.items():
    rep = [".", "'", " ", ","]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    # print(category_name)
    # делаю запросы по ссылкам категорий записывая в отдельную папку
    req = requests.get(category_location, headers=headers)
    src = req.text
    with open(f"data_my_pars_education/{count}_{category_name}.html", "w", encoding='UTF-8-sig') as file:
        file.write(src)

    # теперь использую этот файл
    with open(f"data_my_pars_education/{count}_{category_name}.html", encoding='UTF-8-sig') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    # проверка на наличие таблицы
    alert_block = soup.find(class_="uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top")
    if alert_block is not None:
        continue

    # нахожу заголовки таблицы и записываю в сsv файл
    table_head = soup.find(class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find("tr").find_all("th")
    # print(table_head)
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text
    # print(carbohydrates)

    with open(f"data_my_pars_education/{count}_{category_name}.csv", "w", encoding='UTF-8-sig') as file:
        writer = csv.writer(file, delimiter=';', lineterminator='\n')
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # собираю данные продуктов
    product_data = soup.find(class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find("tbody").find_all("tr")

    product_info = []

    for item in product_data:
        product_tds = item.find_all("td")
        # print(product_tds)
        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        # записываю данные в таблицу
        with open(f"data_my_pars_education/{count}_{category_name}.csv", "a", encoding='UTF-8-sig') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f"data_my_pars_education/{count}_{category_name}.json", "a", encoding='UTF-8-sig') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"Итериция {count}, {category_name} записан...")
    iteration_count -= 1

    if iteration_count == 0:
        print("Итерация закончена.")
        break

    print(f" Итераций осталось {iteration_count}")
    sleep(random.randrange(2, 4))
