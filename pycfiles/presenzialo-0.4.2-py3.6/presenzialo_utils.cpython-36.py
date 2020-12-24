# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/presenzialo_utils.py
# Compiled at: 2020-01-24 06:11:30
# Size of source mod 2**32: 511 bytes
import json, datetime

def convert2time(minutes):
    t = datetime.datetime(1, 1, 1, 0, 0) + datetime.timedelta(minutes=minutes)
    return t.time()


def convert2date(s):
    year = int(s[0:4])
    month = int(s[4:6])
    day = int(s[6:8])
    return datetime.datetime(year, month, day)


def write_data(data, file):
    with open(file, 'w') as (fp):
        json.dump(data, fp, sort_keys=True, indent=4)


def read_data(file):
    with open(file, 'r') as (fp):
        data = json.load(fp)
    return data