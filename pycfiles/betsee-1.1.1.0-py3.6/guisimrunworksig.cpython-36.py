# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/work/guisimrunworksig.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 3269 bytes
"""
Low-level **signals-based simulation phase callbacks** (i.e., collection of all
simulation phase callbacks whose methods emit queued Qt signals) classes.
"""
from betse.science.phase.phasecallbacks import SimCallbacksBC
from betse.util.type.types import type_check
from betsee.util.thread.pool.guipoolworksig import QBetseeThreadPoolWorkerSignals

class SimCallbacksSignaller(SimCallbacksBC):
    __doc__ = '\n    **Signals-based simulation phase callbacks** (i.e., caller-defined object\n    whose methods emit signals on the :class:`QBetseeThreadPoolWorkerSignals`\n    object with which this :class:`SimCallbacksSignaller` object is\n    initializedare on being periodically called while simulating one or more\n    simulation phases).\n\n    This object effectively glues low-level simulation subcommands to\n    high-level simulator widgets, converting callbacks called by the former\n    into signals emitted on slots defined by the latter.\n\n    Attributes\n    ----------\n    _signals : QBetseeThreadPoolWorkerSignals\n        Collection of all signals emittable by simulator workers.\n    '

    @type_check
    def __init__(self, signals):
        """
        Initialize this callbacks collection.

        Parameters
        ----------
        signals : QBetseeThreadPoolWorkerSignals
            Collection of all signals emittable by simulator workers.
        """
        super().__init__()
        self._signals = signals

    @type_check
    def progress_ranged(self, progress_max, progress_min=0):
        super().progress_ranged(progress_min=progress_min,
          progress_max=progress_max)
        self._signals.emit_progress_range(progress_min=progress_min,
          progress_max=progress_max)

    @type_check
    def progress_stated(self, status):
        super().progress_stated(status=status)
        self._signals.emit_progress_state(status=status)

    @type_check
    def progressed(self, progress):
        super().progressed(progress=progress)
        self._signals.emit_progress(progress=progress)