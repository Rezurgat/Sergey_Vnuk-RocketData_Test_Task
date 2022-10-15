import requests
import json
import re
from scrapy.selector import Selector


req = requests.get('https://naturasiberica.ru/our-shops/')

items = Selector(text=req.text).xpath('//p[@class="card-list__description"]/text()').extract()

src = [item.split('/')[-2] for item in Selector(text=req.text).xpath('//a[@class="card-list__link"]/@href').extract()]

headline = Selector(text=req.text).xpath('//*[@id="bx_1573527503_444"]/div[2]/h2/text()').get().split(' ')
name = headline[-2] + ' ' + headline[-1]

for_addresses = []

data_list = []


for i in items:
    for_addresses.append(i.replace('\t', '').replace('\r\n', ''))

for i, loc in enumerate(src):
    data = dict()
    data['address'] = for_addresses[i]

    #session = HTMLSession()

    an_req = requests.get(f'https://www.google.com/maps/search/{for_addresses[i]}')
    #response.html.render(timeout=20)
    data['latlon'] = [float(coord) for coord in re.split('&|=|%2C', Selector(text=an_req.text).xpath('//meta[@itemprop="image"]/@content').get())[1:3]]

    req_new = requests.get('https://naturasiberica.ru/our-shops/' + loc)

    data['name'] = name
    data['phones'] = Selector(text=req_new.text).xpath('//*[@id="shop-phone-by-city"]/text()').extract()
    data['working_hours'] = Selector(text=req_new.text).xpath('//*[@id="schedule1"]/text()').extract()
    print(f'Collecting data from {loc}... ' + f'{i+1} of {len(src)}')
    data_list.append(data)

print(json.dumps(data_list, indent=4, ensure_ascii=False))