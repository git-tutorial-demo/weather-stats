"""weather_stats.py - summarises a year of daily weather per city, in the terminal and as an HTML report.

    python weather_stats.py                 all cities
    python weather_stats.py London Mumbai   only these cities
    python weather_stats.py --sort rain     wettest city first (also: mean, hottest, coldest, rainy)

Reads data/daily_weather.csv (made by get_data.py). Writes output/report.html and output/summary.json:
generated files, which are never committed (anyone can regenerate them by running this script).
Standard library only: no packages to install.
"""
import csv
import html
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "daily_weather.csv"
OUTPUT = HERE / "output"
SORT_KEYS = {"mean": "mean_c", "hottest": "hottest_c", "coldest": "coldest_c",
             "rainy": "rainy_days", "rain": "rain_total_mm"}


def load(path=DATA):
    """Returns {city: [row, ...]} with numbers converted to float."""
    by_city = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in ("t_min", "t_max", "rain_mm"):
                row[key] = float(row[key])
            by_city[row["city"]].append(row)
    return dict(by_city)


def summarise(rows):
    """Statistics for one city's rows."""
    hottest = max(rows, key=lambda r: r["t_max"])
    coldest = min(rows, key=lambda r: r["t_min"])
    wet = [r for r in rows if r["rain_mm"] >= 1.0]
    return {
        "days": len(rows),
        "mean_c": round(sum((r["t_min"] + r["t_max"]) / 2 for r in rows) / len(rows), 1),
        "hottest_c": hottest["t_max"], "hottest_day": hottest["date"],
        "coldest_c": coldest["t_min"], "coldest_day": coldest["date"],
        "rainy_days": len(wet),
        "rain_total_mm": round(sum(r["rain_mm"] for r in rows)),
    }


def resolve(names, known):
    """City names as the user typed them -> (names as in the data, names not found); any upper/lower case."""
    by_lower = {k.lower(): k for k in known}
    found = [by_lower[n.lower()] for n in names if n.lower() in by_lower]
    return found, [n for n in names if n.lower() not in by_lower]


def sort_stats(stats, key):
    """The same statistics, largest value of SORT_KEYS[key] first."""
    return dict(sorted(stats.items(), key=lambda item: item[1][SORT_KEYS[key]], reverse=True))


def table(stats):
    lines = [f"{'City':<10} {'Mean':>6} {'Hottest':>8} {'Coldest':>8} {'Rainy days':>11} {'Rain':>8}"]
    for city, s in stats.items():
        lines.append(f"{city:<10} {s['mean_c']:>5.1f}C {s['hottest_c']:>7.1f}C {s['coldest_c']:>7.1f}C "
                     f"{s['rainy_days']:>11} {s['rain_total_mm']:>6} mm")
    return "\n".join(lines)


def report_html(stats):
    rows = "\n".join(
        f"<tr><td>{html.escape(c)}</td><td>{s['mean_c']:.1f}</td><td>{s['hottest_c']:.1f} ({s['hottest_day']})</td>"
        f"<td>{s['coldest_c']:.1f} ({s['coldest_day']})</td><td>{s['rainy_days']}</td><td>{s['rain_total_mm']}</td></tr>"
        for c, s in stats.items())
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Weather Stats report</title>
<style>body{{font-family:system-ui,sans-serif;margin:2rem}}td,th{{padding:.3rem .8rem;text-align:right}}
td:first-child,th:first-child{{text-align:left}}</style></head>
<body><h1>Weather in 2025</h1>
<table><tr><th>City</th><th>Mean &deg;C</th><th>Hottest &deg;C</th><th>Coldest &deg;C</th>
<th>Rainy days</th><th>Rain mm</th></tr>
{rows}
</table></body></html>
"""


def main(argv):
    if not DATA.exists():
        sys.exit("No data yet: run  python get_data.py  first.")
    sort_key = None
    if "--sort" in argv:
        i = argv.index("--sort")
        if i + 1 >= len(argv) or argv[i + 1] not in SORT_KEYS:
            sys.exit(f"--sort needs one of: {', '.join(SORT_KEYS)}")
        sort_key = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    data = load()
    cities, unknown = resolve(argv, data) if argv else (sorted(data), [])
    if unknown:
        sys.exit(f"Unknown city: {', '.join(unknown)}. Known: {', '.join(sorted(data))}")
    stats = {c: summarise(data[c]) for c in cities}
    if sort_key:
        stats = sort_stats(stats, sort_key)
    print(table(stats))
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "summary.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    (OUTPUT / "report.html").write_text(report_html(stats), encoding="utf-8")
    print(f"\nReport: output/report.html  (summary: output/summary.json)")


if __name__ == "__main__":
    main(sys.argv[1:])
