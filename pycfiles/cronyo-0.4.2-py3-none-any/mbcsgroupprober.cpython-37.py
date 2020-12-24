# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/chardet/chardet/mbcsgroupprober.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 2012 bytes
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