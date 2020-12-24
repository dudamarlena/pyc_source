# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/datawatcher/datawatcherprocess.py
# Compiled at: 2020-01-24 07:42:12
# Size of source mod 2**32: 10143 bytes
"""
This module analyze headDir data directory to detect scan to be reconstructed
"""
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '14/10/2016'
from glob import glob
import subprocess
from tomwer.core.signal import Signal
from tomwer.core.process.reconstruction.ftseries.params.fastsetupdefineglobals import *
from tomwer.web.client import OWClient
from tomwer.core.log import TomwerLogger
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.edfscan import EDFTomoScan
from .status import OBSERVATION_STATUS
try:
    from tomwer.synctools.rsyncmanager import RSyncManager
    has_rsync = False
except ImportError:
    logger.warning('rsyncmanager not available')
    has_rsync = True

logger = TomwerLogger(__name__)

class _DataWatcherProcess(OWClient):
    __doc__ = "\n    DataWatcherProcess is the process managing the observation of acquisition.\n    Since we want to loop infinitly on a root folder we have to ignore the\n    folder we previously detected. Otherwise if those folders are not removed\n     we will loop infinitly. That is why we now have the ignoredFolders\n     parameter.\n\n    Example of usage of srcPattern and destPattern:\n\n        For example during acquisition in md05 acquisition files are stored\n        in /lbsram/data/visitor/x but some information (as .info) files are\n        stored in /data/visitor/x.\n        So we would like to check information in both directories.\n        Furthermore we would like that all file not in /data/visitor/x will be\n        copied as soon as possible into /data/visitor/x (using RSyncManager)\n\n        To do so we can define a srcPattern ('/lbsram' in our example) and\n        destPattern : a string replacing to srcPattern in order to get both\n        repositories. ('' in out example)\n        If srcPattern or destPattern are setted to None then we won't apply\n        this 'two directories' synchronization and check\n\n    :param  str dataDir: Root directory containing data\n    :param  bool waitXML: if True then we will be waiting for the XML of\n        the acquisition to be writted. Otherwise we will look for the .info\n        file and wait until all file will be copied\n    :param str srcPattern: the pattern to change by destPattern.\n    :param str destPattern: the pattern that will replace srcPattern in the\n        scan path\n    :param list ignoredFolders: the list of folders to ignored on parsing\n                                 (them and sub folders)\n    "
    sigNbDirExplored = Signal(int)
    sigAdvanceExploration = Signal(int)
    sigNewObservation = Signal(tuple)
    sigNewInformation = Signal(str)
    INITIAL_STATUS = 'not processing'

    def __init__(self, dataDir, srcPattern=None, destPattern=None):
        super(_DataWatcherProcess, self).__init__(logger)
        self.RootDir = os.path.abspath(dataDir)
        self.parsing_dir = os.path.abspath(dataDir)
        self.oldest = 0
        self.curdir = ''
        self.scan_name = ''
        self.scan_completed = False
        self.reconstructed = False
        self.status = self.INITIAL_STATUS
        self.quitting = False
        self._removed = None
        srcPatternInvalid = srcPattern not in (None, '') and not os.path.isdir(srcPattern)
        destPatternInvalid = destPattern not in (None, '') and not os.path.isdir(destPattern)
        if srcPatternInvalid or destPatternInvalid:
            srcPattern = None
            destPattern = None
        self.srcPattern = srcPattern if destPattern is not None else None
        self.destPattern = destPattern if srcPattern is not None else None

    def _setStatus(self, status, info=None):
        if not status in OBSERVATION_STATUS:
            raise AssertionError
        else:
            self.status = status
            if info is None:
                self.sigNewObservation.emit((status,))
            else:
                self.sigNewObservation.emit((status, info))

    def _removeAcquisition(self, scanID, reason):
        raise NotImplementedError('Base class')

    def dir_explore(self):
        """
        Explore directory tree until valid .file_info_ext file is found.
        Tree explored by ascending order relative to directory date depending
        self.oldest

        :return: True if the acquisition as started else False
        """
        self.status = 'start acquisition'

    def _sync(self):
        """Start to copy files from /lbsram/path to path if on lbsram

        :return: True if the synchronization starts
        """
        if has_rsync:
            return False
            if self.srcPattern:
                if not os.path.isdir(self.srcPattern):
                    if not self.srcPattern == '':
                        raise AssertionError
        else:
            if not os.path.isdir(self.destPattern):
                assert self.destPattern == ''
            if self.RootDir.startswith(self.srcPattern):
                source = os.path.join(self.RootDir, self.parsing_dir)
                target = source.replace(self.srcPattern, self.destPattern, 1)
                info = 'Start synchronization between %s and %s' % (source, target)
                self.sigNewInformation.emit(info)
                target_dirname = os.path.dirname(target)
                try:
                    if not RSyncManager().hasActiveSync(source, target_dirname):
                        RSyncManager().syncFolder(source, target_dirname)
                except subprocess.TimeoutExpired:
                    RSyncManager().syncFolder(source, target_dirname)

                return True
            else:
                return False

    def is_data_complete(self):
        """
        Check that data file is found and complete

        :return: - 0 if the acquisition is no finished
                 - 1 if the acquisition is finished
                 - -1 observation has been stopped
        """
        raise NotImplementedError('_DataWatcherProcess is a pure virtual class')

    def getCurrentDir(self):
        """Return the current dircetory parsed absolute path"""
        return os.path.join(self.RootDir, self.parsing_dir)

    def _isScanDirectory(self, directory):
        if EDFTomoScan.directory_contains_scan(directory, src_pattern=(self.srcPattern),
          dest_pattern=(self.destPattern)):
            scan = EDFTomoScan(directory)
            aux = directory.split(os.path.sep)
            scan_name = aux[(len(aux) - 1)]
            infoname = os.path.join(directory, aux[(-1)] + EDFTomoScan.INFO_EXT)
            if self.srcPattern:
                infoname = infoname.replace(self.srcPattern, self.destPattern, 1)
            gd = glob(os.path.join(directory, infoname))
            if len(gd) == 0:
                gd = glob(os.path.join(directory, EDFTomoScan.INFO_EXT))
                if len(gd) > 0:
                    self.detector = 'Dimax'
        elif HDF5TomoScan.directory_contains_scan(directory, src_pattern=(self.srcPattern),
          dest_pattern=(self.destPattern)):
            scan = HDF5TomoScan(scan=directory)
        else:
            return False
        if scan.is_abort(src_pattern=(self.srcPattern), dest_pattern=(self.destPattern)):
            self._removeAcquisition(scanID=directory, reason='acquisition aborted by the user')
        self._setStatus('started')
        return True

    def is_abort(self):
        raise NotImplementedError('Base class')


class _DataWatchEmpty(_DataWatcherProcess):
    __doc__ = 'A data watcher which just look under sub directories'

    def is_data_complete(self):
        return False

    def _removeAcquisition(self, scanID, reason):
        pass