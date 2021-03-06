# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/datawatcher/edfdwprocess.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 10565 bytes
"""
data watcher classes used to define the status of an acquisition for EDF
acquisitions
"""
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '30/09/2019'
from .datawatcherprocess import _DataWatcherProcess
import logging, os, shutil
from tomwer.core.scan.edfscan import EDFTomoScan
import silx.third_party.EdfFile as EdfFile
from subprocess import getstatusoutput as myux
from glob import glob
import time, sys
_logger = logging.getLogger(__name__)
try:
    from tomwer.synctools.rsyncmanager import RSyncManager
    has_rsync = False
except ImportError:
    _logger.warning('rsyncmanager not available')
    has_rsync = True

def get_dir_size(dir):
    if not os.path.isdir(dir):
        err = "%s is not a directory, can't get size" % dir
        raise ValueError(err)
    else:
        aux = myux('du -ms ' + dir.replace(' ', '\\ '))
        if len(aux) < 2:
            return 0
        return float(aux[1].split('\t')[0])


def get_info_val(l, key):
    r = range(len(l))
    key = key + '='
    for i in r:
        if key in l[i]:
            val = float(l[i].split('=')[1])

    return val


class _DataWatcherEDFProcess(_DataWatcherProcess):
    __doc__ = '\n    Base class for edf acquisition observation\n    '
    XML_EXT = '.xml'
    SLICE_WC = 'slice'
    INFO_EXT = '.info'
    FILE_INFO_KEYS = [
     'TOMO_N', 'REF_ON', 'REF_N', 'DARK_N']
    DEFAULT_DETECTOR = 'Frelon'
    DATA_EXT = '0000.edf'

    def __init__(self, dataDir, srcPattern=None, destPattern=None):
        super(_DataWatcherEDFProcess, self).__init__(dataDir=dataDir, srcPattern=srcPattern,
          destPattern=destPattern)
        self.expected_dirsize = 0
        self.dirsize = 0
        self.file_rec_ext = '.rec'

    def _removeAcquisition(self, scanID, reason):
        if os.path.exists(scanID):
            if os.path.isdir(scanID):
                if self._removed is None:
                    _logger.info('removing folder %s because %s' % (scanID, reason))
                    if has_rsync:
                        RSyncManager().removeDir(scanID)
                        self._removed = scanID
                    else:
                        shutil.rmtree(scanID)

    def info_validate(self, infoname):
        """
        Check that file found is a valid one.

        :return: True if the file is valid
        """
        assert os.path.isfile(infoname)
        try:
            fd = open(infoname, 'r')
            lines = fd.read()
            fd.close()
            lg = len(self.FILE_INFO_KEYS)
            vali = 0
            for i in range(lg):
                vali = vali + (self.FILE_INFO_KEYS[i] in lines)

            return vali == lg
        except Exception as e:
            try:
                e = sys.exc_info()[0]
                _logger.error('fail to get info from %s' % infoname)
                raise e
            finally:
                e = None
                del e

    def is_abort(self):
        if os.path.exists(path=(self.scan_name)):
            return EDFTomoScan(scan=(self.scan_name)).is_abort(src_pattern=(self.srcPattern), dest_pattern=(self.destPattern))
        return False


class _DataWatcherProcessXML(_DataWatcherEDFProcess):
    __doc__ = '\n    This method will parse the [scan].info file and look if all .edf file\n    specified in the .info file are recorded and complete.\n    '

    def __init__(self, dataDir, srcPattern, destPattern):
        _DataWatcherEDFProcess.__init__(self, dataDir, srcPattern, destPattern)

    def is_data_complete(self):
        self._sync()
        aux = self.parsing_dir.split(os.path.sep)
        xmlfilelbsram = os.path.join(self.RootDir, self.parsing_dir, aux[(len(aux) - 1)] + self.XML_EXT)
        if self.srcPattern is None:
            self.scan_completed = os.path.isfile(xmlfilelbsram)
        else:
            xmlfilenice = xmlfilelbsram.replace(self.srcPattern, self.destPattern, 1)
            self.scan_completed = os.path.isfile(xmlfilenice) or os.path.isfile(xmlfilelbsram)
        return self.scan_completed


