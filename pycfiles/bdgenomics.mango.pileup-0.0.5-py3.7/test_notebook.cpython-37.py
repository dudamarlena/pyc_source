# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/pileup/test/test_notebook.py
# Compiled at: 2019-09-04 14:12:25
# Size of source mod 2**32: 1401 bytes
import unittest
from bdgenomics.mango.pileup.test import PileupTestCase

class MangoVizExampleTest(PileupTestCase):

    def test_notebook_example(self):
        bedFile = self.exampleFile('chr17.582500-594500.bed')
        alignmentJsonFile = self.dataFile('alignments.ga4gh.chr17.1-250.json')
        testMode = True
        pileupFile = self.notebookFile('pileup-tutorial.py')
        exec(open(pileupFile).read())


if __name__ == '__main__':
    unittest.main()