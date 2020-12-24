# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/adagios/adagios/daemon.py
# Compiled at: 2018-05-16 10:07:32
"""Methods for controlling and getting status of the Nagios daemon"""
from pynag.Control import daemon
from adagios import settings

class Daemon(daemon):

    def __init__(self):
        super(Daemon, self).__init__()
        if settings.nagios_binary:
            self.nagios_bin = settings.nagios_binary
        if settings.nagios_config:
            self.nagios_cfg = settings.nagios_config
        if settings.nagios_init_script:
            self.nagios_init = settings.nagios_init_script
        if settings.nagios_service:
            self.service_name = settings.nagios_service