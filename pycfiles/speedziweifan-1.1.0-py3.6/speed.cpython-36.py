# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\speed.py
# Compiled at: 2018-06-19 23:52:41
# Size of source mod 2**32: 551 bytes


def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    else:
        if ':' in time_string:
            splitter = ':'
        else:
            return time_string
    mins, secs = time_string.split(splitter)
    return mins + '.' + secs


def get_coach_data(filename):
    try:
        with open(filename) as (f):
            data = f.readline()
        temp = data.strip().split(',')
        return {'Name':temp.pop(0),  'DOB':temp.pop(0), 
         'Times':str(sorted(set([sanitize(t) for t in temp]))[0:3])}
    except IOError as ioerr:
        print('File error: ' + str(ioerr))
        return