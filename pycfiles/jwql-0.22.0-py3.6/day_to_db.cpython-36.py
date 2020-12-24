# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/day_to_db.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 4184 bytes
import statistics, os, glob, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.mnemonics as mn, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.sql_interface as sql, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.csv_to_AstropyTable as apt
from jwql.utils.utils import get_config, filename_parser
from astropy.table import Table, Column
from jwql.instrument_monitors.nirspec_monitors.data_trending.utils.process_data import whole_day_routine, wheelpos_routine
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
directory = os.path.join(get_config()['outputs'], 'nirspec_data_trending', 'nirspec_more', '*.CSV')
filenames = glob.glob(directory)
test = 'FOFTLM2019073163845064.CSV'

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
    return_data, lamp_data = whole_day_routine(m_raw_data)
    FW, GWX, GWY = wheelpos_routine(m_raw_data)
    for key, values in FW.items():
        for data in values:
            sql.add_wheel_data(conn, 'INRSI_C_FWA_POSITION_{}'.format(key), data)

    for key, values in GWX.items():
        for data in values:
            sql.add_wheel_data(conn, 'INRSI_C_GWA_X_POSITION_{}'.format(key), data)

    for key, values in GWY.items():
        for data in values:
            sql.add_wheel_data(conn, 'INRSI_C_GWA_Y_POSITION_{}'.format(key), data)

    for key, value in return_data.items():
        m = m_raw_data.mnemonic(key)
        length = len(value)
        if length > 2:
            mean = statistics.mean(value)
            deviation = statistics.stdev(value)
            dataset = (float(m.meta['start']), float(m.meta['end']), length, mean, deviation)
            sql.add_data(conn, key, dataset)

    for identifier in mn.mnemSet_day:
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
            print('No data for {}'.format(identifier))
            print(temp)
        del temp

    for key, values in lamp_data.items():
        for data in values:
            dataset_volt = (
             data[0], data[1], data[5], data[6], data[7])
            dataset_curr = (data[0], data[1], data[2], data[3], data[4])
            sql.add_data(conn, 'LAMP_{}_VOLT'.format(key), dataset_volt)
            sql.add_data(conn, 'LAMP_{}_CURR'.format(key), dataset_curr)


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