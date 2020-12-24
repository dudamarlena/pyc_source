# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kpages/kpages_web.py
# Compiled at: 2019-01-22 20:15:37
"""
    author comger@gmail.com
"""
import sys, json
from datetime import datetime
from pprint import pprint
from kpages import run

def callback(app):
    print ('Start time: {0}').format(datetime.now().isoformat(' '))
    print 'Config Params'
    for k in sorted(app.settings.keys()):
        if k.startswith('__'):
            continue
        print ('  {0:<40} : {1}').format(k, app.settings[k])

    print 'UI Modules'
    for k, v in app.uimodules.items():
        print (' {0:<20} :{1}').format(k, v.__doc__)

    print 'UI  Methods'
    for k, v in app.uimethods.items():
        print (' {0:<20} :{1}').format(k, v.__intro__)

    print 'Router Handlers'
    for h in app.handlers:
        print ('  {0:<50} : {1}').format(h[1], h[0])


if __name__ == '__main__':
    try:
        run(callback)
    except KeyboardInterrupt:
        print 'exit server '