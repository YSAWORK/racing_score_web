import pytest
from bs4 import BeautifulSoup
import racing_report

@pytest.fixture
def client():
    with racing_report.app.test_client() as client:
        yield client


###### test main page ######
def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Main page"


###### test func 'racing' ######
def test_racing_valid_order_desc(client):
    response = client.get('/report?order=desc')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert str(1) in [i.strip() for i in soup.find('td', class_='Position').contents]

def test_racing_report_order_asc(client, mocker):
    mock_data = ([dict(position=3, name='Driver_3'),
       dict(position=2, name='Driver_2'),
       dict(position=1, name='Driver_1')], [])
    mocker.patch('racing_report.main_public.get_list_info', return_value=mock_data)
    response = client.get('/report?order=asc')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    result = list(sorted([item['position'] for item in mock_data[0]]))
    assert str(result[-1]) in [i.strip() for i in soup.find('td', class_='Position').contents]

def test_racing_function_invalid_sorted(client, mocker):
    response = client.get('/report?order=invalid')
    assert response.status_code == 500


###### test func 'drivers' ######
def test_drivers_all(client, mocker):
    mock_data = ([dict(abbr='DRO', name='Driver_3', error=None),
       dict(abbr='DRT', name='Driver_2', error=None),
       dict(abbr='DRR', name='Driver_1', error=None)], [])
    mocker.patch('racing_report.main_public.get_list_info', return_value=mock_data)
    response = client.get('/drivers')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    test_result = list(sorted([driver['name'] for driver in mock_data[0]]))[0]
    assert test_result in [i.strip() for i in soup.find('td', class_='Name').contents]

def test_drivers_one(client, mocker):
    mock_data = (dict(abbr='DRT', name='Driver_2', error=None), [])
    mocker.patch('racing_report.main_public.get_driver_info', return_value=mock_data)
    response = client.get(f'/drivers?driver_id={mock_data[0]['abbr']}')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert mock_data[0]['abbr'] in [i.strip() for i in soup.find('td', class_='Code').contents]
