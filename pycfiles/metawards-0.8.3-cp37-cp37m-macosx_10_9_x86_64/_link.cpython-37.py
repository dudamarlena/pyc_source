# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/_link.py
# Compiled at: 2020-04-20 09:02:59
# Size of source mod 2**32: 674 bytes
from dataclasses import dataclass
__all__ = [
 'Link']

@dataclass
class Link:
    __doc__ = 'This is a link between nodes in the network'
    ifrom = None
    ifrom: int
    ito = None
    ito: int
    weight = None
    weight: float
    suscept = None
    suscept: float
    distance = None
    distance: float
    A = None
    A: int