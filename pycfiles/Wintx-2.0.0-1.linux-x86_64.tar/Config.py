# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/drivers/dummy/Config.py
# Compiled at: 2016-03-23 14:50:19
from voluptuous import All, Length, Optional, Range, Required

class Config(object):
    CONFIG_SCHEMA = {'test_key': str, 
       Required('test_required'): All(str, Length(min=1, max=10)), 
       Required('test_required_int'): All(int, Range(min=50)), 
       Optional('test_optional'): All(int, Range(min=0, max=100))}