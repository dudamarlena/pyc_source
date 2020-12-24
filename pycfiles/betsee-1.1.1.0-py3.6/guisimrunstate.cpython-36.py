# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/guisimrunstate.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 14335 bytes
"""
Low-level **simulator state** (i.e., abstract node in the finite state automata
corresponding to this simulator) functionality.
"""
from PySide2.QtCore import QCoreApplication
from betse.science.pipe.export.pipeexpenum import SimExportType
from betse.science.enum.enumphase import SimPhaseKind
from betsee.gui.simtab.run.guisimrunenum import SimmerState, SimmerModelState
SIM_PHASE_KIND_TO_NAME = {SimPhaseKind.SEED: QCoreApplication.translate('guisimrunstate', 'seed'), 
 
 SimPhaseKind.INIT: QCoreApplication.translate('guisimrunstate', 'initialization'), 
 
 SimPhaseKind.SIM: QCoreApplication.translate('guisimrunstate', 'simulation')}
SIMMER_STATES = set(simmer_state for simmer_state in SimmerState)
SIMMER_STATES_IDLE = {
 SimmerState.UNQUEUED,
 SimmerState.QUEUED}
SIMMER_STATES_RUNNING = {
 SimmerState.MODELLING,
 SimmerState.EXPORTING}
SIMMER_STATES_WORKING = SIMMER_STATES_RUNNING | {SimmerState.PAUSED}
SIMMER_STATES_HALTING = {
 SimmerState.PAUSED,
 SimmerState.STOPPING,
 SimmerState.FINISHED}
SIMMER_STATES_UNWORKABLE = {
 SimmerState.UNQUEUED,
 SimmerState.STOPPING}
SIMMER_STATES_FROM_FLUID = {
 SimmerState.UNQUEUED,
 SimmerState.QUEUED,
 SimmerState.FINISHED,
 SimmerState.STOPPING}
SIMMER_STATES_FROM_FIXED = SIMMER_STATES - SIMMER_STATES_FROM_FLUID
SIMMER_STATES_INTO_FLUID = {
 SimmerState.UNQUEUED,
 SimmerState.QUEUED}
SIMMER_STATES_INTO_FIXED = SIMMER_STATES - SIMMER_STATES_INTO_FLUID
SIMMER_STATE_TO_PHASE_STATUS = {SimmerState.UNQUEUED: QCoreApplication.translate('guisimrunstate', 'Unqueued'), 
 
 SimmerState.QUEUED: QCoreApplication.translate('guisimrunstate', 'Queued'), 
 
 SimmerState.MODELLING: QCoreApplication.translate('guisimrunstate', 'Modelling'), 
 
 SimmerState.EXPORTING: QCoreApplication.translate('guisimrunstate', 'Exporting'), 
 
 SimmerState.PAUSED: QCoreApplication.translate('guisimrunstate', 'Paused'), 
 
 SimmerState.STOPPING: QCoreApplication.translate('guisimrunstate', 'Finishing'), 
 
 SimmerState.FINISHED: QCoreApplication.translate('guisimrunstate', 'Finished')}
SIMMER_STATE_TO_PROACTOR_STATUS = {SimmerState.UNQUEUED: QCoreApplication.translate('guisimrunstate', 'Waiting for phase(s) to be queued...'), 
 
 SimmerState.QUEUED: QCoreApplication.translate('guisimrunstate', 'Waiting for queued phase(s) to be started...'), 
 
 SimmerState.MODELLING: QCoreApplication.translate('guisimrunstate', 'Modelling <b>{phase_type}</b> phase...'), 
 
 SimmerState.EXPORTING: QCoreApplication.translate('guisimrunstate', 'Exporting <b>{phase_type}</b> phase...'), 
 
 SimmerState.PAUSED: QCoreApplication.translate('guisimrunstate', 'Paused {status_prior}.'), 
 
 SimmerState.STOPPING: QCoreApplication.translate('guisimrunstate', 'Finishing {status_prior}...'), 
 
 SimmerState.FINISHED: QCoreApplication.translate('guisimrunstate', 'Finished {status_prior}.')}
SIMMER_STATE_TO_PROACTOR_SUBSTATUS = {SimmerState.UNQUEUED: QCoreApplication.translate('guisimrunstate', 'Queued {queued_modelling} phase(s) for modelling and {queued_exporting} phase(s) for exporting.'), 
 
 SimmerState.QUEUED: QCoreApplication.translate('guisimrunstate', 'Queued {queued_modelling} phase(s) for modelling and {queued_exporting} phase(s) for exporting.'), 
 
 SimmerState.MODELLING: {SimPhaseKind.SEED: None, 
                         SimPhaseKind.INIT: {SimmerModelState.PREPARING: QCoreApplication.translate('guisimrunstate', 'Loading seeded cell cluster...'), 
                                             
                                             SimmerModelState.MODELLING: QCoreApplication.translate('guisimrunstate', 'Initialized <b>{progress_current}</b> <i>of</i> <b>{progress_maximum}</b> simulation time steps.'), 
                                             
                                             SimmerModelState.FINISHING: QCoreApplication.translate('guisimrunstate', 'Saving initialization results...')}, 
                         
                         SimPhaseKind.SIM: {SimmerModelState.PREPARING: QCoreApplication.translate('guisimrunstate', 'Loading initialization results...'), 
                                            
                                            SimmerModelState.MODELLING: QCoreApplication.translate('guisimrunstate', 'Simulated <b>{progress_current}</b> <i>of</i> <b>{progress_maximum}</b> simulation time steps.'), 
                                            
                                            SimmerModelState.FINISHING: QCoreApplication.translate('guisimrunstate', 'Saving simulation results...')}}, 
 
 SimmerState.EXPORTING: {SimExportType.CSV: QCoreApplication.translate('guisimrunstate', 'Exported comma-separated value (CSV) file <pre>"{pathname}"</pre>.'), 
                         
                         SimExportType.PLOT: QCoreApplication.translate('guisimrunstate', 'Exported image <pre>"{pathname}"</pre>.'), 
                         
                         SimExportType.ANIM: QCoreApplication.translate('guisimrunstate', 'Exported animation <pre>"{pathname}"</pre>.')}, 
 
 SimmerState.PAUSED: '{substatus_prior}', 
 SimmerState.STOPPING: '{substatus_prior}', 
 SimmerState.FINISHED: '{substatus_prior}'}