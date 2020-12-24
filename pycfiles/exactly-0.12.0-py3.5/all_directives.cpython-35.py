# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/directives/all_directives.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 328 bytes
from typing import List
from exactly_lib.help.entities.directives.contents_structure import DirectiveDocumentation
from exactly_lib.help.entities.directives.objects.file_inclusion import FileInclusionDocumentation

def all_directives() -> List[DirectiveDocumentation]:
    return [
     FileInclusionDocumentation()]