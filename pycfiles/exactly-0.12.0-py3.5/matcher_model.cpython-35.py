# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/matcher_model.py
# Compiled at: 2020-01-13 16:12:08
# Size of source mod 2**32: 422 bytes
from exactly_lib.util import name
LINE_MATCHER_MODEL = name.NameWithGenderWithFormatting(name.a_name_with_plural_s('line'))
FILE_MATCHER_MODEL = name.NameWithGenderWithFormatting(name.a_name_with_plural_s('file'))
STRING_MATCHER_MODEL = name.NameWithGenderWithFormatting(name.a_name_with_plural_s('string'))
FILES_MATCHER_MODEL = name.NameWithGenderWithFormatting(name.a_name(name.Name('set of files', 'sets of files')))