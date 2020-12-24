# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/python_generator.py
# Compiled at: 2019-01-24 16:56:47
"""Python library generator.

This module generates Python code from a Google API discovery documents.
"""
__author__ = 'akesling@google.com(Alex Kesling), aiuto@google.com (Tony Aiuto)'
from apiclient import discovery as discovery_client
from googleapis.codegen import api
from googleapis.codegen import api_library_generator
from googleapis.codegen import language_model
from googleapis.codegen import utilities

class PythonLanguageModel(language_model.LanguageModel):
    """A LanguageModel for Python."""
    language = 'python'
    _SCHEMA_TYPE_TO_PYTHON_TYPE = {'any': 'object', 
       'array': 'list', 
       'boolean': 'bool', 
       'integer': 'long', 
       'number': 'float', 
       'object': 'object', 
       'string': 'str'}
    _PYTHON_KEYWORDS = discovery_client.RESERVED_WORDS
    RESERVED_CLASS_NAMES = _PYTHON_KEYWORDS
    array_of_policy = language_model.NamingPolicy(format_string='list')
    map_of_policy = language_model.NamingPolicy(format_string='dict')

    def __init__(self):
        super(PythonLanguageModel, self).__init__(class_name_delimiter='.')
        self._SUPPORTED_TYPES['array'] = self._List
        self._SUPPORTED_TYPES['boolean'] = self._Boolean
        self._SUPPORTED_TYPES['object'] = self._Dictionary

    def _Boolean(self, data_value):
        """Convert provided boolean to language specific literal."""
        return unicode(bool(data_value.value))

    def _Dictionary(self, data_value):
        """Convert provided object to language specific literal."""
        wrapper = '{%s}'
        pairs = []
        for key, val in data_value.value.iteritems():
            val = self.RenderDataValue(val)
            pairs.append('"%s": %s' % (key, val))

        return wrapper % (', ').join(pairs)

    def _List(self, data_value):
        """Convert provided array to language specific literal."""
        wrapper = '[%s]'
        items = [ self.RenderDataValue(element) for element in data_value.value ]
        return wrapper % (', ').join(items)

    def GetCodeTypeFromDictionary(self, def_dict):
        """Gets an element's data type from its JSON definition.

    Overrides the default.

    Args:
      def_dict: (dict) The definition dictionary for this type
    Returns:
      A name suitable for use as a Python data type
    """
        json_type = def_dict.get('type', 'string')
        native_type = self._SCHEMA_TYPE_TO_PYTHON_TYPE.get(json_type) or self._SCHEMA_TYPE_TO_PYTHON_TYPE.get('string')
        return native_type

    def ToMemberName(self, s, the_api):
        """Convert a wire format name into a suitable Python variable name."""
        return s.replace('-', '_')


PYTHON_LANGUAGE_MODEL = PythonLanguageModel()

class PythonGenerator(api_library_generator.ApiLibraryGenerator):
    """The Python code generator."""

    def __init__(self, discovery_doc, options=None):
        super(PythonGenerator, self).__init__(PythonApi, discovery_doc, language='python', language_model=PYTHON_LANGUAGE_MODEL, options=options)

    def AnnotateMethod(self, the_api, method, resource):
        """Correct naming for APIClient methods in Python.

    Overrides default implementation.

    Args:
      the_api: (Api) The Api.
      method: (Method) The Method to annotate.
      resource: (Resource) The Resource which owns this Method.
    """
        method.SetTemplateValue('codeName', discovery_client.fix_method_name(method.codeName))

    def AnnotateParameter(self, method, parameter):
        """Correct naming for APIClient parameters in Python.

    Overrides default implementation.

    Args:
      method: (Method) The Method this parameter belongs to.
      parameter: (Parameter) The Parameter to annotate.
    """
        parameter.SetTemplateValue('codeName', discovery_client.key2param(parameter.codeName))

    def AnnotateResource(self, the_api, resource):
        """Correct naming for APIClient resources in Python.

    Overrides default implementation.

    Args:
      the_api: (Api) The Api which owns this resource.
      resource: (Resource) The Resource to annotate.
    """
        resource.SetTemplateValue('codeName', discovery_client.fix_method_name(resource.codeName))


class PythonApi(api.Api):
    """An Api with Python annotations."""

    def __init__(self, discovery_doc, **unused_kwargs):
        super(PythonApi, self).__init__(discovery_doc)

    def ToClassName(self, s, element, element_type=None):
        """Convert a discovery name to a suitable Python class name.

    Overrides the default.

    Args:
      s: (str) A rosy name of data element.
      element: (object) The object we need a class name for.
      element_type: (str) The kind of element (resource|method) to name.
    Returns:
      A name suitable for use as a class in the generator's target language.
    """
        if s.lower() in PythonLanguageModel.RESERVED_CLASS_NAMES:
            return '%s%s' % (utilities.CamelCase(self.values['name']),
             utilities.CamelCase(s))
        return utilities.CamelCase(s)