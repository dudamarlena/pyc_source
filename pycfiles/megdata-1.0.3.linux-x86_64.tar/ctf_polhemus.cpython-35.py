# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/megdata/ctf_polhemus.py
# Compiled at: 2018-10-24 06:01:48
# Size of source mod 2**32: 2790 bytes
import numpy, os
from .common import *

class CTFPolhemus(object):

    @classmethod
    def from_file(cls, filename):
        """
        Read a CTF Polhemus file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        f = os.fdopen(os.dup(fd))
        num_bytes = 0
        dat = f.readline()
        num_bytes += len(dat)
        expected_points = int(dat.strip())
        if expected_points < 1:
            raise ValueError('Fewer than 1 point expected in header of file')
        pts = []
        for p in range(expected_points):
            dat = f.readline()
            num_bytes += len(dat)
            posnum, x, y, z = dat.split()
            posnum = int(posnum)
            if posnum != p + 1:
                raise ValueError('File inconsistency in point number when reading point %d' % (p + 1))
            pts.append([float(x), float(y), float(z)])

        ret.points = numpy.array(pts, dtype=numpy.float64)
        ret.fiducial_names = []
        pts = []
        while True:
            dat = f.readline()
            if len(dat) == 0:
                break
            num_bytes += len(dat)
            fidname, x, y, z = dat.split()
            ret.fiducial_names.append(fidname)
            pts.append([float(x), float(y), float(z)])

        ret.fiducial_pos = numpy.array(pts, dtype=numpy.float64)
        f.close()
        os.lseek(fd, num_bytes, os.SEEK_CUR)
        return ret

    def str_indent(self, indent=0):
        s = ''
        s += ' ' * indent + '<CTFPolhemus\n'
        s += ' ' * indent + '  Num Points:        %d\n' % self.points.shape[0]
        s += ' ' * indent + '  Points:            ' + megdata_array_print(self.points) + '\n'
        s += ' ' * indent + '  Num Fiducials      %d\n' % len(self.fiducial_names)
        s += ' ' * indent + '  Fiducial Names:      \n'
        for f in self.fiducial_names:
            s += ' ' * indent + '    %s\n' % f

        s += ' ' * indent + '  Fiducials:         ' + megdata_array_print(self.fiducial_pos) + '\n'
        s += ' ' * indent + '>\n'
        return s

    def __str__(self):
        return self.str_indent()