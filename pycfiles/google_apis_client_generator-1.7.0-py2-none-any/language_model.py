# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/language_model.py
# Compiled at: 2019-01-24 16:56:47
"""A class holding utilities and concepts specific to a programming language.

The LanguageModel class contains conceptual elements which are common to
programming languages, but differ in the details. For example, this class
had the concept of the delimiter between parts of a module. In Java this
would be a '.', in C++ a '::'.
"""
__author__ = 'aiuto@google.com (Tony Aiuto)'
from googleapis.codegen import utilities
PRESERVE_CASE = 0
LOWER_CASE = 1
UPPER_CASE = 2
LOWER_CAMEL_CASE = 3
UPPER_CAMEL_CASE = 4
LOWER_UNCAMEL_CASE = 5
UPPER_UNCAMEL_CASE = 6
CAP_FIRST = 7
ATSIGN_STRIP = 0
ATSIGN_BREAK = 1

class NamingPolicy(object):
    """The policy for transforming a wireName into a language suitable format.

  A naming policy consists of 3 parameters which define the transformation
  of a wireName into a particular type of programming language construct. For
  example, in C++, we might want max-results to be set_max_results when used as
  a setter and _max_results when used as the name of a member variable. The
  parameters are

  case_transform: (enum) The case transform for use for building a name. For
      the input 'hello worlD', the choices yield:
          language_model.PRESERVE_CASE => hello worlD
          language_model.LOWER_CASE => hello world
          language_model.UPPER_CASE => HELLO WORLD
          language_model.LOWER_CAMEL_CASE => hello WorlD
          language_model.UPPER_CAMEL_CASE => Hello WorlD
          language_model.LOWER_UNCAMEL_CASE => hello wor ld
          language_model.UPPER_UNCAMEL_CASE => HELLO WOR LD
  format_string: (str) The format string which wraps the transformed, separated
      name we are building. May be None for the identity format.
  separator: (char) The character which will be used to separate the
      parts of a name. May be None to indicate no separator.
  conflict_policy: (NamingPolicy) If the result of the name is a reserved word
      then try this policy as a fallback (and so on). It is the responsiblity
      of the LanguageModel sub-classer to provide a conflict_policy which
      will always result in a safe name. Note that the conflict_policy may, in
      turn, provide it's own conflict_policy. That allows one to construct a
      chain of formats to try.
  atsign_policy: (enum AtSignPolicy) The policy for handling '@' in names.
  """

    def __init__(self, case_transform=None, format_string=None, separator=None, conflict_policy=None, atsign_policy=ATSIGN_STRIP):
        self.case_transform = case_transform
        self.format_string = format_string
        self.separator = separator
        self.conflict_policy = conflict_policy
        self.atsign_policy = atsign_policy


