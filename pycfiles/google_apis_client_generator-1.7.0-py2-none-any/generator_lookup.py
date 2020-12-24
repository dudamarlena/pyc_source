# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/generator_lookup.py
# Compiled at: 2019-01-24 16:56:47
"""Common generator index utilities."""
__author__ = 'akesling@google.com (Alex Kesling)'
from googleapis.codegen import cpp_generator
from googleapis.codegen import csharp_generator
from googleapis.codegen import dart_generator
from googleapis.codegen import gwt_generator
from googleapis.codegen import java_generator
from googleapis.codegen import objc_generator
from googleapis.codegen import php_generator
from googleapis.codegen import python_generator
from googleapis.codegen import sample_generator
_GENERATORS_BY_LANGUAGE = {'cpp': cpp_generator.CppGenerator, 
   'csharp': csharp_generator.CSharpGenerator, 
   'dart': dart_generator.DartGenerator, 
   'gwt': gwt_generator.GwtGenerator, 
   'java': java_generator.Java14Generator, 
   'java1_15': java_generator.Java14Generator, 
   'objc': objc_generator.ObjCGenerator, 
   'php': php_generator.PHPGenerator, 
   'python': python_generator.PythonGenerator, 
   'sample': sample_generator.SampleGenerator}

def GetGeneratorByLanguage(language_or_generator):
    """Return the appropriate generator for this language.

  Args:
    language_or_generator: (str) the language for which to return a generator,
        or the name of a specific generator.

  Raises:
    ValueError: If provided language isn't supported.

  Returns:
    The appropriate code generator object (which may be None).
  """
    try:
        return _GENERATORS_BY_LANGUAGE[language_or_generator]
    except KeyError:
        raise ValueError('Unsupported language: %s' % language_or_generator)


def SupportedLanguages():
    """Return the list of languages we support.

  Returns:
    list(str)
  """
    return sorted(_GENERATORS_BY_LANGUAGE)