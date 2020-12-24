# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/utilities/name_validator.py
# Compiled at: 2019-01-30 13:37:02
"""Validation routines for discovery elements.

This is a singleton class which provides validation for names which can
appear in discovery documents
"""
__author__ = 'wclarkso@google.com (Will Clarkson)'
import re
_VARNAME_REGEX = re.compile('^[a-zA-Z]$|([a-zA-Z_/$@][a-zA-Z0-9_./$-]+)$')
_API_NAME_REGEX = re.compile('[a-z][a-zA-Z0-9_]*$')
_API_VERSION_REGEX = re.compile('[a-z0-9][a-zA-Z0-9._-]*$')

class ValidationError(ValueError):
    pass


def Validate(name):
    """Validates the name against a regular expression object.

  If the name matches the regular expression, we return nothing.
  If the name fails to match, we generate an exception.

  Args:
    name: (str) name of variable or method
  Returns:
    (str) The name.

  Raises:
    ValidationError: An Error if name does not conform to style
  """
    if _VARNAME_REGEX.match(name) is None:
        raise ValidationError('Variable %s does not conform to style guide' % name)
    return name


def ValidateApiName(api_name):
    """Validates a potential API name.

  An API name must match the regular expression[a-z0-9][a-zA-Z0-9_]*

  Args:
    api_name: (str) The API name to check.
  Returns:
    (str) The api name.

  Raises:
    ValidationError: An Error if name does not conform to style
  """
    if _API_NAME_REGEX.match(api_name) is None:
        raise ValidationError('API name %s does not conform to style guide' % api_name)
    return api_name


def ValidateApiVersion(api_version):
    """Validates a potential API version.

  An API version must match the regular expression[a-z0-9][a-zA-Z0-9.]*

  Args:
    api_version: (str) The API version to check.
  Returns:
    (str) The api version.

  Raises:
    ValidationError: An Error if version does not conform to style
  """
    if _API_VERSION_REGEX.match(api_version) is None:
        raise ValidationError('API version %s does not conform to style guide' % api_version)
    return api_version


def ValidateAndSanitizeComment(comment_string):
    """Validates a comment string.

  Remove comment terminators (e.g. */) from a string.

  TODO(user): Make a per-language validator. Allow non-dangerous symbols
  depending on language. e.g. */ is OK for Python but not PHP

  Args:
    comment_string: (str|unicode) input comment string
  Returns:
    (unicode) String with invalid character sequences removed
  """
    invalid_strings = [
     '/*',
     '*/',
     '"""',
     '///',
     '\\*']
    if isinstance(comment_string, str):
        comment_string = comment_string.decode('utf-8')
    change_made = True
    while change_made:
        change_made = False
        beginning_length = len(comment_string)
        for substring in invalid_strings:
            comment_string = comment_string.replace(substring, '')

        if len(comment_string) != beginning_length:
            change_made = True

    return comment_string