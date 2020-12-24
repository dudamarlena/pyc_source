# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/property/integer_property.py
# Compiled at: 2018-03-19 11:25:21
"""Integer property."""
from types import NoneType
from safe.common.exceptions import MetadataCastError
from safe.metadata.property import BaseProperty
__copyright__ = 'Copyright 2016, The InaSAFE Project'
__license__ = 'GPL version 3'
__email__ = 'info@inasafe.org'
__revision__ = '$Format:%H$'

class IntegerProperty(BaseProperty):
    """A property that accepts integer input."""
    _allowed_python_types = [
     int, NoneType]

    def __init__(self, name, value, xml_path):
        super(IntegerProperty, self).__init__(name, value, xml_path, self._allowed_python_types)

    @classmethod
    def is_valid(cls, value):
        return True

    def cast_from_str(self, value):
        try:
            return int(value)
        except ValueError as e:
            raise MetadataCastError(e)

    @property
    def xml_value(self):
        if self.python_type is int:
            return str(self.value)
        if self.python_type is NoneType:
            return ''
        raise RuntimeError('self._allowed_python_types and self.xml_valueare out of sync. This should never happen')