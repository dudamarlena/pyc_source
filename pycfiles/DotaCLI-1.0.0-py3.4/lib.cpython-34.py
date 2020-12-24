# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Diretide/lib.py
# Compiled at: 2015-09-16 18:25:08
# Size of source mod 2**32: 1777 bytes
"""
lib.py
"""
from string import printable as printable_chrs
from collections import namedtuple
from requests import get as re_get
from datetime import datetime
API_URL = 'http://dailydota2.com/match-api'
Match = namedtuple('Match', ['timediff', 'series_type', 'link', 'starttime',
 'status', 'starttime_unix', 'comment', 'viewers',
 'team1', 'team2', 'league'])

def get_url(url):
    return re_get(url).json()


def get_longest(matches):
    return max([max(len(x.team1['team_name']), len(x.team2['team_name'])) for x in matches])


def print_match(m, longest):
    """Do all the match info here"""
    print('=== {} (best of {}) ==='.format(m.league['name'], m.series_type))
    print('{[team_name]:<{width}} vs. {[team_name]:>{width}}'.format(m.team1, m.team2, width=longest))
    print(display_time(m))
    print()


def display_time(m):
    """Convert unix time to readable"""
    x = int(m.timediff)
    if x <= 0:
        return '***Currently Running***'
    return 'Time until: {}'.format(datetime.fromtimestamp(x).strftime('%H:%M:%S'))


def main(*args, **kwargs):
    """
    Main function
    Retrieves, forms data, and prints out information
    """
    print()
    data = get_url(API_URL)
    matches = [Match(**unpack) for unpack in data['matches']]
    longest = get_longest(matches)
    for match in matches:
        print_match(match, longest)


if __name__ == '__main__':
    main()