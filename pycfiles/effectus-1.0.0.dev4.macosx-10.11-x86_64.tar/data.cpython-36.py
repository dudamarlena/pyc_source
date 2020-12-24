# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminweb/22_Projekte/Pareto/python/venv/lib/python3.6/site-packages/effectus/data.py
# Compiled at: 2017-01-30 19:08:29
# Size of source mod 2**32: 9586 bytes
"""Example data sets from real life."""
import csv
from pkg_resources import resource_filename
from effectus.helpers import get_values, unfold_values

def get_data(filepath):
    """Read and unfold value-frequency mappings from file.

    Args:
        filepath: File path to source file.

    Returns:
        A list with unfolded values.
    """
    with open(resource_filename(__name__, filepath), 'r') as (csvfile):
        reader = csv.reader(csvfile)
        vafreqs = get_values(reader)
        return unfold_values(vafreqs)


MISSING_TEETH = get_data('csv/missing_teeth.csv')
BELLS = tuple(get_data('csv/bells.csv'))
WOMEN_INTERCOURSE = tuple(get_data('csv/women_intercourse.csv'))
BOXOFFICE = tuple(get_data('csv/boxoffice.csv'))
WKZS = tuple(get_data('csv/wkzs.csv'))
OIL_RESERVES = (55.0, 172.2, 10.8, 2.4, 13.0, 2.3, 8.0, 1.4, 0.7, 300.9, 0.5, 7.0,
                0.6, 0.6, 30.0, 8.0, 0.6, 102.4, 0.6, 2.8, 0.6, 2.1, 157.8, 143.1,
                101.5, 5.3, 25.7, 266.6, 2.5, 97.8, 3.0, 0.2, 12.2, 12.7, 1.5, 1.6,
                3.5, 1.1, 2.0, 48.4, 37.1, 3.5, 1.5, 0.4, 3.7, 4.0, 1.1, 18.5, 5.7,
                3.6, 3.6, 0.4, 4.4, 1.3)
OIL_CONSUMPTION = (19396, 2322, 1926, 23644, 679, 3157, 368, 331, 253, 243, 38, 678,
                   1336, 7083, 263, 99, 145, 661, 88, 200, 165, 177, 1606, 2338,
                   303, 154, 143, 1262, 271, 54, 835, 234, 546, 243, 191, 3113, 78,
                   1226, 299, 228, 835, 146, 183, 1559, 59, 677, 18380, 1947, 239,
                   531, 324, 3895, 901, 1733, 9570, 422, 824, 649, 1993, 3888, 1006,
                   112, 11968, 368, 4159, 1628, 4150, 831, 159, 517, 399, 1339, 2575,
                   1031, 1344, 422, 436, 32444)
CO2 = (5485.7, 532.5, 474.2, 190.0, 487.8, 90.1, 97.3, 37.1, 50.8, 26.7, 169.2, 227.7,
       62.8, 32.0, 56.3, 111.5, 45.2, 98.6, 37.6, 41.3, 309.4, 753.6, 73.9, 44.2,
       38.6, 341.5, 184.8, 11.2, 210.1, 36.7, 295.8, 52.5, 70.7, 1483.2, 31.1, 291.7,
       47.8, 39.1, 336.3, 92.6, 195.1, 436.9, 115.4, 225.1, 630.2, 74.4, 107.9, 111.1,
       624.5, 264.7, 355.1, 137.1, 212.1, 436.5, 416.2, 400.2, 72.9, 9153.9, 91.2,
       2218.4, 611.4, 1207.8, 246.9, 35.7, 179.5, 106.5, 205.0, 648.7, 268.5, 295.9,
       169.0, 155.2)
SP500 = tuple(get_data('csv/sp500.csv'))
GDP = tuple(get_data('csv/gdp.csv'))
EURO_COINS = (327.34000000000003, 502.28000000000003, 975.45, 1414.8000000000002, 2155.6,
              2950.5, 6977, 11630)
EURO_BANKNOTES = (9025, 23870, 71800, 461550, 243300, 46800, 270000)
HOPEI_RAIN = tuple(get_data('csv/hopei_rain.csv'))
HOPEI_SUN = tuple(get_data('csv/hopei_sun.csv'))
GERMAN_RIVERS = (1236, 1091, 866, 744, 524, 371, 300, 290, 256, 220, 219, 208, 188,
                 185, 182, 176, 169, 166, 165, 153, 153, 150, 143, 128, 124, 121,
                 118, 114, 107, 105, 105, 102, 101, 97, 97, 92, 91, 90, 80, 75, 73,
                 72, 72, 70, 68, 68, 67, 67, 65, 67, 63, 63, 62, 62, 61, 60, 60,
                 59, 59, 58, 57, 57, 57, 57, 57, 56, 55, 54, 52, 52, 52, 51, 50,
                 49, 49, 49, 48, 47, 47, 46, 45, 45, 45, 45, 45, 44, 43, 42, 42,
                 40, 40, 40, 40, 40, 40, 40, 39, 39, 38, 37, 37, 37, 36, 35, 35,
                 35, 35, 35, 35, 34, 34, 34, 34, 33, 33, 33, 33, 32, 31, 31, 31,
                 31, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 29, 29, 29, 28, 28,
                 28, 28, 28, 28, 27, 27, 27, 27, 27, 26, 26, 26, 25, 25, 25, 25,
                 25, 25, 25, 25, 24, 24, 24, 24, 24, 23, 23, 23, 23, 23, 22, 22,
                 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 21, 21,
                 21, 21, 21, 20, 20, 20, 20, 20, 19, 18, 18, 18, 18, 18, 18, 18,
                 18, 17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16,
                 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14,
                 14, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 12,
                 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 10,
                 10, 10)
GERMAN_MOTORWAYS = tuple(get_data('csv/german_motorways.csv'))
GERMAN_HIGHWAYS = tuple(get_data('csv/german_highways.csv'))
COUNTRIES_AREA = tuple(get_data('csv/countries_area.csv'))
COUNTRIES_POPULATION = tuple(get_data('csv/countries_population.csv'))
CHEESE = tuple(get_data('csv/cheese.csv'))