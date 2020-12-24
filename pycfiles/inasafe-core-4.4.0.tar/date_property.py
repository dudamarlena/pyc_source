# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/property/date_property.py
# Compiled at: 2017-12-28 04:19:26
"""Date Property."""
from datetime import datetime, date
from types import NoneType
from PyQt4.QtCore import QDate, Qt, QDateTime
from safe.common.exceptions import MetadataCastError
from safe.metadata.property import BaseProperty
__copyright__ = 'Copyright 2016, The InaSAFE Project'
__license__ = 'GPL version 3'
__email__ = 'info@inasafe.org'
__revision__ = '$Format:%H$'

class DateProperty(BaseProperty):
    """A property that accepts date input."""
    _allowed_python_types = [
     QDate, datetime, date, NoneType, QDateTime]

    def __init__(self, name, value, xml_path):
        super(DateProperty, self).__init__(name, value, xml_path, self._allowed_python_types)

    @classmethod
    def is_valid(cls, value):
        return True

    def cast_from_str(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            try:
                return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    return datetime.strptime(value, '%Y-%m-%d')
                except ValueError as e:
                    raise MetadataCastError(e)

    @property
    def xml_value(self):
        if self.python_type is datetime:
            return self.value.date().isoformat()
        if self.python_type is QDate:
            return self.value.toString(Qt.ISODate)
        if self.python_type is QDateTime:
            return self.value.toString(Qt.ISODate)
        if self.python_type is date:
            return self.value.isoformat()
        if self.python_type is NoneType:
            return ''
        raise RuntimeError('self._allowed_python_types and self.xml_value are out of sync. This should never happen')