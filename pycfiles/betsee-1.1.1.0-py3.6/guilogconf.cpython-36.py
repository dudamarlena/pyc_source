# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/io/log/guilogconf.py
# Compiled at: 2019-08-01 01:07:00
# Size of source mod 2**32: 3164 bytes
"""
Low-level :mod:`PySide2`-specific logging configuration.
"""
from betse.util.io.log import logs
from betse.util.io.log.conf import logconf
from betse.util.io.log.logenum import LogLevel
from betse.util.io.log.logfilter import LogFilterThirdPartyDebug
from betse.util.type.types import type_check
from betsee.util.io.log.guiloghandle import LogHandlerSignal
from betsee.util.widget.stock.guitextedit import QBetseePlainTextEdit

@type_check
def log_to_text_edit(text_edit: QBetseePlainTextEdit) -> None:
    """
    Append all unfiltered log records to the passed text widget in an
    autoscrolling, non-blocking, thread-safe manner.

    This function integrates the default logging configuration for the active
    Python process with the current :mod:`PySide2` application. Specifically,
    this function reconfigures logging to additionally forward all relevant log
    records logged to the root handler onto the relevant slot connected to the
    relevant signal of the passed text widget, where "relevant log records"
    means:

    * If verbosity is enabled (e.g., via the ``--verbose`` command-line
      option), all log records.
    * Else, all log records with level ``LogLevel.INFO`` and higher.

    Parameters
    ----------
    text_edit : QBetseePlainTextEdit
        Text widget to append relevant log records to.
    """
    log_config = logconf.get_log_conf()
    logger_root_handler_signal = LogHandlerSignal(signal=(text_edit.append_text_signal))
    logger_root_handler_signal.setLevel(LogLevel.ALL if log_config.is_verbose else LogLevel.INFO)
    logger_root_handler_signal.addFilter(LogFilterThirdPartyDebug())
    log_config.logger_root.addHandler(logger_root_handler_signal)
    logs.log_info('Initializing GUI...')