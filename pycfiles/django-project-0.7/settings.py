# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: settings.py
# Compiled at: 2011-06-19 18:28:03
import sys

def settings_required():
    settings_set = False
    for k in sys.argv:
        if k.split('=')[0] == '--settings':
            settings_set = True

    if not settings_set:
        sys.stderr.write('There is no settings specified (default was turned off)\nPlease, specify --settings parameter.')
        sys.exit(1)


settings_required()