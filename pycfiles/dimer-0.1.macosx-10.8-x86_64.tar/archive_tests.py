# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/archive_tests.py
# Compiled at: 2013-07-11 19:10:33
import unittest, tempfile, numpy as np, pandas as pd, archive

class TestArchive(unittest.TestCase):

    def test_basename(self):
        from archive import basename, archname, join, split
        self.assertEqual(basename('/a/b.h5:ciao'), 'ciao')
        self.assertEqual(archname('/a/b.h5:ciao'), '/a/b.h5')
        self.assertEqual(join('/a/b.h5', 'ciao'), '/a/b.h5:ciao')
        self.assertEqual(('/a/b.h5', 'ciao'), split('/a/b.h5:ciao'))

    def test_io(self):
        from archive import __SPEC_SEP__, __HDF_SUFFIX__, split
        with tempfile.NamedTemporaryFile(suffix='.' + __HDF_SUFFIX__) as (fd):
            p, k = split(__SPEC_SEP__.join((fd.name, 'empty')))
            obj = pd.Series(np.ones((5, )), index=range(5, 10))
            archive.save_object(p, k, obj)
            ro = archive.load_object(p, k)
            self.assertTrue(np.all(ro.values == obj.values))


class TestExp(unittest.TestCase):

    def test_trname(self):
        import experiment
        tn = experiment.this_train_name('/a/something.cfg')
        print tn
        self.assertTrue(tn.startswith('train_something_'))