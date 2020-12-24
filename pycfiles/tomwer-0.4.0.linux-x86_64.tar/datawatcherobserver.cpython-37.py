# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/datawatcher/datawatcherobserver.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 9691 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2019'
import os
from silx.gui import qt
from tomwer.core.process.datawatcher.datawatcherobserver import _OngoingObservation
from tomwer.core.process.datawatcher.datawatcherobserver import _DataWatcherObserver_MixIn
from tomwer.core.process.datawatcher.datawatcherobserver import _DataWatcherFixObserverMixIn
from tomwer.core.scan.scanbase import TomoBase
import tomwer.core.process.datawatcher as datawatcherstatus
from tomwer.core.log import TomwerLogger
from tomwer.core.scan.scanfactory import ScanFactory
logger = TomwerLogger(__name__)

class _QDataWatcherObserver(_DataWatcherObserver_MixIn, qt.QThread):
    __doc__ = '\n    DatWatcherObserver implementation with a qt.QThread\n\n    We have two implementations in order to avoid hard dependancy on qt for\n    tomwer.core package\n    '
    sigScanReady = qt.Signal(TomoBase)

    def __init__(self, obsMethod, observationClass, headDir=None, startByOldest=False, srcPattern=None, destPattern=None, ignoredFolders=None):
        qt.QThread.__init__(self)
        _DataWatcherObserver_MixIn.__init__(self, obsMethod=obsMethod,
          observationClass=observationClass,
          headDir=headDir,
          startByOldest=startByOldest,
          srcPattern=srcPattern,
          destPattern=destPattern,
          ignoredFolders=ignoredFolders,
          time_between_loops=0.2)
        self.observations.sigScanReady.connect(self._signalScanReady)

    def _signalScanReady(self, scan):
        assert isinstance(scan, TomoBase)
        self.sigScanReady.emit(scan)

    def _getObserver(self, scanID):
        return _QDataWatcherFixObserver(scanID=scanID, obsMethod=(self.obsMethod),
          srcPattern=(self.srcPattern),
          destPattern=(self.destPattern),
          patternObs=(self._patternObs),
          observationRegistry=(self.observations))

    def run(self):

        def process(directory):
            if self.observations.isObserving(directory) is False:
                if self.dataWatcherProcess._isScanDirectory(directory):
                    if directory not in self.observations.ignoredFolders:
                        self.observe(directory)
            try:
                for f in os.listdir(directory):
                    if os.path.isdir(os.path.join(directory, f)):
                        process(os.path.join(directory, f))

            except:
                pass

        if not os.path.isdir(self.headDir):
            logger.warning("can't observe %s, not a directory" % self.headDir)
            return
        self.dataWatcherProcess = self._getDataWatcherProcess()
        process(self.headDir)
        self._processObservation()

    def waitForObservationFinished(self, timeOut=10):
        threads = list(self.observations.dict.values())
        for thread in threads:
            thread.wait(timeOut)

    def wait(self):
        self.waitForObservationFinished()
        super(_QDataWatcherObserver, self).wait()


class _QOngoingObservation(_OngoingObservation, qt.QObject):
    __doc__ = '\n    _OngoingObservation with a QObject and signals for each event\n    '
    sigScanReady = qt.Signal(TomoBase)
    sigObsAdded = qt.Signal(str)
    sigObsRemoved = qt.Signal(str)
    sigObsStatusReceived = qt.Signal(str, str)

    def __init__(self):
        qt.QObject.__init__(self)
        _OngoingObservation.__init__(self)

    def _acquisition_ended(self, scanID):
        _OngoingObservation._acquisition_ended(self, scanID=scanID)
        try:
            scan = ScanFactory.create_scan_object(scan_path=scanID)
        except Exception as e:
            try:
                logger.error('Fail to create TomoBase instance from', scanID, 'Error is', e)
            finally:
                e = None
                del e

        else:
            self.sigScanReady.emit(scan)

    def add(self, observer):
        already_observing = self.isObserving(observer.path)
        _OngoingObservation.add(self, observer=observer)
        if not already_observing:
            observer.sigStatusChanged.connect(self._updateStatus)
            self.sigObsAdded.emit(observer.path)

    def remove(self, observer):
        observing = self.isObserving(observer.path)
        _OngoingObservation.remove(self, observer=observer)
        if observing is True:
            observer.sigStatusChanged.disconnect(self._updateStatus)
            self.sigObsRemoved.emit(observer.path)

    def _updateStatus(self, status, scan):
        if self.isObserving(scan) is True:
            self.sigObsStatusReceived.emit(scan, datawatcherstatus.DICT_OBS_STATUS[status])
        _OngoingObservation._updateStatus(self, status=status, scan=scan)

    def reset(self):
        for scanID, observer in self.dict:
            observer.sigStatusChanged.disconnect(self._updateStatus)
            observer.quit()

        self.dict = {}


class _QDataWatcherFixObserver(_DataWatcherFixObserverMixIn, qt.QThread):
    __doc__ = '\n    Implementation of the _DataWatcherFixObserverMixIn with a qt.QThread\n    '
    sigStatusChanged = qt.Signal(int, str)

    def __init__(self, scanID, obsMethod, srcPattern, destPattern, patternObs, observationRegistry):
        qt.QThread.__init__(self)
        _DataWatcherFixObserverMixIn.__init__(self, scanID=scanID,
          obsMethod=obsMethod,
          srcPattern=srcPattern,
          destPattern=destPattern,
          patternObs=patternObs,
          observationRegistry=observationRegistry)

    def run(self):
        if not os.path.isdir(self.path):
            logger.info("can't observe %s, not a directory" % self.path)
            self.status = 'failure'
            self.sigStatusChanged.emit(datawatcherstatus.OBSERVATION_STATUS[self.status], self.path)
            self.validation = -1
            return
        try:
            scan = ScanFactory.create_scan_object(scan_path=(self.path))
        except ValueError as e:
            try:
                logger.error(e)
            finally:
                e = None
                del e

        else:
            if scan.is_abort(src_pattern=(self.srcPattern), dest_pattern=(self.destPattern)):
                if self.status != 'aborted':
                    logger.info('Acquisition %s has been aborted' % self.path)
                    self.dataWatcherProcess._removeAcquisition(scanID=(self.path),
                      reason='acquisition aborted by the user')
                    self.status = 'aborted'
                self.sigStatusChanged.emit(datawatcherstatus.OBSERVATION_STATUS[self.status], self.path)
                self.validation = -2
                return
            dataComplete = self.dataWatcherProcess.is_data_complete()
            if dataComplete == True:
                self.status = 'acquisition ended'
                self.sigStatusChanged.emit(datawatcherstatus.OBSERVATION_STATUS[self.status], self.path)
                self.validation = 1
            else:
                self.status = 'waiting for acquisition ending'
                self.sigStatusChanged.emit(datawatcherstatus.OBSERVATION_STATUS[self.status], self.path)
                self.validation = 0