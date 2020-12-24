# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_repr.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 1136 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, time
from concrete import AnnotationMetadata, Tokenization, UUID
from test_helper import read_test_comm

def test_repr_on_comm():
    """Verify that Communications can be converted to strings.

    Checks for the issue addressed in this commit:

    commit 0ee3317454543b63dc7a273d92e5720bb9210b03
    Author: Craig Harman <craig@craigharman.net>
    Date:   Tue Dec 16 13:08:44 2014 -0500

    Fixed infinite recursion bug in Tokenization.__repr__()

    The addition of an in-memory "backpointer" from a Tokenization to the
    Tokenization's enclosing Sentence inadvertently broke the
    (Thrift auto-generated) Tokenization.__repr__() function.  Modified the
    function to ignore the backpointer when generating the string
    representation for a Tokenization.
    """
    comm = read_test_comm()
    comm.__repr__()


def test_repr_on_tokenization():
    tokenization = Tokenization(metadata=AnnotationMetadata(tool='test', timestamp=int(time.time())), uuid=UUID(uuidString='01234567-0123-4567-89ab-cdef89abcdef'))
    tokenization.__repr__()