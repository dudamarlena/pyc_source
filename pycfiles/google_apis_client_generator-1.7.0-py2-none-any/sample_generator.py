# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/sample_generator.py
# Compiled at: 2019-01-24 16:56:47
"""Sample library generator.

This module generates code from a Google API discovery documents.
"""
from googleapis.codegen import api
from googleapis.codegen import api_library_generator
from googleapis.codegen import language_model
from googleapis.codegen import utilities

class SampleLanguageModel(language_model.LanguageModel):
    """A LanguageModel for a sample language."""
    language = 'sample'
    allowed_characters = '_'
    array_of_policy = language_model.NamingPolicy(format_string='{module}::Array<{name}>')
    map_of_policy = language_model.NamingPolicy(format_string='Map<string, {name}>')
    class_name_policy = language_model.NamingPolicy(case_transform=language_model.LOWER_CASE, separator='_')
    constant_policy = language_model.NamingPolicy(case_transform=language_model.UPPER_CASE, separator='_')
    member_policy = language_model.NamingPolicy(format_string='_{name}', separator='_')
    getter_policy = language_model.NamingPolicy(case_transform=language_model.UPPER_CAMEL_CASE, format_string='get{name}')
    setter_policy = language_model.NamingPolicy(case_transform=language_model.UPPER_CAMEL_CASE, format_string='set{name}')
    parameter_name_policy = language_model.NamingPolicy(format_string='{name}', separator='_')
    _SCHEMA_TYPE_TO_LANGUAGE_TYPE = {'any': 'object', 
       'array': 'array', 
       'boolean': 'bool', 
       'integer': 'long', 
       'number': 'float', 
       'object': 'object', 
       'string': 'str'}
    RESERVED_CLASS_NAMES = [
     'class', 'import', 'return']

    def __init__(self):
        super(SampleLanguageModel, self).__init__(module_name_delimiter='::')
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
      A name suitable for use as a data type
    """
        json_type = def_dict.get('type', 'string')
        native_type = self._SCHEMA_TYPE_TO_LANGUAGE_TYPE.get(json_type) or self._SCHEMA_TYPE_TO_LANGUAGE_TYPE.get('string')
        return native_type

    def ToMemberName(self, s, unused_api):
        """Convert a wire format name into a suitable variable name."""
        return s.replace('-', '_')


class SampleGenerator(api_library_generator.ApiLibraryGenerator):
    """The Sample code generator."""

    def __init__(self, discovery_doc, options=None):
        super(SampleGenerator, self).__init__(SampleApi, discovery_doc, language='sample', language_model=SampleLanguageModel(), options=options)


class SampleApi(api.Api):
    """An Api with annotations for this language."""

    def __init__(self, discovery_doc, **unused_kwargs):
        super(SampleApi, self).__init__(discovery_doc)

    def ToClassName(self, s, element, element_type=None):
        """Convert a discovery name to a suitable class name.

    Overrides the default.

    Args:
      s: (str) A rosy name of data element.
      element: (object) The object we need a class name for.
      element_type: (str) The kind of element (resource|method) to name.
    Returns:
      A name suitable for use as a class in the generator's target language.
    """
        if s.lower() in SampleLanguageModel.RESERVED_CLASS_NAMES:
            return '%s%s' % (utilities.CamelCase(self.values['name']),
             utilities.CamelCase(s))
        return utilities.CamelCase(s)