# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/narmer/stats.py
# Compiled at: 2015-05-12 23:59:21
"""narmer.stats

The stats module defines functions for calculating various statistical data
about linguistic objects.

Currently implements:
    Weissman score calculation

Copyright 2015 by Christopher C. Little.
This file is part of Narmer.

Narmer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Narmer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Narmer. If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals
from __future__ import division
import math

def weissman(r_tar, t_tar, r_src, t_src, alpha=1):
    u"""Return the Weissman score based on entered statistics

    Arguments:
    r_tar -- the target algorithm's compression ratio
    t_tar -- the target algorithm's compression time
    r_src -- a standard algorithm's compression ratio
    t_src -- a standard algorithm's compression time
    alpha -- a scaling constant (1 by default)

    The score is:
    W = α * (r / r_bar) * (log(t_bar) / log(t))

    In practice, the score can be used to rate time-intensive tasks on the
    basis of other metrics, also, e.g. F_1 score.

    Sources:
    http://spectrum.ieee.org/view-from-the-valley/computing/software/a-madefortv-compression-metric-moves-to-the-real-world
    """
    return alpha * (r_tar / r_src) * (math.log(t_src) / math.log(t_tar))