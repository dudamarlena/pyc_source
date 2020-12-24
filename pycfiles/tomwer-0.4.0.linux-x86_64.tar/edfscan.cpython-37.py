# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/scan/edfscan.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 25159 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '09/08/2018'
import glob, os, re
from collections import OrderedDict
import fabio, numpy, json, io, functools
from tomwer.core.log import TomwerLogger
from tomwer.core.process.reconstruction.darkref.settings import REFHST_PREFIX, DARKHST_PREFIX
from tomwer.core import utils
from tomwer.core.progress import Progress
from tomwer.core.utils.ftseriesutils import orderFileByLastLastModification
from silx.io.url import DataUrl
import silx.io.utils
from glob import glob
from .scanbase import TomoBase
from multiprocessing import Pool
_logger = TomwerLogger(__name__)
counter_rand = 1

class EDFTomoScan(TomoBase):
    __doc__ = '\n    Class used to represent a tomography acquisition with hdf5 files.\n\n    :param Union[str, None] scan: path of the scan\n    '
    _TYPE = 'edf'
    INFO_EXT = '.info'
    ABORT_FILE = '.abo'

    def __init__(self, scan):
        TomoBase.__init__(self, scan=scan, _type=(self._TYPE))
        self._dark = None
        self._EDFTomoScan__tomo_n = None
        self._EDFTomoScan__ref_n = None
        self._EDFTomoScan__dark_n = None
        self._EDFTomoScan__dim1 = None
        self._EDFTomoScan__dim2 = None
        self._EDFTomoScan__pixel_size = None
        self._EDFTomoScan__ref_on = None
        self._EDFTomoScan__scan_range = None
        if scan is not None:
            self._process_file = os.path.join(scan, 'tomwer_processes.h5')
        else:
            self._process_file = None
        if scan is not None:
            self.updateDataset()

    @staticmethod
    def directory_contains_scan(directory, src_pattern, dest_pattern):
        """
        Check if the given directory is holding an acquisition

        :param str directory: directory we want to check
        :param str src_pattern: buffer name pattern ('lbsram')
        :param dest_pattern: output pattern (''). Needed because some
                             acquisition can split the file produce between
                             two directories. This is the case for edf,
                             where .info file are generated in /data/dir
                             instead of /lbsram/data/dir
        :return: does the given directory contains any acquisition
        :rtype: bool
        """
        aux = directory.split(os.path.sep)
        infoname = os.path.join(directory, aux[(-1)] + EDFTomoScan.INFO_EXT)
        if src_pattern:
            infoname = infoname.replace(src_pattern, dest_pattern, 1)
        return os.path.isfile(infoname)

    def get_info_file(self):
        if self.path is None:
            return
        info_file = os.path.join(self.path, os.path.basename(self.path) + '.info')
        if os.path.exists(info_file):
            return info_file
        return

    @functools.lru_cache(maxsize=3)
    def getFlat(self, index=None):
        """
        If projectionI is not requested then return the mean value. Otherwise
        return the interpolated value for the requested projection.

        :param Union[int,None] index: index of the projection for which we want
                                      the flat
        :return: Flat field value or None if can't deduce it
        """
        data = self._extractFromOneFile('refHST.edf', what='flat')
        if data is not None:
            return data
        data = self._extractFromPrefix(REFHST_PREFIX, what='flat', proI=index)
        if data is not None:
            return data
        _logger.warning('Cannot retrieve flat file from %s' % self.path)

    def is_abort(self, src_pattern, dest_pattern):
        """
        Check if the acquisition have been aborted. In this case the directory
        should contain a [scan].abo file

        :param str src_pattern: buffer name pattern ('lbsram')
        :param dest_pattern: output pattern (''). Needed because some
                             acquisition can split the file produce between
                             two directories. This is the case for edf,
                             where .info file are generated in /data/dir
                             instead of /lbsram/data/dir
        :return: True if the acquisition have been abort and the directory
                 should be abort
        """
        abort_file = os.path.join(self.path, os.path.basename(self.path) + self.ABORT_FILE)
        if src_pattern:
            abort_file = abort_file.replace(src_pattern, dest_pattern, 1)
        return os.path.isfile(abort_file)

    @functools.lru_cache()
    def getDark(self):
        """
        For now only deal with one existing dark file.

        :return: image of the dark if existing. Else None
        """
        if self._dark is None:
            self._dark = self._extractFromOneFile('dark.edf', what='dark')
            if self._dark is None:
                self._dark = self._extractFromOneFile('darkHST.edf', what='dark')
            if self._dark is None:
                self._dark = self._extractFromPrefix(DARKHST_PREFIX, what='dark')
            if self._dark is None:
                self._dark = self._extractFromPrefix('darkend', what='dark')
            if self._dark is None:
                _logger.warning('Cannot retrieve dark file from %s' % self.path)
        return self._dark

    def _extractFromOneFile(self, f, what):
        if self.path is None:
            return
        else:
            path = os.path.join(self.path, f)
            if os.path.exists(path):
                _logger.info('Getting %s from %s' % (what, f))
                try:
                    data = fabio.open(path).data
                except:
                    return
                else:
                    if data.ndim is 2:
                        return data
                    if data.ndim is 3:
                        _logger.warning('%s file contains several images. Taking the mean value' % what)
                        return numpy.mean(data.ndim)
            else:
                return

    def _extractFromPrefix(self, pattern, what, proI=None):
        if self.path is None:
            return
        files = glob(os.path.join(self.path, pattern + '*.edf'))
        if len(files) is 0:
            return
        d = {}
        for f in files:
            index = self.guessIndexFromEDFFileName(f)
            if index is None:
                _logger.error('cannot retrieve projection index for %s' % f)
                return
            d[index] = fabio.open(f).data

        if len(files) is 1:
            return d[list(d.keys())[0]]
        oProj = OrderedDict(sorted(d.items()))
        lowPI = list(oProj.keys())[0]
        uppPI = list(oProj.keys())[(-1)]
        lowPD = oProj[lowPI]
        uppPD = oProj[uppPI]
        if len(oProj) > 2:
            _logger.info('Only bordering projections (%s and %s) will be used for extracting %s' % (
             lowPI, uppPI, what))
        uppPI = uppPI
        index = proI
        if index is None:
            index = (uppPI - lowPI) / 2
        if (index >= lowPI) is False:
            index = lowPI
            _logger.warning('ProjectionI not in the files indexesrange (projectionI >= lowerProjIndex)')
        if (index <= uppPI) is False:
            index = uppPI
            _logger.warning('ProjectionI not in the files indexesrange upperProjIndex >= projectionI')
        _nRef = uppPI - lowPI
        lowPI = lowPI
        w0 = (lowPI + (uppPI - index)) / _nRef
        w1 = index / _nRef
        return w0 * lowPD + w1 * uppPD

    @staticmethod
    def guessIndexFromEDFFileName(_file):
        name = _file.rstrip('.edf')
        ic = []
        while name[(-1)].isdigit():
            ic.append(name[(-1)])
            name = name[:-1]

        if len(ic) is 0:
            return
        orignalOrder = ic[::-1]
        return int(''.join(orignalOrder))

    def getProjectionsUrl(self, use_cache: bool=True):
        """
        Return all projections as a dictionary with angle as key and
        DataUrl as value

        :param bool use_cache: if this function has already been called then
                               the result is in cache. If no modification
                               have been bring to the scan the value didn't
                               change

        :return: one DataUrl instance for each projections
        :rtype: dict
        """
        if not use_cache:
            self._cache_proj_urls = None
        elif self._cache_proj_urls is None:
            if self.path is None:
                _logger.warning('no path specified for scan, unable to retrieve all the projections')
                self._cache_proj_urls = {}
            else:
                n_projection = self.get_tomo_n()
                radios = EDFTomoScan.getRadioPaths(self.path)
                sorted_keys = list(radios.keys())
                sorted_keys.sort()
                data_urls = []
                pool = Pool(5)
                sorted_radios = []
                [sorted_radios.append(radios[key]) for key in sorted_keys]
                results = pool.map(_get_urls_list, sorted_radios)
                for result in results:
                    data_urls.extend(result)

                if n_projection is None:
                    raise ValueError('unable to get n projection')
                if len(data_urls) < n_projection:
                    mes = 'incoherence between the number of projection found (%s) and the number of theoretical projection (%s). Maybe the acquisition is not complete ?' % (
                     len(data_urls), n_projection)
                    _logger.warning(mes)
                self._cache_proj_urls = TomoBase.map_urls_on_scan_range(urls=data_urls, n_projection=n_projection,
                  scan_range=(self.get_scan_range()))
        return self._cache_proj_urls

    def flatFieldCorrection(self, data):
        """
        Apply the flat field correction on the given data.

        :param numpy.ndarray data: radio to correct
        :return numpy.ndarray: corrected data
        """
        if not type(data) is numpy.ndarray:
            raise AssertionError
        else:
            can_process = True
            dark = self.getDark()
            if dark is None:
                _logger.error('cannot make flat field correction, dark not found')
                can_process = False
            if dark is not None:
                if dark.ndim != 2:
                    _logger.error('cannot make flat field correction, dark should be of dimension 2')
                    can_process = False
            flat = self.getFlat()
            if flat is None:
                _logger.error('cannot make flat field correction, flat not found')
                can_process = False
            if flat is not None:
                if flat.ndim != 2:
                    _logger.error('cannot make flat field correction, flat should be of dimension 2')
                    can_process = False
            if dark is not None:
                if flat is not None:
                    if dark.shape != flat.shape:
                        _logger.error('Given dark and flat have incoherent dimension')
                        can_process = False
            if dark is not None and data.shape != dark.shape:
                _logger.error('Image has invalid. Cannot apply flat fieldcorrection it')
                can_process = False
        if can_process is False:
            return data
        div = flat - dark
        div[div == 0] = 1
        return (data - dark) / div

    def updateDataset(self):
        """update list of radio and reconstruction by parsing the scan folder
        """
        self.projections = EDFTomoScan.getRadioPaths(self.path)
        self.reconstructions = EDFTomoScan.getReconstructionsPaths(self.path)

    @staticmethod
    def getReconstructionsPaths(scanID, withIndex=False):
        """
        Return the dict of files:
        * fitting with a reconstruction pattern and ending by .edf
        * .vol files

        :param scanID: is the path to the folder of acquisition
        :param bool withIndex: if False then return a list of slices otherwise
            return a dict with the index of the slice reconstructed.
        """

        def containsDigits(input):
            return any((char.isdigit() for char in input))

        if not (scanID is None or os.path.isdir(scanID)):
            if withIndex is True:
                return {}
            return []
        pyhst_files = EDFTomoScan.getPYHST_ReconsFile(scanID)
        if pyhst_files is not None:
            return EDFTomoScan.getReconstructedFilesFromParFile(pyhst_files, with_index=withIndex)
        folderBasename = os.path.basename(scanID)
        files = {} if withIndex is True else []
        if os.path.isdir(scanID):
            for f in os.listdir(scanID):
                if f.endswith('.edf') and f.startswith(folderBasename) and 'slice_' in f:
                    localstring = f.rstrip('.edf')
                    if 'slice_' in localstring:
                        localstring = f.rstrip('.edf')
                        if 'slice_pag_' in localstring:
                            indexStr = localstring.split('slice_pag_')[(-1)].split('_')[0]
                        else:
                            indexStr = localstring.split('slice_')[(-1)].split('_')[0]
                        if containsDigits(indexStr):
                            gfile = os.path.join(scanID, f)
                            if not os.path.isfile(gfile):
                                raise AssertionError
                            elif withIndex is True:
                                files[EDFTomoScan.getIndexReconstructed(f, scanID)] = gfile
                            else:
                                files.append(gfile)
                if f.endswith('.vol'):
                    if withIndex is True:
                        files[EDFTomoScan.getIndexReconstructed(f, scanID)] = os.path.join(scanID, f)
                    else:
                        files.append(os.path.join(scanID, f))

        return files

    @staticmethod
    def getRadioPaths(scanID):
        """Return the dict of radios for the given scan.
        Keys of the dictionary is the slice number
        Return all the file on the root of scan starting by the name of scan and
        ending by .edf

        :param scanID: is the path to the folder of acquisition
        :return: dict of radios files with radio index as key and file as value
        :rtype: dict
        """
        files = dict({})
        return scanID is None or os.path.isdir(scanID) or files
        if os.path.isdir(scanID):
            for f in os.listdir(scanID):
                if EDFTomoScan.isARadioPath(f, scanID):
                    gfile = os.path.join(scanID, f)
                    files[EDFTomoScan.getIndexReconstructed(f, scanID)] = gfile

        return files

    @staticmethod
    def isARadioPath(fileName, scanID):
        """Return True if the given fileName can fit to a Radio name
        """
        fileBasename = os.path.basename(fileName)
        folderBasename = os.path.basename(scanID)
        if fileBasename.endswith('.edf'):
            if fileBasename.startswith(folderBasename):
                localstring = fileName.rstrip('.edf')
                localstring = re.sub(folderBasename, '', localstring)
                if 'slice_' in localstring:
                    return False
                if 'refHST' in localstring:
                    return False
                s = localstring.split('_')
                if s[(-1)].isdigit():
                    return True
        return False

    @staticmethod
    def getIndexReconstructed(reconstructionFile, scanID):
        """Return the slice reconstructed of a file from her name

        :param str reconstructionFile: the name of the file
        """
        global counter_rand
        folderBasename = os.path.basename(scanID)
        if reconstructionFile.endswith('.edf') and reconstructionFile.startswith(folderBasename):
            localstring = reconstructionFile.rstrip('.edf')
            localstring = re.sub(folderBasename, '', localstring)
            s = localstring.split('_')
            if s[(-1)].isdigit():
                return int(s[(-1)])
            _logger.warning('Fail to find the slice reconstructed for file %s' % reconstructionFile)
        else:
            counter_rand = counter_rand + 1
            return counter_rand

    @staticmethod
    def getPYHST_ReconsFile(scanID):
        """Return the .par file used for the current reconstruction if any.
        Otherwise return None """
        if scanID == '':
            return
        if scanID is None:
            raise RuntimeError('No current acquisition to validate')
        assert type(scanID) is str
        assert os.path.isdir(scanID)
        folderID = os.path.basename(scanID)
        parFiles = glob(os.path.join(scanID + folderID) + '*_slice.par')
        if len(parFiles) > 0:
            return orderFileByLastLastModification(scanID, parFiles)[(-1)]
        return

    def load_from_dict(self, desc):
        from tomwer.core.process.reconstruction.ftseries.params import ReconsParams
        from tomwer.core.process.reconstruction.axis.params import AxisRP
        if isinstance(desc, io.TextIOWrapper):
            data = json.load(desc)
        else:
            data = desc
        if not (self._DICT_TYPE_KEY in data and data[self._DICT_TYPE_KEY] == self._TYPE):
            raise ValueError('Description is not an EDFScan json description')
        assert self._DICT_PATH_KEY in data
        assert self._DICT_LAMINO_RP_KEY in data
        self.path = data[self._DICT_PATH_KEY]
        recons_param_data = data[self._DICT_TOMO_RP_KEY]
        if recons_param_data is not None:
            self.ftseries_recons_params = ReconsParams.from_dict(recons_param_data)
        self.lamino_recons_params = data[self._DICT_LAMINO_RP_KEY]
        axis_params = data[self._DICT_AXIS_KEYS]
        if axis_params is not None:
            self.axis_params = AxisRP.from_dict(axis_params)
        return self

    load_from_dict.__doc__ = TomoBase.load_from_dict.__doc__

    def get_ff_interval(self):
        """

        :param clear_cache: if true then recompute the cache containing
                            the acquisition information
        :type: bool
        :return: number of radio between each reference / flat field
        :rtype: int
        """
        return self.get_ref_on()

    def get_tomo_n(self):
        if self._EDFTomoScan__tomo_n is None:
            self._EDFTomoScan__tomo_n = utils.getTomo_N(scan=(self.path))
        return self._EDFTomoScan__tomo_n

    def get_dark_n(self):
        if self._EDFTomoScan__dark_n is None:
            self._EDFTomoScan__dark_n = utils.getDARK_N(scan=(self.path))
        return self._EDFTomoScan__dark_n

    def get_ref_n(self):
        if self._EDFTomoScan__ref_n is None:
            self._EDFTomoScan__ref_n = utils.getRef_N(scan=(self.path))
        return self._EDFTomoScan__ref_n

    def get_pixel_size(self):
        """

        :return: pixel size
        :rtype: float
        """
        if self._EDFTomoScan__pixel_size is None:
            self._EDFTomoScan__pixel_size = utils.getPixelSize(scan=(self.path))
        return self._EDFTomoScan__pixel_size

    def get_dim_1(self):
        """

        :return: image dim1
        :rtype: int
        """
        if self._EDFTomoScan__dim1 is None:
            self._EDFTomoScan__dim1, self._EDFTomoScan__dim2 = utils.getDim1Dim2(scan=(self.path))
        return self._EDFTomoScan__dim1

    def get_dim_2(self):
        """

        :return: image dim2
        :rtype: int
        """
        if self._EDFTomoScan__dim2 is None:
            self._EDFTomoScan__dim1, self._EDFTomoScan__dim2 = utils.getDim1Dim2(scan=(self.path))
        return self._EDFTomoScan__dim2

    def get_ref_on(self):
        if self._EDFTomoScan__ref_on is None:
            self._EDFTomoScan__ref_on = utils.getRefOn(scan=(self.path))
        return self._EDFTomoScan__ref_on

    def get_scan_range(self):
        if self._EDFTomoScan__scan_range is None:
            self._EDFTomoScan__scan_range = utils.getScanRange(scan=(self.path))
        return self._EDFTomoScan__scan_range

    def _get_scheme(self):
        """

        :return: scheme to read url
        :rtype: str
        """
        return 'fabio'

    @functools.lru_cache(maxsize=16, typed=True)
    def get_sinogram(self, line, subsampling=1):
        """
        TODO: handle several sinogram load

        extract the sinogram from the radios / projections

        :param line: which sinogram we want
        :type: int
        :param subsampling: subsampling to apply if any. Allows to skip some io
        :type: int
        :return: sinogram from the radio lines
        :rtype: numpy.array
        """
        _logger.info('compute sinogram for line %s of %s (subsampling: %s)' % (line, self.path, subsampling))
        assert isinstance(line, int)
        if self.get_tomo_n() is not None and self.get_dim_2() is not None and line > self.get_dim_2():
            raise ValueError('requested line %s is not in the scan')
        else:
            sinogram = numpy.empty((self.get_tomo_n() // subsampling + 1, self.get_dim_1()))
            proj_urls = self.getProjectionsUrl()
            proj_sort = list(proj_urls.keys())
            proj_sort = list(filter(lambda x: not isinstance(x, str), proj_sort))
            proj_sort.sort()
            advancement = Progress(name=('compute sinogram for %s, line=%s,sampling=%s' % (
             os.path.basename(self.path),
             line, subsampling)))
            advancement.setMaxAdvancement(len(proj_sort))
            for i_proj, proj in enumerate(proj_sort):
                if i_proj % subsampling == 0:
                    url = proj_urls[proj]
                    radio = silx.io.utils.get_data(url)
                    radio = self.flatFieldCorrection(radio)
                    sinogram[i_proj // subsampling] = radio[line]
                advancement.increaseAdvancement(1)

            return sinogram


def _get_urls_list(radio):
    """create the list of urls contained in a .edf file"""
    with fabio.open(radio) as (edf_reader):
        if edf_reader.nframes is 1:
            return [
             DataUrl(file_path=radio, scheme='fabio')]
        res = []
        for iframe in range(edf_reader.nframes):
            res.append(DataUrl(file_path=radio, data_slice=[iframe], scheme='fabio'))

        return res