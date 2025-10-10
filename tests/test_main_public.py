###### import tools ######
from datetime import datetime
import pytest
from bs4 import BeautifulSoup
import racing_report
from racing_report import Drivers



# create a test client using the Flask application configured for testing
@pytest.fixture
def client():
    """ Fixture to create a test client for the Flask application. """
    with racing_report.app.test_client() as client:
        yield client


###### test main page ######
def test_main_page(client):
    """ Test the main page of the application. """
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Main page"


###### test func 'racing' ######
#----- test sorting by order DESC -----#
def test_racing_valid_order_desc(client):
    """ Test the racing report page with valid 'desc' order parameter. """
    response = client.get("/report?order=desc")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    positions = []
    times = []
    for position in soup.find_all("td", class_="Position"):
        positions.append(int(position.contents[2].strip()))
    for time in soup.find_all("td", class_="Time"):
        times.append(datetime.strptime(time.contents[2].strip(), "%H:%M:%S.%f").time())
    assert positions == sorted(positions)
    assert times == sorted(times)

#----- test sorting by order ASC -----#
def test_racing_report_order_asc(client):
    """ Test the racing report page with valid 'asc' order parameter. """
    response = client.get("/report?order=asc")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    positions = []
    times = []
    for position in soup.find_all("td", class_="Position"):
        positions.append(int(position.contents[2].strip()))
    for time in soup.find_all("td", class_="Time"):
        times.append(datetime.strptime(time.contents[2].strip(), "%H:%M:%S.%f").time())
    assert positions == list(reversed(sorted(positions)))
    assert times == list(reversed(sorted(times)))

#----- test with different order`s data -----#
def test_racing_function_invalid_sorted(client, mocker):
    """ Test the racing report page with various 'order' parameters. """
    order_list = ('desc', "asc", '', "NOT_EXISTS_ORDER")
    for order in order_list:
        response = client.get(f"/report?order={order}")
        assert response.status_code == 200


###### test func 'drivers' ######
#----- test creating the drivers`s list -----#
def test_drivers_all(client, mocker):
    """ Test the drivers page displaying all drivers. """
    mock_data = (
        [
            Drivers(
                abbr="DRO",
                name="Driver_3",
                error=None,
                team="Any",
                start_time=None,
                end_time=None,
            ),
            Drivers(
                abbr="DRT",
                name="Driver_2",
                error=None,
                team="Any",
                start_time=None,
                end_time=None,
            ),
            Drivers(
                abbr="DRR",
                name="Driver_1",
                error=None,
                team="Any",
                start_time=None,
                end_time=None,
            ),
        ],
        [],
    )
    mocker.patch("racing_report.main_public.get_list_info", return_value=mock_data)
    response = client.get("/drivers")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    test_result = [driver.name for driver in mock_data[0]]
    assert test_result == [x.text.strip() for x in soup.find_all(class_="Name")]


#----- test raising exceptions in func 'drivers' with invalid input data -----#
def test_drivers_all_invalid_data(client):
    """ Test the drivers page with invalid data causing TypeError. """
    with pytest.raises(TypeError):
        mock_data = (
            [
                Drivers(
                    abbr="DRO",
                    error=None,
                    team="Any",
                    start_time=None,
                    end_time=None,
                ),
                Drivers(
                    abbr="DRT",
                    name="Driver_2",
                    age=23,
                    error=None,
                    team="Any",
                    start_time=None,
                    end_time=None,
                ),
            ],
            [],
        )

#----- test getting info about driver -----#
def test_drivers_one(client, mocker):
    """ Test the drivers page displaying information about a specific driver. """
    mock_data = Drivers(
        abbr="DRT",
        name="Driver_2",
        error=None,
        team="Any",
        start_time=None,
        end_time=None,
    )
    mocker.patch("racing_report.main_public.get_driver_info", return_value=mock_data)
    response = client.get(f"/drivers?driver_id={mock_data.abbr}")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    assert mock_data.abbr in [i.strip() for i in soup.find(class_="Code").contents]

#----- test with different drivers`s id`s data -----#
def test_drivers_one_driver_id(client, mocker):
    """ Test the drivers page with various 'driver_id' parameters. """
    mock_data = Drivers(
        abbr="DRT",
        name="Driver_2",
        error=None,
        team="Any",
        start_time=None,
        end_time=None,
    )
    driver_id_list = (mock_data.abbr, "", "NOT_EXISTS_DRIVER")
    mocker.patch("racing_report.main_public.get_driver_info", return_value=mock_data)
    for id_item in driver_id_list:
        response = client.get(f"/drivers?driver_id={id_item}")
        assert response.status_code == 200
