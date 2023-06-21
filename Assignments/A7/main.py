import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


def processJson():
    with open('./airport-codes.json', 'r',encoding = 'utf-8') as f:
        data = json.load(f)

    return data


def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return. Valid values are 'tuple', 'list', or 'dict'.
    """
    now = datetime.now()
    if returnType == 'tuple':
        return now.month, now.day, now.year
    elif returnType == 'list':
        return [now.month, now.day, now.year]
    elif returnType == 'dict':
        return {
            'day': now.day,
            'month': now.month,
            'year': now.year
        }


def scrapeWeatherData(url):
    try:
        # Retrieve weather data
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant data from the parsed HTML
        weather_data = soup.find_all('span', class_='wx-value')

        if len(weather_data) >= 8:
            high_temp = weather_data[0].text
            low_temp = weather_data[1].text
            avg_temp = weather_data[2].text
            precip = weather_data[3].text
            dew_point = weather_data[4].text
            max_wind_speed = weather_data[5].text
            visibility = weather_data[6].text
            sea_level_pressure = weather_data[7].text

            return {
                'High Temp': high_temp,
                'Low Temp': low_temp,
                'Avg Temp': avg_temp,
                'Precipitation': precip,
                'Dew Point': dew_point,
                'Max Wind Speed': max_wind_speed,
                'Visibility': visibility,
                'Sea Level Pressure': sea_level_pressure
            }
        else:
            raise ValueError('Error: Unable to scrape weather data.')

    except requests.exceptions.RequestException:
        sg.popup('Error: Failed to retrieve weather data!')


def buildWeatherURL(json_data, airport_codes):
    # Get the current date
    current_month, current_day, current_year = currentDate('tuple')

    # PySimpleGUI layout for input form
    layout = [
        [sg.Text('Day'), sg.Combo(values=[str(i) for i in range(1, 32)], default_value=str(1), key='day')],
        [sg.Text('Month'), sg.Combo(values=[str(i) for i in range(1, 13)], default_value=str(1), key='month')],
        [sg.Text('Year'), sg.Combo(values=[str(i) for i in range(2000, 2024)], default_value=str(2000), key='year')],
        [sg.Text('Airport Code'), sg.Combo(values=airport_codes, key='airport')],
        [sg.Button('Submit')]
    ]

    # Create the PySimpleGUI window for input form
    window = sg.Window('Weather Data Input', layout)

    # Event Loop for input form
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        day = values['day']
        month = values['month']
        year = values['year']
        airport_code = values['airport']

        # Build the weather URL
        url = f"https://www.wunderground.com/history/daily/{airport_code}/date/{year}-{month}-{day}"
        window.close()

        try:
            # Retrieve weather data
            weather_data = scrapeWeatherData(url)

            # PySimpleGUI layout for output table
            layout = [
                [sg.Table(values=[list(weather_data.values())],
                          headings=list(weather_data.keys()),
                          auto_size_columns=True,
                          justification='center')],
                [sg.Button('OK')]
            ]

            # Create the PySimpleGUI window for output table
            window = sg.Window('Weather Data Output', layout)

            # Event Loop for output table
            while True:
                event, _ = window.read()
                if event == sg.WINDOW_CLOSED or event == 'OK':
                    break

            window.close()

        except ValueError as e:
            sg.popup(str(e))


if __name__ == "__main__":
    json_data = processJson()
    airport_codes = [item['icao'] for item in json_data]
    buildWeatherURL(json_data, airport_codes)
