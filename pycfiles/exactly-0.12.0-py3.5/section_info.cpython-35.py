# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/section_info.py
# Compiled at: 2018-09-19 20:55:32
# Size of source mod 2**32: 657 bytes
from exactly_lib.definitions.cross_ref.app_cross_ref import CrossReferenceId
from exactly_lib.definitions.formatting import SectionName

class SectionInfo:
    __doc__ = 'Information about a section, useful in help texts'

    def __init__(self, name: str):
        self._section_name = SectionName(name)

    @property
    def name(self) -> SectionName:
        return self._section_name

    @property
    def cross_reference_target(self) -> CrossReferenceId:
        raise NotImplementedError('abstract method')

    def instruction_cross_reference_target(self, instruction_name: str) -> CrossReferenceId:
        raise NotImplementedError('abstract method')