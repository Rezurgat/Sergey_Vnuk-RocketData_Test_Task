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

with open('pages/natura_siberica.html', 'w', encoding='utf-8') as file:
    file.write(src)

with open('pages/natura_siberica.html', encoding='utf-8') as file:
    src = file.read()
