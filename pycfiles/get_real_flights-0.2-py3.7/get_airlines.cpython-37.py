# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\src\get_airlines.py
# Compiled at: 2019-02-03 20:20:25
# Size of source mod 2**32: 503 bytes
import flightradar24
from collections import defaultdict
fr = flightradar24.Api()
airlines = fr.get_airlines()

def get_airlines():
    output = list()
    string = ''
    for airline in airlines['rows']:
        output.append((airline['ICAO'], airline['Name'].replace('-', '')))

    for item in output:
        string += '{icao} {name} - Unknow\r'.format(icao=(item[0]), name=(item[1]))

    return output