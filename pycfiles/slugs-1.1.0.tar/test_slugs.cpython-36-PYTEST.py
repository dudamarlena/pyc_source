# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/peter/slugs/slugs/tests/unit/test_slugs.py
# Compiled at: 2018-03-12 11:15:11
# Size of source mod 2**32: 1257 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, testtools

class TestSLUGS(testtools.TestCase):

    def setUp(self):
        super(TestSLUGS, self).setUp()

    def test_version(self):
        """
        Verify that the slugs module has a __version__ attribute and that its
        value is correct.
        """
        slugs = __import__('slugs')
        self.assertTrue(hasattr(slugs, '__version__'))
        version = __import__('slugs.version')
        self.assertTrue(hasattr(version, '__version__'))
        observed = getattr(slugs, '__version__')
        expected = getattr(version, '__version__')
        self.assertEqual(expected, observed)