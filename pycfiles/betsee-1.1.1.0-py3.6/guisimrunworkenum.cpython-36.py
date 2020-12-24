# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/work/guisimrunworkenum.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2146 bytes
"""
Low-level **simulator worker enumeration** (e.g., :class:`enum.Enum` subclass
describing different types of simulator work) functionality.
"""
from betsee.gui.simtab.run.guisimrunenum import SimmerState
from enum import Enum

class SimmerPhaseSubkind(Enum):
    __doc__ = '\n    Enumeration of each kind of **simulator subcommand worker** (i.e., type of\n    work performed within a given simulation phase by a given simulator\n    worker).\n\n    This child enumeration is a proper subset of the parent\n    :class:`SimmerState` enumeration differentiating simulator workers from one\n    another in a convenient manner permitting the state of each simulator phase\n    acted upon by each such worker to be trivially set.\n\n    Attributes\n    ----------\n    MODELLING : enum\n        Modelling state, implying this worker to model its simulator phase.\n    EXPORTING : enum\n        Exporting state, implying this worker to export its simulator phase.\n\n    Examples\n    ----------\n    To trivially map between members of these two correlated enumerations, each\n    member of this child enumeration is guaranteed to have the same ``value``\n    attribute as each corresponding member of the parent :class:`SimmerState`\n    enumeration: e.g.,\n\n        >>> from betsee.gui.simtab.run.guisimrunstate import SimmerState\n        >>> from betsee.gui.simtab.run.work.guisimrunworkenum import (\n        ...     SimmerPhaseSubkind)\n        >>> SimmerPhaseSubkind.MODELLING.value == (\n        ...     SimmerState.MODELLING.value)\n        True\n        >>> SimmerPhaseSubkind.EXPORTING.value == (\n        ...     SimmerState.EXPORTING.value)\n        True\n    '
    MODELLING = SimmerState.MODELLING.value
    EXPORTING = SimmerState.EXPORTING.value