# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_forward.py
# Compiled at: 2019-01-13 18:15:19
# Size of source mod 2**32: 142 bytes
from parsr import Forward, Literal

def test_forward():
    true = Forward()
    true <= Literal('True', value=True)
    assert true('True')