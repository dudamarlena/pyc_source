# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    return (
     st1, st2)