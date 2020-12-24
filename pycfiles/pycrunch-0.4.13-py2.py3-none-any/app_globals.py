# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/lib/app_globals.py
# Compiled at: 2008-06-20 04:56:00
__doc__ = "The application's Globals object"
import re
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        self.number = '09283205839'
        self.show_pages = 10
        self.function_delete = 'Delete'
        self.folder_inbox = 1
        self.folder_archive = 2
        self.folder_outbox = 3
        self.folder_sent = 4
        prefixes = ['^0', '^63', '^\\+63', '^27763']
        self.prefixes = list((re.compile(pre) for pre in prefixes))
        self.base_url = config['base_url']
        self.debug = config['debug']
        self.show_pages = 10
        self.function_delete = 'Delete'