# Webscrapping Assignment

<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A7/Input.PNG">

<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A7/Output.PNG">

### Code
```cpp
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


def processJson():
    # Function to read and return data from the airport-codes.json file
    with open('./airport-codes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def currentDate(returnType='tuple'):
    # Function to get the current date in the desired format
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
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant data from the parsed HTML
        weather_data = {}

        # Example: Extract temperature data
        high_temp_elem = soup.select_one('.summary-table .temp .hi')
        high_temp = high_temp_elem.text if high_temp_elem else 'N/A'

        low_temp_elem = soup.select_one('.summary-table .temp .lo')
        low_temp = low_temp_elem.text if low_temp_elem else 'N/A'

        avg_temp_elem = soup.select_one('.summary-table .temp .wx-value')
        avg_temp = avg_temp_elem.text if avg_temp_elem else 'N/A'

        precip_elem = soup.select_one('.summary-table .precip .wx-value')
        precip = precip_elem.text if precip_elem else 'N/A'

        dew_point_elem = soup.select_one('.summary-table .dewpoint .wx-value')
        dew_point = dew_point_elem.text if dew_point_elem else 'N/A'

        max_wind_speed_elem = soup.select_one('.summary-table .wind .wx-value')
        max_wind_speed = max_wind_speed_elem.text if max_wind_speed_elem else 'N/A'

        visibility_elem = soup.select_one('.summary-table .visibility .wx-value')
        visibility = visibility_elem.text if visibility_elem else 'N/A'

        sea_level_pressure_elem = soup.select_one('.summary-table .pressure .wx-value')
        sea_level_pressure = sea_level_pressure_elem.text if sea_level_pressure_elem else 'N/A'

        weather_data['High Temp'] = high_temp
        weather_data['Low Temp'] = low_temp
        weather_data['Avg Temp'] = avg_temp
        weather_data['Precipitation'] = precip
        weather_data['Dew Point'] = dew_point
        weather_data['Max Wind Speed'] = max_wind_speed
        weather_data['Visibility'] = visibility
        weather_data['Sea Level Pressure'] = sea_level_pressure

        return weather_data

    except (requests.exceptions.RequestException, ValueError) as e:
        raise ValueError('Error: Failed to retrieve weather data!' + str(e))


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

        # Find the city name for the selected airport code
        city = ''
        for item in json_data:
            if item['icao'] == airport_code:
                city = item['city']
                break

        # Build the weather URL
        url = f"https://www.wunderground.com/history/daily/{airport_code}/date/{year}-{month}-{day}"
        window.close()

        try:
            # Retrieve weather data
            weather_data = scrapeWeatherData(url)

            # Add city name to the weather data dictionary
            weather_data['City'] = city

            # PySimpleGUI layout for output table
            layout = [
                [sg.Text(f'City: {city}')],
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
    ```
    
