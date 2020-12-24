# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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