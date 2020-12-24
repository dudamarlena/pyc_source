# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/padraig/libNeuroML/neuroml/test/test_integration.py
# Compiled at: 2017-07-07 13:05:49
import neuroml, neuroml.arraymorph as am, neuroml.writers as writers
try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """
        Make an optimized morphology, add a couple of segments, save it
        and then load it back
        """
        vertices = [
         [
          0, 0, 0, 0.1], [1, 0, 0, 0.2], [2, 0, 0, 0.3], [3, 0, 0, 0.4]]
        connectivity = [-1, 0, 1, 2]
        self.optimized_morphology = am.ArrayMorphology(vertices=vertices, connectivity=connectivity, id='arraymorph_test')
        seg = neuroml.Segment()
        doc = neuroml.NeuroMLDocument()
        cell = neuroml.Cell()

    def test_to_neuroml_morphology_and_write(self):
        neuroml_morphology = self.optimized_morphology.to_neuroml_morphology(id='Test')
        self.assertEqual(neuroml_morphology.id, 'Test')
        self.assertEqual(len(neuroml_morphology.segments), 3)
        self.assertIsNone(writers.NeuroMLWriter.write(neuroml_morphology, '/dev/null'))

    def test_arraymorph_properties(self):
        self.assertEqual(self.optimized_morphology.id, 'arraymorph_test')

    def test_arraymorph_write(self):
        writers.NeuroMLWriter.write(self.optimized_morphology, '/dev/null')