# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/NameMapper_pure.py
# Compiled at: 2019-09-22 10:12:27
import sys, unittest
try:
    from Cheetah import _namemapper
except ImportError:
    pass

def _setNameMapperFunctions():
    from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrame, valueFromFrameOrSearchList
    from Cheetah.Tests import NameMapper
    for func in [
     NotFound, valueForName, valueFromSearchList,
     valueFromFrame, valueFromFrameOrSearchList]:
        setattr(NameMapper, func.__name__, func)


def setUpModule():
    if 'Cheetah.NameMapper' in sys.modules:
        del sys.modules['Cheetah.NameMapper']
    sys.modules['Cheetah._namemapper'] = None
    _setNameMapperFunctions()
    return


def tearDownModule():
    del sys.modules['Cheetah.NameMapper']
    del sys.modules['Cheetah._namemapper']
    del sys.modules['Cheetah.Tests.NameMapper']
    _setNameMapperFunctions()


class NameMapperTest(unittest.TestCase):

    def test_valueForName(self):
        from Cheetah.NameMapper import valueForName
        self.assertEqual(valueForName('upper', 'upper', True), 'UPPER')