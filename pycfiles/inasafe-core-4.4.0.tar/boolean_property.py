# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/property/boolean_property.py
# Compiled at: 2018-03-19 11:25:21
"""Boolean property."""
from types import NoneType
from safe.common.exceptions import MetadataCastError
from safe.metadata.property import BaseProperty
__copyright__ = 'Copyright 2016, The InaSAFE Project'
__license__ = 'GPL version 3'
__email__ = 'info@inasafe.org'
__revision__ = '$Format:%H$'

class BooleanProperty(BaseProperty):
    """A property that accepts boolean."""
    _allowed_python_types = [
     bool, NoneType]

    def __init__(self, name, value, xml_path):
        super(BooleanProperty, self).__init__(name, value, xml_path, self._allowed_python_types)

    @classmethod
    def is_valid(cls, value):
        return True

    def cast_from_str(self, value):
        try:
            return bool(int(value))
        except ValueError as e:
            raise MetadataCastError(e)

    @property
    def xml_value(self):
        if self.python_type is bool:
            return str(int(self.value))
        if self.python_type is NoneType:
            return ''
        raise RuntimeError('self._allowed_python_types and self.xml_valueare out of sync. This should never happen')