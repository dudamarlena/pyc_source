# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_import.py
# Compiled at: 2020-04-23 10:30:11
# Size of source mod 2**32: 360 bytes
import pytest

def test_import():
    import gen3


def test_cdisutilstest():
    import cdisutilstest


def test_indexclient():
    import indexclient


def test_auth_import():
    from gen3.auth import Gen3Auth


def test_submission_import():
    from gen3.submission import Gen3Submission


def test_file_import():
    from gen3.file import Gen3File