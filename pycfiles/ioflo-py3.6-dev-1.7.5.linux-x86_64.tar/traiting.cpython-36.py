# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/traiting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 615 bytes
"""traiting.py goal action module

"""
import time, struct
from collections import deque
import inspect
from ..aid.sixing import *
from ..aid.odicting import odict
from . import acting
from ..aid.consoling import getConsole
console = getConsole()

class Trait(acting.Actor):
    __doc__ = 'Trait Class for configuration feature\n\n    '
    Registry = odict()


class TraitDepth(Trait):
    __doc__ = 'TraitDepth Trait\n\n    '

    def action(self, value=0.0, **kw):
        """Use depth """
        console.profuse('Use depth of {0:0.3f}\n'.format(value))