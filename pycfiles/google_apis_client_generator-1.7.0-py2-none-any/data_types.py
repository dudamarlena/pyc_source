# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/data_types.py
# Compiled at: 2019-01-24 16:56:47
"""Template objects which represent data types.

This module contains objects which usable in templates and represent data type
idioms.
"""
__author__ = 'aiuto@google.com (Tony Aiuto)'
from googleapis.codegen import template_objects

class DataType(template_objects.CodeObject):
    """Template object which represents a data type.

  This is the base class for things which might be data type definitions, such
  as Schema objects derived from JSONSchema blocks or primitive types.
  """

    def __init__(self, def_dict, api, parent=None, language_model=None):
        """Construct a DataType.

    Args:
      def_dict: (dict) The discovery dictionary for this element.
      api: (Api) The Api instance which owns this element.
      parent: (CodeObject) The parent of this element.
      language_model: (LanguageModel) The language we are targetting.
        Dynamically defaults to the parent's language model.
    """
        super(DataType, self).__init__(def_dict, api, parent=parent, language_model=language_model)
        self._json_type = def_dict.get('type')
        schema_id = def_dict.get('id')
        if schema_id:
            self.SetTemplateValue('className', schema_id)
        if self.api and hasattr(self.api, 'model_module'):
            self._module = self.api.model_module
        annotations = def_dict.get('annotations')
        if annotations:
            required = annotations.get('required')
            self.SetTemplateValue('required_for_methods', required)

    @property
    def json_type(self):
        """Expose the type element from the JSON Schema type definition."""
        return self._json_type

    @property
    def code_type(self):
        """Returns the string representing this datatype."""
        return self.values.get('codeType') or self.values.get('className')

    @property
    def safe_code_type(self):
        """Returns the safe code type representing this datatype."""
        return self.safeClassName or self.code_type

    @property
    def primitive_data_type(self):
        """Returns the language specific primitive representing this datatype."""
        return

    @property
    def class_name(self):
        return self.GetTemplateValue('className')

    @property
    def safeClassName(self):
        """Returns a language appropriate name for this object.

    This property should only be used during template expansion. It is computed
    once, using the LanguageModel in play, and then that value is cached.

    Returns:
      (str) a name for an instance of this object.
    """
        safe_class_name = self.GetTemplateValue('safe_class_name')
        if not safe_class_name:
            safe_class_name = self.values.get('wireName')
            if not safe_class_name:
                return None
            if self.language_model:
                safe_class_name = self.language_model.ToSafeClassName(safe_class_name, self._api, self._parent)
            self.SetTemplateValue('safeClassName', safe_class_name)
        return safe_class_name


class PrimitiveDataType(DataType):
    """DataType which represents a "built in" data type.

  Primitive types are those which are provided by the language or one of its
  packages, rather than those defined by the API.  A language specific
  generater should annotate PrimitiveDataType objects with a specific codeType
  before using them to generate code.
  """

    def __init__(self, def_dict, api, parent=None):
        """Construct a PrimitiveDataType.

    Args:
      def_dict: (dict) The discovery dictionary for this element.
      api: (Api) The Api instance which owns this element.
      parent: (TemplateObject) The parent of this object.
    """
        super(PrimitiveDataType, self).__init__(def_dict, api, parent=parent)
        self.SetTemplateValue('builtIn', True)
        self.SetTemplateValue('isScalar', True)

    @property
    def class_name(self):
        return self.code_type

    @property
    def fullClassName(self):
        """Override the TemplateObject path chaining."""
        return self.code_type

    @property
    def code_type(self):
        """Returns the language specific type representing this datatype."""
        user_override = self.values.get('codeType')
        if user_override:
            return user_override
        if self.language_model:
            s = self.language_model.GetCodeTypeFromDictionary(self._def_dict)
            return s
        return self.values.get('type')

    @property
    def safe_code_type(self):
        """Returns the safe code type representing this datatype."""
        return self.code_type

    @property
    def primitive_data_type(self):
        """Returns the language specific type representing this datatype."""
        if self.language_model:
            s = self.language_model.GetPrimitiveTypeFromDictionary(self._def_dict)
            return s
        else:
            return

    @property
    def json_format(self):
        """Expose the format element from the JSON Schema type definition."""
        return self.values.get('format')


