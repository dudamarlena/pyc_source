# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/tests/test_zipfile.py
# Compiled at: 2020-01-29 20:14:20
# Size of source mod 2**32: 1968 bytes
"""
Copyright 2019 Brain Electrophysiology Laboratory Company LLC

Licensed under the ApacheLicense, Version 2.0(the "License");
you may not use this module except in compliance with the License.
You may obtain a copy of the License at:

http: // www.apache.org / licenses / LICENSE - 2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied.
"""
from os.path import join, dirname
import pytest
from ..zipfile import ZipFile
from zipfile import ZipFile as stlZipFile
examples_path = join(dirname(__file__), '..', '..', 'examples')

@pytest.fixture
def stlmff():
    """load zipped mff file with standard `zipfile`"""
    filename = join(examples_path, 'example_1.mfz')
    return stlZipFile(filename)


@pytest.fixture
def mymff():
    """load zipped mff file with custom `zipfile`"""
    filename = join(examples_path, 'example_1.mfz')
    return ZipFile(filename)


def test_enter(mymff, stlmff):
    """test enter and read from a `FilePart`"""
    expected = stlmff.open('epochs.xml').read()
    with mymff.open('epochs.xml') as (fp):
        output = fp.read()
    if not fp.closed:
        raise AssertionError
    elif not output == expected:
        raise AssertionError


def test_close(mymff):
    """test closing a `FilePart`"""
    fp = mymff.open('epochs.xml')
    fp.close()
    assert fp.closed


def test_seek_tell(mymff):
    """test seek in a `FilePart`"""
    with mymff.open('epochs.xml') as (fp):
        if not fp.tell() == 0:
            raise AssertionError
        else:
            fp.seek(12)
            assert fp.tell() == 12
            fp.seek(12, 1)
            assert fp.tell() == 24
            fp.seek(0, 2)
            assert fp.tell() == fp.end - fp.start


@pytest.mark.parametrize('whence', [-1, 3])
def test_wrong_whence(mymff, whence):
    """test wrong `whence` parameter throws `ValueError`"""
    with mymff.open('epochs.xml') as (fp):
        with pytest.raises(ValueError):
            fp.seek(0, whence)