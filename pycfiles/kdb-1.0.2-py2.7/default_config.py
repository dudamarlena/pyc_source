# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/default_config.py
# Compiled at: 2014-04-26 09:00:59
"""defaults - System Defaults

This module contains default configuration and sane defaults for various
parts of the system. These defaults are used by the environment initially
when no environment has been created.
"""
CONFIG = {'server': {'host': 'irc.freenode.net', 
              'port': 6667}, 
   'bot': {'nick': 'kdb', 
           'ident': 'kdb', 
           'name': 'Knowledge Database Bot', 
           'channels': '#circuits'}, 
   'plugins': {'broadcast.*': 'enabled', 
               'channels.*': 'enabled', 
               'core.*': 'enabled', 
               'ctcp.*': 'enabled', 
               'dnstools.*': 'enabled', 
               'eval.*': 'enabled', 
               'google.*': 'enabled', 
               'greeting.*': 'enabled', 
               'help.*': 'enabled', 
               'irc.*': 'enabled', 
               'remote.*': 'enabled', 
               'rmessage.*': 'enabled', 
               'rnotify.*': 'enabled', 
               'stats.*': 'enabled', 
               'swatch.*': 'enabled', 
               'timers.*': 'enabled'}}