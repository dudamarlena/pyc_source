# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/main_program/render.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 718 bytes
from exactly_lib.help.program_modes.main_program.contents import MainCliSyntaxDocumentation
from exactly_lib.help.render.cli_program import ProgramDocumentationSectionContentsConstructor
from exactly_lib.util.textformat.constructor.environment import ConstructionEnvironment
from exactly_lib.util.textformat.constructor.section import SectionContentsConstructor
from exactly_lib.util.textformat.structure import document as doc

class OverviewConstructor(SectionContentsConstructor):

    def apply(self, environment: ConstructionEnvironment) -> doc.SectionContents:
        renderer = ProgramDocumentationSectionContentsConstructor(MainCliSyntaxDocumentation())
        return renderer.apply(environment)