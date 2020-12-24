# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/fstTest.py
# Compiled at: 2014-08-29 00:09:34
from fst import Fst
import unittest

class FstTests(unittest.TestCase):

    def setUp(self):
        states = [
         (0, 'a', 'b', 1),
         (0, 'b', 'a', 1),
         (1, 'b', 'a', 1)]
        self.fst = Fst(states, ['a', 'b'], ['a', 'b'], 0, 1)

    def testInverse(self):
        """
        This function is testing if the inverse is as it should be.
        """
        states = [
         (0, 'b', 'a', 1),
         (0, 'a', 'b', 1),
         (1, 'a', 'b', 1)]
        inverseFst = Fst(states, ['a', 'b'], ['a', 'b'], 0, 1)
        realInverseFst = self.fst.inverse()
        errorMsg = '\nThe inverse of fst:\n' + str(self.fst) + '\n\nshould be like:\n' + str(inverseFst) + "\n\nbut it's like:\n" + str(realInverseFst)
        self.assert_(inverseFst == realInverseFst, msg=errorMsg)


if __name__ == '__main__':
    unittest.main()