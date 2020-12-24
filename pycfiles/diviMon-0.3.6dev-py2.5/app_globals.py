# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/lib/app_globals.py
# Compiled at: 2008-08-07 05:50:38
"""The application's Globals object"""
from pylons import config
from re import *

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        self.base_url = ''
        self.debug = True
        self.show_pages = 10
        self.function_delete = 'Delete'
        self.session = {}
        self.permissions = {1: {'*': ('*', )}, 
           2: dict(delivery_receipt=('*', )), 
           3: dict(inventory=('list', 'add'))}

    def new_session(self, id, user=None):

        class Session(object):

            def __init__(self, id, user):
                from datetime import datetime
                self.id = id
                self.login = datetime.now()
                self.user = user

        self.session[id] = Session(id, user)
        return self.session[id]

    class currency(float):

        def __init__(self, amount):
            self.amount = amount

        def __str__(self):
            temp = '%.2f' % self.amount
            profile = compile('(\\d)(\\d\\d\\d[.,])')
            while 1:
                (temp, count) = subn(profile, '\\1,\\2', temp)
                if not count:
                    break

            return temp