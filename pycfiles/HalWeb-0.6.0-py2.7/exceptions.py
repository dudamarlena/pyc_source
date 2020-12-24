# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/exceptions.py
# Compiled at: 2011-12-23 04:19:50
"""
Created on 17.1.2010

@author: KMihajlov
"""

class ResourceNotAllowed(Exception):

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return self.value or "You don't have access to View this resource"