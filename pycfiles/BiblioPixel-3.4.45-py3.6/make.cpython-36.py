# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/make.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 889 bytes
import tempfile
from unittest.mock import patch
from bibliopixel.project import project
from bibliopixel.util import data_file
from ..mark_tests import SKIP_LONG_TESTS

def make_project(data):
    if isinstance(data, dict):
        desc = data
        name = None
    else:
        if not isinstance(data, str):
            raise ValueError('Cannot understand data %s' % data)
        else:
            if '{' in data or ':' in data:
                fp = tempfile.NamedTemporaryFile(mode='w')
                fp.write(data)
                fp.seek(0)
                name = fp.name
            else:
                name = data
            desc = data_file.load(name)
    return project.project(desc, root_file=name)


def make(data, run_start=not SKIP_LONG_TESTS):
    project = make_project(data)
    if run_start:
        with patch('time.sleep', autospec=True):
            project.animation.start()
    return project.animation