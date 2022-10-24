import re
import requests
from bs4 import BeautifulSoup
import json
from scrapy.selector import Selector



url = 'https://som1.ru/shops/'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117'
}

# req = requests.get(url=url, headers=headers)
# src = req.text

# with open('pages\som.html', 'w', encoding='utf-8') as file:
#     file.write(src)

with open('pages\som.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_pages_dict = {}
all_pages = soup.find_all('div', class_='shops-col shops-button')
count = 1
for link in all_pages:
    item_text = f'som_{count}'
    item_href = 'https://som1.ru' + link.find('a').get('href')
    all_pages_dict[item_text] = [item_href]
    count += 1
"""Сохраню полученный словарь в json-файл. Сохранение в json удобен и сокращает время поиска
информации в интернете"""

# with open('pages/all_pages.json', 'w', encoding='utf-8') as file:
#     json.dump(all_pages_dict, file, indent=4, ensure_ascii=False)

with open('pages/all_pages.json', encoding='utf-8') as file:
    all_pages_links = json.load(file)

data_list = []
for shop_name, shop_href in all_pages_links.items():

    req = requests.get(url=shop_href[0], headers=headers)
    src = req.text
    src_coords = Selector(text=req.text).xpath("//script/text()").extract()


    """Сохраню страницы в html, чтобы обойтись без бана при большом кол-ве запросов"""

    # with open(f'pages/{shop_name}.html', 'w', encoding='utf-8') as file:
    #     file.write(src)

    with open(f'pages/{shop_name}.html', encoding='utf-8') as file:
        for_soup = file.read()

    soup = BeautifulSoup(for_soup, 'lxml')

    all_info = [info.text.strip().split('\n') for info in soup.find('table', class_='shop-info-table').find_all('tr')]

    address = all_info[0][1].strip()

    loc = [script for script in src_coords if 'showShopsMap' in script]
    rgx = re.compile(r'\((.+)\)')
    cut = json.loads(rgx.search(loc[0]).group(1).replace("'", '"'))

    latlon = []
    for item in cut:
        coord = [float(cord) for cord in item['cords']]
        item['cords'] = coord
        latlon.append(coord)

    name = soup.find('div', class_='page-body').find('div', class_='container').find('h1').text
    phones = all_info[1][1].split(',')
    working_hours = [all_info[2][1]]

    data = {
        'address': address,
        'latlon': [float(latlon[0][0]), float(latlon[0][1])],
        'name': name,
        'phones':  phones,
        'working_hours': working_hours
    }

    data_list.append(data)
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data_list, file, indent=4, ensure_ascii=False)
