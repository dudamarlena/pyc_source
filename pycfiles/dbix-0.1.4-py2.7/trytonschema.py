# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbix/trytonschema.py
# Compiled at: 2017-10-18 09:37:15
from __future__ import print_function
from collections import OrderedDict
from trytond.model import fields
from .schema import schema

class TRYTONSchema(Schema):

    def get_entity(self, name, attr_conv=dict(), only_in_conv=True):
        type_converter = dict(integer='Integer', tinyint='Integer', smallint='Integer', enum='Char', float='Float', decimal='Decimal', numeric='Decimal', char='Char', varchar='Char', text='Text', mediumtext='Text', date='Date', time='Time', datetime='DateTime', boolean='Boolean')
        attr_converter = dict(data_type=(
         None, lambda c, x: type_converter.get(x)), is_nullable=(
         'required', lambda c, x: not int(x)), default_value=('default', None), size=('size',
                                                                                      None), extra=(
         'domain', lambda c, x: x['list']))
        entity = super(Schema, self).get_entity(name, attr_converter, only_in_conv=True)
        entity['fields'] = OrderedDict([ (name, (attrs.pop('data_type'), attrs)) for name, attrs in entity['fields'].items() if hasattr(fields, attrs['data_type'])
                                       ])
        return entity