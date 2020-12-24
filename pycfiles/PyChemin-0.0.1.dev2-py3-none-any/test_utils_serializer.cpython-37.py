# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_utils_serializer.py
# Compiled at: 2020-01-17 14:24:45
# Size of source mod 2**32: 894 bytes
import unittest, numpy as np
from pychemia.utils.serializer import generic_serializer

class SerializerTest(unittest.TestCase):

    def test_serializer(self):
        """
        Test (pychemia.utils.serializer)                            :
        """
        a = np.array([1, 2, 3])
        assert generic_serializer(a) == [1, 2, 3]
        b = np.array([[1, 2, 3], [4, 5, 6]])
        assert generic_serializer(b) == [[1, 2, 3], [4, 5, 6]]
        c = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]])
        assert generic_serializer(c) == [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]
        mydict = {'a':a,  'b':b,  'c':c}
        assert generic_serializer(mydict) == {'a':[1, 2, 3],  'b':[
          [
           1, 2, 3], [4, 5, 6]], 
         'c':[
          [
           [
            1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]}