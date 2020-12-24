# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\to_csv.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 1358 bytes
import csv, sys

def write_to_file(data, path, date_format='%Y-%m-%d'):
    """Export extracted fields to csv

    Appends .csv to path if missing and generates csv file in specified directory, if not then in root

    Parameters
    ----------
    data : dict
        Dictionary of extracted fields
    path : str
        directory to save generated csv file
    date_format : str
        Date format used in generated file

    Notes
    ----
    Do give file name to the function parameter path.
    """
    if path.endswith('.csv'):
        filename = path
    else:
        filename = path + '.csv'
    if sys.version_info[0] < 3:
        openfile = open(filename, 'wb')
    else:
        openfile = open(filename, 'w', newline='')
    with openfile as (csv_file):
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            first_row = []
            for k, v in line.items():
                first_row.append(k)

        writer.writerow(first_row)
        for line in data:
            csv_items = []
            for k, v in line.items():
                if not k.startswith('date'):
                    if k.endswith('date'):
                        v = v.strftime(date_format)
                    csv_items.append(v)

            writer.writerow(csv_items)