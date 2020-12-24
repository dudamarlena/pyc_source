# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/mcomplex_base.py
# Compiled at: 2018-08-17 21:53:27


class McomplexEngine(object):
    """
    A base for classes that modify or add extra structure to a t3mlite.Mcomplex.
    """

    def __init__(self, mcomplex):
        """
        Constructor takes the t3mlite.Mcomplex we want to operate on.

        Any modifications to the Mcomplex are not supposed to be done in the
        constructor itself but by other methods on the derived class.

        Static convenience methods can offer functionality such as constructing
        an engine and perform certain modifications, see, e.g.,
        FundamentalPolyhedronEngine.fromManifoldAndShapesMatchingSnapPea.
        """
        self.mcomplex = mcomplex