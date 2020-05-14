# Made with love by Karl. Telegram: @karlpy

import datetime
import requests
from lxml import etree
import lxml.html as lh
from io import StringIO
import unicodedata
from pymongo import MongoClient

# configuration
stationsFile = open('stations.txt', 'r') 
urls = stationsFile.readlines() 
todaysDate = datetime.datetime.today()
numberOfDays = 30
dbclient = MongoClient('localhost:27017')
wunderground_db = dbclient['wunderground']

def formatKey(key):
    return key.replace(' ','_').replace('.','')

def scrapStation(weather_station_url):
    url_generator = (f'{weather_station_url}/table/{(todaysDate - datetime.timedelta(days=x)).strftime("%Y-%m-%d")}/{(todaysDate - datetime.timedelta(days=x)).strftime("%Y-%m-%d")}/daily' for x in range(numberOfDays))

    parser = etree.HTMLParser(recover=True)
    session = requests.Session()
    collection_name = f'{weather_station_url}'

    for url in url_generator:
        print(f'get url: {url}')
        html_string = session.get(url)
        doc = lh.fromstring(html_string.content)
        history_table = doc.xpath('//*[@id="inner-content"]/section[1]/div[1]/div/div/div/div/lib-history/div[2]/lib-history-table/div/div/div/table/tbody')
        history_table = doc.xpath('//*[@id="inner-content"]/section[1]/div[1]/div/div/div/div/lib-history/div[2]/lib-history-table/div/div/div/table/tbody')
        if not history_table:
            continue
        tr_elements = [tr for tr in history_table[0].xpath('//tr') if len(tr) == 12]
        headers_list = []
        data_rows = []

        # set Table Headers
        for header in tr_elements[0]:
            headers_list.append(header.text)

        for tr in tr_elements[1:]:
            row_dict = {}
            for i, td in enumerate(tr.getchildren()):
                row_dict[formatKey(headers_list[i])] = unicodedata.normalize("NFKD", td.text_content())
            data_rows.append(row_dict)

        print(f'Saving {len(data_rows)} rows')
        wunderground_db[collection_name].insert_many(data_rows)

for url in urls:
    url = url.strip()
    print(url)
    scrapStation(url)