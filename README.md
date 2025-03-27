![Screenshot](media/racing_flag.jpg)

# FLASK application "Web racing report" (WRR)
## Description
[**WRR**](#flask-application-web-racing-report-wrr) processes results of Racing in keys of drivers\`s list, general score and drivers`s personals results.
Using log files with results of racings WRR makes table with results.

WRR is able to filter errors which consist with wrong or invalid input data.
## How to use
### Get the list of drivers
Via the path ```\drivers``` WRR print the list of drivers and there results of racing.
### Get info about driver
Via the path ```\drivers?driver_id=<driver_abbr>``` WRR print info about driver`s result of racing.
> ```driver_abbr``` is the abbreviation of driver which are given in the first column of drivers\`s table.

You also can get info about driver via the link in [drivers\`s results table](#get-the-list-of-drivers)
### Get results of racing
Via the path ```\report``` WRR print the results of racing.<br/>Also, you can set the order od drivers\`s ranking (from the fastest to lowest and reversed).<br/>It`s controlled by the parameters ```desc```(fastest to lowest) / ```asc```(lowest to fastest).

Default value - ```desc```

Via path ```\report?order=asc>``` you can change this parameter.
## Tools
Used tools specified in [requirements.txt](requirements.txt)