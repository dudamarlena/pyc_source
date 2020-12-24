# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/fixtures.py
# Compiled at: 2018-02-26 21:32:40
# Size of source mod 2**32: 163 bytes
import pytest
from taskloaf.run import null_comm_worker

@pytest.fixture(scope='function')
def w():
    with null_comm_worker() as (worker):
        yield worker