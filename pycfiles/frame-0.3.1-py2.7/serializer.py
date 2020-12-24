# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/serializer.py
# Compiled at: 2013-02-20 22:25:29
from orm.datatypes import CustomType
from treedict import TreeDict
import json

class Serializer(object):

    def serialize(self):
        data = {}
        for key, value in self.data.iteritems():
            data_type = value.__class__.__name__
            data[key] = {'dataType': data_type, 
               'required': key in self.model.required_fields, 
               'options': value.get_options()}

        return data