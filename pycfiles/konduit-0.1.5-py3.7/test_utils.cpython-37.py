# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_utils.py
# Compiled at: 2020-04-20 03:12:39
# Size of source mod 2**32: 576 bytes
import os, pytest
from konduit.utils import *

@pytest.mark.unit
def test_unix_replacement():
    file_path = 'C:\\foo\\bar;baz'
    unix_path = to_unix_path(file_path)
    assert unix_path == 'C:/foo/bar{}baz'.format(os.pathsep)
    step_config = {'python_path':file_path, 
     'bar':42,  'keep_this':file_path}
    unix_step_config = update_dict_with_unix_paths(step_config)
    assert unix_step_config['python_path'] == 'C:/foo/bar{}baz'.format(os.pathsep)
    assert unix_step_config['bar'] == 42
    assert unix_step_config['keep_this'] == file_path