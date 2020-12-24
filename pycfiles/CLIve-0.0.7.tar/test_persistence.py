# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/cliutils/tests/test_persistence.py
# Compiled at: 2008-10-03 23:10:39
import unittest, os, tempfile
from cliutils.persistence import storage_dir, ConfigStorage

class TestPersistence(unittest.TestCase):
    __module__ = __name__

    def test_storage_dir(self):
        mydir = tempfile.mkdtemp()
        d = storage_dir(mydir)
        self.assertEqual(mydir, d)
        self.assert_(os.path.exists(d))
        mydir = '.testing'
        d2 = storage_dir(mydir)
        config = os.path.expanduser('~/.testing')
        self.assertEqual(d2, config)
        self.assert_(os.path.exists(d2))
        os.rmdir(d)
        os.rmdir(d2)

    def test_config(self):
        filename = tempfile.mkstemp()[1]
        config = ConfigStorage(filename)
        self.assertEqual(config.sections(), [])
        config['sec1']['option2'] = 75
        self.assertEqual(open(filename).read().strip(), '[sec1]\noption2 = 75')
        config2 = ConfigStorage(filename)
        self.assertEqual(config2.keys(), ['sec1'])
        self.assertEqual(config2['sec1'].items(), [('option2', '75')])


if __name__ == '__main__':
    unittest.main()