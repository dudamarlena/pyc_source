# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_io.py
# Compiled at: 2020-01-17 14:31:19
# Size of source mod 2**32: 625 bytes
import pychemia, tempfile
from .samples import CaTiO3

def test_xyz():
    """
    Test (pychemia.io.xyz)                                      :
    """
    st1 = CaTiO3()
    st1.set_periodicity(False)
    file = tempfile.NamedTemporaryFile()
    pychemia.io.xyz.save(st1, file.name)
    st2 = pychemia.io.xyz.load(file.name)
    assert st1 == st2


def test_ascii():
    """
    Test (pychemia.io.ascii)                                    :
    """
    st1 = CaTiO3()
    file = tempfile.NamedTemporaryFile()
    pychemia.io.ascii.save(st1, file.name)
    st2 = pychemia.io.ascii.load(file.name)
    return (st1, st2)