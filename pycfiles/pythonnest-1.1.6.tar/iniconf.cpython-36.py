# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/PythonNest/pythonnest/iniconf.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 426 bytes
from djangofloor.conf.fields import BooleanConfigField
from djangofloor.conf.mapping import BASE_MAPPING, REDIS_MAPPING
__author__ = 'flanker'
VALUES = [
 BooleanConfigField('global.read_only', 'READ_ONLY_MIRROR', 'Set to "true" if this mirror is a read-only mirror.No update can be made by users.')]
INI_MAPPING = BASE_MAPPING + REDIS_MAPPING + VALUES