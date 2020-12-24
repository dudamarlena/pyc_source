# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: X:\Workspaces\dee\kabaret\kabaret.naming\kabaret\naming\fields\computed.py
# Compiled at: 2013-01-23 08:04:33
"""
    Copyright (c) Supamonks Studio and individual contributors.
    All rights reserved.

    This file is part of kabaret, a python Digital Creation Framework.

    Kabaret is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Redistributions of source code must retain the above copyright notice, 
    this list of conditions and the following disclaimer.
        
    Redistributions in binary form must reproduce the above copyright 
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
    
    Kabaret is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public License
    along with kabaret.  If not, see <http://www.gnu.org/licenses/>

--
    The kabaret.naming.fields.computed module.
    
"""
from .field import Field, FieldValueError

class ComputedField(Field):

    def __init__(self, parent):
        super(ComputedField, self).__init__(parent)

    def pformat(self, indent=0, ns=''):
        return super(ComputedField, self).pformat(indent, ns) + ' (Computed)'

    def compute_value(self):
        raise NotImplementedError

    def set_value(self, value):
        cvalue = self.compute_value()
        if value != cvalue:
            raise FieldValueError('Value %r does not match the computed value %r in field %r' % (
             value, cvalue, self.key))
        super(ComputedField, self).set_value(value)