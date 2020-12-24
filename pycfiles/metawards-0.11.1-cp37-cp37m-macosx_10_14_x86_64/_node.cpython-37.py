# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_node.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 1348 bytes
from dataclasses import dataclass
__all__ = [
 'Node']

@dataclass
class Node:
    __doc__ = 'This class represents an electoral ward (node) in the network'
    label = None
    label: int
    begin_to = None
    begin_to: int
    end_to = None
    end_to: int
    self_w = None
    self_w: int
    begin_p = None
    begin_p: int
    end_p = None
    end_p: int
    self_p = None
    self_p: int
    day_foi = 0.0
    day_foi: float
    night_foi = 0.0
    night_foi: float
    weekend_foi = 0.0
    weekend_foi: float
    play_suscept = 0.0
    play_suscept: float
    save_play_suscept = 0.0
    save_play_suscept: float
    denominator_n = 0.0
    denominator_n: float
    denominator_d = 0.0
    denominator_d: float
    denominator_p = 0.0
    denominator_p: float
    denominator_pd = 0.0
    denominator_pd: float
    x = 0.0
    x: float
    y = 0.0
    y: float