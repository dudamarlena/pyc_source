# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/lib/app_globals.py
# Compiled at: 2011-02-18 19:15:09
"""The application's Globals object"""
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import atexit
from turbomail import interface
from turbomail.adapters import tm_pylons

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))
        atexit.register(tm_pylons.shutdown_extension)
        interface.start(tm_pylons.FakeConfigObj(config))