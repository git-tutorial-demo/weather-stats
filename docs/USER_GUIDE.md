# Weather Stats User Guide

Version 1.0

Weather Stats summarises a year of daily weather for several cities: mean temperature, the hottest and the coldest
day, rainy days and total rain. It prints a table and writes an HTML report.

## Requirements

Python 3 on Windows, macOS or Linux. No packages to install.

## Install

Clone the repository and change into its folder:

    git clone https://github.com/YOUR-USERNAME/weather-stats.git
    cd weather-stats

## Get the data

    python get_data.py

This creates `data/daily_weather.csv`, one row per city and day.

## Run

    python weather_stats.py                  all cities
    python weather_stats.py London Mumbai    only these cities

The table appears in the terminal. The same numbers are saved in `output/report.html` (open it in a browser) and
`output/summary.json` (for other programs).

## Read the report

- **Mean** is the average of the daily mean temperatures, in degrees Celsius.
- **Hottest** and **Coldest** are the highest maximum and the lowest minimum of the year.
- A **rainy day** has at least 1 mm of rain.
- **Rain** is the total for the year, in millimetres.

## Troubleshooting

| Message | What to do |
|---|---|
| `No data yet: run  python get_data.py  first.` | Run `python get_data.py`, then try again |
| `Unknown city: ...` | Use one of the cities that the message lists, spelt exactly as shown |
| `python: command not found` | Type `python3` instead (macOS, Linux) |
