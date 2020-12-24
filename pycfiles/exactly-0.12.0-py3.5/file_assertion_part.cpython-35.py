# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/assert_/utils/file_contents/parts/file_assertion_part.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 441 bytes
from exactly_lib.instructions.assert_.utils.assertion_part import IdentityAssertionPart
from exactly_lib.type_system.logic.string_matcher import FileToCheck

class FileContentsAssertionPart(IdentityAssertionPart[FileToCheck]):
    __doc__ = '\n    A :class:`AssertionPart` that is given\n    the path of a file to operate on.\n\n    This class is just a marker for more informative types.\n\n    Behaviour is identical to :class:`AssertionPart`.\n    '