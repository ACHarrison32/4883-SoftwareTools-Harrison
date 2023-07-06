import json
import requests
from bs4 import BeautifulSoup
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Read airport codes and names from the JSON file
airport_data = []
with open('airport-codes.json') as json_file:
    airport_data = json.load(json_file)

airport_codes = [entry['icao'] for entry in airport_data]
airport_names = {entry['icao']: entry['name'] for entry in airport_data}

# Define the GUI layout using PySimpleGUI
layout = [
    [sg.Text('Day'), sg.Combo(list(range(1, 32)), key='-DAY-', size=(5, 1))],
    [sg.Text('Month'), sg.Combo(list(range(1, 13)), key='-MONTH-', size=(5, 1))],
    [sg.Text('Year'), sg.Combo(list(range(2000, 2024)), key='-YEAR-', size=(5, 1))],
    [sg.Text('Airport Code'), sg.Combo(airport_codes, key='-AIRPORT-', size=(10, 1))],
    [sg.Button('Submit'), sg.Button('Exit')],
    [sg.Table(values=[], headings=['Airport', 'Date', 'Temperature', 'Precipitation'], key='-TABLE-', max_col_width=25, auto_size_columns=True)]
]

# Create the GUI window
window = sg.Window('Weather Data Scraper', layout)

def scrape_weather_data(url, airport_code):
    # Use Selenium to obtain the dynamically loaded weather data
    driver = webdriver.Chrome()  # Make sure you have Chrome WebDriver installed and in PATH
    driver.get(url)

    # Wait for the weather data to be loaded asynchronously
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'summary-table')))

    # Extract the HTML content
    html = driver.page_source
    driver.quit()

    # Use BeautifulSoup to parse the HTML and extract the desired data
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='days ng-star-inserted')

    if table is None:
        return []

    rows = table.find_all('tr')

    # Extract the weather data from the table rows
    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 9:
            date = cells[0].get_text(strip=True)
            temperature = cells[1].get_text(strip=True)
            precipitation = cells[7].get_text(strip=True)
            airport_name = airport_names.get(airport_code, '')
            data.append([airport_name, date, temperature, precipitation])

    return data

# Event loop to handle GUI events
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    if event == 'Submit':
        day = values['-DAY-']
        month = values['-MONTH-']
        year = values['-YEAR-']
        airport_code = values['-AIRPORT-']

        # Build the URL to scrape weather data from
        base_url = "https://www.wunderground.com/history"
        url = f"{base_url}/daily/{airport_code}/date/{year}-{month}-{day}"

        # Scrape weather data using the constructed URL
        weather_data = scrape_weather_data(url, airport_code)

        # Update the table with the scraped data
        table = window['-TABLE-']
        
        if len(weather_data) == 0:
            sg.popup('No weather data available for the selected date and airport.')
        else:
            table.update(values=weather_data)

window.close()
