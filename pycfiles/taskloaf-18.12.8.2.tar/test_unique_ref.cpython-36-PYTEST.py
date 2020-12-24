# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_unique_ref.py
# Compiled at: 2018-02-21 18:41:41
# Size of source mod 2**32: 611 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from taskloaf.new_allocator import ShmemAllocator, BlockManager
from taskloaf.shmem import page4kb
import copy, pickle

class UniqueRefCopy(Exception):
    pass


class UniqueRef:

    def __init__(self, obj):
        self.obj = obj

    def __getstate__(self):
        raise UniqueRefCopy('UniqueRef can only be moved')


def test_no_copy():
    ref = UniqueRef(1)
    ref2 = copy.copy(ref)


def test_no_serialize():
    ref = UniqueRef(1)
    ref2 = pickle.dumps(ref)