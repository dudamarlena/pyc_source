# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/tests/test_conf.py
# Compiled at: 2011-05-01 06:46:14
import os, unittest, dfuzz
from dfuzz.core import conf

class testConf(unittest.TestCase):

    def setUp(self):
        def_path = os.path.join(os.path.dirname(dfuzz.__file__), 'cfg')
        self.c = conf.Config(def_path, 'defaults.ini')
        self.attr = 'timeout'

    def test_init(self):
        pass

    def test_attrs(self):
        self.assertTrue(hasattr(self.c, self.attr))

    def test_as_dict(self):
        self.assertEqual(self.c.as_dict()[self.attr], getattr(self.c, self.attr))

    def test_dict_update(self):
        setattr(self.c, self.attr, 'new')
        self.assertEqual(self.c.as_dict()[self.attr], getattr(self.c, self.attr))


if __name__ == '__main__':
    unittest.main()