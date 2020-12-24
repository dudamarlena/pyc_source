# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/megdata/bti_dipolefile.py
# Compiled at: 2018-10-24 06:01:48
# Size of source mod 2**32: 8945 bytes
import os
from .common import *

class BTIDipole(object):
    __doc__ = 'Individual dipole object within a .dipole file'

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.position = megdata_read_vec3(fd)
        ret.orientation = megdata_read_vec3(fd)
        ret.correlation = megdata_read_float(fd)
        ret.goodness = megdata_read_float(fd)
        ret.cx = megdata_read_float(fd)
        ret.cy = megdata_read_float(fd)
        ret.cz = megdata_read_float(fd)
        ret.rms = megdata_read_float(fd)
        ret.latency = megdata_read_float(fd)
        ret.epoch = megdata_read_int16(fd)
        ret.iterations = megdata_read_int16(fd)
        ret.color = megdata_read_int16(fd)
        ret.shape = megdata_read_int16(fd)
        ret.label = megdata_read_str(fd, 65)
        ret.scan = megdata_read_str(fd, 11)
        ret.session = megdata_read_str(fd, 16)
        ret.run = megdata_read_str(fd, 3)
        ret.pdf_name = megdata_read_str(fd, 73)
        ret.patient = megdata_read_str(fd, 11)
        megdata_read_char(fd, 1)
        ret.avgChannelNoise = megdata_read_float(fd)
        ret.channelListLen = megdata_read_int16(fd)
        megdata_read_char(fd, 2)
        ret.channelList = ''.join(megdata_read_char(fd, ret.channelListLen)[:-1]).split(',')
        return ret

    def str_indent(self, indent=0):
        s = ' ' * indent + '<BTIDipole\n'
        s += ' ' * indent + '  Position:         ' + str(self.position) + '\n'
        s += ' ' * indent + '  Orientation:      ' + str(self.orientation) + '\n'
        s += ' ' * indent + '  Correlation:      %e\n' % self.correlation
        s += ' ' * indent + '  Confidence Area:  %e %e %e\n' % (self.cx, self.cy, self.cz)
        s += ' ' * indent + '  RMS:              %e\n' % self.rms
        s += ' ' * indent + '  Latency:          %.6f\n' % self.latency
        s += ' ' * indent + '  Epoch:            %d\n' % self.epoch
        s += ' ' * indent + '  Num Iterations:   %d\n' % self.iterations
        s += ' ' * indent + '  Colour / Shape:   %d / %d\n' % (self.color, self.shape)
        s += ' ' * indent + '  Avg Chan Noise:   %e\n' % self.avgChannelNoise
        s += ' ' * indent + '  Num Channels:     %d\n' % len(self.channelList)
        s += ' ' * indent + '  Channels:         %s\n' % ','.join(self.channelList)
        s += ' ' * indent + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIDipoleFile(object):

    @staticmethod
    def _parse_string(val):
        try:
            ret = val.split(' : ')[1]
            if ret.endswith(';'):
                ret = ret[:-1]
        except Exception as e:
            print(e)
            raise ValueError('Parse error reading string')

        return ret

    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI dipole data file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.version = ret._parse_string(megdata_read_bytes(fd))
        if ret.version != '4.0':
            raise Exception('Bad version number (only 4.0 supported)')
        ret.patient_id = ret._parse_string(megdata_read_bytes(fd))
        num_entries = int(ret._parse_string(megdata_read_bytes(fd)))
        ret.dipoles = []
        for k in range(num_entries):
            dip = BTIDipole.from_fd(fd)
            ret.dipoles.append(dip)

        return ret

    def str_indent(self, indent=0):
        s = ' ' * indent + '<BTIDipoleFile\n'
        s += ' ' * indent + '  Version:          %s\n' % self.version
        s += ' ' * indent + '  Patient ID:       %s\n' % self.patient_id
        s += ' ' * indent + '  Dipole Count:     %d\n' % len(self.dipoles)
        s += ' ' * indent + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIDipoleTextFile(object):

    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI text dipole file from a filename
        """
        from numpy import array
        f = open(filename, 'r')
        ret = cls()
        ret.dipoles = []
        data = [x.strip() for x in f.readlines()]
        cur_epoch = None
        average_noise = None
        patient = None
        scan = None
        session = None
        run = None
        pdf_name = None
        channel_group = None
        local_sphere = None
        ignored_chans = None
        skipif = [
         'Page', 'Output', 'Sensors', 'Default', 'Grid',
         'Ignored', 'Patient', 'Latency', 'skipping', '(msec)']
        for line in data:
            skip = False
            for s in skipif:
                if line.startswith(s):
                    skip = True

            if len(line.strip()) == 0:
                skip = True
            if skip:
                pass
            else:
                if line.startswith('EPOCH'):
                    cur_epoch = int(line.split()[1])
                    continue
                if line.startswith('Average Noise'):
                    average_noise = float(line.split()[2])
                    continue
                    if line.startswith('Input'):
                        line = line.split()
                        patient = line[1]
                        scan = line[2]
                        session = ' '.join(line[3:5])
                        run = int(line[5])
                        pdf_name = line[6]
                        channel_group = line[7]
                        local_sphere = [float(x) for x in line[8].strip('(').strip(')').split(',')]
                        continue
                        if line.startswith('Ignored'):
                            line = line.split()
                            print(line)
                            ignored_chans = line[3]
                            continue
                            linedat = line.split()
                            if len(linedat) != 17:
                                print('Error, ', len(linedat))
                                print(linedat)
                            latency = float(linedat[0])
                            x = float(linedat[1]) / 100.0
                            y = float(linedat[2]) / 100.0
                            z = float(linedat[3]) / 100.0
                            Qx = float(linedat[4]) / 100.0
                            Qy = float(linedat[5]) / 100.0
                            Qz = float(linedat[6]) / 100.0
                            radius = float(linedat[7]) / 100.0
                            modQ = float(linedat[8])
                            rms = float(linedat[9])
                            cvol = float(linedat[10])
                            cx = float(linedat[11]) / 100.0
                            cy = float(linedat[12]) / 100.0
                            cz = float(linedat[13]) / 100.0
                            corr = float(linedat[14])
                            gof = float(linedat[15])
                            iteration = int(linedat[16])
                            dip = BTIDipole()
                            dip.position = array([[x, y, z]])
                            dip.orientation = array([Qx, Qy, Qz])
                            dip.correlation = corr
                            dip.goodness = gof
                            dip.cx = cx
                            dip.cy = cy
                            dip.cz = cz
                            dip.rms = rms
                            dip.latency = latency
                            dip.epoch = cur_epoch
                            dip.iterations = iteration
                            dip.color = 0
                            dip.shape = 0
                            dip.label = ''
                            dip.scan = scan
                            dip.session = session
                            dip.run = run
                            dip.pdf_name = pdf_name
                            dip.patient = patient
                            dip.avgChannelNoise = average_noise
                            dip.channelListLen = 1
                            dip.channelList = [channel_group]
                            ret.dipoles.append(dip)

        return ret

    def str_indent(self, indent=0):
        s = ' ' * indent + '<BTIDipoleTextFile\n'
        s += ' ' * indent + '  Dipole Count:     %d\n' % len(self.dipoles)
        s += ' ' * indent + '>\n'
        return s

    def __str__(self):
        return self.str_indent()