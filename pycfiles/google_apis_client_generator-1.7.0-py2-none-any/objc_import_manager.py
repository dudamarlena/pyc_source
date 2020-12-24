# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/objc_import_manager.py
# Compiled at: 2019-01-24 16:56:47
"""Objective-C library generator's import manager."""
__author__ = 'qwandor@google.com (Andrew Walbran)'

class ObjCImportManager(object):
    """The import manager for the Objective-C code generator."""

    def __init__(self, element):
        """Construct an import manager for the specified element.

    Args:
      element: (Schema) or (Api). The element we want to create an import
        manager for.
    """
        self._element = element
        self._element.SetTemplateValue('importManager', self)
        self._type_dependencies = set()
        self._imports = set()

    @classmethod
    def ForElement(cls, element):
        manager = element.get('importManager')
        if manager:
            return manager
        return cls(element)

    def ImportLists(self):
        """Returns the set of import lists."""
        return [
         sorted(self._imports)]

    def AddDataType(self, data_type):
        self._type_dependencies.add(data_type.code_type)
        return self.AddImport('"%s.h"' % data_type.code_type)

    def AddImport(self, filename):
        """Adds the specified import to the import manager.

    Args:
      filename: (str) The filename we want to add to this instance of import
        manager.

    Returns:
      True- If adding the import is successful.
      False- If adding the import fails.
    """
        self._imports.add(filename)
        return True

    @property
    def type_dependencies(self):
        return sorted(self._type_dependencies)