# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_1_doctest_core.py
# Compiled at: 2019-12-13 10:17:40
# Size of source mod 2**32: 1184 bytes
import doctest, unittest
from pychemia.core.composition import Composition
from .doctest_2to3 import doctest_suite

def test_structure():
    """
    DocTests (pychemia.core.structure)                           :
    """
    import pychemia.core.structure
    dt = doctest.testmod((pychemia.core.structure), verbose=True)
    assert dt.failed == 0


def test_composition():
    """
    DocTests (pychemia.core.composition)                         :
    """
    import pychemia.core.composition
    dt = doctest.testmod((pychemia.core.composition), verbose=True)
    assert dt.failed == 0


def div(a, b):
    return a / b


class raiseTest(unittest.TestCase):

    def testraise(self):
        """
        Test exceptions in Composition                               :
        """
        a = Composition('H2O')
        self.assertRaises(ValueError, a.covalent_volume, 'torus')


if __name__ == '__main__':
    test_composition()
    test_structure()
    unittest.main()