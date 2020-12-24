# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davisagli/Plone/kittycat/kittycat/__init__.py
# Compiled at: 2018-11-06 18:14:31
# Size of source mod 2**32: 189 bytes
from guillotina import *
from guillotina.commands import command_runner
from guillotina.commands import MISSING_SETTINGS
MISSING_SETTINGS['jsapps']['+admin'] = 'kittycat:static/catherder'