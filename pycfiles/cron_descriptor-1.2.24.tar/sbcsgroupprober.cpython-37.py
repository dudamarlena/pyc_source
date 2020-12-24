# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/chardet/chardet/sbcsgroupprober.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 3546 bytes
from .charsetgroupprober import CharSetGroupProber
from .sbcharsetprober import SingleByteCharSetProber
from .langcyrillicmodel import Win1251CyrillicModel, Koi8rModel, Latin5CyrillicModel, MacCyrillicModel, Ibm866Model, Ibm855Model
from .langgreekmodel import Latin7GreekModel, Win1253GreekModel
from .langbulgarianmodel import Latin5BulgarianModel, Win1251BulgarianModel
from .langthaimodel import TIS620ThaiModel
from .langhebrewmodel import Win1255HebrewModel
from .hebrewprober import HebrewProber
from .langturkishmodel import Latin5TurkishModel

class SBCSGroupProber(CharSetGroupProber):

    def __init__(self):
        super(SBCSGroupProber, self).__init__()
        self.probers = [
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
         SingleByteCharSetProber(TIS620ThaiModel),
         SingleByteCharSetProber(Latin5TurkishModel)]
        hebrew_prober = HebrewProber()
        logical_hebrew_prober = SingleByteCharSetProber(Win1255HebrewModel, False, hebrew_prober)
        visual_hebrew_prober = SingleByteCharSetProber(Win1255HebrewModel, True, hebrew_prober)
        hebrew_prober.set_model_probers(logical_hebrew_prober, visual_hebrew_prober)
        self.probers.extend([hebrew_prober, logical_hebrew_prober,
         visual_hebrew_prober])
        self.reset()