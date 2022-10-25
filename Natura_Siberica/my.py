import requests
import json
import re
from scrapy.selector import Selector
from bs4 import BeautifulSoup

url = 'https://naturasiberica.ru/our-shops/'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

# req = requests.get(url=url, headers=headers)
# src = req.text

# with open('pages/natura_siberica.html', 'w', encoding='utf-8') as file:
#     file.write(src)

with open('pages/natura_siberica.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_pages_dict = {}
pages_link = soup.find_all('a', class_='card-list__link')
count = 0
for link in pages_link:
    link_name = f'natura_siberica_{count}'
    link_href = 'https://naturasiberica.ru' + link.get('href')
    all_pages_dict[link_name] = [link_href]
    count += 1


# with open('pages/all_pages.json', 'w', encoding='utf-8') as file:
#     json.dump(all_pages_dict, file, indent=4, ensure_ascii=False)

with open('pages/all_pages.json', encoding='utf-8') as file:
    all_pages_links = json.load(file)

data_list = []
for shop_name, shop_href in all_pages_links.items():

    pages = requests.get(url=shop_href[0], headers=headers)
    head_items = Selector(text=pages.text).xpath('//p[@class="card-list__description"]/text()').extract()
    print(head_items)


