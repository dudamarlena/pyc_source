# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\landon\dropbox\documents\pycharmprojects\mezzanine-wiki\mezzanine_wiki\utils.py
# Compiled at: 2018-01-31 08:31:33
# Size of source mod 2**32: 188 bytes
import re
from django.conf import settings

def urlize_title(title):
    return re.sub('\\s+', '_', title)


def deurlize_title(title):
    return re.sub('[_\\s]+', ' ', title)