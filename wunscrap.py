# Made with love by Karl. Telegram: @karlpy

import datetime
from datetime import datetime as dt
import requests
from lxml import etree
import lxml.html as lh
from io import StringIO
import unicodedata
from pymongo import MongoClient

# configuration
stations_file = open('stations.txt', 'r') 
urls = stations_file.readlines() 
todays_date = datetime.datetime.today()
number_of_days = 3
dbclient = MongoClient('localhost:27017')
wunderground_db = dbclient['wunderground']

def format_key(key):
    return key.replace(' ','_').replace('.','')

def date_difference(day):
    return (todays_date - datetime.timedelta(days=day)).strftime("%Y-%m-%d")

def url_generator(weather_station_url, number_of_days):
    for day in range(number_of_days):
        date_string = date_difference(day)
        url = f'{weather_station_url}/table/{date_string}/{date_string}/daily'
        yield date_string, url

def scrap_station(weather_station_url):

    url_gen = url_generator(weather_station_url, number_of_days)

    parser = etree.HTMLParser(recover=True)
    session = requests.Session()
    collection_name = f'{weather_station_url}'

    for date_string, url in url_gen:
        print(f'get url: {url}')
        html_string = session.get(url)
        doc = lh.fromstring(html_string.content)
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
                td_content = unicodedata.normalize("NFKD", td.text_content())

                # replace time with datetime in first column
                if i == 0:
                    td_content = f'{date_string} {td_content}'
                    date_time = dt.strptime(td_content, "%Y-%m-%d %I:%M %p")
                    row_dict[format_key(headers_list[i])] = td_content
                else:
                    row_dict[format_key(headers_list[i])] = td_content
            data_rows.append(row_dict)

        print(f'Saving {len(data_rows)} rows')
        wunderground_db[collection_name].insert_many(data_rows)

for url in urls:
    url = url.strip()
    print(url)
    scrap_station(url)