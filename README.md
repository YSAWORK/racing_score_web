# FLASK application "Web racing report" (WRR)
## Description
[**WRR**](#flask-application-web-racing-report-wrr) processes results of Racing in keys of drivers\`s list, general score and drivers`s personals results.
Using log files with results of racings WRR makes table with results.<br>
WRR is able to filter errors which consist with wrong or invalid input data.

## Installation and Setup
+ Requirements
+ Python 3.8+
+ Flask

### Install Dependencies
```pip install -r requirements.txt```
### Run the Application
```python racing_report/main_public.py```
## API Routes
### Main Page
#### GET /
Returns the text `Main page`.
### Race Results
Returns a page with race results sorted by time and drivers`s positions.
#### Parameters:
order (optional, default `desc`) — sorting order (`asc` or `desc`).
### Drivers Information
#### GET / drivers
Returns a page with a list of drivers.
#### Parameters:
order (optional, default `desc`) — sorting order by name (`asc` or `desc`).
### Driver Information
#### GET / drivers ?driver_id=...
Returns information about a specific driver.
#### Parameters:
`driver_id` - `driver_abbr` is the abbreviation of driver which are given in the first column of drivers\`s table

## Configuration
The configuration is loaded from the config module. Main parameters:
+ `BASE_DIR` — path to templates and static files.
+ `debug` — debug mode.
+ `passthrough_errors`, `use_debugger`, `use_reloader` — Flask settings.

## Testing
### Running Tests
To run the test suite, use:
```commandline
$ pytest
```
### Test Details
The test suite includes:
+ Main Page Test: Ensures the main page loads correctly.
+ Race Results Tests:
  - Validates sorting order (asc and desc).
  - Ensures invalid parameters return appropriate errors.
+ Driver Information Tests:
  - Checks retrieval of all drivers.
  - Tests retrieval of a specific driver by ID.
  - Verifies handling of incorrect data inputs.

The tests use pytest, BeautifulSoup for HTML parsing, and pytest-mock for mocking dependencies.<br>
Ensure all tests pass before deploying changes.

## License
BSL-1.0

## Developers
Project author: FoxmindEd<br>
Project developer: Stanislav Yena
