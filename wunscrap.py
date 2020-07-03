# Made with love by Karl
# Contact me on Telegram: @karlpy

from util.UnitConverter import ConvertToSystem
from util.Parser import Parser
from util.WeatherClass import Weather

from datetime import datetime, date, timedelta
import requests, csv
from lxml import etree
import lxml.html as lh
from io import StringIO
from pymongo import MongoClient

# configuration
stations_file = open('stations.txt', 'r') 
urls = stations_file.readlines() 

# Date format: YYYY-MM-DD
start_date = date(2020, 5, 1)
end_date = date(2020, 6, 1)
# set to "metric" or "imperial"
unit_system = "metric"

# dbclient = MongoClient('localhost:27017')
# wunderground_db = dbclient['wunderground']

def datetime_range_generator(start, end):
    span = end - start
    for i in range(span.days + 1):
        yield start + timedelta(days=i)

def date_url_generator(weather_station_url):
    date_range = datetime_range_generator(start_date, end_date)
    for date in date_range:
        date_string = date.strftime("%Y-%m-%d")
        url = f'{weather_station_url}/table/{date_string}/{date_string}/daily'
        yield date_string, url

def scrap_station(weather_station_url):
    url_gen = date_url_generator(weather_station_url)
    parser = etree.HTMLParser(recover=True)
    session = requests.Session()
    collection_name = f'{weather_station_url}'

    with open('weather_data.csv', 'w', newline='') as csvfile:
        fieldnames = []
        fieldnames = ['Date', 'Time',	'Temperature',	'Dew_Point',	'Humidity',	'Wind',	'Speed',	'Gust',	'Pressure',	'Precip_Rate',	'Precip_Accum',	'UV',   'Solar']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        # Write the headers of the CSV
        if unit_system == "metric":
            # 12:04 AM	24.4 C	18.3 C	69 %	SW	0.0 km/h	0.0 km/h	1,013.88 hPa	0.00 mm	0.00 mm	0	0 w/m²
            writer.writerow({'Date': 'Date', 'Time': 'Time',	'Temperature': 'Temperature_C',	'Dew_Point': 'Dew_Point_C',	'Humidity': 'Humidity_%',	'Wind': 'Wind',	'Speed': 'Speed_kmh',	'Gust': 'Gust_kmh',	'Pressure': 'Pressure_hPa',	'Precip_Rate': 'Precip_Rate_mm',	'Precip_Accum': 'Precip_Accum_mm',	'UV': 'UV',   'Solar': 'Solar_w/m2'})
        elif unit_system == "imperial":
            # 12:04 AM	75.9 F	65.0 F	69 %	SW	0.0 mph	0.0 mph	29.94 in	0.00 in	0.00 in	0	0 w/m²
            writer.writerow({'Date': 'Date', 'Time': 'Time',	'Temperature': 'Temperature_F',	'Dew_Point': 'Dew_Point_F',	'Humidity': 'Humidity_%',	'Wind': 'Wind',	'Speed': 'Speed_mph',	'Gust': 'Gust_mph',	'Pressure': 'Pressure_in',	'Precip_Rate': 'Precip_Rate_in',	'Precip_Accum': 'Precip_Accum_in',	'UV': 'UV',   'Solar': 'Solar_w/m2'})
        else:
            raise Exception("please set 'unit_system' to either \"metric\" or \"imperial\"! ")

        for date_string, url in url_gen:
            print(f'get url: {url}')
            html_string = session.get(url)
            doc = lh.fromstring(html_string.content)
            history_table = doc.xpath('//*[@id="inner-content"]/section[1]/div[1]/div/div/div/div/lib-history/div[2]/lib-history-table/div/div/div/table/tbody')
            if not history_table:
                raise Exception('Table not found, please update xpath!')

            # parse html table rows
            data_rows = Parser.parse_html_table_row(date_string, history_table)

            # convert to metric system
            converter = ConvertToSystem("metric")
            data_to_write = converter.convert_dict_list(data_rows)
                
            print(f'Saving {len(data_to_write)} rows')
            writer.writerows(data_to_write)
            # wunderground_db[collection_name].insert_many(data_to_write)


for url in urls:
    url = url.strip()
    print(url)
    scrap_station(url)