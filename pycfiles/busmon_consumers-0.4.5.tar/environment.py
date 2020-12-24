# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/threebean/devel/busmon/busmon/config/environment.py
# Compiled at: 2012-10-04 13:49:55
__doc__ = 'WSGI environment setup for busmon.'
from busmon.config.app_cfg import base_config
__all__ = [
 'load_environment']
load_environment = base_config.make_load_environment()