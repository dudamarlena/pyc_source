# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/help/documentation_text.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 308 bytes
from typing import List
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.structure.core import ParagraphItem
POSIX_SYNTAX = 'Posix syntax'

def paths_uses_posix_syntax() -> List[ParagraphItem]:
    return docs.paras('Paths uses ' + POSIX_SYNTAX + '.')