class _DataWatcherProcessUserFilePattern(_DataWatcherEDFProcess):
    __doc__ = '\n    This method will look for a specific pattern given by the user.\n    If a file in the given folder exists then we will consider the acquisition\n    ended\n\n    :param str pattern: the pattern we are looking for\n    '

    def __init__(self, dataDir, srcPattern, destPattern, pattern):
        _DataWatcherEDFProcess.__init__(self, dataDir, srcPattern, destPattern)
        self.pattern = pattern

    def is_data_complete(self):
        self._sync()
        fullPattern = os.path.join(self.getCurrentDir(), self.pattern)
        self.scan_completed = len(glob(fullPattern)) > 0
        return self.scan_completed


class _DataWatcherProcessParseInfo(_DataWatcherEDFProcess):
    __doc__ = "\n    This method will look for a '[scan].xml' pattern\n    "
    TYPES = {'SignedByte':1, 
     'UnsignedByte':1, 
     'SignedShort':2, 
     'UnsignedShort':2, 
     'SignedInteger':4, 
     'UnsignedInteger':4, 
     'SignedLong':4, 
     'UnsignedLong':4, 
     'Signed64':8, 
     'Unsigned64':8, 
     'FloatValue':4, 
     'Float':4, 
     'DoubleValue':8}
    TIME_LOOP_DATA_INCOMPLETE = 4

    def __init__(self, dataDir, srcPattern, destPattern):
        _DataWatcherEDFProcess.__init__(self, dataDir, srcPattern, destPattern)
        self.Dim1 = None
        self.Dim2 = None
        self.Tomo = None

    @staticmethod
    def get_data_size(edfType):
        if edfType in _DataWatcherProcessParseInfo.TYPES:
            return _DataWatcherProcessParseInfo.TYPES[edfType]
        return 2

    def info_validate(self):
        """
        Check that file found is a valid one and set acquisition information

        :return: True if the file is valid
        """
        if _DataWatcherEDFProcess.info_validate(self):
            if not os.path.isfile(self.infoname):
                raise AssertionError
            else:
                try:
                    fd = open(self.infoname, 'r')
                    lines = fd.read()
                    fd.close()
                    self.curdir = os.path.join(self.RootDir, self.parsing_dir)
                    if not os.path.isdir(self.curdir):
                        return False
                    self.dirsize = get_dir_size(self.curdir)
                    lines = lines.split('\n')
                    self.Dim1 = int(get_info_val(lines, 'Dim_1'))
                    self.Dim2 = int(get_info_val(lines, 'Dim_2'))
                    self.Tomo = int(get_info_val(lines, 'TOMO_N'))
                except:
                    e = sys.exc_info()[0]
                    _logger.error('fail to get info from %s' % self.infoname)
                    raise e
                else:
                    return True

    def is_data_complete(self):
        self._sync()
        try:
            limit = True
            while limit:
                try:
                    filno = os.open(self.dataname, os.O_RDONLY)
                    limit = False
                except:
                    if self.quitting is True:
                        return -1
                    time.sleep(self.TIME_LOOP_DATA_INCOMPLETE)

            os.close(filno)
            old_size = 0
            datafile1_ready = False
            while datafile1_ready is False:
                if self.quitting is True:
                    return -1
                    time.sleep(self.TIME_LOOP_DATA_INCOMPLETE)
                    mystat = os.stat(self.dataname)
                    fstat_st_size = mystat.st_size
                    if fstat_st_size > old_size:
                        old_size = fstat_st_size
                else:
                    datafile1_ready = True

            edf = EdfFile(self.dataname).Images[0]
            self.dataType = _DataWatcherProcessParseInfo.get_data_size(edf.DataType)
            headerLength = edf.DataPosition
            multif = 1
            if self.detector == 'Dimax':
                multif = self.Tomo
            deltas = multif * (self.Dim1 * self.Dim2 * self.dataType + headerLength) - fstat_st_size
            if deltas == 0:
                if self.detector == 'Dimax':
                    self.scan_completed = True
                    return 1
            limit = True
            while limit:
                r = glob(self.curdir + '/*')
                if len(r) > self.Tomo:
                    limit = False
                else:
                    if self.quitting is True:
                        return -1
                    _logger.info('waiting for more data')
                    self._sync()
                    time.sleep(1)

            self.scan_completed = True
            return 1
        except Exception as e:
            try:
                _logger.error('fail during is_data_validate')
                raise e
            finally:
                e = None
                del e