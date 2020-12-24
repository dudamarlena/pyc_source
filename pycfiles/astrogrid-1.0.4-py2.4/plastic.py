# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/plastic.py
# Compiled at: 2007-05-29 11:51:01
__id__ = '$Id: plastic.py 97 2007-05-29 15:51:00Z eddie $'
__docformat__ = 'restructuredtext en'
from astrogrid import acr
from decorators import deprecated

@deprecated
def broadcast(*args, **kwargs):
    return acr.plastic.broadcast(*args, **kwargs)