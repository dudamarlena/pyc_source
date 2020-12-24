# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/megdata/ctf_dataset.py
# Compiled at: 2018-10-24 06:01:48
# Size of source mod 2**32: 6922 bytes
import os, numpy
from .common import *
from .ctf_res4 import *

class CTFDataset(object):

    @classmethod
    def from_file(cls, filename, data_filename=None):
        """
        Set up a wrapper CTFDataset object from a .res4 file.
        It is assumed (unless data_filename is set) that the data
        is in a .meg4 file next to the .res4 file.
        """
        if data_filename is None:
            if filename.endswith('.res4'):
                data_filename = filename[:-5] + '.meg4'
            else:
                data_filename = filename + '.meg4'
            if not os.path.isfile(data_filename):
                raise IOError('Cannot find data file %s' % data_filename)
            fd = os.open(filename, os.O_RDONLY)
            ret = cls()
            ret.res = CTFRes4File.from_fd(fd)
            ret.res_filename = filename
            ret.data_filename = data_filename
            ret.data_file = open(data_filename, 'rb')
            ret.init_data_information()
            os.close(fd)
            return ret

    def init_data_information(self):
        self.data_file.seek(0)
        hdrstring = megdata_read_str(self.data_file.fileno(), 8)
        if hdrstring != 'MEG41CP' and hdrstring != 'MEG42CP':
            raise ValueError('Unknown data format %s' % hdrstring)
        self.data_file.seek(0, os.SEEK_END)
        file_size = self.data_file.tell()
        self.data_file.seek(0, os.SEEK_SET)
        self.bytes_per_channel_seg = 4 * self.res.no_samples
        self.bytes_per_epoch = self.bytes_per_channel_seg * self.res.no_channels
        if self.bytes_per_epoch * self.res.no_trials + 8 != file_size:
            raise ValueError("Trials (%d), Samples (%d) and Channels (%d) doesn't match file size (%d)" % (
             self.res.no_trials,
             self.res.no_samples,
             self.res.no_channels,
             file_size))
        self.scales = numpy.ones((1, self.res.no_channels), dtype=numpy.float64)
        self.meg_indices = []
        self.ref_indices = []
        self.eeg_indices = []
        self.eeg_ref_indices = []
        self.aux_indices = []
        for c in range(self.res.no_channels):
            if self.res.channels[c].ctype >= 0 and self.res.channels[c].ctype <= 7:
                self.scales[(0, c)] = 1000000000000000
                if self.res.channels[c].ctype <= 4:
                    self.ref_indices.append(c)
                else:
                    self.meg_indices.append(c)
            else:
                if self.res.channels[c].ctype >= 8 and self.res.channels[c].ctype <= 10:
                    self.scales[(0, c)] = 1000000
                    if self.res.channels[c].ctype == 8:
                        self.eeg_indices.append(c)
                    else:
                        if self.res.channels[c].ctype == 9:
                            self.eeg_ref_indices.append(c)
                        else:
                            self.aux_indices.append(c)
                else:
                    self.aux_indices.append(c)
            self.scales[(0, c)] = self.scales[(0, c)] / (self.res.channels[c].gain * self.res.channels[c].q_gain)

    @property
    def total_slices(self):
        return self.res.no_samples * self.res.no_trials

    @property
    def numpy_datatype(self):
        return numpy.dtype('>i4')

    def read_raw_data(self, slices=None, indices=None):
        total_slices = self.total_slices
        if slices is None:
            startp = 0
            endp = total_slices
        else:
            startp = slices[0]
            endp = slices[1]
        if startp < 0 or endp > total_slices or startp >= endp:
            raise RuntimeError('Invalid start and end slices for get_slice_range(): %d, %d' % (startp, endp))
        epochlist = list(range(int(startp / self.res.no_samples), int((endp - 1) / self.res.no_samples) + 1))
        unordered_data = numpy.empty((len(epochlist) * self.res.no_samples, self.res.no_channels), self.numpy_datatype)
        pos = 0
        for e in epochlist:
            self.data_file.seek(8 + e * self.bytes_per_epoch, os.SEEK_SET)
            dat = numpy.reshape(numpy.fromfile(self.data_file, dtype=self.numpy_datatype, count=self.res.no_samples * self.res.no_channels), [
             self.res.no_samples, self.res.no_channels], order='F')
            unordered_data[pos:pos + self.res.no_samples, :] = dat
            pos += self.res.no_samples

        start_offset = startp % self.res.no_samples
        unordered_data = unordered_data[start_offset:start_offset + (endp - startp), :]
        if indices is None:
            data = unordered_data
        else:
            if isinstance(indices, int):
                data = unordered_data[:, indices]
            else:
                rows = numpy.arange(unordered_data.shape[0])
                cols = numpy.array(indices)
                data = unordered_data.ravel()[(cols + (rows * unordered_data.shape[1]).reshape((-1,
                                                                                                1))).ravel()].reshape(rows.size, cols.size)
                del unordered_data
        return data

    def str_indent(self, indent=0):
        s = ''
        s += ' ' * indent + '<CTFDataset\n'
        s += ' ' * indent + '  Resource Filename: %s\n' % self.res_filename
        s += ' ' * indent + '  Data Filename:     %s\n' % self.data_filename
        s += self.res.str_indent(indent=indent + 2)
        s += ' ' * indent + '>\n'
        return s

    def __str__(self):
        return self.str_indent()