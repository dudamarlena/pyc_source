# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/krikava/.python-virtenvs/omnigraffle-export/lib/python2.7/site-packages/tests/test_omnigraffle_export.py
# Compiled at: 2015-03-12 08:07:44
import os, tempfile, unittest, shutil, time, logging
from omnigraffle_export import omnigraffle
from omnigraffle_export import omnigraffle_export

class OmniGraffleExportTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(OmniGraffleExportTest, self).__init__(methodName)
        self.files_to_remove = []

    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data', 'basic', 'test.graffle')
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        for f in self.files_to_remove:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.unlink(f)

    def testGetCanvasList(self):
        schema = omnigraffle.OmniGraffle().open(self.path)
        self.assertEqual(['Canvas 1', 'Canvas 2'], schema.get_canvas_list())

    def testExport(self):
        schema = omnigraffle.OmniGraffle().open(self.path)
        tmpfile = self.genTempFileName('pdf')
        self.assertTrue(omnigraffle_export.export_one(schema, tmpfile, 'Canvas 1'))
        self.assertFalse(omnigraffle_export.export_one(schema, tmpfile, 'Canvas 1'))
        self.files_to_remove.append(tmpfile)

    def testExportWithForceOption(self):
        schema = omnigraffle.OmniGraffle().open(self.path)
        tmpfile = self.genTempFileName('pdf')
        self.assertTrue(omnigraffle_export.export_one(schema, tmpfile, 'Canvas 1'))
        time.sleep(2)
        self.assertTrue(omnigraffle_export.export_one(schema, tmpfile, 'Canvas 1', force=True))
        self.files_to_remove.append(tmpfile)

    def testNotExportingIfNotChanged(self):
        schema = omnigraffle.OmniGraffle().open(self.path)
        tmpfile = self.genTempFileName('pdf')
        self.assertTrue(omnigraffle_export.export_one(schema, tmpfile, 'Canvas 1'))
        time.sleep(2)
        self.assertFalse(omnigraffle_export.export_one(schema, tmpfile, 'Canvas 1'))
        time.sleep(2)
        self.assertTrue(omnigraffle_export.export_one(schema, tmpfile, 'Canvas 1', force=True))
        self.files_to_remove.append(tmpfile)

    def testExportAll(self):
        tmpdir = tempfile.mkdtemp()
        omnigraffle_export.export(self.path, tmpdir)
        self.assertTrue(os.path.exists(os.path.join(tmpdir, 'Canvas 1.pdf')))
        self.assertTrue(os.path.exists(os.path.join(tmpdir, 'Canvas 2.pdf')))
        self.files_to_remove.append(tmpdir)

    @staticmethod
    def genTempFileName(suffix):
        tmpfile = tempfile.mkstemp(suffix='.pdf')[1]
        os.unlink(tmpfile)
        return tmpfile


if __name__ == '__main__':
    unittest.main()