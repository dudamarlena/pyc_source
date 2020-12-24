# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/mbcsgroupprober.py
# Compiled at: 2013-12-09 06:41:17
from charsetgroupprober import CharSetGroupProber
from utf8prober import UTF8Prober
from sjisprober import SJISProber
from eucjpprober import EUCJPProber
from gb2312prober import GB2312Prober
from euckrprober import EUCKRProber
from big5prober import Big5Prober
from euctwprober import EUCTWProber

class MBCSGroupProber(CharSetGroupProber):

    def __init__(self):
        CharSetGroupProber.__init__(self)
        self._mProbers = [
         UTF8Prober(),
         SJISProber(),
         EUCJPProber(),
         GB2312Prober(),
         EUCKRProber(),
         Big5Prober(),
         EUCTWProber()]
        self.reset()