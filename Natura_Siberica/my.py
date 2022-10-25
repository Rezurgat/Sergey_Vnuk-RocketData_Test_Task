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

req = requests.get(url=url, headers=headers)
src = req.text

# with open('pages/natura_siberica.html', 'w', encoding='utf-8') as file:
#     file.write(src)

with open('pages/natura_siberica.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_pages_dict = {}
all_pages = soup.find_all('a', class_='card-list__link')
print(all_pages)
for link in all_pages:
    link_name = soup.find('p', class_='card-list__name')
    print(link_name)
    # item_href = 'https://naturasiberica.ru' + item.get('href')
    # all_pages_dict[item_text] = [item_href]
