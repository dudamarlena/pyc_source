# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Work/config.py
# Compiled at: 2011-06-07 12:12:56
__doc__ = 'Common configuration constants\n'
from Products.Archetypes.atapi import DisplayList
PROJECTNAME = 'Products.Work'
ADD_PERMISSIONS = {'Work': 'Products.Work: Add Work'}
MESSAGE_PRIORITIES = DisplayList((
 ('high', 'High Priority'),
 ('normal', 'Normal Priority'),
 ('low', 'Low Priority')))