# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/aiding.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 1544 bytes
"""
aiding.py

"""
from __future__ import division
from ..aid.aiding import reverseCamel, nameToPath, repack, just, isPath, isIdentifier, isIdentPub, packByte, unpackByte, hexize, unhexize, denary2BinaryStr, dec2BinStr, printHex, printDecimal, crc16, crc64, ocfn, load, dump, dumpJson, loadJson
from ..aid.timing import Timer, MonoTimer, StoreTimer, totalSeconds
from ..aid.classing import metaclassify, NonStringIterable, NonStringSequence, nonStringIterable, nonStringSequence
from ..aid.navigating import Sign, Delta, Wrap2, MoveByHSD, MoveToHSD, RotateFSToNE, RotateNEToFS, AlongCrossTrack, CrabSpeed, CrossProduct3D, DotProduct, PerpProduct2D, DistancePointToTrack2D, SpheroidLLLLToDNDE, SphereLLLLToDNDE, SphereLLByDNDEToLL, SphereLLbyRBtoLL, SphereLLLLToRB, RBToDNDE, DNDEToRB, DegMinToFracDeg, FracDegToDegMin, FracDegToHuman, HumanLatToFracDeg, HumanLonToFracDeg, HumanToFracDeg, HumanLLToFracDeg, Midpoint, Endpoint
from ..aid.blending import Blend0, Blend1, Blend2, Blend3