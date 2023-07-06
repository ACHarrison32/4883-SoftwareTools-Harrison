from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
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
