# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywebuml\parsers\constants.py
# Compiled at: 2011-04-02 11:36:12
"""
Has different constants used in the different parsers.

@author: tzulberti
"""
MODIFIERS = [
 'abstract',
 'const',
 'event',
 'extern',
 'delegate',
 'new',
 'internal',
 'override',
 'private',
 'protected',
 'public',
 'readonly',
 'sealed',
 'static',
 'unsafe',
 'virtual',
 'volatile',
 'final',
 'transient',
 'synchronized']
ABSTRACT_KEYWORDS = [
 'abstract',
 'delegate',
 'extern']
CLASS_KEYWORDS = [
 'class',
 'struct',
 'interface',
 'partial',
 'enum']
CONST_KEYWORDS = [
 'const',
 'readonly']
PREPROCESSOR_DIRECTIVES = [
 '#if',
 '#else',
 '#elif',
 '#endif',
 '#undef',
 '#define',
 '#warning',
 '#error',
 '#line',
 '#region',
 '#endregion',
 '#pragma',
 '#pragma warning',
 '#pragma checksum']
SIMPLE_PREPROCESSOR_DIRECTIVES = [
 '#warning',
 '#error',
 '#line',
 '#region',
 '#endregion',
 '#pragma',
 '#pragma warning',
 '#pragma checksum']
COMMENTS_MARKERS = [
 '//',
 '///',
 '/*',
 '/**',
 '*/',
 '*']
LANGUAGE_BASE_VALUES = [
 'int',
 'int?',
 'float',
 'float?',
 'double',
 'double?',
 'long',
 'long?',
 'string',
 'string?',
 'char',
 'char?',
 'bool',
 'bool?',
 'boolean',
 'object',
 'Object',
 'enum',
 'String',
 'Boolean',
 'Integer',
 'Long',
 'Double',
 'BigInt']
JAVA_LANGUAGE_METHODS = [
 'clone',
 'equals',
 'finalize',
 'getClass',
 'hashCode',
 'notify',
 'notifyAll',
 'toString',
 'wait']