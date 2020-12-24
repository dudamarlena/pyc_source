# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/symbol/custom_symbol.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 548 bytes
from typing import Sequence
from exactly_lib.definitions.cross_ref.app_cross_ref import SeeAlsoTarget
from exactly_lib.util.textformat.structure.document import SectionContents

class CustomSymbolDocumentation:

    def __init__(self, single_line_description: str, documentation: SectionContents, see_also: Sequence[SeeAlsoTarget]=()):
        self.single_line_description = single_line_description
        self.documentation = documentation
        self.see_also = see_also