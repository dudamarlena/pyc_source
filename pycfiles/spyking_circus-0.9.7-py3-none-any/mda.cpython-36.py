# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/files/mda.py
# Compiled at: 2019-11-21 11:07:32
# Size of source mod 2**32: 4206 bytes
import numpy, re, sys, re, logging, struct
from circus.shared.messages import print_and_log
from .raw_binary import RawBinaryFile
logger = logging.getLogger(__name__)

class MdaHeader:

    def __init__(self, dt0, dims0):
        uses64bitdims = max(dims0) > 2000000000.0
        self.uses64bitdims = uses64bitdims
        self.dt_code = _dt_code_from_dt(dt0)
        self.dt = dt0
        self.num_bytes_per_entry = get_num_bytes_per_entry_from_dt(dt0)
        self.num_dims = len(dims0)
        self.dimprod = numpy.prod(dims0)
        self.dims = dims0
        if uses64bitdims:
            self.header_size = 12 + self.num_dims * 8
        else:
            self.header_size = (3 + self.num_dims) * 4


def _dt_from_dt_code(dt_code):
    if dt_code == -2:
        dt = 'uint8'
    else:
        if dt_code == -3:
            dt = 'float32'
        else:
            if dt_code == -4:
                dt = 'int16'
            else:
                if dt_code == -5:
                    dt = 'int32'
                else:
                    if dt_code == -6:
                        dt = 'uint16'
                    else:
                        if dt_code == -7:
                            dt = 'float64'
                        else:
                            if dt_code == -8:
                                dt = 'uint32'
                            else:
                                dt = None
    return dt


def _dt_code_from_dt(dt):
    if dt == 'uint8':
        return -2
    else:
        if dt == 'float32':
            return -3
        else:
            if dt == 'int16':
                return -4
            else:
                if dt == 'int32':
                    return -5
                if dt == 'uint16':
                    return -6
            if dt == 'float64':
                return -7
        if dt == 'uint32':
            return -8


def get_num_bytes_per_entry_from_dt(dt):
    if dt == 'uint8':
        return 1
    else:
        if dt == 'float32':
            return 4
        else:
            if dt == 'int16':
                return 2
            else:
                if dt == 'int32':
                    return 4
                if dt == 'uint16':
                    return 2
            if dt == 'float64':
                return 8
        if dt == 'uint32':
            return 4


def _read_int32(f):
    return struct.unpack('<i', f.read(4))[0]


def _read_int64(f):
    return struct.unpack('<q', f.read(8))[0]


def _read_header(path):
    f = open(path, 'rb')
    try:
        dt_code = _read_int32(f)
        _ = _read_int32(f)
        num_dims = _read_int32(f)
        uses64bitdims = False
        if num_dims < 0:
            uses64bitdims = True
            num_dims = -num_dims
        if num_dims < 1 or num_dims > 6:
            print('Invalid number of dimensions: {}'.format(num_dims))
            f.close()
            return
        dims = []
        dimprod = 1
        if uses64bitdims:
            for _ in range(0, num_dims):
                tmp0 = _read_int64(f)
                dimprod = dimprod * tmp0
                dims.append(tmp0)

        else:
            for _ in range(0, num_dims):
                tmp0 = _read_int32(f)
                dimprod = dimprod * tmp0
                dims.append(tmp0)

        dt = _dt_from_dt_code(dt_code)
        if dt is None:
            print('Invalid data type code: {}'.format(dt_code))
            f.close()
            return
        H = MdaHeader(dt, dims)
        if uses64bitdims:
            H.uses64bitdims = True
            H.header_size = 12 + H.num_dims * 8
        f.close()
        return H
    except Exception as e:
        print(e)
        f.close()
        return


class MdaFile(RawBinaryFile):
    description = 'mda'
    extension = ['.mda']
    _required_fields = {'sampling_rate': float}

    def _get_header(self):
        try:
            mda_header = _read_header(self.file_name)
            header = {}
            header['data_dtype'] = mda_header.dt
            header['data_offset'] = mda_header.header_size
            header['gain'] = 1
            header['nb_channels'] = mda_header.dims[0]
            return header
        except Exception:
            print_and_log(['Wrong MDA header'], 'error', logger)
            sys.exit(1)

    def _read_from_header(self):
        header = self._get_header()
        self.data = numpy.memmap((self.file_name), offset=(header['data_offset']), dtype=(header['data_dtype']), mode='r')
        self.size = len(self.data)
        self._shape = (self.size // header['nb_channels'], header['nb_channels'])
        del self.data
        return header