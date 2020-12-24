# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lbusoni/git/palpao/test/types/deformable_mirror_status_test.py
# Compiled at: 2018-10-01 02:57:02
# Size of source mod 2**32: 837 bytes
import unittest, numpy as np
from palpao.types.deformable_mirror_status import DeformableMirrorStatus

class DeformableMirrorStatusTest(unittest.TestCase):

    def testHappyPath(self):
        numberOfActs = 10
        numberOfModes = 8
        actuatorCommands = np.arange(numberOfActs)
        commandCounter = 42
        status = DeformableMirrorStatus(numberOfActs, numberOfModes, actuatorCommands, commandCounter)
        self.assertEqual(numberOfActs, status.numberOfActuators())
        self.assertEqual(numberOfModes, status.numberOfModes())
        self.assertTrue(np.allclose(actuatorCommands, status.actuatorCommands()))
        self.assertEqual(commandCounter, status.commandCounter())


if __name__ == '__main__':
    unittest.main()