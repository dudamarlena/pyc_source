# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craiglabenz/Sites/tablets/tablets/j2/exceptions.py
# Compiled at: 2016-10-06 09:07:10
# Size of source mod 2**32: 147 bytes
from __future__ import unicode_literals

class Jinja2NotInstalled(Exception):
    message = 'Error: Must install jinja2 to use Jinja2 templates.'