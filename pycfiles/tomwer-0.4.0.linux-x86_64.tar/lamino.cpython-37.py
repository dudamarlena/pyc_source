# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/stacks/reconstruction/lamino.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 7697 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '01/10/2018'
from queue import Queue
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.process.reconstruction.lamino.tofu import _tofu_lamino_reconstruction
import copy
from tomwer.core.process.reconstruction.lamino.tofu import LaminoReconstruction
from tomwer.core.utils.Singleton import singleton
from tomwer.web.client import OWClient
logger = TomwerLogger(__name__)

@singleton
class LaminoReconstructionStack(qt.QObject, Queue, OWClient):
    __doc__ = '\n    Manage a stack of lamino (tofu) reconstruction\n    '
    sigReconsFinished = qt.Signal(TomoBase)
    sigReconsFailed = qt.Signal(TomoBase)
    sigReconsMissParams = qt.Signal(TomoBase)
    sigReconsStarted = qt.Signal(TomoBase)

    def __init__(self):
        qt.QObject.__init__(self)
        Queue.__init__(self)
        OWClient.__init__(self, logger)
        self.reconsThread = _LaminoReconsThread()
        self.reconsThread.sigThReconsFinished.connect(self._dealWithFinishedRecons)
        self.reconsThread.sigThReconsFailed.connect(self._dealWithFailedRecons)
        self.reconsThread.sigThMissingParams.connect(self._dealWithThMissingParams)
        self._forceSync = False

    def add(self, recons_obj, recons_params, additional_opts, scan_id, remove_existing, callback):
        """
        add a reconstruction and will run it as soon as possible

        :param recons_obj: reconstructor, keeping trace of preprocess flat field
                           correction for example.
        :type recons_obj: LaminoReconstruction
        :param dict reconsParams: parameters of the reconstruction
        :param dict additional_opts: not managed directly by the gui
        :param scan_id: the folder of the acquisition to reconstruct
        :type: TomoBase
        :param bool remove_existing: if True then remove output dir before
                                     reconstruction
        :param callback: function to call after the reconstruction execution
        """
        assert isinstance(recons_obj, LaminoReconstruction)
        Queue.put(self, (recons_obj, recons_params, additional_opts, scan_id, remove_existing, callback))
        if self.canExecNext():
            self.execNext()

    def execNext(self):
        """
        Launch the next reconstruction if any
        """
        if Queue.empty(self):
            return
        assert not self.reconsThread.isRunning()
        recons_obj, recons_params, additional_opts, scan, remove_existing, callback = Queue.get(self)
        self.sigReconsStarted.emit(scan)
        self.reconsThread.init(recons_obj=recons_obj, recons_params=recons_params,
          additional_opts=additional_opts,
          scan_id=scan,
          remove_existing=remove_existing)
        self.reconsThread.sigThReconsFinished.connect(callback)
        self.reconsThread.start()
        if self._forceSync is True:
            self.reconsThread.wait()

    def canExecNext(self):
        """
        Can we launch an ftserie reconstruction.
        Reconstruction can't be runned in parallel

        :return: True if no reconstruction is actually running
        """
        return not self.reconsThread.isRunning()

    def _dealWithFinishedRecons(self, scan):
        assert isinstance(scan, TomoBase)
        info = 'reconstruction %s is finished' % scan.path
        logger.info(info)
        self.sigReconsFinished.emit(scan)
        self.execNext()

    def _dealWithThMissingParams(self, scan):
        assert isinstance(scan, TomoBase)
        self.sigReconsMissParams.emit(scan)
        self.execNext()

    def _dealWithFailedRecons(self, scan):
        assert isinstance(scan, TomoBase)
        self.sigReconsFailed.emit(scan)
        self.execNext()

    def setMockMode(self, b):
        self.reconsThread.setMockMode(b)
        self.execNext()

    def setForceSync(self, b=True):
        self._forceSync = b


class _LaminoReconsThread(qt.QThread):
    __doc__ = 'Thread used for running lamino reconstrucion using Tofu'
    sigThReconsFinished = qt.Signal(TomoBase)
    sigThReconsFailed = qt.Signal(TomoBase)
    sigThMissingParams = qt.Signal(TomoBase)

    def __init__(self):
        qt.QThread.__init__(self)
        self.scan = None
        self.recons_params = None
        self.additional_opts = None
        self.callback = None
        self.remove_existing = False

    def init(self, recons_obj, recons_params, additional_opts, remove_existing, scan_id):
        assert isinstance(recons_obj, LaminoReconstruction)
        self.recons_obj = recons_obj
        self.recons_params = recons_params
        self.additional_opts = additional_opts
        self.remove_existing = remove_existing
        self.scan = scan_id

    def run(self):
        recons_obj = copy.deepcopy(self.recons_obj)
        recons_obj.reconstruction_parameters = self.recons_params
        recons_obj.additional_reco_options = self.additional_opts
        try:
            recons_obj.process(scan=(self.scan))
        except ValueError as error:
            try:
                logger.warning(error)
                self.sigThMissingParams.emit('Some parameters are missing or are incoherent')
            finally:
                error = None
                del error

        except Exception as error:
            try:
                logger.error('fail to run lamino reconstruction for %s reason is %s' % (
                 self.scan, error))
                self.sigThReconsFailed.emit('fail to run reconstruction %s' % self.scan.path)
            finally:
                error = None
                del error

        else:
            self.sigThReconsFinished.emit(self.scan)