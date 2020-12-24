# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/property/character_string_property.py
# Compiled at: 2018-03-19 11:25:21
"""
InaSAFE Disaster risk assessment tool developed by AusAid -
**metadata module.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.
"""
from types import NoneType
from safe.metadata.property import BaseProperty
__author__ = 'marco@opengis.ch'
__revision__ = '$Format:%H$'
__date__ = '27/05/2015'
__copyright__ = 'Copyright 2012, Australia Indonesia Facility for Disaster Reduction'

class CharacterStringProperty(BaseProperty):
    """A property that accepts any type of input and stores it as string."""
    _allowed_python_types = [
     str, unicode, int, float, NoneType]

    def __init__(self, name, value, xml_path):
        if isinstance(value, str):
            value = unicode(value)
        super(CharacterStringProperty, self).__init__(name, value, xml_path, self._allowed_python_types)

    @classmethod
    def is_valid(cls, value):
        return True

    def cast_from_str(self, value):
        return value

    @property
    def xml_value(self):
        if self.python_type is NoneType:
            return ''
        if self.python_type in self.allowed_python_types and self.python_type != unicode:
            return str(self.value)
        if self.python_type == unicode:
            return unicode(self.value)
        raise RuntimeError('self._allowed_python_types and self.xml_valueare out of sync. This should never happen')