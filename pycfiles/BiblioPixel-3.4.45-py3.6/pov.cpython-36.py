# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/layout/pov.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 297 bytes
import math, threading, time
from .matrix import Matrix
from ..util import deprecated
if deprecated.allowed():

    class POV(Matrix):

        def __init__(self, *args, **kwds):
            raise ValueError('layout.POV has been removed. Use animation.POV')


    LEDPOV = POV