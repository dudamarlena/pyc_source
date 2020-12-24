# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/side-3.6/lib/python2.7/site-packages/collectd/__init__.py
# Compiled at: 2020-01-23 23:59:52
from .dispatcher import Values
from .registry import register_config, register_init, register_read, register_write, info