# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/utils/tests/test_io.py
# Compiled at: 2019-09-20 05:21:31
# Size of source mod 2**32: 597 bytes
import os, platform, pytest
from skhubness.utils.io import create_tempfile_preferably_in_dir

@pytest.mark.parametrize('directory', [None, '/does/not/exist/kluawev'])
@pytest.mark.parametrize('persistent', [True, False])
def test_tempfile(directory, persistent):
    f = create_tempfile_preferably_in_dir(directory=directory, persistent=persistent)
    assert isinstance(f, str)
    if persistent:
        if platform.system() != 'Windows':
            os.remove(f)