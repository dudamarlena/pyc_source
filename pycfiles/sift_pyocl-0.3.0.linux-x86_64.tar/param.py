# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kieffer/workspace/sift_pyocl/build/lib.linux-x86_64-2.7/sift_pyocl/param.py
# Compiled at: 2014-10-24 01:43:39


class Enum(dict):
    """
    Simple class half way between a dict and a class, behaving as an enum
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError


par = Enum(OctaveMax=100000, DoubleImSize=0, order=3, InitSigma=1.6, BorderDist=5, Scales=3, PeakThresh=10.200000000000001 / 3.0, EdgeThresh=0.06, EdgeThresh1=0.08, OriBins=36, OriSigma=1.5, OriHistThresh=0.8, MaxIndexVal=0.2, MagFactor=3, IndexSigma=1.0, IgnoreGradSign=0, MatchRatio=0.73, MatchXradius=1000000.0, MatchYradius=1000000.0, noncorrectlylocalized=0)