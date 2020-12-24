# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/alias.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 2331 bytes
from __future__ import unicode_literals
from warnings import warn
from weakref import proxy
from ....package.loader import traverse
from ....schema import Attribute

class Alias(Attribute):
    __doc__ = "Reference a field, potentially nested, elsewhere in the document.\n\t\n\tThis provides a shortcut for querying nested fields, for example, in GeoJSON, to more easily access the latitude\n\tand longitude:\n\t\n\t\tclass Point(Document):\n\t\t\tkind = String('type', default='point', assign=True)\n\t\t\tcoordinates = Array(Number(), default=lambda: [0, 0], assign=True)\n\t\t\tlatitude = Alias('coordinates.1')\n\t\t\tlongitude = Alias('coordinates.0')\n\t\n\tYou can now read and write `latitude` and `longitude` on instances of `Point`, as well as query the nested values\n\tthrough class attribute access.\n\t\n\tAnother common use case for these types of aliases is deprecation; if deprecate is truthy, attemps to get or set\n\tthe field will raise a DeprecationWarning, and if non-boolean, the string value will be added to the message.\n\t"
    path = Attribute()
    deprecate = Attribute(default=False)

    def __init__(self, path, **kw):
        (super(Alias, self).__init__)(path=path, **kw)

    def __fixup__(self, document):
        """Called after an instance of our Field class is assigned to a Document."""
        self.__document__ = proxy(document)

    def __get__(self, obj, cls=None):
        if self.deprecate:
            message = 'Retrieval of ' + self.path + ' via ' + self.__name__ + ') is deprecated.'
            if not isinstance(self.deprecate, bool):
                message += '\n' + str(self.deprecate)
            warn(message, DeprecationWarning, stacklevel=2)
        if obj is None:
            return traverse(self.__document__, self.path)
        else:
            return traverse(obj, self.path)

    def __set__(self, obj, value):
        if self.deprecate:
            message = 'Assignment of ' + self.path + ' via ' + self.__name__ + ' is deprecated.'
            if not isinstance(self.deprecate, bool):
                message += '\n' + str(self.deprecate)
            warn(message, DeprecationWarning, stacklevel=2)
        else:
            parts = self.path.split('.')
            final = parts.pop()
            current = obj
            for part in parts:
                if part.lstrip('-').isdigit():
                    current = current[int(part)]
                else:
                    current = getattr(current, part)

            if final.lstrip('-').isdigit():
                current[int(final)] = value
            else:
                setattr(current, final, value)