# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/utils.py
# Compiled at: 2019-09-30 06:45:25
# Size of source mod 2**32: 460 bytes


def assert_valid_suffix(filename, allowed_suffixes):
    """
    Check that `filename` has one of the strings in `allowed_suffixes` as a
    suffix. Raises an AssertionError if not.
    """
    if not any((filename.endswith(suffix) for suffix in allowed_suffixes)):
        err_msg = "File '{}' does not end an allowed filename suffix ({})".format(filename, ', '.join(allowed_suffixes))
        raise AssertionError(err_msg)