class LanguageModel(object):
    """The base class for all LanguageModels.

  There is a matrix of options of the form {TypeOfName}_{Option}, where the
  nametype specifies the kind of variable name we want and the option
  specifies the case transformation, separator or format. The meaning of
  these three options are:

  The nametypes we define are
     array_of: For making a declaration of an array of some data type.
     class_name: For making a name for a class.
     constant: For making a name for a constant.
     member: For making a class member name.
  """
    language = ''
    allowed_characters = ''
    array_of_policy = None
    map_of_policy = None
    class_name_policy = NamingPolicy()
    constant_policy = NamingPolicy()
    member_policy = NamingPolicy()
    parameter_name_policy = NamingPolicy()
    getter_policy = NamingPolicy()
    setter_policy = NamingPolicy()
    unset_policy = NamingPolicy()
    has_policy = NamingPolicy()
    enum_policy = NamingPolicy()
    reserved_words = []

    def __init__(self, class_name_delimiter='.', module_name_delimiter=None):
        """Create a LanguageModel.

    Args:
      class_name_delimiter: (str) The string which delimits parts of a class
          name in code.
      module_name_delimiter: (str) The string which delimits parts of a module
          name in code. Defaults to class_name_delimiter
    Raises:
      ValueError: if some element of the class is mis-configured.
    """
        super(LanguageModel, self).__init__()
        self._class_name_delimiter = class_name_delimiter
        self._module_name_delimiter = module_name_delimiter or class_name_delimiter
        self._SUPPORTED_TYPES = {'integer': self._Integer, 
           'number': self._Float, 
           'string': self._String}
        self._policies_by_name = {'class_name': self.class_name_policy, 
           'constant': self.constant_policy, 
           'getter': self.getter_policy, 
           'has': self.has_policy, 
           'member': self.member_policy, 
           'parameter_name': self.parameter_name_policy, 
           'setter': self.setter_policy, 
           'unset': self.unset_policy, 
           'enum': self.enum_policy}

    def _Integer(self, data_value):
        """Convert provided int to language specific literal.

    Subclasses should override as appropriate.

    Args:
      data_value: The DataValue object representing the value to be converted
        to a integer literal.

    Returns:
      (str) String representation of value once cast to an integer.
    """
        return '%d' % long(data_value.value)

    def _Float(self, data_value):
        """Convert provided float to language specific literal.

    Args:
      data_value: The DataValue object representing the value to be converted
        to a float literal.

    Returns:
      (str) String representation of value once cast to an float.

    Raises:
      ValueError: if float is inf as we don't support rendering an inf.
    """
        value = float(data_value.value)
        if value == float('inf'):
            raise ValueError('DataValue does not support rendering of provided Type (%s)' % value)
        value = unicode(value)
        return value

    def _String(self, data_value):
        """Convert provided string to language specific literal.

    Subclasses should override as appropriate.

    Args:
      data_value: The DataValue object representing the value to be converted
        to a string literal.

    Returns:
      (str) Value written out as a string wrapped in double quotes.
    """
        literal_escape = [
         ('\\', '\\\\'),
         ('"', '\\"'),
         ('\n', '\\n'),
         ('\t', '\\t'),
         ('\r', '\\r'),
         ('\x0c', '\\f')]
        value = unicode(data_value.value)
        for special, replacement in literal_escape:
            value = value.replace(special, replacement)

        return '"%s"' % value

    @property
    def class_name_delimiter(self):
        return self._class_name_delimiter

    @property
    def module_name_delimiter(self):
        return self._module_name_delimiter

    def GetCodeTypeFromDictionary(self, json_schema):
        """Convert a json schema primitive type into the most suitable class name.

    Subclasses should override as appropriate.

    Args:
      json_schema: (dict) The defintion dictionary for this type
    Returns:
      A name suitable for use as a class in the generator's target language.
    """
        raise NotImplementedError('Subclasses of LanguageModel must implement GetCodeTypeFromDictionary')

    def GetPrimitiveTypeFromDictionary(self, unused_json_schema):
        """Convert a json schema primitive type into a language primitive.

    Subclasses should override as appropriate. This should be the primitive
    form of the result from GetCodeTypeFromDictionary(), or None if no primitive
    exists.

    Args:
      unused_json_schema: (dict) The defintion dictionary for this type
    Returns:
      A name suitable for use as a class in the generator's target language.
    """
        return

    def ArrayOf(self, variable, type_name):
        """Produce the string declaring an array of a data type.

    Args:
      variable: (DataType) the data we want an array of.
      type_name: (str) the printable name of that data type. Usually
          variable.codeType.
    Returns:
      (str)
    """
        if self.array_of_policy:
            return self.ApplyFormat(variable, type_name, self.array_of_policy)
        raise NotImplementedError('Subclasses of LanguageModel must implement ArrayOf or provide array_of_policy')

    def MapOf(self, variable, type_name):
        """Produce the string declaring a map of string to a data type.

    Args:
      variable: (DataType) the data we want an array of.
      type_name: (str) the printable name of that data type. Usually
          variable.codeType.
    Returns:
      (str)
    """
        if self.map_of_policy:
            return self.ApplyFormat(variable, type_name, self.map_of_policy)
        raise NotImplementedError('Subclasses of LanguageModel must implement MapOf or provide map_of_policy')

    def CodeTypeForVoid(self):
        """Return the type name for a void.

    Subclasses may override this default implementation.

    Returns:
      (str) 'void'
    """
        return 'void'

    def ApplyPolicy(self, policy_name, variable, name):
        """Apply a naming policy to a string.

    Maps the policy name to the tranformation class and applies it.

    Args:
      policy_name: (str) The name of a policy.
      variable: (CodeObject) an element which may appear in the templates,
          but typically a Property.
      name: (str) The Discovery name of the variable.
    Returns:
      (str) The input string transformed as specified by the policy.
    """
        policy = self._policies_by_name[policy_name]
        return self.TransformString(variable, name, policy)

    def ToMemberName(self, s, api):
        """Convert a name to a suitable member name in the target language.

    Subclasses should override as appropriate.

    TODO(user): Make a pass to replace uses of this with ToMemberName or
    whatever is appropriate,

    Args:
      s: (str) A canonical name for data element. (Usually the API wire format)
      api: (Api) The API this element is part of. For use as a hint when the
        name cannot be used directly.
    Returns:
      A name suitable for use as an element in the generator's target language.
    """
        return s

    def ToSafeClassName(self, s, api, parent):
        """Convert a name to a suitable class name in the target language.

    Subclasses should override as appropriate.

    Args:
      s: (str) A canonical name for data element. (Usually the API wire format)
      api: (Api) The API this element is part of. For use as a hint when the
        name cannot be used directly.
      parent: The schema where I was referenced.
    Returns:
      A name suitable for use as an element in the generator's target language.
    """
        return utilities.CamelCase(s)

    def ToPropertyGetterMethodWithDelim(self, prop_name):
        """Convert a property name to the name of the getter method that returns it.

    Subclasses should override as appropriate.

    Args:
      prop_name: (str) The name of a property.
    Returns:
      The language specific name of the getter method that returns the specified
      property. The default implementation returns .getxyz for a property called
      xyz.
    """
        return '%sget%s()' % (self._class_name_delimiter, prop_name)

    def RenderDataValue(self, data_value):
        """Translate a value to an appropriate structure for the target language.

    Args:
      data_value: The DataValue object rendered.
    Returns:
      The string representation of the value the target language expects
      of the type represented by the schema (e.g. a value [1, 2, 3] with
      a schema representing a list would be translated to "[1, 2, 3]" in
      Python but "Arrays.asList({1, 2, 3})" in Java).

    Raises:
      ValueError: if the provided schema is for an unsupported type.
    """
        type_str = data_value.data_type.json_type
        if type_str in self._SUPPORTED_TYPES:
            return self._SUPPORTED_TYPES[type_str](data_value)
        raise ValueError('Rendering the provided type (%s) is not supported by the %s.' % (
         type_str, type(self).__name__))

    def DefaultContainerPathForOwner(self, module):
        """Computes the default path to a module for the given owner information.

    For a given module, compute the portions of the path which are determined
    by the owner of the module - excluding the module path itself.

    Subclasses almost certainly want to override this.

    Args:
      module: (template_objects.Module) The module.
    Returns:
      (str) The path to use for the namespace of this API.
    """
        return ('/').join(utilities.ReversedDomainComponents(module.owner_domain))

    def ApplyCaseTransform(self, s, policy):
        """Applies a Policy's case transforms to a string.

    Args:
      s: (str) A string to transform.
      policy: (NamingPolicy) The naming policy to use for the transform.
    Returns:
      Case transformed string.
    """
        if policy.case_transform == LOWER_CASE:
            transform = lambda s, _: ('').join(s).lower()
        else:
            if policy.case_transform == UPPER_CASE:
                transform = lambda s, _: ('').join(s).upper()
            elif policy.case_transform == UPPER_CAMEL_CASE:
                transform = lambda s, _: ('').join([s[0].upper()] + s[1:])
            elif policy.case_transform == LOWER_CAMEL_CASE:
                transform = lambda s, first_word: ('').join([s[0].lower() if first_word else s[0].upper()] + s[1:])
            elif policy.case_transform == LOWER_UNCAMEL_CASE:
                transform = lambda s, _: utilities.UnCamelCase(('').join(s))
            elif policy.case_transform == UPPER_UNCAMEL_CASE:
                transform = lambda s, _: utilities.UnCamelCase(('').join(s)).upper()
            elif policy.case_transform == CAP_FIRST:
                transform = lambda s, first_word: ('').join([s[0].upper() if first_word else s[0]] + s[1:])
            else:
                transform = lambda s, _: ('').join(s)
            if policy.atsign_policy == ATSIGN_STRIP:
                s = s.replace('@', '')
            if policy.atsign_policy == ATSIGN_BREAK:
                s = s.replace('@', policy.separator or chr(1))
            parts = []
            curpart = []
            for c in s:
                if not c.isalnum() and c not in self.allowed_characters:
                    if curpart:
                        parts.append(transform(curpart, not parts))
                        curpart = []
                else:
                    curpart.append(c)

        if curpart:
            parts.append(transform(curpart, not parts))
        join_char = policy.separator or ''
        return join_char.join(parts)

    def TransformString(self, variable, s, policy):
        """Applies the transforms of a naming policy to a string.

    Takes a string (usually a wireName) which might be in any case and have
    reserved characters in it and transforms by the rules specified. The string
    is divided into parts at reserved characters, then each part is transformed
    by the case rule and then the parts are joined by the reserved character
    replacement.  Multiple reserved characters in a row are treated as one.

    Note that the camel case transformations preserve existing case except for
    the first character of each word. This provides good results for cases
    where the use has provided a camel cased or proper name. E.g. maxResults,
    YouTube, NASA.

    Note: Do we need rule that transforms NASA to Nasa and nasa when in the
    upper and lower camel variations?  That is, if you specify something in
    ALL CAPS, we assume it is not a mixed case spelling.

    Args:
      variable: (CodeObject) The template variable this string came from. This
          is used to extract details about the variable which may be useful in
          building a name, such as the module it belongs to.
      s: (str) A string to transform.
      policy: (NamingPolicy) The naming policy to use for the transform.
    Returns:
      Transformed string.
    """
        name = self.ApplyCaseTransform(s, policy)
        if policy.format_string:
            name = self.ApplyFormat(variable, name, policy)
        if name.lower() in self.reserved_words:
            if policy.conflict_policy:
                return self.TransformString(variable, s, policy.conflict_policy)
            else:
                return name + '__'

        return name

    def ApplyFormat(self, variable, name, policy):
        """Applies the format of a naming policy to a string.

    Args:
      variable: (CodeObject) The template variable this string came from. This
          is used to extract details about the variable which may be useful in
          building a name, such as the module it belongs to.
      name: (str) A name to transform.
      policy: (NamingPolicy) The naming policy to use for the transform.
    Returns:
      Transformed string.
    """
        expansions = dict(name=name)
        parent_name = 'global'
        if variable:
            if hasattr(variable, 'module'):
                expansions['module'] = variable.module.name
            if hasattr(variable, 'api'):
                api = variable.api
                if api:
                    api_name = api.GetTemplateValue('wireName') or parent_name
                expansions['api_name'] = self.ApplyCaseTransform(api_name, policy)
            if hasattr(variable, 'parent'):
                parent = variable.parent
                if parent:
                    parent_name = parent.GetTemplateValue('wireName') or parent_name
            if hasattr(variable, 'schema'):
                expansions['schema'] = variable.schema
            expansions['variable_name'] = self.ApplyCaseTransform(variable.GetTemplateValue('wireName') or '', policy)
        expansions['parent_name'] = self.ApplyCaseTransform(parent_name, policy)
        return policy.format_string.format(**expansions)


class DocumentingLanguageModel(LanguageModel):
    """A language model which displays things in a way humans can read.

  This model is useful for language neutral expression of an Api.
  """
    array_of_policy = NamingPolicy(format_string='Array<{name}>')
    map_of_policy = NamingPolicy(format_string='Map<string, {name}>')
    class_name_policy = NamingPolicy(case_transform=UPPER_CAMEL_CASE)

    def GetCodeTypeFromDictionary(self, json_schema):
        """Convert a json schema primitive type into the most suitable class name.

    Subclasses should override as appropriate.

    Args:
      json_schema: (dict) The defintion dictionary for this type
    Returns:
      A name suitable for use as a class in the generator's target language.
    """
        json_type = json_schema.get('type', 'UNKNOWN')
        json_format = json_schema.get('format')
        if json_format:
            json_type = '%s (%s)' % (json_type, json_format)
        return json_type