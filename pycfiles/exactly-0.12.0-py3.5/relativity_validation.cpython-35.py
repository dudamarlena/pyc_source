# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_file_structure/relativity_validation.py
# Compiled at: 2017-05-02 08:48:26
# Size of source mod 2**32: 444 bytes
from exactly_lib.test_case_file_structure.path_relativity import SpecificPathRelativity, PathRelativityVariants

def is_satisfied_by(specific_relativity: SpecificPathRelativity, accepted_relativities: PathRelativityVariants) -> bool:
    if specific_relativity.is_absolute:
        return accepted_relativities.absolute
    else:
        return specific_relativity.relativity_type in accepted_relativities.rel_option_types