# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/scan/scanfactory.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 4744 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '27/02/2019'
from .scanbase import ScanBase
from .edfscan import EDFTomoScan
from .hdf5scan import HDF5TomoScan
import os, glob, json

class ScanFactory(object):

    @staticmethod
    def create_scan_object(scan_path):
        """
        
        :param TextIOWrapper scan_path: path to the scan directory or file
        :return: ScanBase instance fitting the scan folder or scan path
        :rtype: tomwer.core.scan.scanbase.ScanBase
        :raises: ValueError if scan_path is not containing a scan
        """
        if ScanFactory.is_tomo_scandir(scan_path):
            if ScanFactory.is_edf_tomo(scan_path):
                return EDFTomoScan(scan=scan_path)
            if ScanFactory.is_hdf5_tomo(scan_path):
                return HDF5TomoScan(scan=scan_path)
        raise ValueError('Unable to generate a scan object from %s' % scan_path)

    @staticmethod
    def mock_scan(type='edf'):
        """Mock a scan structure which is not associated to any real acquistion
        """
        if type == 'edf':
            return EDFTomoScan(scan=None)
        raise NotImplementedError('Other TomoScan are not defined yet')

    @staticmethod
    def create_scan_object_frm_dict(_dict):
        if ScanBase._DICT_TYPE_KEY not in _dict:
            raise ValueError('given dict is not recognized. Cannot find', ScanBase._DICT_TYPE_KEY)
        else:
            if _dict[ScanBase._DICT_TYPE_KEY] == EDFTomoScan._TYPE:
                return EDFTomoScan(scan=None).load_from_dict(_dict)
            raise ValueError('Scan type', _dict[ScanBase._DICT_TYPE_KEY], 'is not managed')

    @staticmethod
    def is_tomo_scandir(scan_path):
        """
        
        :param str scan_path: path to the scan directory or file
        :return: True if the given path / file is a tomo_scandir. For now yes by
                 default
        :rtype: bool
        """
        return True

    @staticmethod
    def is_edf_tomo(scan_path):
        """
        
        :param str scan_path: path to the scan directory or file
        :return: True if given path define a tomo scan based on .edf file
        :rtype: bool
        """
        if scan_path:
            if os.path.isdir(scan_path):
                file_basename = os.path.basename(scan_path)
                has_info_file = len(glob.glob(os.path.join(scan_path, file_basename + '*.info'))) > 0
                not_lbs_scan_path = scan_path.replace('lbsram', '', 1)
                has_notlbsram_info_file = len(glob.glob(os.path.join(not_lbs_scan_path, file_basename + '*.info'))) > 0
                if not has_info_file:
                    if has_notlbsram_info_file:
                        return True
        return False

    @staticmethod
    def is_hdf5_tomo(scan_path):
        """

        :param scan_path:
        :return:
        """
        return HDF5TomoScan.directory_contains_scan(scan_path)

    @staticmethod
    def create_from_json(desc):
        """Create a ScanBase instance from a json description"""
        data = json.load(desc)
        if ScanBase._DICT_TYPE_KEY not in data:
            raise ValueError('json not recognize')
        else:
            if data[ScanBase._DICT_TYPE_KEY] == EDFTomoScan._TYPE:
                scan = EDFTomoScan(scan=None).load_from_dict(data)
                return scan
            raise ValueError('Type', data[ScanBase.type], 'is not managed')