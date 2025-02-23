import pandas as pd
import requests
from datetime import datetime, timezone, timedelta

# API parameters
api_key = ''
lat = "59.329323"
lon = "18.068581"
request_type = 'hour'  # More specific request type, if available

start_date = datetime(2023, 6, 1, tzinfo=timezone.utc)
end_date = datetime(2023, 6, 30, tzinfo=timezone.utc)

all_data_json = []  # List to store JSON responses

while start_date < end_date:
    # Calculate the end date of the current 7-day period
    end_date_week = start_date + timedelta(days=6)
    if end_date_week > end_date:
        end_date_week = end_date

    # Convert start and end to Unix time
    start_unix_time = int(start_date.timestamp())
    end_unix_time = int(end_date_week.timestamp())

    # Format the URL with the correct parameters
    url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type={request_type}&start={start_unix_time}&end={end_unix_time}&appid={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        all_data_json.append(data)
    else:
        print(f"Failed to fetch data for period starting {start_date}. Status code: {response.status_code}")

    # Update start_date for the next iteration
    start_date = end_date_week + timedelta(days=1)

# Once all data is collected, convert the list of JSON objects to a DataFrame
historicdata = pd.json_normalize(all_data_json)

dfdata = historicdata['list'].explode().apply(pd.Series)
historicdata = pd.concat([historicdata, dfdata], axis=1)
historicdata = historicdata.drop(['list'], axis=1)
historicdata = historicdata.reset_index(drop=True)

dfmain = pd.json_normalize(historicdata['main'])
dfmain = dfmain.rename(columns={'temp': 'main_temp', 'feels_like': 'main_feels_like', 'pressure': 'main_pressure',
                                'humidity': 'main_humidity', 'temp_min': 'main_temp_min', 'temp_max': 'main_temp_max'})
dfwind = pd.json_normalize(historicdata['wind'])
dfwind = dfwind.rename(columns={'speed': 'wind_speed', 'deg': 'wind_deg'})
dfcloud = pd.json_normalize(historicdata['clouds'])
dfcloud = dfcloud.rename(columns={'all': 'overall_cloud'})

first_weather_conditions = [weather[0] if weather else {} for weather in historicdata['weather']]
dfweather = pd.json_normalize(first_weather_conditions)
dfweather = dfweather.rename(
    columns={'id': 'weather_id', 'main': 'main_weather', 'description': 'main_description', 'icon': 'main_icon'})

historicdata = pd.concat([historicdata, dfmain, dfwind, dfcloud, dfweather], axis=1)
historicdata = historicdata.drop(['main', 'clouds', 'weather', 'wind'], axis=1)
historicdata = historicdata.reset_index(drop=True)

# Convert 'dt' column to datetime
# Conver Kelvin to Celcius

historicdata['dt'] = pd.to_datetime(historicdata['dt'], unit='s')
historicdata['main_temp'] = (historicdata['main_temp'] - 273.15).round(2)
historicdata['main_feels_like'] = (historicdata['main_feels_like'] - 273.15).round(2)
historicdata['main_temp_min'] = (historicdata['main_temp_min'] - 273.15).round(2)
historicdata['main_temp_max'] = (historicdata['main_temp_max'] - 273.15).round(2)

print(historicdata)

historicdata.to_csv('weather_Juni_Stockholm.csv', index=False)
