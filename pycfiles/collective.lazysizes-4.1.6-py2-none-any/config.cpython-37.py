# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/config.py
# Compiled at: 2018-09-10 10:36:01
# Size of source mod 2**32: 139 bytes
from plone import api
PROJECTNAME = 'collective.lazysizes'
IS_PLONE_5 = api.env.plone_version().startswith('5')