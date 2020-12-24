# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/wheel_to_db.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 2212 bytes
import statistics, os, glob, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.mnemonics as mn, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.sql_interface as sql, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.csv_to_AstropyTable as apt
from jwql.utils.utils import get_config, filename_parser
from astropy.table import Table, Column
from jwql.instrument_monitors.nirspec_monitors.data_trending.utils.process_data import wheelpos_routine
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
directory = os.path.join(get_config()['outputs'], 'nirspec_data_trending', 'nirspec_wheels', '*.CSV')
filenames = glob.glob(directory)

def process_file(conn, path):
    m_raw_data = apt.mnemonics(path)
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