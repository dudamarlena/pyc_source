# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/recipe/backup/testing.py
# Compiled at: 2009-11-25 08:12:07
import os
DEBUG = os.path.join(os.path.dirname(__file__), 'DEBUG')

def set_input(response):
    open(DEBUG, 'w').write(str(response))


def get_input(msg):
    if not os.path.exists(DEBUG):
        return
    res = open(DEBUG).read()
    print '%s %s' % (msg, res)
    return res


def remove_input():
    os.remove(DEBUG)