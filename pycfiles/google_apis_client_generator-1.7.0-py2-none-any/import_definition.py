# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/import_definition.py
# Compiled at: 2019-01-24 16:56:47
"""Contains information necessary to define an import."""
__author__ = 'rmistry@google.com (Ravi Mistry)'

class ImportDefinition(object):
    """Contains all required information about an import.

  Intended for use in the type_format_to_datatype_and_imports dictionaries.
  """

    def __init__(self, imports=None, template_values=None):
        """Construct a definition of an import.

    Args:
      imports: (sequence of str) Contains all imports required by a data type.
      template_values: (sequence of str) Contains all required additional
        template values that are required to be set to handle the imports.
    """
        self._imports = imports or []
        self._template_values = template_values or []

    @property
    def imports(self):
        return self._imports

    @property
    def template_values(self):
        return self._template_values