# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/scan/hdf5scan.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 14178 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '09/08/2018'
from .scanbase import TomoBase
import json, io, os, h5py, numpy
from silx.io.url import DataUrl
import logging
_logger = logging.getLogger(__name__)

class HDF5TomoScan(TomoBase):
    __doc__ = "\n    This is the implementation of a TomoBase class for an acquisition stored\n    in a HDF5 file.\n\n    For now several property of the acquisition is accessible thought a getter\n    (like get_scan_range) and a property (scan_range).\n\n    This is done to be compliant with TomoBase instanciation. But his will be\n    replace progressively by properties at the 'TomoBase' level\n\n    :param scan: scan directory or scan masterfile.h5\n    :type: Union[str,None]\n    "
    _TYPE = 'hdf5'

    def __init__(self, scan):
        if scan is not None:
            if os.path.isfile(scan):
                self.master_file = scan
                scan = os.path.dirname(scan)
            else:
                self.master_file = os.path.join(scan, os.path.basename(scan))
                if os.path.exists(self.master_file + '.hdf5'):
                    self.master_file = self.master_file + '.hdf5'
                else:
                    self.master_file = self.master_file + '.h5'
        else:
            self.master_file = None
        super(HDF5TomoScan, self).__init__(scan=scan, _type=(HDF5TomoScan._TYPE))
        self._entry = '1_tomo'
        self._tomo_n = None
        self._dark_n = None
        self._ref_n = None
        self._ref_on = None
        self._scan_range = None
        self._dim_1, self._dim_2 = (None, None)
        self._pixel_size = None
        if scan is not None:
            self._process_file = os.path.join(scan, 'tomwer_processes.h5')

    @staticmethod
    def directory_contains_scan(directory, src_pattern=None, dest_pattern=None):
        """

        Check if the given directory is holding an acquisition

        :param str directory: directory we want to check
        :param str src_pattern: buffer name pattern ('lbsram')
        :param dest_pattern: output pattern (''). Needed because some
                             acquisition can split the file produce between
                             two directories. This is the case for edf,
                             where .info file are generated in /data/dir
                             instead of /lbsram/data/dir
        :type: str
        :return: does the given directory contains any acquisition
        :rtype: bool
        """
        master_file = os.path.join(directory, os.path.basename(directory))
        if os.path.exists('master_file.hdf5'):
            return True
        return os.path.exists(master_file + '.h5')

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
        return False

    @staticmethod
    def from_dict(_dict):
        scan = HDF5TomoScan(scan=None)
        scan.load_from_dict(_dict=_dict)
        return scan

    def load_from_dict(self, _dict):
        """

        :param _dict:
        :return:
        """
        from tomwer.core.process.reconstruction.ftseries.params import ReconsParams
        if isinstance(_dict, io.TextIOWrapper):
            data = json.load(_dict)
        else:
            data = _dict
        if not (self._DICT_TYPE_KEY in data and data[self._DICT_TYPE_KEY] == self._TYPE):
            raise ValueError('Description is not an EDFScan json description')
        assert self._DICT_PATH_KEY in data
        assert self._DICT_LAMINO_RP_KEY in data
        self.path = data[self._DICT_PATH_KEY]
        recons_param_data = data[self._DICT_TOMO_RP_KEY]
        if recons_param_data is not None:
            self.ftseries_recons_params = ReconsParams.from_dict(recons_param_data)
        self.lamino_recons_params = data[self._DICT_LAMINO_RP_KEY]
        return self

    @property
    def projections(self):
        """list of projections files"""
        if self._projections is None or len(self._projections) != self.tomo_n:
            self.updateDataset()
        return self._projections

    @projections.setter
    def projections(self, projections):
        self._projections = projections

    def getDark(self):
        _logger.warning('dark path not defined yet for hdf5')

    def getFlat(self, index=None):
        _logger.warning('ref path not defined yet for hdf5')

    def updateDataset(self):
        """update list of radio and reconstruction by parsing the scan folder
        """
        if not os.path.exists(self.master_file):
            return
        self.projections = self.getRadioUrls()
        self.reconstructions = self.getReconstructionsUrls()

    def getRadioUrls(self):
        """

        :param path:
        :return:
        """
        return self.master_file is None or os.path.exists(self.master_file) or None
        with h5py.File(self.master_file, 'r') as (h5_file):
            urls = []
            if self._entry in h5_file:
                if 'measurement/pcoedge64:image' in h5_file[self._entry]:
                    image = h5_file[self._entry]['measurement/pcoedge64:image']

                    def get_reader(extension):
                        extension = extension.lower()
                        if extension == 'edf':
                            return 'fabio'
                        if extension == 'hdf5':
                            return 'silx'
                        _logger.warning('extension', extension, 'unrecognized to define a reader')
                        return

                    for i_slice, slice_data in enumerate(image):
                        if isinstance(slice_data, numpy.ndarray) and slice_data.ndim == 2:
                            silx_url = DataUrl(file_path=(self.master_file), data_path=('/'.join((self._entry, 'measurement/pcoedge64:image'))),
                              data_slice=(
                             i_slice,),
                              scheme='silx')
                        else:
                            scheme = get_reader(slice_data[1])
                            file_path = slice_data[4]
                            data_path = '/'.join((slice_data[3], 'measurement', 'pcoedge64', 'data'))
                            slice_number = slice_data[2]
                            silx_url = DataUrl(file_path=file_path, data_path=data_path, data_slice=(
                             slice_number,),
                              scheme=scheme)
                        urls.append(silx_url)

            return urls

    def getReconstructionsUrls(self):
        return []

    def get_tomo_n(self):
        """return the tomo_n property"""
        return self.tomo_n

    @property
    def tomo_n(self):
        if self._tomo_n is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file, 'r') as (h5_file):
                        self._tomo_n = h5_file[self._entry]['scan_meta/technique/scan/tomo_n'][()]
        return self._tomo_n

    def get_dark_n(self):
        """return the dark_n property"""
        return self.dark_n

    @property
    def dark_n(self):
        if self._dark_n is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file, 'r') as (h5_file):
                        self._dark_n = h5_file[self._entry]['scan_meta/technique/scan/dark_n'][()]
        return self._dark_n

    def get_ref_n(self):
        """return the ref_n property"""
        return self.ref_n

    @property
    def ref_n(self):
        if self._ref_n is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file, 'r') as (h5_file):
                        self._ref_n = h5_file[self._entry]['scan_meta/technique/scan/ref_n'][()]
        return self._ref_n

    def get_ref_on(self):
        """return the ref_on property"""
        return self.ref_on

    @property
    def ref_on(self):
        if self._ref_on is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file, 'r') as (h5_file):
                        self._ref_on = h5_file[self._entry]['scan_meta/technique/scan/ref_n'][()]
        return self._ref_on

    def get_scan_range(self):
        """return scan_range property"""
        return self.scan_range

    @property
    def scan_range(self):
        if self._scan_range is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file, 'r') as (h5_file):
                        self._scan_range = h5_file[self._entry]['scan_meta/technique/scan/scan_range'][()]
        return self._scan_range

    def get_dim_1(self):
        """return dim_1 property"""
        return self.dim_1

    @property
    def dim_1(self):
        if self._dim_1 is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file, 'r') as (h5_file):
                        self._dim_1 = h5_file[self._entry]['scan_meta/technique/detector/size'][0]
        return self._dim_1

    def get_dim_2(self):
        """return dim_2 property"""
        return self.dim_2

    @property
    def dim_2(self):
        if self._dim_2 is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file, 'r') as (h5_file):
                        self._dim_2 = h5_file[self._entry]['scan_meta/technique/detector/size'][()][1]
        return self._dim_2

    def getProjectionsUrl(self, use_cache=True):
        if not use_cache:
            self._cache_proj_urls = None
        elif self._cache_proj_urls is None:
            can_compute = True
            scan_range = self.scan_range
            if scan_range is None:
                _logger.warning('unable to deduced scan range so unable tocompute projection angles')
                can_compute = False
            projection_urls = self.projections
            if not projection_urls is None:
                if len(projection_urls) == 0:
                    _logger.warning('unable to retrieve projection')
                    can_compute = False
                tomo_n = self.tomo_n
                if tomo_n is None:
                    _logger.warning('unable find the theoretical number of projection')
                    can_compute = False
                if can_compute is False:
                    self._cache_proj_urls = None
            else:
                self._cache_proj_urls = TomoBase.map_urls_on_scan_range(urls=projection_urls, n_projection=tomo_n,
                  scan_range=scan_range)
        return self._cache_proj_urls

    getProjectionsUrl.__doc__ = TomoBase.__doc__

    def _get_scheme(self):
        """

        :return: scheme to read url
        :rtype: str
        """
        return 'silx'

    def get_pixel_size(self):
        """return pixel_size property"""
        return self.pixel_size

    @property
    def pixel_size(self):
        if self._pixel_size is None:
            if self.master_file:
                if os.path.exists(self.master_file):
                    with h5py.File(self.master_file) as (h5_file):
                        self._pixel_size = h5_file[self._entry]['scan_meta/technique/detector/pixel_size'][()]
        return self._pixel_size

    def is_finish(self):
        return len(self.projections) >= self.tomo_n

    def get_ff_interval(self):
        """

        :param clear_cache: if true then recompute the cache containing
                            the acquisition information
        :type: bool
        :return: number of radio between each reference / flat field
        :rtype: int
        """
        return self.get_ref_on()