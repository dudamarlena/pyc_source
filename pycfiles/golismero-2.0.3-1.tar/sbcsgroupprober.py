# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/sbcsgroupprober.py
# Compiled at: 2013-12-09 06:41:17
import constants, sys
from charsetgroupprober import CharSetGroupProber
from sbcharsetprober import SingleByteCharSetProber
from langcyrillicmodel import Win1251CyrillicModel, Koi8rModel, Latin5CyrillicModel, MacCyrillicModel, Ibm866Model, Ibm855Model
from langgreekmodel import Latin7GreekModel, Win1253GreekModel
from langbulgarianmodel import Latin5BulgarianModel, Win1251BulgarianModel
from langhungarianmodel import Latin2HungarianModel, Win1250HungarianModel
from langthaimodel import TIS620ThaiModel
from langhebrewmodel import Win1255HebrewModel
from hebrewprober import HebrewProber

class SBCSGroupProber(CharSetGroupProber):

    def __init__(self):
        CharSetGroupProber.__init__(self)
        self._mProbers = [
         SingleByteCharSetProber(Win1251CyrillicModel),
         SingleByteCharSetProber(Koi8rModel),
         SingleByteCharSetProber(Latin5CyrillicModel),
         SingleByteCharSetProber(MacCyrillicModel),
         SingleByteCharSetProber(Ibm866Model),
         SingleByteCharSetProber(Ibm855Model),
         SingleByteCharSetProber(Latin7GreekModel),
         SingleByteCharSetProber(Win1253GreekModel),
         SingleByteCharSetProber(Latin5BulgarianModel),
         SingleByteCharSetProber(Win1251BulgarianModel),
         SingleByteCharSetProber(Latin2HungarianModel),
         SingleByteCharSetProber(Win1250HungarianModel),
         SingleByteCharSetProber(TIS620ThaiModel)]
        hebrewProber = HebrewProber()
        logicalHebrewProber = SingleByteCharSetProber(Win1255HebrewModel, constants.False, hebrewProber)
        visualHebrewProber = SingleByteCharSetProber(Win1255HebrewModel, constants.True, hebrewProber)
        hebrewProber.set_model_probers(logicalHebrewProber, visualHebrewProber)
        self._mProbers.extend([hebrewProber, logicalHebrewProber, visualHebrewProber])
        self.reset()