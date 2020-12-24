# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/truepy/__init__.py
# Compiled at: 2020-01-23 12:02:01
# Size of source mod 2**32: 1055 bytes
import xml.etree.ElementTree as _tostring
from xml.etree.ElementTree import fromstring
import sys
if sys.version_info.major > 2:

    def tostring(e):
        return str(_tostring(e), 'ascii')


else:
    tostring = _tostring
from ._info import *
from ._license_data import LicenseData
from ._license import License
from ._name import Name