# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/mbcsgroupprober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 1967 bytes
from .charsetgroupprober import CharSetGroupProber
from .utf8prober import UTF8Prober
from .sjisprober import SJISProber
from .eucjpprober import EUCJPProber
from .gb2312prober import GB2312Prober
from .euckrprober import EUCKRProber
from .cp949prober import CP949Prober
from .big5prober import Big5Prober
from .euctwprober import EUCTWProber

class MBCSGroupProber(CharSetGroupProber):

    def __init__(self):
        CharSetGroupProber.__init__(self)
        self._mProbers = [
         UTF8Prober(),
         SJISProber(),
         EUCJPProber(),
         GB2312Prober(),
         EUCKRProber(),
         CP949Prober(),
         Big5Prober(),
         EUCTWProber()]
        self.reset()