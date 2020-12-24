# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\prboard\constants.py
# Compiled at: 2016-04-22 00:09:12
from functools import partial
import filters

class State(object):
    """

    """
    Open = 'open'
    Closed = 'closed'
    All = 'all'


FILTER_COMMAND_MAPPING = {'num': filters.PRNumberFilter, 
   'title': filters.PRFilter, 
   'etitle': partial(filters.PRFilter, wildcard=True), 
   'labels': filters.LabelFilter}

class Colors(object):
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'


INFO_LEVEL, WARNING_LEVEL, ERROR_LEVEL, SEVERE_LEVEL = range(4)