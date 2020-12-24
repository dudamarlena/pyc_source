# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/ponyexpress/couch_sync.py
# Compiled at: 2011-09-15 19:23:11
"""Command-line tool to sync up the couchdb views

Usage::

                $ python -m ponyexpress.couch_sync

"""
import sys, manage
if __name__ == '__main__':
    outfile = sys.stdout
    outfile.write(manage.couch_sync())