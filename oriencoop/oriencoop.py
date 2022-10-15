import re
import requests
from bs4 import BeautifulSoup
import json



url = 'https://oriencoop.cl/sucursales.htm'

headers = {
    'Accept': 'text/css,*/*;q=0.1',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117'
}

# req = requests.get(url=url, headers=headers)
# src = req.text
#
# with open('pages/oriencoop.html', 'w', encoding='utf-8') as file:
#     file.write(src)

with open('pages/oriencoop.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_pages_dict = {}
all_pages = soup.find('ul',class_='c-list c-accordion').find_all('a')
for item in all_pages:
    item_text = item.text
    item_href = 'https://oriencoop.cl' + item.get('href')
    if 'javascript:void(0);' not in item_href:
        all_pages_dict[item_text] = [item_href]

"""Сохраню полученный словарь в json-файл. Сохранение в json удобен и сокращает время поиска
информации в интернете"""

# with open('pages/all_pages.json', 'w', encoding='utf-8') as file:
#     json.dump(all_pages_dict, file, indent=4, ensure_ascii=False)

with open('pages/all_pages.json', encoding='utf-8') as file:
    all_pages_links = json.load(file)

data_list = []
for city_name, city_href in all_pages_links.items():

    req = requests.get(url=city_href, headers=headers)
    src = req.text

    """Сохраню страницы под именем городов, чтобы обойтись без бана при большом кол-ве запросов"""

    # with open(f'pages/{city_name}.html', 'w', encoding='utf-8') as file:
    #     file.write(src)

    with open(f'pages/{city_name}.html', encoding='utf-8') as file:
        for_soup = file.read()

    soup = BeautifulSoup(for_soup, 'lxml')

    all_info =[info.text.strip() for info in soup.find(class_='s-dato').find_all('span')]

    geocode_url = soup.find('div', class_='s-mapa').find_all('iframe')[0]['src']
    coord = re.compile(r'\!2d([^!]+)\!3d([^!]+)')
    geocode = list(map(float, coord.search(geocode_url).group(1, 2)))

    default_phones = [phone.text.strip() for phone in soup.find_all(class_='call')]

    address = all_info[0].strip()
    name = 'Oriencoop'
    phones = [all_info[1], default_phones[0], default_phones[1]]
    working_hours = [all_info[3], all_info[4]]

    data = {
        'address': address,
        'latlon': geocode,
        'name': name,
        'phones':  phones,
        'working_hours': working_hours
    }

    data_list.append(data)

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data_list, file, indent=4, ensure_ascii=False)
