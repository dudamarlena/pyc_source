# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/media_types/stl/model_loader.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 4311 bytes
import struct

class ThreeDeeParseError(Exception):
    pass


class ThreeDee(object):
    __doc__ = '\n    3D model parser base class.  Derrived classes are used for basic\n    analysis of 3D models, and are not intended to be used for 3D\n    rendering.\n    '

    def __init__(self, fileob):
        self.verts = []
        self.average = [
         0, 0, 0]
        self.min = [None, None, None]
        self.max = [None, None, None]
        self.width = 0
        self.depth = 0
        self.height = 0
        self.load(fileob)
        if not len(self.verts):
            raise ThreeDeeParseError('Empty model.')
        for vector in self.verts:
            for i in range(3):
                num = vector[i]
                self.average[i] += num
                if not self.min[i]:
                    self.min[i] = num
                    self.max[i] = num
                else:
                    if self.min[i] > num:
                        self.min[i] = num
                    if self.max[i] < num:
                        self.max[i] = num
                        continue

        for i in range(3):
            self.average[i] /= len(self.verts)

        self.width = abs(self.min[0] - self.max[0])
        self.depth = abs(self.min[1] - self.max[1])
        self.height = abs(self.min[2] - self.max[2])

    def load(self, fileob):
        """Override this method in your subclass."""
        pass


class ObjModel(ThreeDee):
    __doc__ = '\n    Parser for textureless wavefront obj files.  File format\n    reference: http://en.wikipedia.org/wiki/Wavefront_.obj_file\n    '

    def __vector(self, line, expected=3):
        nums = map(float, line.strip().split(' ')[1:])
        return tuple(nums[:expected])

    def load(self, fileob):
        for line in fileob:
            line = line.strip()
            if line[0] == 'v':
                self.verts.append(self._ObjModel__vector(line))
                continue


class BinaryStlModel(ThreeDee):
    __doc__ = '\n    Parser for ascii-encoded stl files.  File format reference:\n    http://en.wikipedia.org/wiki/STL_%28file_format%29#Binary_STL\n    '

    def load(self, fileob):
        fileob.seek(80)
        count = struct.unpack('<I', fileob.read(4))[0]
        for i in range(count):
            fileob.read(12)
            for v in range(3):
                self.verts.append(struct.unpack('<3f', fileob.read(12)))

            fileob.read(2)


def auto_detect(fileob, hint):
    """
    Attempt to divine which parser to use to divine information about
    the model / verify the file."""
    if hint == 'obj' or not hint:
        try:
            return ObjModel(fileob)
        except ThreeDeeParseError:
            pass

    if hint == 'stl' or not hint:
        try:
            return ObjModel(fileob)
        except ThreeDeeParseError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass

        try:
            return BinaryStlModel(fileob)
        except ThreeDeeParseError:
            pass
        except MemoryError:
            pass

    raise ThreeDeeParseError('Could not successfully parse the model :(')