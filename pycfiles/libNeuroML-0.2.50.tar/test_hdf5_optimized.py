# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/padraig/libNeuroML/neuroml/test/test_hdf5_optimized.py
# Compiled at: 2019-11-06 05:47:09
"""
Unit tests for loaders

"""
from neuroml import loaders
import neuroml.writers as writers, os
from neuroml.test.test_xml_parser import compare
try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLHDF5Optimized(unittest.TestCase):
    base_dir = os.path.dirname(__file__)

    def runTest(self):
        print 'Running tests in TestNeuroMLHDF5Optimized'

    def test_write_load(self):
        for f in ['simplenet.nml', 'MediumNet.net.nml']:
            file_name = '%s/../examples/test_files/%s' % (self.base_dir, f)
            print 'Loading %s' % file_name
            nml_doc0 = loaders.read_neuroml2_file(file_name, include_includes=True)
            summary0 = nml_doc0.summary()
            print summary0
            nml_h5_file = '%s/../examples/tmp/%s__1.h5' % (self.base_dir, f)
            writers.NeuroMLHdf5Writer.write(nml_doc0, nml_h5_file)
            print 'Written to: %s' % nml_h5_file
            nml_doc1 = loaders.read_neuroml2_file(nml_h5_file, include_includes=True, optimized=True)
            summary1 = nml_doc1.summary().replace(' (optimized)', '')
            print '\n' + summary1
            compare(summary0, summary1)
            nml_h5_file_2 = '%s/../examples/tmp/%s__2.h5' % (self.base_dir, f)
            writers.NeuroMLHdf5Writer.write(nml_doc1, nml_h5_file_2)
            print 'Written to: %s' % nml_h5_file_2
            nml_doc2 = loaders.read_neuroml2_file(nml_h5_file_2, include_includes=True)
            summary2 = nml_doc2.summary()
            print 'Reloaded: %s' % nml_h5_file_2
            print '\n' + summary2
            compare(summary0, summary2)
            nml_h5_file_3 = '%s/../examples/tmp/%s__3.nml' % (self.base_dir, f)
            writers.NeuroMLWriter.write(nml_doc1, nml_h5_file_3)
            print 'Written to: %s' % nml_h5_file_3
            nml_doc3 = loaders.read_neuroml2_file(nml_h5_file_3, include_includes=True)
            summary3 = nml_doc3.summary()
            print 'Reloaded: %s' % nml_h5_file_3
            print '\n' + summary3
            compare(summary0, summary3)


if __name__ == '__main__':
    tnxp = TestNeuroMLHDF5Optimized()
    tnxp.test_write_load()