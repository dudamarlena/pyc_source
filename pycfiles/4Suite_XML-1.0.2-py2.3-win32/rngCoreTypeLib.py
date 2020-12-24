# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\rngCoreTypeLib.py
# Compiled at: 2005-01-07 01:28:10
import re

class stringType(unicode):
    """
    This class is strictly identical to the python's unicode type
 """
    __module__ = __name__


class tokenType(unicode):
    __module__ = __name__

    def __new__(cls, value=''):
        return unicode.__new__(cls, re.sub('[\n\t ]+', ' ', value).strip())