# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/html_doc/parts/help.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 447 bytes
from exactly_lib.help.program_modes.help.cli_syntax import HelpCliSyntaxDocumentation
from exactly_lib.help.render.cli_program import ProgramDocumentationSectionContentsConstructor
from exactly_lib.util.textformat.section_target_hierarchy import hierarchies as h

def root(header: str) -> h.SectionHierarchyGenerator:
    return h.leaf(header, ProgramDocumentationSectionContentsConstructor(HelpCliSyntaxDocumentation()))