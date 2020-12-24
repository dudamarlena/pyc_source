# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/ivoa/ivoa_column.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 315 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_column import BaseColumn

class IvoaColumn(BaseColumn):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, ivoa_table, json_object=None, url=None):
        """
        Constructor
        """
        super().__init__(ivoa_table, json_object, url)