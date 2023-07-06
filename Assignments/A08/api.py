from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import csv

app = FastAPI(
    description="""🚀
    ## 4883 Software Tools
    ### Where awesomeness happens
    """
)

db = []

# Open the CSV file
# Populates the `db` list with all the CSV data
with open('data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    i = 0
    # Read each row in the CSV file
    for row in reader:
        if i == 0:
            i += 1
            continue
        db.append(row)


def getUniqueCountries():
    global db
    countries = set()

    for row in db:
        countries.add(row[2])

    return list(countries)


def getUniqueWhos():
    global db
    whos = set()

    for row in db:
        whos.add(row[3])

    return list(whos)


@app.get("/")
async def docs_redirect():
    """API's base route that redirects to the documentation."""
    return RedirectResponse(url="/docs")


@app.get("/countries/")
async def countries():
    """Retrieves a list of unique countries from the database."""
    return {"countries": getUniqueCountries()}


@app.get("/whos/")
async def whos():
    """Retrieves a list of unique WHO regions from the database."""
    return {"whos": getUniqueWhos()}


@app.get("/casesByRegion/")
async def cases_by_region(year: int = None):
    """
    Retrieves the number of cases by region.
    If a year is specified, it filters the cases for that year.
    """
    cases = {}

    for row in db:
        if year is not None and int(row[0][:4]) != year:
            continue

        if row[3] not in cases:
            cases[row[3]] = 0

        cases[row[3]] += int(row[4])

    return {"data": cases, "success": True, "message": "Cases by Region", "size": len(cases), "year": year}


my_list = ['apple', 'banana', 'cherry', 'date', 'elderberry']


@app.get("/get_values1/")
def get_values1(index1: int = None, index2: int = None):
    try:
        value1 = my_list[index1]
        value2 = my_list[index2]
        return [value1, value2]
    except IndexError:
        return {"error": "Invalid index provided."}


@app.get("/get_values2/{index1}/{index2}")
def get_values2(index1: int, index2: int):
    try:
        value1 = my_list[index1]
        value2 = my_list[index2]
        return [value1, value2]
    except IndexError:
        return {"error": "Invalid index provided."}


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
 
