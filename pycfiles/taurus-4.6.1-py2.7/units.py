# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/units.py
# Compiled at: 2019-08-19 15:09:29
"""
This module provides a pint unit registry instance (`UR`) to be used by all
taurus objects. It also provides the `Quantity` factory from that registry
(also aliased as `Q_`).
"""
__all__ = [
 'UR', 'Quantity', 'Q_']
from pint import UnitRegistry
UR = UnitRegistry()
UR.default_format = '~'
Q_ = Quantity = UR.Quantity