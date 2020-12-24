# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/constructor/environment.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 667 bytes
from exactly_lib.util.textformat.constructor.text import CrossReferenceTextConstructor

class ConstructionEnvironment(tuple):

    def __new__(cls, cross_ref_text_constructor: CrossReferenceTextConstructor, construct_simple_header_value_lists_as_tables: bool=False):
        return tuple.__new__(cls, (cross_ref_text_constructor,
         construct_simple_header_value_lists_as_tables))

    @property
    def cross_ref_text_constructor(self) -> CrossReferenceTextConstructor:
        return self[0]

    @property
    def construct_simple_header_value_lists_as_tables(self) -> bool:
        return self[1]