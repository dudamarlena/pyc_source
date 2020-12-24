# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/java_import_manager.py
# Compiled at: 2019-01-24 16:56:47
"""Java library generator's import manager."""
__author__ = 'rmistry@google.com (Ravi Mistry)'
_CLASS_NAME_TO_IMPORT_MANAGER = {}

class JavaImportManager(object):
    """The import manager for the Java code generator."""
    _JAVA_LANG_IMPORT = 'java.lang'

    def __init__(self, element):
        """Construct an import manager for the specified element.

    Args:
      element: (Schema) or (Api). The element we want to create an import
        manager for.
    """
        self._element = element
        self._element.SetTemplateValue('importManager', self)
        self._class_name_to_qualified_name = {}
        self._google_imports = set()
        self._other_imports = set()
        self._java_imports = set()

    @classmethod
    def GetCachedImportManager(cls, element):
        """Gets an import manager instance that corresponds to the class name.

    If the schema does not have a cached import manager, one is created
    and added to the cache.

    Args:
      element: (Schema) or (Api). The element we want to create an import
        manager for.
    Returns:
      The import manager instance for this schema.
    """
        import_mngr = _CLASS_NAME_TO_IMPORT_MANAGER.get(element)
        if not import_mngr:
            import_mngr = cls(element)
            _CLASS_NAME_TO_IMPORT_MANAGER[element] = import_mngr
        return import_mngr

    def ImportLists(self):
        """Returns the set of import lists."""
        return [
         sorted(self._google_imports),
         sorted(self._java_imports),
         sorted(self._other_imports)]

    def AddImport(self, fully_qualified_class):
        """Adds the specified import to the import manager.

    Args:
      fully_qualified_class: (str) The fully qualified class we want to add to
        this instance of import manager.

    Returns:
      True- If adding the import is successful.
      False- If adding the import results in a name collision.
    """
        if fully_qualified_class.startswith(self._JAVA_LANG_IMPORT):
            return True
        class_name = self.GetClassName(fully_qualified_class)
        current_import = self._class_name_to_qualified_name.get(class_name)
        if current_import:
            return current_import == fully_qualified_class
        if fully_qualified_class.startswith('com.google.'):
            self._google_imports.add(fully_qualified_class)
        elif fully_qualified_class.startswith('java.'):
            self._java_imports.add(fully_qualified_class)
        else:
            self._other_imports.add(fully_qualified_class)
        self._class_name_to_qualified_name[class_name] = fully_qualified_class
        return True

    def GetClassName(self, fully_qualified_class):
        return fully_qualified_class.split('.')[(-1)]

    @property
    def google_imports(self):
        return sorted(self._google_imports)

    @property
    def other_imports(self):
        return sorted(self._other_imports)

    @property
    def java_imports(self):
        return sorted(self._java_imports)