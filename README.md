# The Weather Scraper (🌩⛈🌤🌞🌨)

Need High-resolution Weather Data for Analytics or Machine-learning ? Seek no more.

## Overview

The Weather Scraper downloads download high-resolution weather data (often 5 min. intervals) from Wunderground's public weather stations around the world for you.

#### Install dependencies

```python
pip install -r requirements.txt
```

### How to run TWS?

First, find the weather stations you are looking for.
Then you just have to update 2 config files before running TWS.

1. Go to https://www.wunderground.com/wundermap and zoom in to your location
   🌞 Click on a weather station and then click on the **Station ID** (the Station Summary page will open)
   🌞 Open and copy all Station ID URLs you need

2. Set the weather station urls inside **stations.txt**
   🌞 _one url per line!_

3. Inside **config.py**
   🌞 Set the date-range you want to download your data from
   🌞 Set the unit system you need (metric / imperial)

If you want to download data from 2020/5/1 to 2020/6/1 in metric units your config.py will look like this:

```python
from datetime import date

# Set Date format like: YYYY, MM, DD
START_DATE = date(2020, 5, 1)
END_DATE = date(2020, 6, 1)
# set to "metric" or "imperial"
UNIT_SYSTEM = "metric"
```

Now you are read to run your downloads:

```sh
$ python weather_scraper.py
```

Wait until TWS finishes writing your data to files with this naming pattern **_station_name.csv_** inside the `data` directory!

You resulting CSV file will look something like this (if you give it a nice format)

![CSV example](https://raw.githubusercontent.com/Karlheinzniebuhr/the-weather-scraper/master/resources/csv.JPG)
