from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
from datetime import datetime
import uvicorn

app = FastAPI(
    title="COVID-19 API",
    description="""A RESTful API that provides access to COVID-19 data.""",
    version="1.0.0",
)

db = []

# Open the CSV file
# Populates the `db` list with all the CSV data
with open('data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    next(reader)  # Skip the header row

    # Read each row in the CSV file
    for row in reader:
        db.append(row)


def get_countries():
    countries = set()

    for row in db:
        countries.add(row[2])

    return list(countries)


def get_regions():
    regions = set()

    for row in db:
        regions.add(row[3])

    return list(regions)


def get_total_deaths(country=None, region=None, year=None):
    total_deaths = 0

    for row in db:
        if country and row[2] != country:
            continue

        if region and row[3] != region:
            continue

        if year and int(row[0][:4]) != year:
            continue

        total_deaths += int(row[7])

    return total_deaths


def get_total_cases(country=None, region=None, year=None):
    total_cases = 0

    for row in db:
        if country and row[2] != country:
            continue

        if region and row[3] != region:
            continue

        if year and int(row[0][:4]) != year:
            continue

        total_cases += int(row[5])

    return total_cases


@app.get("/")
async def docs_redirect():
    """API's base route that redirects to the documentation."""
    return RedirectResponse(url="/docs")


@app.get("/countries/")
async def countries():
    """Retrieves a list of unique countries from the database."""
    return {"countries": get_countries()}


@app.get("/regions/")
async def regions():
    """Retrieves a list of available WHO regions from the database."""
    return {"regions": get_regions()}


@app.get("/deaths/")
async def deaths(country: str = None, region: str = None, year: int = None):
    """
    Retrieves the total deaths for the given country, region, and/or year.
    If no parameters are provided, it returns the total deaths for all countries.
    """
    total_deaths = get_total_deaths(country, region, year)

    return {"total_deaths": total_deaths}


@app.get("/cases/")
async def cases(country: str = None, region: str = None, year: int = None):
    """
    Retrieves the total cases for the given country, region, and/or year.
    If no parameters are provided, it returns the total cases for all countries.
    """
    total_cases = get_total_cases(country, region, year)

    return {"total_cases": total_cases}


@app.get("/maxdeaths/")
async def max_deaths():
    """
    Retrieves the country with the maximum number of deaths.
    """
    max_deaths_country = max(db, key=lambda row: int(row[7]))[2]

    return {"max_deaths_country": max_deaths_country}


@app.get("/mindeaths/")
async def min_deaths():
    """
    Retrievesthe country with the minimum number of deaths.
    """
    min_deaths_country = min(db, key=lambda row: int(row[7]))[2]

    return {"min_deaths_country": min_deaths_country}


@app.get("/mostdeathsduring/")
async def most_deaths(start_date: str, end_date: str):
    """
    Retrieves the country with the most deaths between the specified start and end dates.
    Date format: year-month-day.
    """
    most_deaths_country = ""
    most_deaths = 0

    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    for row in db:
        date = datetime.strptime(row[0], "%Y-%m-%d")

        if start_datetime <= date <= end_datetime:
            deaths = int(row[7])

            if deaths > most_deaths:
                most_deaths = deaths
                most_deaths_country = row[2]

    return {"most_deaths_country": most_deaths_country, "most_deaths": most_deaths}


@app.get("/leastdeathsduring/")
async def least_deaths(start_date: str, end_date: str):
    """
    Retrieves the country with the least deaths between the specified start and end dates.
    Date format: year-month-day.
    """
    least_deaths_country = ""
    least_deaths = float("inf")

    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    for row in db:
        date = datetime.strptime(row[0], "%Y-%m-%d")

        if start_datetime <= date <= end_datetime:
            deaths = int(row[7])

            if deaths < least_deaths:
                least_deaths = deaths
                least_deaths_country = row[2]

    return {"least_deaths_country": least_deaths_country, "least_deaths": least_deaths}


@app.get("/average_deaths/")
async def average_deaths():
    """
    Calculates the average number of deaths between all countries.
    """
    total_deaths = get_total_deaths()

    num_countries = len(get_countries())

    if num_countries > 0:
        average_deaths = total_deaths / num_countries
    else:
        average_deaths = 0

    return {"average_deaths": average_deaths}


# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, log_level="debug", reload=True)
