# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/threebean/devel/busmon/busmon/config/environment.py
# Compiled at: 2012-10-04 13:49:55
"""WSGI environment setup for busmon."""
from busmon.config.app_cfg import base_config
__all__ = [
 'load_environment']
load_environment = base_config.make_load_environment()