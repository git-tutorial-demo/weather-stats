"""test_weather_stats.py - unit tests for weather_stats.py.

    python -m unittest -v
"""
import unittest

from weather_stats import report_html, resolve, sort_stats, summarise, table

ROWS = [
    {"date": "2025-01-01", "city": "Testville", "t_min": -2.0, "t_max": 4.0, "rain_mm": 0.0},
    {"date": "2025-07-01", "city": "Testville", "t_min": 18.0, "t_max": 30.0, "rain_mm": 12.5},
    {"date": "2025-07-02", "city": "Testville", "t_min": 17.0, "t_max": 27.0, "rain_mm": 0.4},
]


class SummariseTest(unittest.TestCase):
    def test_mean_is_the_average_of_daily_means(self):
        self.assertEqual(summarise(ROWS)["mean_c"], 15.7)

    def test_extremes_and_their_dates(self):
        s = summarise(ROWS)
        self.assertEqual((s["hottest_c"], s["hottest_day"]), (30.0, "2025-07-01"))
        self.assertEqual((s["coldest_c"], s["coldest_day"]), (-2.0, "2025-01-01"))

    def test_a_rainy_day_needs_at_least_1_mm(self):
        s = summarise(ROWS)
        self.assertEqual(s["rainy_days"], 1)
        self.assertEqual(s["rain_total_mm"], 13)


class OutputTest(unittest.TestCase):
    def test_table_and_report_name_every_city(self):
        stats = {"Testville": summarise(ROWS), "A<B": summarise(ROWS)}
        self.assertIn("Testville", table(stats))
        self.assertIn("A&lt;B", report_html(stats))      # city names are escaped in the HTML


class SortTest(unittest.TestCase):
    def test_sort_by_rain_puts_the_wettest_city_first(self):
        dry = [dict(r, rain_mm=0.0) for r in ROWS]
        stats = {"Dryville": summarise(dry), "Testville": summarise(ROWS)}
        self.assertEqual(list(sort_stats(stats, "rain")), ["Testville", "Dryville"])


class ResolveTest(unittest.TestCase):
    def test_city_names_match_in_any_case(self):
        self.assertEqual(resolve(["mumbai", "LONDON", "Paris"], ["London", "Mumbai"]), (["Mumbai", "London"], ["Paris"]))


if __name__ == "__main__":
    unittest.main()
