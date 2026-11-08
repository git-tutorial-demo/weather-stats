"""get_data.py - creates the data set that weather_stats.py analyses: data/daily_weather.csv.

    python get_data.py

A real project would download its data here (from a weather service, a public data portal or a URL in .env).
This starter project generates a realistic sample instead, so that it works offline and gives the same numbers on
every computer: one year (2025) of daily weather for four cities, about 1,460 rows and 50 KB.
Like a downloaded data set, data/ is never committed to Git: anyone can recreate it with this script.
"""
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
OUT = DATA / "daily_weather.csv"

# city: (mean temperature in C, half the summer-winter swing, chance of rain on a day, mean rain in mm on a wet day)
CITIES = {
    "New York": (13.0, 11.5, 0.33, 9.0),
    "London": (11.5, 6.5, 0.45, 4.5),
    "Mumbai": (27.5, 2.5, 0.30, 25.0),
    "Sydney": (18.5, -5.0, 0.30, 8.0),     # southern hemisphere: summer in January
}


def generate(seed=2026):
    rng = random.Random(seed)
    rows = []
    start = date(2025, 1, 1)
    for city, (mean, swing, p_rain, rain_mm) in CITIES.items():
        for d in range(365):
            day = start + timedelta(days=d)
            season = -math.cos(2 * math.pi * (d - 15) / 365)        # -1 in mid-January, +1 in mid-July
            if city == "Mumbai":                                     # the monsoon: June to September
                wet = 0.85 if 152 <= d <= 273 else 0.05
            else:
                wet = p_rain
            t_mean = mean + swing * season + rng.gauss(0, 2.5)
            spread = rng.uniform(4, 10)
            rain = round(rng.expovariate(1 / rain_mm), 1) if rng.random() < wet else 0.0
            rows.append({"date": day.isoformat(), "city": city,
                         "t_min": round(t_mean - spread / 2, 1), "t_max": round(t_mean + spread / 2, 1),
                         "rain_mm": rain})
    return rows


if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)
    rows = generate()
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "city", "t_min", "t_max", "rain_mm"])
        writer.writeheader()
        writer.writerows(rows)
    size = OUT.stat().st_size / 1000
    print(f"Wrote {len(rows)} rows for {len(CITIES)} cities to data/{OUT.name} ({size:.0f} KB)")
