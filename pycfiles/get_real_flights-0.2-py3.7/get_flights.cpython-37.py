# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\src\get_flights.py
# Compiled at: 2019-02-03 20:53:18
# Size of source mod 2**32: 649 bytes
from collections import defaultdict
import json, random

def get_flights(total):
    with open('data/output.json', 'r') as (file):
        items = json.loads(file.read())
    flights = defaultdict(list)
    callsigns = []
    for callsign in items:
        callsigns.append(callsign)

    random_callsigns = random.sample(callsigns, len(callsigns))
    for x in range(0, total):
        flights[random_callsigns[x]].append(items[random_callsigns[x]])

    return flights