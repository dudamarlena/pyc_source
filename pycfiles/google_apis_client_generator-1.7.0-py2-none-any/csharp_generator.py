# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/csharp_generator.py
# Compiled at: 2019-01-24 16:56:47
"""C# library generator.

This module generates C# code from a Google API discovery documents.
"""
__author__ = 'aiuto@google.com (Tony Aiuto)'
from googleapis.codegen import api
from googleapis.codegen import api_library_generator
from googleapis.codegen import language_model
from googleapis.codegen import schema
from googleapis.codegen import utilities

class CSharpLanguageModel(language_model.LanguageModel):
    """A LanguageModel for C#."""
    language = 'csharp'
    allowed_characters = '<>,'
    array_of_policy = language_model.NamingPolicy(format_string='System.Collections.Generic.IList<{name}>')
    map_of_policy = language_model.NamingPolicy(format_string='System.Collections.Generic.IDictionary<string,{name}>')
    constant_policy = language_model.NamingPolicy(case_transform=language_model.UPPER_CAMEL_CASE)
    class_name_policy = language_model.NamingPolicy(case_transform=language_model.UPPER_CAMEL_CASE, separator='.')
    member_policy = language_model.NamingPolicy(case_transform=language_model.UPPER_CAMEL_CASE)
    _SCHEMA_TYPE_TO_CSHARP_TYPE = {('any', None): 'object', 
       ('boolean', None): 'System.Nullable<bool>', 
       ('integer', None): 'System.Nullable<int>', 
       ('number', None): 'System.Nullable<double>', 
       ('integer', 'int16'): 'System.Nullable<short>', 
       ('integer', 'int32'): 'System.Nullable<int>', 
       ('integer', 'uint32'): 'System.Nullable<long>', 
       ('number', 'double'): 'System.Nullable<double>', 
       ('number', 'float'): 'System.Nullable<float>', 
       ('string', None): 'string', 
       ('string', 'byte'): 'string', 
       ('string', 'date'): 'string', 
       ('string', 'date-time'): 'System.Nullable<System.DateTime>', 
       ('string', 'int64'): 'System.Nullable<long>', 
       ('string', 'uint64'): 'System.Nullable<ulong>', 
       ('object', None): 'object'}
    _CSHARP_KEYWORDS = [
     'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch',
     'char', 'checked', 'class', 'const', 'continue', 'decimal', 'default',
     'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern',
     'false', 'finally', 'fixed', 'float', 'for', 'foreach', 'goto', 'if',
     'implicit', 'in', 'int', 'interface', 'internal', 'is', 'lock', 'long',
     'namespace', 'new', 'null', 'object', 'operator', 'out', 'override',
     'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return',
     'sbyte', 'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'string',
     'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint',
     'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void',
     'volatile', 'while', 'async', 'await']
    RESERVED_CLASS_NAMES = _CSHARP_KEYWORDS
    reserved_words = RESERVED_CLASS_NAMES

    def __init__(self):
        super(CSharpLanguageModel, self).__init__(class_name_delimiter='.')

    def GetCodeTypeFromDictionary(self, def_dict):
        """Gets an element's data type from its JSON definition.

    Overrides the default.

    Args:
      def_dict: (dict) The defintion dictionary for this type
    Returns:
      A name suitable for use as a C# data type
    """
        json_type = def_dict.get('type', 'string')
        json_format = def_dict.get('format')
        native_type = self._SCHEMA_TYPE_TO_CSHARP_TYPE.get((json_type, json_format))
        if not native_type:
            native_type = 'object'
        return native_type

    def ApplyPolicy(self, policy_name, variable, value):
        """Override the default policy applier so we can do special things."""
        if policy_name == 'member':
            return self.ToClassMemberName(variable, value)
        return super(CSharpLanguageModel, self).ApplyPolicy(policy_name, variable, value)

    def ToClassMemberName(self, variable, name):
        formatted = super(CSharpLanguageModel, self).ApplyPolicy('member', variable, name)
        if isinstance(variable, schema.Property):
            if variable.schema.values.get('className') == formatted:
                formatted += 'Value'
        return formatted

    def ToMemberName(self, s, the_api):
        """CamelCase a wire format name into a suitable C# variable name."""
        camel_s = utilities.CamelCase(s)
        if s in self.RESERVED_CLASS_NAMES:
            return '%s%s' % (the_api.values['name'], camel_s)
        return camel_s[0].lower() + camel_s[1:]

    def DefaultContainerPathForOwner(self, module):
        """Returns the default path for the module containing this API."""
        return '%s/Apis' % utilities.CamelCase(module.owner_name)

    def ToSafeClassName(self, name, the_api, parent):
        if parent:
            for child in parent.children:
                if child.get('wireName') == name:
                    return child.className.split('.')[(-1)]

        if parent:
            name += '_data'
        return utilities.CamelCase(name)


