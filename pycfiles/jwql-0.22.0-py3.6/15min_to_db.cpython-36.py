# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/15min_to_db.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 3223 bytes
import statistics, os, glob, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.mnemonics as mn, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.sql_interface as sql, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.csv_to_AstropyTable as apt
from jwql.utils.utils import get_config, filename_parser
from astropy.table import Table, Column
from jwql.instrument_monitors.nirspec_monitors.data_trending.utils.process_data import once_a_day_routine
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
directory = os.path.join(get_config()['outputs'], 'nirspec_data_trending', 'nirspec_new_15min', '*.CSV')
filenames = glob.glob(directory)

def process_file(conn, path):
    """Parse CSV file, process data within and put to DB
    Parameters
    ----------
    conn : DBobject
        Connection object to temporary database
    path : str
        defines path to the files
    """
    m_raw_data = apt.mnemonics(path)
    returndata = once_a_day_routine(m_raw_data)
    for key, value in returndata.items():
        m = m_raw_data.mnemonic(key)
        length = len(value)
        mean = statistics.mean(value)
        deviation = statistics.stdev(value)
        dataset = (float(m.meta['start']), float(m.meta['end']), length, mean, deviation)
        sql.add_data(conn, key, dataset)

    for identifier in mn.mnemSet_15min:
        m = m_raw_data.mnemonic(identifier)
        temp = []
        for element in m:
            temp.append(float(element['value']))

        if len(temp) > 2:
            length = len(temp)
            mean = statistics.mean(temp)
            deviation = statistics.stdev(temp)
            dataset = (
             float(m.meta['start']), float(m.meta['end']), length, mean, deviation)
            sql.add_data(conn, identifier, dataset)
        else:
            if len(temp) == 2:
                dataset = (
                 float(element['time']), float(element['time']), 1, temp[0], 0)
                sql.add_data(conn, identifier, dataset)
            else:
                print('No data for {}'.format(identifier))
                print(temp)
        del temp


def main():
    DATABASE_LOCATION = os.path.join(get_config()['jwql_dir'], 'database')
    DATABASE_FILE = os.path.join(DATABASE_LOCATION, 'nirspec_database.db')
    conn = sql.create_connection(DATABASE_FILE)
    for path in filenames:
        process_file(conn, path)

    sql.close_connection(conn)
    print('done')


if __name__ == '__main__':
    main()