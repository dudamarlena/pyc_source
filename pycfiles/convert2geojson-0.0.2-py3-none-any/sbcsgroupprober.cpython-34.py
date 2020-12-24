# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/sbcsgroupprober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 3291 bytes
from .charsetgroupprober import CharSetGroupProber
from .sbcharsetprober import SingleByteCharSetProber
from .langcyrillicmodel import Win1251CyrillicModel, Koi8rModel, Latin5CyrillicModel, MacCyrillicModel, Ibm866Model, Ibm855Model
from .langgreekmodel import Latin7GreekModel, Win1253GreekModel
from .langbulgarianmodel import Latin5BulgarianModel, Win1251BulgarianModel
from .langhungarianmodel import Latin2HungarianModel, Win1250HungarianModel
from .langthaimodel import TIS620ThaiModel
from .langhebrewmodel import Win1255HebrewModel
from .hebrewprober import HebrewProber

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
        logicalHebrewProber = SingleByteCharSetProber(Win1255HebrewModel, False, hebrewProber)
        visualHebrewProber = SingleByteCharSetProber(Win1255HebrewModel, True, hebrewProber)
        hebrewProber.set_model_probers(logicalHebrewProber, visualHebrewProber)
        self._mProbers.extend([hebrewProber, logicalHebrewProber,
         visualHebrewProber])
        self.reset()