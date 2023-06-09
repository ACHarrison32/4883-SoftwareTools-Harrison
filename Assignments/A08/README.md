# :computer: A08 - Fast API With Covid Data
## :name_badge: Andrew Harrison
## :school: 4883 Software Tools
## :date: 07/05/2023
## 
## :memo: Description
#### Create a RESTful API using FastAPI that provides access to COVID-19 data. The API will fetch the data from a publicly available data source and expose endpoints to retrieve various statistics related to COVID-19 cases.

| # | File |
| - | ---- |
| 1 | [api.py](https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/api.py) |
| 2 | [data.csv](https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/data.csv)|

## :question: How to run my code
#### First start by opening the folder in vs code.
#### Open up [api.py](https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/api.py) and run it. 
#### Look into your command terminal and select the following:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/LocalHost.PNG" width = "850">

#### Once you open this up it will bring you to this site:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/LocalHost5000Site.PNG" width = "700">

#### This is where you can look at the Covid Data


## :bookmark_tabs: Explaing each API Endpoint
| Route | Explanation |
| ----- | ----------- |
|  '/'  | This is the base route of the API. |
| 'countries' | This route retrieves a list of countries from the database. It returns a JSON response containing the list of countries. |
| 'regions' | This route retrieves a list of WHO regions from the database. It returns a JSON response containing the list of regions.|
| 'deaths' | This route retrieves the total deaths for the given country, region, and/or year. It accepts the following query parameters: country, region, and year. If no parameters are provided, it returns the total deaths for all countries. It returns a JSON response containing the total deaths. |
| 'cases' | This route retrieves the total cases for the given country, region, and/or year. It accepts the same query parameters as the /deaths/ route (country, region, year). If no parameters are provided, it returns the total cases for all countries. It returns a JSON response containing the total cases.|
| 'maxdeaths' | This route retrieves the country with the maximum number of deaths. It returns a JSON response with the country name. |
| 'mindeaths' | This route retrieves the country with the minimum number of deaths. It returns a JSON response with the country name. |
| 'mostdeathsduring' | This route retrieves the country with the most deaths between the specified start and end dates. Accepts two query parameters: start_date and end_date (both in the format "year-month-day"). It returns a JSON response with the country name and the number of deaths. |
| 'leastdeathsduring' | This route retrieves the country with the least deaths between the specified start and end dates. Accepts two query parameters: start_date and end_date (both in the format "year-month-day"). It returns a JSON response with the country name and the number of deaths. |
| 'average_deaths' | This route calculates the average number of deaths between all countries. It returns a JSON response with the average number of deaths. |

## :fountain_pen: Implementation
#### Importing- The code imports modules such as FastAPI, csv, uvicorn, etc.
#### Loading Covid Data- The code opens the data.csv file and reads its contents using a CSV reader.
#### Data Processing Functions
 - get_countries(): Retrieves a list of countries from the data.
 - get_regions(): Retrieves a list of WHO regions from the data.
 - get_total_deaths(): Calculates the total deaths based on provided country, region, and year parameters.
 - get_total_cases(): Calculates the total cases based on provided country, region, and year parameters.
#### CORS Middleware- The code adds CORS middleware to allow cross-origin requests.
#### Running the Application- The code uses uvicorn to run the FastAPI application on the specified host and port.

## :heavy_exclamation_mark: Challenges Faced
#### The main challenge I faced is lack of knowledge on this assignment. The day that we went over this assignment I had missed classed because I was sick. Because of this it was difficult at first to get a good understanding on what I was doing. Luckily I was able to obtain some help from some classmates to get me started.

## :camera: Output Photos
### There is nothing else past the output photos
### 	:world_map: Countries
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/Countries.PNG" width = "750">

### :earth_africa: Regions
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/Regions.PNG" width = "750">

### :skull: Deaths
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/Deaths.PNG" width = "750">

### :bar_chart: Cases
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/Cases.PNG" width = "750">

### :skull_and_crossbones: Max Deaths
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/MaxDeaths.PNG" width = "750">

### :knife: Min Deaths
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/MinDeaths.PNG" width = "750">

### :chart_with_upwards_trend: Most Deaths During
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/MostDeaths.PNG" width = "750">

### :chart_with_downwards_trend: Least Deaths During
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/LeastDeaths.PNG" width = "750">

### 	:imp: Average Deaths
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A08/AvgDeaths.PNG" width = "750">
