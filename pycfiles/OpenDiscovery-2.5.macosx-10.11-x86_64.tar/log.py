# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/OpenDiscovery/helpers/log.py
# Compiled at: 2014-08-19 20:12:50
import logging
from termcolor import colored

class ColourLog(object):
    colormap = dict(debug=dict(color='grey', attrs=['bold']), info=dict(color='white'), warn=dict(color='yellow', attrs=['bold']), warning=dict(color='yellow', attrs=['bold']), error=dict(color='red'), critical=dict(color='red', attrs=['bold']))

    def __init__(self, logger):
        self._log = logger

    def __getattr__(self, name):
        if name in ('debug', 'info', 'warn', 'warning', 'error', 'critical'):
            return lambda s, *args: getattr(self._log, name)(colored(s, **self.colormap[name]), *args)
        return getattr(self._log, name)