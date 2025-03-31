import config
from flask import Flask, render_template, request
from functools import lru_cache
from racing_report.bild_report import get_list_info, get_driver_info

app = Flask(
    __name__,
    template_folder=f"{config.BASE_DIR}/templates",
    static_folder=f"{config.BASE_DIR}/static",
)

###### main page ######
@app.route("/")
@lru_cache(maxsize=100)
def main():
    return "Main page"


###### page with main racing results ######
@app.route("/report")
def racing():
    order = request.args.get("order", default="desc", type=str)
    if order not in ("desc", "asc", ""):
        return f"Wrong parameter 'order' -> '{order}'. Choose from between 'desc' and 'asc' (for example: '/drivers?order=asc')"
    else:
        racing_info = get_list_info(order, "time")
        return render_template(
            "racing.html", data=racing_info[0], errors=racing_info[1]
        )


###### page with info about drivers ######
@app.route("/drivers")
def drivers():
    @lru_cache(maxsize=100)
    def wrong_data_func(data):
        return filter(lambda el: el.error == "incorrect data", data)

    order = request.args.get("order", default="desc", type=str)
    driver_id = request.args.get("driver_id", type=str)
    if order not in ("desc", "asc"):
        return f"Wrong parameter 'order' -> '{order}'. Choose from between 'desc' and 'asc' (for example: '/drivers?order=asc')"
    else:
        # info about one driver
        if driver_id:
            try:
                return render_template(
                    "driver_info.html", driver=get_driver_info(driver_id)
                )
            except ValueError:
                return f"Wrong parameter 'driver_id' -> '{driver_id}'."
                # info about all drivers
        else:
            racing_info = get_list_info(order, "name")
            wrong_data = wrong_data_func(tuple(racing_info[0]))
            return render_template(
                "drivers.html",
                data=racing_info[0],
                wrong_data=wrong_data,
                errors=racing_info[1],
            )


if __name__ == "__main__":  # pragma: no cover
    app.run(
        debug=config.debug,
        passthrough_errors=config.passthrough_errors,
        use_debugger=config.use_debugger,
        use_reloader=config.use_reloader,
    )
