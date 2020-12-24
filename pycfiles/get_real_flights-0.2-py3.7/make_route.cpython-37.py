# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\src\make_route.py
# Compiled at: 2019-02-03 20:53:18
# Size of source mod 2**32: 2008 bytes
import json
from src import AIRPORT_SETTINGS
from datetime import datetime
from src import get_metars
from collections import defaultdict

def make_route():
    items_list = defaultdict(list)
    output = defaultdict(list)
    with open('data/flight_radar.json', 'r') as (file):
        items_tap = json.loads(file.read())
    print('==========')
    for item in items_tap:
        items_list[item].append(items_tap[item])

    for item in items_list:
        if len(items_list[item][0]) != 0:
            dep_icao = items_list[item][0][0]['origin']
            arr_icao = items_list[item][0][0]['destination']
            dep_time = items_list[item][0][0]['dep_time']
            arr_time = items_list[item][0][0]['arr_time']
            aircraft = items_list[item][0][0]['aircraft']
            d_icao = ''
            a_icao = ''
            route = ''
            for key in dep_icao:
                d_icao = key

            for key in arr_icao:
                a_icao = key

            if d_icao != '':
                try:
                    route = AIRPORT_SETTINGS[d_icao][a_icao]['ROUTE']
                except:
                    print((d_icao, a_icao))

            dep_metar = get_metars.get_metar(d_icao)
            arr_metar = get_metars.get_metar(a_icao)
        if len(items_list[item][0]) != 0 and route != '':
            output[item].append({'origin':dep_icao, 
             'destination':arr_icao, 
             'aircraft':aircraft, 
             'dep_time':dep_time, 
             'arr_time':arr_time, 
             'route':route, 
             'dep_metar':dep_metar, 
             'arr_metar':arr_metar})

    with open('data/output.json', 'w') as (file):
        file.write(json.dumps(output, indent=4))