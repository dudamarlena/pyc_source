# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/PyChemia/tests/test_1_doctest_crystal.py
# Compiled at: 2019-05-14 13:43:02
# Size of source mod 2**32: 575 bytes
import doctest

def test_symmetry():
    """
    DocTests (pychemia.crystal.symmetry)                         :
    """
    import pychemia
    if pychemia.HAS_SPGLIB:
        import pychemia.crystal
        dt = doctest.testmod((pychemia.crystal.symmetry), verbose=True)
        assert dt.failed == 0


def test_lattice():
    """
    DocTests (pychemia.crystal.lattice)                          :
    """
    import pychemia.crystal.lattice
    dt = doctest.testmod((pychemia.crystal.lattice), verbose=True, optionflags=(doctest.NORMALIZE_WHITESPACE))
    assert dt.failed == 0