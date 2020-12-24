# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Work/config.py
# Compiled at: 2011-06-07 12:12:56
"""Common configuration constants
"""
from Products.Archetypes.atapi import DisplayList
PROJECTNAME = 'Products.Work'
ADD_PERMISSIONS = {'Work': 'Products.Work: Add Work'}
MESSAGE_PRIORITIES = DisplayList((
 ('high', 'High Priority'),
 ('normal', 'Normal Priority'),
 ('low', 'Low Priority')))