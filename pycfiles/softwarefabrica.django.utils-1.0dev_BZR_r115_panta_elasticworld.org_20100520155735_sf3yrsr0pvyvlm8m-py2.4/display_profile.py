# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/display_profile.py
# Compiled at: 2009-11-08 05:29:18
import sys
from pstats import Stats

def main():
    stats = Stats(sys.argv[1])
    stats.sort_stats('time', 'cumulative').print_stats('.py')


if __name__ == '__main__':
    main()