# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/aegis_model/main/run.py
# Compiled at: 2020-01-27 21:51:56
# Size of source mod 2**32: 443 bytes
from wows_stats.model.winrate_model import build_winrate_model
from aegis_data.api.wows_api import WowsAPIRequest
START_DATE = '2019-09-18'
CONFIG_FILE = ''

def database_update():
    WowsAPIRequest(CONFIG_FILE).request_historical_stats_all_accounts_last_month(start_date=START_DATE)


def model_update():
    build_winrate_model()


if __name__ == '__main__':
    database_update()
    model_update()
    print('Main function finished!')