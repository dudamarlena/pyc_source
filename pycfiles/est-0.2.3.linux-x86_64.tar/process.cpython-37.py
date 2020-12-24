# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/process.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 5021 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/07/2019'
from silx.gui import qt
from Orange.widgets import gui
import logging
_logger = logging.getLogger(__file__)

class _ProcessForOrangeMixIn(object):
    __doc__ = "\n    Group processing and progress display in a common class for xasObject\n    process.\n\n    If this process own a widget to display the xas object then this one should\n    be named '_window'\n    "

    def __init__(self):
        self._progress = gui.ProgressBar(self, 100)
        self._ProcessForOrangeMixIn__processingThread = None
        self._progress = gui.ProgressBar(self, 100)

    def _startProcess(self):
        if hasattr(self, '_window'):
            self._window.setEnabled(False)
        self._progress.widget.progressBarInit()

    def _endProcess(self, xas_obj):
        if hasattr(self, '_window'):
            self._window.setEnabled(True)
        else:
            if self._callback_finish:
                try:
                    self.getProcessingThread()._process_obj._advancement.sigProgress.disconnect(self._setProgressValue)
                except ... as e:
                    try:
                        _logger.error(str(e))
                    finally:
                        e = None
                        del e

                self.getProcessingThread().finished.disconnect(self._callback_finish)
                self._callback_finish = None
            if xas_obj is None:
                return
            if hasattr(self, '_window') and hasattr(self._window, 'xasObjViewer'):
                self._window.xasObjViewer.setXASObj(xas_obj=xas_obj)
        self.Outputs.res_xas_obj.send(xas_obj)

    def _canProcess(self):
        return self._ProcessForOrangeMixIn__processingThread is None or not self._ProcessForOrangeMixIn__processingThread.isRunning()

    def getProcessingThread(self):
        if self._ProcessForOrangeMixIn__processingThread is None:
            self._ProcessForOrangeMixIn__processingThread = ProcessQThread(parent=self)
        return self._ProcessForOrangeMixIn__processingThread

    def _setProgressValue(self, value):
        self._progress.widget.progressBarSet(value)


class ProcessRunnable(qt.QRunnable):
    __doc__ = '\n    qt Runnable for standard process.\n    process function should take as input(spectrum, configuration, overwrite)\n\n    :param function pointer fct: process function\n    :param :class:`.Spectrum`: spectrum to process\n    :param dict configuration: configuration of the process\n    :param function pointer callback: optional callback to execute at the end of\n                                      the run. Should take no parameter\n    '

    def __init__(self, fct, spectrum, configuration, callback=None):
        qt.QRunnable.__init__(self)
        self._spectrum = spectrum
        self._configuration = configuration
        self._callback = callback
        self._function = fct

    def run(self):
        try:
            self._configuration, self._spectrum = self._function(spectrum=(self._spectrum),
              configuration=(self._configuration),
              overwrite=True)
        except (KeyError, ValueError) as e:
            try:
                _logger.error(e)
            finally:
                e = None
                del e

        if self._callback:
            self._callback()


class ProcessQThread(qt.QThread):
    __doc__ = '\n    Thread dedicated to process execution.\n    '

    def __init__(self, parent=None):
        qt.QThread.__init__(self, parent)

    def init(self, xas_obj, process_obj):
        """
        Initialize the thread for processing xas_obj from proces_obj

        :param :class:`.XASObject` xas_obj: object to process 
        :param :class:`.Process` process_obj: object to process xas_obj
        """
        self._xas_obj = xas_obj
        self._process_obj = process_obj

    def run(self):
        self._xas_obj = self._process_obj.process(self._xas_obj)