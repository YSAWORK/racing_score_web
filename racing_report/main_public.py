from flask import Flask, render_template, request
import os, sys
sys.path.append("racing_reports_2018")
from racing_report.bild_report import get_list_info

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

app = Flask(__name__,
            template_folder=f'{BASE_DIR}/templates',
            static_folder=f'{BASE_DIR}/static')

@app.route("/")
def main():
    return "Main page"

# page with main racing results
@app.route("/report")
def racing():
    order = request.args.get('order', default='desc', type=str)
    racing_info = get_list_info(order, 'time')
    return render_template('racing.html',
                           data=racing_info[0],
                           errors = racing_info[1])

# page with info about drivers
@app.route("/drivers")
def drivers():
    order = request.args.get('order', default='desc', type=str)
    driver_id = request.args.get('driver_id', type=str)
# info about one driver
    if driver_id:
        return render_template('driver_info.html', driver=get_driver_info(driver_id))
# info about all drivers
    else:
        racing_info = get_list_info(order, 'name')
        wrong_data = list(filter(lambda el: el.error == 'incorrect data', racing_info[0]))
        return render_template('drivers.html',
                               data=racing_info[0],
                               wrong_data = wrong_data,
                               errors = racing_info[1])

if __name__ == '__main__':
    import sys
    sys.path.append("racing_report")
    from racing_report.bild_report import get_list_info, get_driver_info
    app.run(debug=True)