class ComplexDataType(DataType):
    """A DataType which requires a definition: that is, not primitive.

  ComplexDataTypes are structured objects and containers of objects.
  """

    def __init__(self, default_name, def_dict, api, parent=None, language_model=None, wire_name=None):
        """Construct an ComplexDataType.

    Args:
      default_name: (str) The name to give this type if there is no 'id' in
        the default dict.
      def_dict: (dict) The discovery dictionary for this element.
      api: (Api) The Api instance which owns this element.
      parent: (CodeObject) The parent of this element.
      language_model: (LanguageModel) The language we are targetting.
        Dynamically defaults to the parent's language model.
      wire_name: (str) The identifier used in the wire protocol for this object.
    Raises:
      ValueError: if there is no identifing name for this object.
    """
        super(ComplexDataType, self).__init__(def_dict, api, parent=parent, language_model=language_model)
        name = def_dict.get('id') or default_name or wire_name
        if not name:
            raise ValueError('Complex data types must have an id or be assigned a name: %s' % def_dict)
        self.SetTemplateValue('wireName', wire_name or name)

    @property
    def code_type(self):
        """Returns the string representing this datatype."""
        return self.values.get('codeType') or self.className

    @property
    def safe_code_type(self):
        """Returns the safe code type representing this datatype."""
        return self.safeClassName or self.code_type

    @property
    def class_name(self):
        return self.values.get('className')

    @property
    def className(self):
        return self.class_name or self.safeClassName


class ContainerDataType(ComplexDataType):
    """Superclass for all DataTypes which represent containers."""

    def __init__(self, name, base_type, parent=None, wire_name=None):
        """Construct an ArrayDataType.

    Args:
      name: (str) The name to give this type if there is no 'id' in
        the default dict.
      base_type: (DataType) The DataType to represent an array of.
      parent: (TemplateObject) The parent of this object.
      wire_name: (str) The identifier used in the wire protocol for this object.
    """
        super(ContainerDataType, self).__init__(name, {}, base_type.api, parent=parent, language_model=base_type._language_model, wire_name=wire_name)
        self._base_type = base_type
        self.SetTemplateValue('isContainer', True)
        self.SetTemplateValue('baseType', base_type)
        self.SetTemplateValue('builtIn', True)
        if isinstance(base_type, PrimitiveDataType):
            self._base_type.SetParent(self)


class ArrayDataType(ContainerDataType):
    """DataType which represents a array of another DataType."""

    def __init__(self, name, base_type, parent=None, wire_name=None):
        """Construct an ArrayDataType.

    Args:
      name: (str) The name to give this type.
      base_type: (DataType) The DataType to represent an array of.
      parent: (TemplateObject) The parent of this object.
      wire_name: (str) The identifier used in the wire protocol for this object.
    """
        super(ArrayDataType, self).__init__(name, base_type, parent=parent, wire_name=wire_name)
        self._json_type = 'array'
        self.SetTemplateValue('arrayOf', base_type)

    @property
    def code_type(self):
        """Returns the string representing the datatype of this variable.

    Note: This may should only be called after the language model is set.

    Returns:
      (str) A printable representation of this data type.
    """
        return self.language_model.ArrayOf(self._base_type, self._base_type.code_type)

    @property
    def safe_code_type(self):
        return self.language_model.ArrayOf(self._base_type, self._base_type.safe_code_type)


class MapDataType(ContainerDataType):
    """DataType which represents a map of string to another DataType.

  This is the base class for things which might be data type definitions, such
  as Schema objects derived from JSONSchema blocks or primitive types.
  """

    def __init__(self, name, base_type, parent=None, wire_name=None):
        """Construct a MapDataType.

    Args:
      name: (str) The name to give this type.
      base_type: (DataType) The DataType to represent an map of string to.
      parent: (TemplateObject) The parent of this object.
      wire_name: (str) The identifier used in the wire protocol for this object.
    """
        super(MapDataType, self).__init__(name, base_type, parent=parent, wire_name=wire_name)
        self._json_type = 'map'
        self.SetTemplateValue('mapOf', base_type)

    @property
    def code_type(self):
        """Returns the string representing the datatype of this variable.

    Note: This may should only be called after the language model is set.

    Returns:
      (str) A printable representation of this data type.
    """
        return self.language_model.MapOf(self._base_type, self._base_type.code_type)

    @property
    def safe_code_type(self):
        """Returns the string representing the safe datatype of this variable.

    Note: This may should only be called after the language model is set.

    Returns:
      (str) A printable representation of this data type.
    """
        return self.language_model.MapOf(self._base_type, self._base_type.safe_code_type)


