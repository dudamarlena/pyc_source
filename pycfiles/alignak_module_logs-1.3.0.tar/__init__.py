# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alignak/alignak-module-logs/alignak_module_logs/__init__.py
# Compiled at: 2017-01-05 09:31:30
"""
This module is an Alignak Broker module that collects the `monitoring_log` broks to send
them to a Python logger configured in the module configuration file
"""
from .logs import properties, get_instance