# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/cpp_import_manager.py
# Compiled at: 2019-01-30 13:37:02
"""C++ library generator's import manager."""
__author__ = 'ewiseblatt@google.com (Eric Wiseblatt)'
from googleapis.codegen.utilities import ordered_set

class CppImportManager(object):
    """The import manager for the C++ code generator."""

    def __init__(self, element):
        """Construct an import manager for the specified element.

    Args:
      element: (Schema) or (Api). The element we want to create an import
        manager for.
    """
        self._element = element
        self._element.SetTemplateValue('importManager', self)
        self._class_name_to_qualified_name = {}
        self._google_imports = ordered_set.MutableOrderedSet()
        self._platform_imports = ordered_set.MutableOrderedSet()
        self._other_imports = ordered_set.MutableOrderedSet()
        self._type_dependencies = ordered_set.MutableOrderedSet()

    @classmethod
    def ForElement(cls, element):
        manager = element.get('importManager')
        if manager:
            return manager
        return cls(element)

    def ImportLists(self):
        """Returns the set of import lists."""
        return [
         sorted(self._platform_imports) + sorted(self._google_imports),
         sorted(self._other_imports)]

    def AddDataType(self, data_type):
        self._type_dependencies.add(data_type)
        return self.AddImport('"%s"' % data_type.values['include_path'])

    def AddImport(self, fully_qualified_class):
        """Adds the specified import to the import manager.

    Args:
      fully_qualified_class: (str) The fully qualified class we want to add to
        this instance of import manager.

    Returns:
      True- If adding the import is successful.
      False- If adding the import results in a name collision.
    """
        class_name = self.GetClassName(fully_qualified_class)
        current_import = self._class_name_to_qualified_name.get(class_name)
        if current_import:
            return current_import == fully_qualified_class
        if fully_qualified_class.startswith('"googleapis/'):
            self._google_imports.add(fully_qualified_class)
        elif self.IsPlatformClass(fully_qualified_class):
            self._platform_imports.add(fully_qualified_class)
        else:
            self._other_imports.add(fully_qualified_class)
        self._class_name_to_qualified_name[class_name] = fully_qualified_class
        return True

    def IsPlatformClass(self, fully_qualified_class):
        return fully_qualified_class.startswith('<')

    def GetClassName(self, fully_qualified_class):
        return fully_qualified_class.split('::')[(-1)]

    @property
    def type_dependencies(self):
        return self._type_dependencies

    @property
    def google_imports(self):
        return self._google_imports

    @property
    def platform_imports(self):
        return self._platform_imports

    @property
    def other_imports(self):
        return self._other_imports