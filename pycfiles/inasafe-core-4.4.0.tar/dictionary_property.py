# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/property/dictionary_property.py
# Compiled at: 2018-03-19 11:25:21
"""Dictionary property."""
import json
from datetime import datetime
from types import NoneType
from safe.common.exceptions import MetadataCastError
from safe.metadata.property import BaseProperty
from safe.metadata.utilities import serialize_dictionary
__copyright__ = 'Copyright 2016, The InaSAFE Project'
__license__ = 'GPL version 3'
__email__ = 'info@inasafe.org'
__revision__ = '$Format:%H$'

class DictionaryProperty(BaseProperty):
    """A property that accepts dictionary input."""
    _allowed_python_types = [
     dict, NoneType]

    def __init__(self, name, value, xml_path):
        super(DictionaryProperty, self).__init__(name, value, xml_path, self._allowed_python_types)

    @classmethod
    def is_valid(cls, value):
        return True

    def cast_from_str(self, value):
        try:
            value = json.loads(value)
            for k, v in value.items():
                if isinstance(v, basestring):
                    try:
                        dictionary_value = json.loads(v)
                        if isinstance(dictionary_value, dict):
                            value[k] = dictionary_value
                    except ValueError:
                        try:
                            value[k] = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                        except ValueError:
                            pass

            return value
        except ValueError as e:
            raise MetadataCastError(e)

    @property
    def xml_value(self):
        if self.python_type is dict:
            try:
                return json.dumps(self.value)
            except (TypeError, ValueError):
                string_value = serialize_dictionary(self.value)
                return json.dumps(string_value)

        else:
            if self.python_type is NoneType:
                return ''
            raise RuntimeError('self._allowed_python_types and self.xml_value are out of sync. This should never happen')