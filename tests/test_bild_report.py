import datetime, pytest, os
import racing_report as code

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def test_get_data():
    with (open(f'{BASE_DIR}/log_data/abbreviations.txt') as drivers,
          open(f'{BASE_DIR}/log_data/start.log') as start,
          open(f'{BASE_DIR}/log_data/end.log') as end):
          assert code.get_data() == (drivers.read().splitlines(),
                                     start.read().splitlines(),
                                     end.read().splitlines())


@pytest.mark.parametrize('time_info, errors, result', [
    (['SVF2018-05-24_12:02:58.917',
      'NHR2018-05-24_12:02:49.914',
      'FAM 2018-05-24_12:13:04.512', # fail (add to errors)
      ''], # fail (ignore)
     [],
     (({'SVF' : datetime.datetime.fromisoformat('2018-05-24T12:02:58.917'),
        'NHR' : datetime.datetime.fromisoformat('2018-05-24T12:02:49.914')}),
     ['FAM 2018-05-24_12:13:04.512 not included in results -- wrong data format in line 3 of resource file.'])),])
def test_get_datetime_info(time_info, errors, result):
    assert code.get_datetime_info(time_info, errors) == result


@pytest.mark.parametrize('time_info, errors', [
    (('SVF2018-05-24_12:02:58.917',), [],),
    (123,[],),
    ({'SVF' : '2018-05-24_12:02:58.917',},[],)])
def test_get_datetime_info_failtype(time_info, errors):
    with pytest.raises(TypeError):
        code.get_datetime_info(time_info, errors)


@pytest.mark.parametrize('drivers_info, start_data, end_data, drivers_data, error_list', [
    (['SVF_Sebastian Vettel_FERRARI',
      'DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER',
      'BRT_Brendon Hartley_SCUDERIA TORO ROSSO HONDA',
      ' ',
      'FAM 2018-05-24_12:13:04.512'],

     ['SVF2018-05-24_12:02:58.917',
      'DRR2018-05-24_12:14:12.054',
      'BHS2018-05-24_12:14:51.985'],

     ['SVF2018-05-24_12:04:03.332',
      'DRR2018-05-24_12:11:24.067',
      'BHS2018-05-24_12:16:05.164'],

     [('SVF',
       'Sebastian Vettel',
       'FERRARI',
       {'SVF' : (datetime.datetime.fromisoformat('2018-05-24T12:02:58.917'),
                 datetime.datetime.fromisoformat('2018-05-24T12:04:03.332'))}),
      ('DRR',
       'Daniel Ricciardo',
       'RED BULL RACING TAG HEUER',
       {'DRR' : (datetime.datetime.fromisoformat('2018-05-24T12:14:12.054'),
                 datetime.datetime.fromisoformat('2018-05-24T12:11:24.067'))}),],

     ['Brendon Hartley (BRT) hasn`t enough data. Not included in results', 'FAM 2018-05-24_12:13:04.512 not included in results -- wrong data format in line 5 of resource file.']),])
def test_get_drivers_list(drivers_info, start_data, end_data, drivers_data, error_list):
    drivers_list = []
    for data in drivers_data:
        object_t = code.Drivers(abbr=data[0],
                                name=data[1],
                                team=data[2],
                                start_time=data[3][data[0]][0],
                                end_time=data[3][data[0]][1])
        object_t.time = object_t.end_time - object_t.start_time
        if int(object_t.time.total_seconds()) < 0:
            object_t.error = 'incorrect data'
        drivers_list.append(object_t)
    assert code.get_drivers_list(drivers_info, start_data, end_data) == (drivers_list, error_list)


@pytest.mark.parametrize('order, attr', [
    ('dsc', 'name'),
    ('asc', 'game'),
    (4, 'name'),
    ('asc', ['name',]),])
def test_get_list_info_failvalue(order, attr):
    with pytest.raises(ValueError):
        code.get_list_info(order, attr)
