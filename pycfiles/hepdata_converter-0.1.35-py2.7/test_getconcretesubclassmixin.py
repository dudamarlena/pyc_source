# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/testsuite/test_getconcretesubclassmixin.py
# Compiled at: 2020-03-05 14:33:22
import abc, unittest
from hepdata_converter.common import GetConcreteSubclassMixin

class ParserTestSuite(unittest.TestCase):
    """Test suite for Parser factory class
    """

    def test_get_all_subclasses(self):

        class A(GetConcreteSubclassMixin):
            pass

        class AB(A):
            pass

        class AC(A):
            pass

        class AAB(AB):
            __metaclass__ = abc.ABCMeta

            @abc.abstractmethod
            def abstract(self):
                pass

        self.assertEqual(set([AB, AC]), set(A.get_all_subclasses()))
        self.assertEqual(set([AB, AC, AAB]), set(A.get_all_subclasses(include_abstract=True)))