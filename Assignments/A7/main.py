import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


def processJson():
    with open('airport-codes.json') as f:
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


def buildWeatherURL(json_data, airport_codes):
    # Get the current date
    current_month, current_day, current_year = currentDate('tuple')

    # PySimpleGUI layout for input form
    layout = [
        [sg.Text('Day'), sg.Combo(values=[str(i) for i in range(1, 32)], default_value=str(current_day), key='day')],
        [sg.Text('Month'), sg.Combo(values=[str(i) for i in range(1, 13)], default_value=str(current_month), key='month')],
        [sg.Text('Year'), sg.Combo(values=[str(i) for i in range(2000, 2024)], default_value=str(current_year), key='year')],
        [sg.Text('Airport Code'), sg.Combo(values=airport_codes, key='airport')],
        [sg.Text('Daily / Weekly / Monthly'), sg.Combo(values=['Daily', 'Weekly', 'Monthly'], key='filter')],
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
        filter = values['filter']

        # Build the weather URL
        url = f"https://www.wunderground.com/history/{filter.lower()}/{airport_code}/date/{year}-{month}-{day}"
        window.close()

        try:
            # Retrieve weather data
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract relevant data from the parsed HTML
            max_temp = soup.find('span', class_='wx-value').text
            avg_temp = soup.find('span', class_='wx-value').find_next('span', class_='wx-unit').text
            min_temp = soup.find('span', class_='wx-value').find_next('span', class_='wx-unit').find_next('span', class_='wx-unit').text
            precip = soup.find('span', class_='wx-value').find_next('span', class_='wx-unit').find_next('span', class_='wx-unit').find_next('span', class_='wx-value').text
            avg_precip = soup.find('span', class_='wx-value').find_next('span', class_='wx-unit').find_next('span', class_='wx-unit').find_next('span', class_='wx-value').find_next('span', class_='wx-unit').text
            wind_max = soup.find('span', class_='wx-value').find_next('span', class_='wx-unit').find_next('span', class_='wx-unit').find_next('span', class_='wx-value').find_next('span', class_='wx-unit').find_next('span', class_='wx-value').text
            dew_point = soup.find('span', class_='wx-value').find_next('span', class_='wx-unit').find_next('span', class_='wx-unit').find_next('span', class_='wx-value').find_next('span', class_='wx-unit').find_next('span', class_='wx-value').find_next('span', class_='wx-unit').text

            # PySimpleGUI layout for output table
            layout = [
                [sg.Table(values=[[f"{month}-{day}-{year}", max_temp, avg_temp, min_temp, precip, avg_precip, wind_max, dew_point]],
                          headings=['Date', 'Max Temp', 'Avg Temp', 'Min Temp', 'Precip', 'Avg Precip', 'Max Wind Speed', 'Dew Point'],
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

        except requests.exceptions.RequestException:
            sg.popup('Error: Failed to retrieve weather data!')


if __name__ == "__main__":
    json_data = processJson()
    airport_codes = [item['icao'] for item in json_data]
    buildWeatherURL(json_data, airport_codes)
