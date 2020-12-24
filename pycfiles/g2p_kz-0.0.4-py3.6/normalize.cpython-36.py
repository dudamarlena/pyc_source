# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kzphoneme\normalize.py
# Compiled at: 2019-09-27 07:23:18
# Size of source mod 2**32: 2396 bytes
import re

class Normalize(object):

    def __init__(self, *args, **kwargs):
        (super(Normalize, self).__init__)(*args, **kwargs)

    @staticmethod
    def _arab_norm(string):
        string = re.sub('[ٴ]', 'ء', string)
        string = re.sub('[ﺎﺍ]', 'ا', string)
        string = re.sub('[ٵ]', 'ءا', string)
        string = re.sub('[ﺩﺪ]', 'د', string)
        string = re.sub('[ﺭﺮ]', 'ر', string)
        string = re.sub('[ﺯﺰ]', 'ز', string)
        string = re.sub('[ﺏﺐﺑﺒ]', 'ب', string)
        string = re.sub('[ﺕﺖﺗﺘ]', 'ت', string)
        string = re.sub('[ﺝﺞﺟﺠ]', 'ج', string)
        string = re.sub('[ﺡﺢﺣﺤ]', 'ح', string)
        string = re.sub('[ﺱﺲﺳﺴ]', 'س', string)
        string = re.sub('[ﺵﺶﺷﺸ]', 'ش', string)
        string = re.sub('[ﻉﻊﻋﻌ]', 'ع', string)
        string = re.sub('[ﻑﻒﻓﻔ]', 'ف', string)
        string = re.sub('[ﻕﻖﻗﻘ]', 'ق', string)
        string = re.sub('[ﻙﻚﻛﻜ]', 'ك', string)
        string = re.sub('[ﻝﻞﻟﻠ]', 'ل', string)
        string = re.sub('[ﻡﻢﻣﻤ]', 'م', string)
        string = re.sub('[ﻥﻦﻧﻨ]', 'ن', string)
        string = re.sub('[ﻯﻰﯨﯩ]', 'ى', string)
        string = re.sub('[ﻱﻲﻳﻴ]', 'ي', string)
        string = re.sub('[ﭖﭗﭘﭙ]', 'پ', string)
        string = re.sub('[ﭺﭻﭼﭽ]', 'چ', string)
        string = re.sub('[ﯓﯔﯕﯖ]', 'ڭ', string)
        string = re.sub('[ﮒﮓﮔﮕ]', 'گ', string)
        string = re.sub('[ﮪﮫﮬﮭ]', 'ھ', string)
        string = re.sub('[ﻭﻮ]', 'و', string)
        string = re.sub('[ﯙﯚ]', 'ۆ', string)
        string = re.sub('[ﯗﯘ]', 'ۇ', string)
        string = re.sub('[ﯞﯟ]', 'ۋ', string)
        string = re.sub('[ﻩﻪ]', 'ه', string)
        string = re.sub('[ٶ]', 'ءو', string)
        string = re.sub('[ٷ]', 'ءۇ', string)
        string = re.sub('[ٸ]', 'ءى', string)
        return string

    @staticmethod
    def _cyril_norm(string):
        return string.lower()

    def norm(self, string: str, script='arab'):
        if script == 'arab':
            return self._arab_norm(string)
        else:
            if script == 'cyril':
                return self._cyril_norm(string)
            return string