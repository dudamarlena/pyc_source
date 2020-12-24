# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/scanvalidator.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 11070 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '18/06/2017'
from collections import OrderedDict
from tomwer.core.signal import Signal
from tomwer.core import settings
from tomwer.core import utils
from tomwer.core.process.baseprocess import BaseProcess, _input_desc, _output_desc
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils import logconfig
from tomwer.core.log import TomwerLogger
from tomwer.core.scan.scanbase import TomoBase, _TomoBaseDock
logger = TomwerLogger(__name__)

class ScanValidator(BaseProcess):
    __doc__ = '\n    Simple workflow locker until the use validate scans\n\n    :param int memReleaserWaitLoop: the time to wait in second between two\n                                    memory overload if we are in lbsram.\n    '
    inputs = [
     _input_desc(name='data', type=TomoBase, handler='addScan', doc='scan path')]
    outputs = [
     _output_desc(name='change recons params', type=_TomoBaseDock, doc='input with scan + reconstruction parameters'),
     _output_desc(name='data', type=TomoBase, doc='scan path')]

    def __init__(self, memoryReleaser):
        BaseProcess.__init__(self)
        self._scansToValidate = OrderedDict()
        self._manualValidation = True
        self._hasToLimitScanBlock = settings.isOnLbsram()
        self._memoryReleaser = memoryReleaser
        self._scans = {}
        if self._hasToLimitScanBlock:
            self._memoryReleaser.finished.connect(self._loopMemoryReleaser)
            self._memoryReleaser.start()

    def __del__(self):
        if self._memoryReleaser is not None:
            self._memoryReleaser.should_be_stopped = True
            self._memoryReleaser.wait()

    @property
    def lastReceivedRecons(self):
        return list(self._scansToValidate.values())[0]

    def addScan(self, ftserie):
        """
        Return the index on the current orderred dict

        :param ftserie:
        :return:
        """
        _ftserie = ftserie
        if type(ftserie) is str:
            _ftserie = ScanFactory.create_scan_object(_ftserie)
        info = 'Scan %s has been added by the Scan validator' % _ftserie.path
        logger.info(info)
        _ftserie = ftserie
        if type(ftserie) is str:
            _ftserie = ScanFactory.create_scan_object(_ftserie)
        self._scansToValidate[_ftserie.path] = _ftserie
        index = len(self._scansToValidate) - 1
        self._freeStackIfNeeded()
        return index

    def _freeStackIfNeeded(self):
        isLowMemoryLbs = settings.isOnLbsram() and utils.isLowOnMemory(settings.get_lbsram_path()) is True
        if not (isLowMemoryLbs or self.isValidationManual()):
            if isLowMemoryLbs:
                mess = 'low memory, free ScanValidator stack '
                logger.processSkipped(mess)
            self._validateStack()

    def _loopMemoryReleaser(self):
        """
        simple loop using the _memoryReleaser and calling the
        _freeStackIfNeeded function
        """
        self._freeStackIfNeeded()
        if self._memoryReleaser:
            if not hasattr(self._memoryReleaser, 'should_be_stopped'):
                self._memoryReleaser.start()

    def _validateStack(self):
        """Validate all the scans in the stack."""
        for scanID in list(self._scansToValidate.keys()):
            self._validated(self._scansToValidate[scanID])

        assert len(self._scansToValidate) == 0

    def _validateScan(self, scan):
        """This will validate the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scan is not None:
            assert isinstance(scan, TomoBase)
            self._validated(scan)

    def _cancelScan(self, scan):
        """This will cancel the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scan is not None:
            assert isinstance(scan, TomoBase)
            self._canceled(scan)

    def _redoAcquisitionScan(self, scan):
        """This will emit a signal to request am acquisition for the current
        ftSerieReconstruction

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scan is not None:
            assert isinstance(scan, TomoBase)
            self._redoacquisition(scan)

    def _validated(self, scan):
        """Callback when the validate button is pushed"""
        if scan is not None:
            assert isinstance(scan, TomoBase)
            info = '%s has been validated' % scan.path
            logger.processEnded(info, extra={logconfig.DOC_TITLE: self._scheme_title, 
             logconfig.SCAN_ID: scan.path})
            self._sendScanReady(scan)
            if scan.path in self._scansToValidate:
                del self._scansToValidate[scan.path]
            if scan.path in self._scans:
                del self._scans[scan.path]

    def _canceled(self, scan):
        """Callback when the cancel button is pushed"""
        if scan is not None:
            assert isinstance(scan, TomoBase)
            info = '%s has been canceled' % scan.path
            logger.processEnded(info, extra={logconfig.DOC_TITLE: self._scheme_title, 
             logconfig.SCAN_ID: scan.path})
            self._sendScanCanceledAt(scan)
            if scan.path in self._scansToValidate:
                del self._scansToValidate[scan.path]
            if scan.path in self._scansToValidate:
                del self._scans[scan.path]
            self.clear()

    def _redoacquisition(self, ftserie):
        """Callback when the redo acquisition button is pushed"""
        raise NotImplementedError('_redoacquisition not implemented yet')

    def _changeReconsParam(self, ftserie):
        """Callback when the change reconstruction button is pushed"""
        if ftserie is None:
            return
        _ftserie = ftserie
        if type(ftserie) is str:
            _ftserie = ScanFactory.create_scan_object(_ftserie)
        if _ftserie.path in self._scansToValidate:
            del self._scansToValidate[_ftserie.path]
        self._sendUpdateReconsParam(_TomoBaseDock(tomo_instance=_ftserie))

    def setProperties(self, properties):
        pass

    def setManualValidation(self, b):
        """if the validation mode is setted to manual then we will wait for
        user approval before validating. Otherwise each previous and next scan
        will be validated

        :param boolean b: False if we want an automatic validation
        """
        self._manualValidation = b
        if not self.isValidationManual():
            self._validateStack()

    def isValidationManual(self):
        """

        :return: True if the validation is waiting for user interaction,
                 otherwise False
        """
        return self._manualValidation

    def _sendScanReady(self):
        raise RuntimeError('ScanValidator is a pure virtual class.')

    def _sendScanCanceledAt(self):
        raise RuntimeError('ScanValidator is a pure virtual class.')

    def _sendUpdateReconsParam(self):
        raise RuntimeError('ScanValidator is a pure virtual class.')

    def clear(self):
        scans = self._scans.values()
        for scan in scans:
            self._cancelScan(scan=(scans[scan]))


class ScanValidatorP(ScanValidator):
    __doc__ = '\n    For now to avoid multiple inheritance from QObject with the process widgets\n    we have to define two classes. One only for the QObject inheritance.\n\n    :param int memReleaserWaitLoop: the time to wait in second between two\n                                    memory overload if we are in lbsram.\n    '
    scanReady = Signal(TomoBase)
    scanCanceledAt = Signal(str)
    updateReconsParam = Signal(TomoBase)

    def __init__(self, memoryReleaser=None):
        ScanValidator.__init__(self, memoryReleaser)

    def _sendScanReady(self, scanID):
        self.scanReady.emit(scanID)

    def _sendScanCanceledAt(self, scanID):
        self.scanCanceledAt.emit(scanID)

    def _sendUpdateReconsParam(self, ftserie):
        self.updateReconsParam.emit(ftserie)