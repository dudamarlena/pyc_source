# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/PyChemia/tests/test_1_doctest_utils.py
# Compiled at: 2019-05-14 13:43:02
# Size of source mod 2**32: 1891 bytes
import doctest, unittest
from .doctest_2to3 import doctest_suite

def broken_function():
    raise Exception('This is broken')


class MyTestCase(unittest.TestCase):

    def test(self):
        """
        DocTests (pychemia.utils) [exceptions]                       :
        """
        from pychemia.utils.periodic import atomic_number
        with self.assertRaises(Exception) as (context):
            atomic_number(['H', 'A'])
        from pychemia.utils.computing import read_file
        with self.assertRaises(Exception) as (context):
            read_file('/dev/abc')
        from pychemia.utils.computing import get_float
        with self.assertRaises(Exception) as (context):
            get_float('3i')


def test_periodic():
    """
    DocTests (pychemia.utils.periodic)                           :
    """
    import pychemia.utils.periodic
    dt = doctest.testmod((pychemia.utils.periodic), verbose=True)
    assert dt.failed == 0


def test_mathematics():
    """
    DocTests (pychemia.utils.mathematics)                        :
    """
    import pychemia.utils.mathematics
    dt = doctest.testmod((pychemia.utils.mathematics), verbose=True)
    assert dt.failed == 0


def test_computing():
    """
    DocTests (pychemia.utils.computing)                          :
    """
    import pychemia.utils.computing
    suite = unittest.TestSuite()
    suite.addTest(doctest_suite(pychemia.utils.computing))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    assert result.wasSuccessful()


if __name__ == '__main__':
    unittest.main(defaultTest='test_computing')
    unittest.main()