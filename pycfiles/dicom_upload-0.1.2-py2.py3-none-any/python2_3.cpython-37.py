# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/python2_3.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1726 bytes
__doc__ = '\nHelper functions that smooth out the differences between python 2 and 3.\n'
import sys

def asUnicode(x):
    if sys.version_info[0] == 2:
        if isinstance(x, unicode):
            return x
        if isinstance(x, str):
            return x.decode('UTF-8')
        return unicode(x)
    else:
        return str(x)


def cmpToKey(mycmp):
    """Convert a cmp= function into a key= function"""

    class K(object):

        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


def sortList(l, cmpFunc):
    if sys.version_info[0] == 2:
        l.sort(cmpFunc)
    else:
        l.sort(key=(cmpToKey(cmpFunc)))


if sys.version_info[0] == 3:
    import builtins
    builtins.basestring = str
    basestring = str

    def cmp(a, b):
        if a > b:
            return 1
        if b > a:
            return -1
        return 0


    builtins.cmp = cmp
    builtins.xrange = range