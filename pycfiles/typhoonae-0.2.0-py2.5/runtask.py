# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/runtask.py
# Compiled at: 2010-12-12 04:36:57
"""Simple console script to run a scheduled task."""
import sys, urllib2

def main():
    url = sys.argv[1]
    req = urllib2.Request(url=url, headers={'X-AppEngine-Cron': 'true'})
    response = urllib2.urlopen(req)
    assert response.code == 200