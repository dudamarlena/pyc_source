# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/brk_raw_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 11648 bytes
import os, struct
from io import SEEK_SET, SEEK_CUR
import numpy as np
from pyxrd.generic.io.utils import get_case_insensitive_glob
from pyxrd.generic.utils import u
from ..base_parser import BaseParser
from .namespace import xrd_parsers
from .xrd_parser_mixin import XRDParserMixin

@xrd_parsers.register_parser()
class BrkRAWParser(XRDParserMixin, BaseParser):
    __doc__ = '\n        Bruker *.RAW format parser\n    '
    description = 'Bruker/Siemens Binary V1/V2/V3 *.RAW'
    extensions = get_case_insensitive_glob('*.RAW')
    mimetypes = ['application/octet-stream']
    __file_mode__ = 'rb'

    @classmethod
    def _clean_bin_str(cls, val):
        return u(val.replace('\x00'.encode(), ''.encode()).strip())

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False):
        f = fp
        try:
            basename = u(os.path.basename(filename))
        except:
            basename = None

        f.seek(0, SEEK_SET)
        version = f.read(4).decode('utf-8')
        if version == 'RAW ':
            version = 'RAW1'
        else:
            if version == 'RAW2':
                version = 'RAW2'
            elif version == 'RAW1':
                if str(f.read(3)) == '.01':
                    version = 'RAW3'
            else:
                if version == 'RAW1':
                    isfollowed = 1
                    num_samples = 0
                    while isfollowed > 0:
                        twotheta_count = int(struct.unpack('I', f.read(4))[0])
                        if num_samples > 0:
                            if twotheta_count == int(struct.unpack('I', 'RAW ')[0]):
                                twotheta_count = int(struct.unpack('I', f.read(4))[0])
                        time_step, twotheta_step, scan_mode = struct.unpack('fff', f.read(12))
                        f.seek(4, SEEK_CUR)
                        twotheta_min, = struct.unpack('f', f.read(4))
                        twotheta_max = twotheta_min + twotheta_step * float(twotheta_count)
                        f.seek(12, SEEK_CUR)
                        sample_name = cls._clean_bin_str(f.read(32))
                        alpha1, alpha2 = struct.unpack('ff', f.read(8))
                        f.seek(72, SEEK_CUR)
                        isfollowed, = struct.unpack('I', f.read(4))
                        data_start = f.tell()
                        f.seek(twotheta_count * 4, SEEK_CUR)
                        data_objects = cls._adapt_data_object_list(data_objects,
                          num_samples=(num_samples + 1),
                          only_extend=True)
                        data_objects[num_samples].update(filename=basename,
                          version=version,
                          name=sample_name,
                          time_step=time_step,
                          twotheta_min=twotheta_min,
                          twotheta_max=twotheta_max,
                          twotheta_step=twotheta_step,
                          twotheta_count=twotheta_count,
                          alpha1=alpha1,
                          alpha2=alpha2,
                          data_start=data_start)
                        num_samples += 1

                else:
                    if version == 'RAW2':
                        num_samples, = struct.unpack('H', f.read(2))
                        data_objects = cls._adapt_data_object_list(data_objects, num_samples=num_samples)
                        f.seek(8, SEEK_SET)
                        sample_name = cls._clean_bin_str(f.read(32))
                        f.seek(148, SEEK_CUR)
                        target_type = u(str(f.read(2)).replace('\x00', '').strip())
                        alpha1, alpha2, alpha_factor = struct.unpack('fff', f.read(12))
                        f.seek(8, SEEK_CUR)
                        time_total, = struct.unpack('f', f.read(4))
                        f.seek(256, SEEK_SET)
                        for i in range(num_samples):
                            header_start = f.tell()
                            header_length, twotheta_count = struct.unpack('HH', f.read(4))
                            data_start = header_start + header_length
                            f.seek(header_start + 12)
                            twotheta_step, twotheta_min = struct.unpack('ff', f.read(8))
                            twotheta_max = twotheta_min + twotheta_step * float(twotheta_count)
                            f.seek(data_start + twotheta_count * 4, SEEK_SET)
                            data_objects[i].update(filename=basename,
                              version=version,
                              name=sample_name,
                              twotheta_min=twotheta_min,
                              twotheta_max=twotheta_max,
                              twotheta_step=twotheta_step,
                              twotheta_count=twotheta_count,
                              alpha1=alpha1,
                              alpha2=alpha2,
                              alpha_factor=alpha_factor,
                              data_start=data_start)

                    else:
                        if version == 'RAW3':
                            f.seek(8, SEEK_SET)
                            file_status = {1:'done', 
                             2:'active', 
                             3:'aborted', 
                             4:'interrupted'}[int(struct.unpack('I', f.read(4))[0])]
                            f.seek(12, SEEK_SET)
                            num_samples, = struct.unpack('I', f.read(4))
                            f.seek(326, SEEK_SET)
                            sample_name = cls._clean_bin_str(f.read(60))
                            f.seek(564, SEEK_SET)
                            radius = float(struct.unpack('f', f.read(4))[0])
                            f.seek(568, SEEK_SET)
                            divergence = float(struct.unpack('f', f.read(4))[0])
                            f.seek(576, SEEK_SET)
                            soller1 = float(struct.unpack('f', f.read(4))[0])
                            f.seek(592, SEEK_SET)
                            soller2 = float(struct.unpack('f', f.read(4))[0])
                            f.seek(608, SEEK_SET)
                            target_type = str(f.read(4))
                            f.seek(616, SEEK_SET)
                            alpha_average, alpha1, alpha2, beta, alpha_factor = struct.unpack('ddddd', f.read(40))
                            f.seek(664, SEEK_SET)
                            time_total, = struct.unpack('f', f.read(4))
                            data_objects = cls._adapt_data_object_list(data_objects, num_samples=num_samples)
                            f.seek(712, SEEK_SET)
                            for i in range(num_samples):
                                header_start = f.tell()
                                f.seek(header_start + 0, SEEK_SET)
                                header_length, = struct.unpack('I', f.read(4))
                                assert header_length == 304, 'Invalid format!'
                                f.seek(header_start + 4, SEEK_SET)
                                twotheta_count, = struct.unpack('I', f.read(4))
                                f.seek(header_start + 8, SEEK_SET)
                                theta_min, twotheta_min = struct.unpack('dd', f.read(16))
                                f.seek(header_start + 176, SEEK_SET)
                                twotheta_step, = struct.unpack('d', f.read(8))
                                f.seek(header_start + 192, SEEK_SET)
                                time_step, = struct.unpack('d', f.read(8))
                                f.seek(header_start + 240, SEEK_SET)
                                alpha_used, = struct.unpack('d', f.read(8))
                                f.seek(header_start + 256, SEEK_SET)
                                supp_headers_size, = struct.unpack('I', f.read(4))
                                data_start = header_start + header_length + supp_headers_size
                                f.seek(data_start + twotheta_count * 4)
                                twotheta_max = twotheta_min + twotheta_step * float(twotheta_count - 0.5)
                                data_objects[i].update(filename=basename,
                                  version=version,
                                  name=sample_name,
                                  twotheta_min=twotheta_min,
                                  twotheta_max=twotheta_max,
                                  twotheta_step=twotheta_step,
                                  twotheta_count=twotheta_count,
                                  alpha1=alpha1,
                                  alpha2=alpha2,
                                  alpha_factor=alpha_factor,
                                  data_start=data_start,
                                  radius=radius,
                                  soller1=soller1,
                                  soller2=soller2,
                                  divergence=divergence)

                        else:
                            raise IOError('Only verson 1, 2 and 3 *.RAW files are supported!')
        if close:
            f.close()
        return data_objects

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=False):
        for data_object in data_objects:
            if data_object.data == None:
                data_object.data = []
            if fp is not None:
                if data_object.version in ('RAW1', 'RAW2', 'RAW3'):
                    fp.seek(data_object.data_start)
                    n = 0
                    while n < data_object.twotheta_count:
                        y, = struct.unpack('f', fp.read(4))
                        x = data_object.twotheta_min + data_object.twotheta_step * float(n + 0.5)
                        data_object.data.append([x, y])
                        n += 1

                else:
                    raise IOError('Only verson 1, 2 and 3 *.RAW files are supported!')
            data_object.data = np.array(data_object.data)

        if close:
            fp.close()
        return data_objects