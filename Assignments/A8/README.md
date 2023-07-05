```py
import csv
from typing import List
from fastapi import FastAPI

app = FastAPI()
data: List[dict] = []  # Global variable to store the CSV data

@app.on_event("startup")
async def load_data():
    """Load data from the CSV file on application startup."""
    try:
        with open("data.csv", 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(dict(row))
    except StopIteration:
        print("CSV file is empty or does not contain any data.")
    except FileNotFoundError:
        print("CSV file not found.")

# Generic Routes
@app.get("/")
def get_documentation():
    """Retrieves the documentation provided by Swagger."""
    return {"documentation": "Link to API documentation"}

@app.get("/countries")
def get_countries_stats():
    """Retrieves statistics for each country: total death count, new cases, and total cases."""
    countries_stats = []
    for row in data:
        country = row['Country']
        total_deaths = int(row['Total_deaths'])
        new_cases = int(row['New_cases'])
        total_cases = int(row['Total_cases'])
        country_stats = {
            "country": country,
            "total_deaths": total_deaths,
            "new_cases": new_cases,
            "total_cases": total_cases
        }
        countries_stats.append(country_stats)
    return {"countries_stats": countries_stats}

# Death Routes
@app.get("/deaths")
def get_total_deaths(country: str = None, region: str = None, year: int = None):
    """
    Retrieves the total deaths based on optional filters.
    - country (str): A country name
    - region (str): A WHO region
    - year (int): A 4-digit year
    """
    filtered_data = data
    if country:
        filtered_data = [row for row in filtered_data if row['Country'].lower() == country.lower()]
    if region:
        filtered_data = [row for row in filtered_data if row['WHO_region'].lower() == region.lower()]
    if year:
        filtered_data = [row for row in filtered_data if row['Year'].startswith(str(year))]
    
    total_deaths = sum(int(row['Total_deaths']) for row in filtered_data)
    return {"total_deaths": total_deaths}

# Case Routes
@app.get("/cases")
def get_total_cases(country: str = None, region: str = None, year: int = None):
    """
    Retrieves the total cases based on optional filters.
    - country (str): A country name
    - region (str): A WHO region
    - year (int): A 4-digit year
    """
    filtered_data = data
    if country:
        filtered_data = [row for row in filtered_data if row['Country'].lower() == country.lower()]
    if region:
        filtered_data = [row for row in filtered_data if row['WHO_region'].lower() == region.lower()]
    if year:
        filtered_data = [row for row in filtered_data if row['Year'].startswith(str(year))]
    
    total_cases = sum(int(row['Total_cases']) for row in filtered_data)
    return {"total_cases": total_cases}

# Aggregate Routes
@app.get("/max_deaths")
def get_country_with_max_deaths(min_date: str = None, max_date: str = None):
    """
    Finds the country with the most deaths between a range of dates.
    - min_date (str): The minimum date in YYYY-MM-DD format
    - max_date (str): The maximum date in YYYY-MM-DD format
    """
    filtered_data = data
    if min_date and max_date:
        filtered_data = [row for row in filtered_data if min_date <= row['Date'] <= max_date]
    
    max_deaths_row = max(filtered_data, key=lambda row: int(row['Total_deaths']))
    country_with_max_deaths = max_deaths_row['Country']
    max_deaths = int(max_deaths_row['Total_deaths'])
    return {"country_with_max_deaths": country_with_max_deaths, "max_deaths": max_deaths}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

```
