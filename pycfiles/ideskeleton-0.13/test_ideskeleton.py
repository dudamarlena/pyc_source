# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\jruizaranguren\ideskeleton\tests\test_ideskeleton.py
# Compiled at: 2015-09-23 03:20:24
import pytest, ideskeleton as sut

def test_if_source_path_does_not_exist_error():
    with pytest.raises(IOError):
        sut.build('C:\not_existing_path|')