class SchemaReference(DataType):
    """DataType which represents a type alias to named schema.

  Provides a lazy reference to schema by name.
  """

    def __init__(self, referenced_schema_name, api):
        """Construct a SchemaReference.

    Args:
      referenced_schema_name: (str) The name of the schema we are referencing.
      api: (Api) The Api instance which owns this element.

    Returns:
      SchemaReference
    """
        super(SchemaReference, self).__init__({}, api)
        self._referenced_schema_name = referenced_schema_name
        self.SetTemplateValue('className', referenced_schema_name)
        self.SetTemplateValue('wireName', referenced_schema_name)
        self.SetTemplateValue('reference', True)

    @property
    def referenced_schema(self):
        """Returns the concrete schema being referenced by this instance."""
        data_type = self
        while isinstance(data_type, SchemaReference):
            data_type = data_type.api.SchemaByName(data_type._referenced_schema_name)

        return data_type

    @property
    def values(self):
        """Forwards the 'values' property of this object to the referenced object.

    This enables GetTemplateValue called on a Ref to effectively return
    the value for the truly desired schema.

    This may be safely called at any time, but may not produce expected
    results until after the entire API has been parsed. In practice, this
    means that anything done during template expansion is fine.

    Returns:
      dict of values which can be used in template.
    """
        s = self.referenced_schema
        if s:
            return s.values
        return self._def_dict

    @property
    def code_type(self):
        """Returns the string representing the datatype of this variable."""
        s = self.referenced_schema
        if s:
            return s.code_type
        return self._def_dict.get('codeType') or self._def_dict.get('className')

    @property
    def safe_code_type(self):
        if not self.referenced_schema:
            return '<bad $ref>'
        return self.referenced_schema.safe_code_type

    @property
    def parent(self):
        """Returns the parent of the schema I reference."""
        return self.referenced_schema.parent

    @property
    def module(self):
        """Returns the module of the schema I reference."""
        return self.referenced_schema.module

    def __str__(self):
        return '<SchemaReference to %s>' % self.code_type


class Void(PrimitiveDataType):
    """DataType which represents a 'void'.

  Some API methods have no response. To provide some consistency in assigning
  a responseType to these methods, we use the Void data type. When it is
  referenced in a template, it forwards requests for it's code_type to a
  langauge model specific emitter.
  """

    def __init__(self, api):
        """Construct a Void.

    Args:
      api: (Api) The Api instance which owns this element. This is used for
        a parent chain so that we can pick up the language model at template
        generation time.

    Returns:
      Void
    """
        super(Void, self).__init__({}, api, parent=api)
        self.SetTemplateValue('isVoid', True)

    @property
    def code_type(self):
        """Returns the string representing the datatype of this variable."""
        if self.language_model:
            return self.language_model.CodeTypeForVoid()
        return 'void'


class Enum(PrimitiveDataType):
    """The definition of an Enum.

  Example enum in discovery.
    "enum": [
        "@comments",
        "@consumption",
        "@liked",
        "@public",
        "@self"
       ],
    "enumDescriptions": [
        "Limit to activities commented on by the user.",
        "Limit to activities to be consumed by the user.",
        "Limit to activities liked by the user.",
        "Limit to public activities posted by the user.",
        "Limit to activities posted by the user."
       ]
  """

    def __init__(self, def_dict, api, wire_name, values, descriptions, parent):
        """Create an enum.

    Args:
      def_dict: (dict) The discovery dictionary for this element.
      api: (Api) The Api which owns this Property
      wire_name: (str) The identifier used in the wire protocol for this enum.
      values: ([str]) List of possible values. If not provided, use the 'enum'
          element from def_dict.
      descriptions: ([str]) List of value descriptions. If not provided, use
          the 'enumDescriptions' element from def_dict.
      parent: (Method) The object owning this enum.
    """
        super(Enum, self).__init__(def_dict, api, parent=parent)
        name = def_dict.get('id') or wire_name
        self.ValidateName(name)
        self.SetTemplateValue('wireName', name)
        self.SetTemplateValue('className', api.ToClassName(name, self, element_type='enum'))
        if values is None:
            values = def_dict.get('enum')
        if descriptions is None:
            descriptions = def_dict.get('enumDescriptions') or []
        self._elements = []
        for i in range(len(values)):
            v = values[i]
            d = descriptions[i] if i < len(descriptions) else None
            self._elements.append(template_objects.Constant(v, description=d, parent=self))

        self.SetTemplateValue('elements', self._elements, meaning='The individual possible values of an Enum data type.')

        def FixName(name):
            name = name[0].isdigit() and 'VALUE_' + name or name.lstrip('@')
            return name.upper().replace('-', '_')

        names = [ FixName(s) for s in values ]

        def FixDescription(desc):
            return self.ValidateAndSanitizeComment(self.StripHTML(desc))

        pairs = zip(names, values, map(FixDescription, descriptions))
        self.SetTemplateValue('pairs', pairs)
        return

    @property
    def enum_name(self):
        return self.language_model.ApplyPolicy('enum', self, self.values['wireName'])


def CreatePrimitiveDataType(def_dict, api, wire_name, parent=None):
    """Creates a PrimitiveDataType from a JSON dictionary.

  Creates a primitive built in type or an enum for a blob of json.

  Args:
    def_dict: (dict) The discovery dictionary for this element.
    api: (Api) The Api instance which owns this element.
    wire_name: (str) The identifier used in the wire protocol for this object.
    parent: (TemplateObject) The parent of this object.
  Returns:
    (PrimitiveDataType) A data type.
  """
    if def_dict.get('enum'):
        return Enum(def_dict, api, wire_name, None, None, parent)
    else:
        return PrimitiveDataType(def_dict, api, parent)