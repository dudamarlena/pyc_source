# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vint/misc.py
# Compiled at: 2013-04-19 06:08:29
from __future__ import unicode_literals
import logging, os
from dateutil import parser
from datetime import datetime
__author__ = b'tchen'
logger = logging.getLogger(__name__)

def calc_time_spent(start):
    started = parser.parse(start)
    now = datetime.now()
    diff = now - started
    return diff.seconds / 60


def get_config():
    from os.path import expanduser
    import ConfigParser
    config = ConfigParser.ConfigParser()
    filename = expanduser(b'~/.vintconfig')
    if os.path.exists(filename):
        config.readfp(open(filename))
        return config
    else:
        return
        return


config = get_config()