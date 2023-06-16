import PySimpleGUI as sg
from datetime import datetime

def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day': datetime.now().day,
        'month': datetime.now().month,
        'year': datetime.now().year
    }

def buildWeatherURL(month=None, day=None, year=None, airport=None, filter=None):
    """ A GUI to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month, current_day, current_year = currentDate('tuple')

    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year

    # Create the GUI's layout using dropdown menus and input boxes for user input
    layout = [
        [sg.Text('Month')],
        [sg.Combo(values=[str(i) for i in range(1, 13)], default_value=str(1))],
        [sg.Text('Day')],
        [sg.Combo(values=[str(i) for i in range(1, 32)], default_value=str(1))],
        [sg.Text('Year')],
        [sg.Combo(values=[str(i) for i in range(2000, 2024)], default_value=str(2000))],
        [sg.Text('Code')],
        [sg.InputText()],
        [sg.Text('Daily / Weekly / Monthly')],
        [sg.Combo(values=['Daily', 'Weekly', 'Monthly'], default_value='Daily')],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Get The Weather', layout)

    event, values = window.read()
    window.close()

    month = int(values[0])
    day = int(values[1])
    year = int(values[2])
    code = values[3]
    filter = values[4]

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, Code: {code}, Filter: {filter}")

    # return the URL to pass to wunderground to get appropriate weather data
    return f"https://www.wunderground.com/history/{filter.lower()}/{airport}/date/{year}-{month:02d}-{day:02d}"

if __name__ == '__main__':
    buildWeatherURL()