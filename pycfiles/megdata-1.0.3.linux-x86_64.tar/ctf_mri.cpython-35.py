# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/megdata/ctf_mri.py
# Compiled at: 2018-10-24 06:01:48
# Size of source mod 2**32: 4732 bytes
import os
from numpy import array
from .common import *

class CTFMRIFile(object):

    @classmethod
    def from_file(cls, filename):
        """
        Read a CTF MRI file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @staticmethod
    def cache_from_fd(fd):
        """
        Reads a dictionary of information from the MRI file.

        :param fd: File descriptor.  Must be at start of first tag.
        :type fd: File descriptor.

        :rtype: dict
        :returns: Dictionary of values from file.
        """
        cache = {}
        while True:
            labelsize = megdata_read_int32(fd)
            label = megdata_read_str(fd, labelsize)
            if label == 'EndOfParameters':
                break
            valuetype = megdata_read_int32(fd)
            if valuetype == 3:
                vsize = megdata_read_int32(fd)
                value = os.lseek(fd, 0, os.SEEK_CUR)
                os.lseek(fd, vsize, os.SEEK_CUR)
            else:
                if valuetype == 4:
                    value = megdata_read_double(fd)
                else:
                    if valuetype == 5:
                        value = megdata_read_int32(fd)
                    else:
                        if valuetype == 6:
                            value = megdata_read_int16(fd)
                        else:
                            if valuetype == 7:
                                value = megdata_read_uint16(fd)
                            else:
                                if valuetype == 10:
                                    vlength = megdata_read_int32(fd)
                                    value = megdata_read_str(fd, vlength)
                                else:
                                    raise Exception('Cannot parse CTF MRI value type %d' % valuetype)
            if label in cache:
                cache[label] = [
                 cache[label]]
                cache[label].append(value)
            else:
                cache[label] = value

        return cache

    @staticmethod
    def array_from_string(string, size):
        return array([float(x) for x in string.split('\\')]).reshape(size)

    @staticmethod
    def array_from_cache(cache, key, size):
        if key in cache:
            return CTFMRIFile.array_from_string(cache[key], size)
        else:
            return

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.version = megdata_read_str(fd, 4)
        if ret.version != 'WS1_':
            raise ValueError('Only support WS1_ format MRI files at the moment (%s)' % ret.version)
        ret.cache = CTFMRIFile.cache_from_fd(fd)
        cache = ret.cache
        ret.identifier = cache.get('_CTFMRI_VERSION', None)
        ret.image_size = cache.get('_CTFMRI_SIZE', None)
        ret.data_size = cache.get('_CTFMRI_DATASIZE', None)
        ret.orthogonal_flag = cache.get('_CTFMRI_ORTHOGONALFLAG', None)
        ret.interpolated_flag = cache.get('_CTFMRI_INTERPOLATEDFLAG', None)
        ret.comment = cache.get('_CTFMRI_COMMENT', None)
        ret.rotation = CTFMRIFile.array_from_cache(cache, '_CTFMRI_ROTATE', (3, 1))
        ret.transform = CTFMRIFile.array_from_cache(cache, '_CTFMRI_TRANSFORMMATRIX', (4,
                                                                                       4))
        ret.mm_per_pix = CTFMRIFile.array_from_cache(cache, '_CTFMRI_MMPERPIXEL', (3,
                                                                                   1))
        ret.hdm_nasion = CTFMRIFile.array_from_cache(cache, '_HDM_NASION', (3, 1))
        ret.hdm_leftear = CTFMRIFile.array_from_cache(cache, '_HDM_LEFTEAR', (3, 1))
        ret.hdm_rightear = CTFMRIFile.array_from_cache(cache, '_HDM_RIGHTEAR', (3,
                                                                                1))
        ret.hdm_sphere = CTFMRIFile.array_from_cache(cache, '_HDM_DEFAULTSPHERE', (4,
                                                                                   1))
        ret.hdm_origin = CTFMRIFile.array_from_cache(cache, '_HDM_HEADORIGIN', (3,
                                                                                1))
        return ret