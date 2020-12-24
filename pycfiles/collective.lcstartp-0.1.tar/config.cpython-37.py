# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/config.py
# Compiled at: 2018-09-10 10:36:01
# Size of source mod 2**32: 139 bytes
from plone import api
PROJECTNAME = 'collective.lazysizes'
IS_PLONE_5 = api.env.plone_version().startswith('5')