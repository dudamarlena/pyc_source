# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\temp\sandbox\config.py
# Compiled at: 2020-02-04 02:27:43
# Size of source mod 2**32: 313 bytes
"""
fabadmin common config module.

Created on 2020-02-04 15:27:42.

"""
import os, config_base
from config_base import version, config_local

class config(config_base.config):
    __doc__ = 'Customize your config.'
    SECRET_KEY = 'qHJrY7plEpKnIPmoDDSqyem0XkU9P9DQFRadShJGdHhs7V3WYeBX5lYtuxVsWtAh'