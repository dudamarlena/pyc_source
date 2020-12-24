# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/elements/dataelement.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..compat import implements_to_string

@implements_to_string
class DataElement(object):

    def __init__(self, element, context):
        self.libid = element.libid
        self.ns = element.xmlns
        self.tag = element._tag_name
        self.data = element.get_all_data_parameters(context).copy()
        self.children = [ DataElement(child, context) for child in element.children() ]

    def __str__(self):
        return (b'<data {}>').format(self.libid)

    def __repr__(self):
        return (b'<data {}>').format(self.libid)