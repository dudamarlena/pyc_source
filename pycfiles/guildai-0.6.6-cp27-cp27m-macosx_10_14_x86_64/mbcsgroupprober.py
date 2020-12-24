# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/chardet/mbcsgroupprober.py
# Compiled at: 2019-09-10 15:18:29
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

    def __init__(self, lang_filter=None):
        super(MBCSGroupProber, self).__init__(lang_filter=lang_filter)
        self.probers = [
         UTF8Prober(),
         SJISProber(),
         EUCJPProber(),
         GB2312Prober(),
         EUCKRProber(),
         CP949Prober(),
         Big5Prober(),
         EUCTWProber()]
        self.reset()