CSHARP_LANGUAGE_MODEL = CSharpLanguageModel()

class CSharpGenerator(api_library_generator.ApiLibraryGenerator):
    """The C# code generator."""
    _NULLABLE_TYPE_TO_REQUIRED = {'object': 'object', 
       'string': 'string', 
       'System.Nullable<bool>': 'bool', 
       'System.Nullable<short>': 'short', 
       'System.Nullable<int>': 'int', 
       'System.Nullable<long>': 'long', 
       'System.Nullable<ulong>': 'ulong', 
       'System.Nullable<double>': 'double', 
       'System.Nullable<float>': 'float', 
       'System.Nullable<System.DateTime>': 'System.DateTime'}

    def __init__(self, discovery, options=None):
        options = options or {}
        options['version_module'] = True
        package_path = options.get('package_path', discovery.get('packagePath'))
        if package_path:
            options['package_path'] = ('.').join([ s[0].upper() + s[1:] for s in package_path.split('.') if s ])
        super(CSharpGenerator, self).__init__(CSharpApi, discovery, language='csharp', language_model=CSHARP_LANGUAGE_MODEL, options=options)

    def AnnotateParameter(self, unused_method, parameter):
        """Annotate a Parameter with C# specific elements."""
        self._Annotate(parameter)

    def AnnotateProperty(self, unused_api, prop, unused_schema):
        """Annotate a Property with C# specific elements."""
        self._Annotate(prop)

    def _Annotate(self, element):
        """Handles imports for the specified element.

    Args:
      element: (Property|Parameter) The property we will set it's nullable data
               type.
    """
        element.SetTemplateValue('requiredType', self._NULLABLE_TYPE_TO_REQUIRED.get(element.codeType))

    def AnnotateApi(self, the_api):
        """Annotate a Api with C# specific elements."""
        the_api.values['revision'] = self._GetValidRevision(the_api.values['revision'])
        super(CSharpGenerator, self).AnnotateApi(the_api)

    def _GetValidRevision(self, rev):
        """Get a valid revision (non negative numeric and less or equal than 65535).

    Args:
      rev: revision number
    Returns:
      A valid revision number.
    """
        try:
            valid_rev = int(rev)
            if valid_rev > 65535 or valid_rev < 0:
                return 0
            return valid_rev
        except ValueError:
            return 0


class CSharpApi(api.Api):
    """An Api with C# annotations."""

    def __init__(self, discovery_doc, **unused_kwargs):
        super(CSharpApi, self).__init__(discovery_doc)
        self.module.SetPath('%s/%s' % (self.values['className'],
         self.values['versionNoDots'].replace('-', '')))
        self.model_module.SetPath('Data')

    def NestedClassNameForProperty(self, name, owning_schema):
        parent_name = owning_schema.class_name.split('.')[(-1)]
        class_name = utilities.CamelCase(name) + 'Data'
        if parent_name == class_name:
            class_name += 'Schema'
        return '%s.%s' % (parent_name, class_name)

    def ToClassName(self, s, element, element_type=None):
        """Convert a discovery name to a suitable C# class name.

    Overrides the default.

    Args:
      s: (str) A rosy name of data element.
      element: (object) The object we need a class name for.
      element_type: (str) The kind of element (resource|method) to name.
    Returns:
      A name suitable for use as a class in the generator's target language.
    """
        if s in CSharpLanguageModel.RESERVED_CLASS_NAMES:
            return '%s%s' % (utilities.CamelCase(self.values['name']),
             utilities.CamelCase(s))
        return ('.').join([ utilities.CamelCase(x) for x in s.split('.') ])