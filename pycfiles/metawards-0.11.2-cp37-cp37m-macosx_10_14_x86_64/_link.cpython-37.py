# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_link.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 621 bytes
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