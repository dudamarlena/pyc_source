# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lbusoni/git/palpao/test/client/simulated_deformable_mirror_client_test.py
# Compiled at: 2018-10-01 17:20:46
# Size of source mod 2**32: 1710 bytes
import unittest, numpy as np
from palpao.client.simulated_deformable_mirror_client import SimulatedDeformableMirrorClient
from test.fake_time_mod import FakeTimeMod

class SimulatedDeformableMirrorClientTest(unittest.TestCase):

    def setUp(self):
        self.timeMod = FakeTimeMod()
        self.dm = SimulatedDeformableMirrorClient(timeModule=(self.timeMod))
        self.nModes = SimulatedDeformableMirrorClient.N_MODES

    def testGetNumberOfModes(self):
        nModes = self.dm.getNumberOfModes()
        self.assertEqual(SimulatedDeformableMirrorClient.N_MODES, nModes)

    def testSetAndGetShape(self):
        wantShape = np.arange(self.nModes)
        self.dm.setShape(wantShape)
        getShape = self.dm.getShape()
        self.assertTrue(np.array_equal(wantShape, getShape))

    def testLoopSequence(self):
        timeStepInSeconds = 0.1
        seqNumberOfTimeSteps = 100
        initialShape = np.arange(self.nModes) * 42
        self.dm.setShape(initialShape)
        seq = np.arange(self.nModes * seqNumberOfTimeSteps).reshape(self.nModes, seqNumberOfTimeSteps)
        self.dm.loadShapeSequence(seq, timeStepInSeconds)
        self.dm.startShapeSequence()
        shapeBefore = self.dm.getShape()
        self.timeMod.sleep(timeStepInSeconds * 2)
        shapeAfter = self.dm.getShape()
        self.assertFalse(np.array_equal(shapeAfter, shapeBefore))
        self.dm.stopShapeSequence()
        shapeBefore = self.dm.getShape()
        self.timeMod.sleep(timeStepInSeconds * 2)
        shapeAfter = self.dm.getShape()
        self.assertTrue(np.array_equal(shapeAfter, shapeBefore))


if __name__ == '__main__':
    unittest.main()