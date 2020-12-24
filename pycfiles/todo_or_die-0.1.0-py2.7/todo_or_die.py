# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/todo_or_die/todo_or_die.py
# Compiled at: 2019-02-09 13:53:12
"""Main module."""
from datetime import datetime

class TODO_or_die:

    def __init__(self, time_of_death):
        self.check_tod(time_of_death)

    def check_tod(self, time_of_death):
        day, month, year = time_of_death.split('/')
        timestamp = datetime.datetime(int(year), int(month), int(day)).timestamp()
        now = datetime.now().timestamp()
        if timestamp > now:
            import sys
            sys.exit()