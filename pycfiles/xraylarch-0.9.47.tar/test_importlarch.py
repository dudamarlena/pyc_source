# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Newville/Codes/xraylarch/tests/test_importlarch.py
# Compiled at: 2017-04-05 21:43:24
""" Larch Tests Version 1 """
import unittest, time, ast, numpy as np
from sys import version_info
from utils import TestCase

class Test1(TestCase):
    """testing of asteval"""

    def test1_import(self):
        imported = False
        try:
            import larch
            imported = True
        except:
            pass

        assert imported

    def test2_create_interp(self):
        import larch
        self.larch = larch.Interpreter()
        self.symtable = self.larch.symtable
        assert self.larch is not None
        assert self.symtable is not None
        return

    def test3_set_symbol(self):
        st = self.symtable
        st.set_symbol('_main.a', value=1)
        st.new_group('g1', s='a string', en=722)
        st.set_symbol('_sys.var', value=1)
        st.set_symbol('_main.b', value='value of b')
        st.set_symbol('_main.g1.t', value='another string')
        st.set_symbol('_main.g1.d', value={'yes': 1, 'no': 0})
        st.new_group('g2')
        st.set_symbol('g2.data', value=[1, 2, 3])
        st.set_symbol('g2.a', value='hello')
        a = st.get_symbol('_main.a')
        assert a == 1
        a = st.get_symbol('_main.g1.d')
        assert a['yes'] == 1
        a = st.get_symbol('g2.data')
        assert len(a) == 3


if __name__ == '__main__':
    for suite in (Test1,):
        suite = unittest.TestLoader().loadTestsFromTestCase(suite)
        unittest.TextTestRunner(verbosity=2).run(suite)