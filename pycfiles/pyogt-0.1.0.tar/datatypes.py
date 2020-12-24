# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/datatypes.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from logging import getLogger
import uuid, struct, math
from pyogp.lib.base.exc import DataParsingError
logger = getLogger('pyogp.lib.base.datatypes')

class Vector3(object):
    """ represents a vector as a tuple"""
    __module__ = __name__

    def __init__(self, bytes=None, offset=0, X=0.0, Y=0.0, Z=0.0):
        if bytes != None:
            self.unpack_from_bytes(bytes, offset)
        else:
            if type(X) != float:
                self.X = float(X)
            else:
                self.X = X
            if type(Y) != float:
                self.Y = float(Y)
            else:
                self.Y = Y
            if type(Z) != float:
                self.Z = float(Z)
            else:
                self.Z = Z
        return

    def unpack_from_bytes(self, bytes, offset):
        """ unpack floats from binary """
        self.X = struct.unpack('<f', bytes[offset:offset + 4])[0]
        self.Y = struct.unpack('<f', bytes[offset + 4:offset + 8])[0]
        self.Z = struct.unpack('<f', bytes[offset + 8:offset + 12])[0]

    def get_bytes(self):
        """ get bytes """
        return struct.pack('<3f', self.X, self.Y, self.Z)

    def data(self):
        return (
         self.X, self.Y, self.Z)

    def copy(self):
        return Vector3(X=self.X, Y=self.Y, Z=self.Z)

    def __repr__(self):
        """ represent a vector as a string """
        return '<%s, %s, %s>' % (self.X, self.Y, self.Z)

    def __call__(self):
        """ represent a vector as a tuple """
        return (
         self.X, self.Y, self.Z)

    def dist_squared(a, b):
        x = a.X - b.X
        y = a.Y - b.Y
        z = a.Z - b.Z
        return x * x + y * y + z * z

    dist_squared = staticmethod(dist_squared)

    @staticmethod
    def parse(s):
        """Parse a string of the form '<x, y, z>' or 'x, y, z' and return a Vector3.
        Will raise a ValueError
        """
        s = s.replace('<', '').replace('>', '')
        dims = s.split(',')
        if len(dims) != 3:
            raise ValueError('Expected 3 values in string')
        (x, y, z) = [ float(d.strip()) for d in dims ]
        return Vector3(X=x, Y=y, Z=z)


class Quaternion(object):
    """ represents a quaternion as a tuple"""
    __module__ = __name__

    def __init__(self, bytes=None, offset=0, length=4, X=0.0, Y=0.0, Z=0.0, W=0.0):
        if bytes != None:
            self.unpack_from_bytes(bytes, offset, length)
        else:
            if type(X) != float:
                self.X = float(X)
            else:
                self.X = X
            if type(Y) != float:
                self.Y = float(Y)
            else:
                self.Y = Y
            if type(Z) != float:
                self.Z = float(Z)
            else:
                self.Z = Z
            if type(W) != float:
                self.W = float(W)
            else:
                self.W = W
        return

    def unpack_from_bytes(self, bytes, offset, length=4):
        """ unpack floats from binary """
        self.X = struct.unpack('<f', bytes[offset:offset + 4])[0]
        self.Y = struct.unpack('<f', bytes[offset + 4:offset + 8])[0]
        self.Z = struct.unpack('<f', bytes[offset + 8:offset + 12])[0]
        try:
            self.W = struct.unpack('<f', bytes[offset + 12:offset + 16])[0]
        except:
            t = 1.0 - (self.X * self.X + self.Y * self.Y + self.Z * self.Z)
            if t > 0:
                self.W = math.sqrt(t)
            else:
                self.W = 0

    def get_bytes(self):
        """ get bytes """
        return struct.pack('<4f', self.X, self.Y, self.Z, self.W)

    def data(self):
        return (
         self.X, self.Y, self.Z, self.W)

    def copy(self):
        return Quaternion(X=self.X, Y=self.Y, Z=self.Z, W=self.W)

    def __repr__(self):
        """ represent a quaternion as a string """
        return str((self.X, self.Y, self.Z, self.W))

    def __call__(self):
        """ represent a quaternion as a tuple """
        return (
         self.X, self.Y, self.Z, self.W)


class UUID(object):
    """ represents a uuid as, well, a uuid 

    inbound LLUUID data from packets is already UUID(), they are 
    already the same 'datatype'
    """
    __module__ = __name__

    def __init__(self, string='00000000-0000-0000-0000-000000000000', bytes=None, offset=0):
        if bytes != None:
            self.unpack_from_bytes(bytes, offset)
        else:
            self.uuid = uuid.UUID(string)
        return

    def random(self):
        if str(self.uuid) == '00000000-0000-0000-0000-000000000000':
            self.uuid = uuid.uuid4()
            return self.uuid
        else:
            logger.warning('Attempted to overwrite a stored uuid %s with a random, that is a bad idea...' % str(self.uuid))

    def unpack_from_bytes(self, bytes, offset):
        """ unpack uuid from binary """
        self.uuid = uuid.UUID(bytes=bytes[offset:offset + 16])

    def get_bytes(self):
        """ get bytes """
        return str(self.uuid.bytes)

    def data(self):
        """ represent a uuid as, well, a uuid """
        return self.uuid

    def copy(self):
        return UUID(string=str(self.uuid))

    def __repr__(self):
        """ represent a uuid as a string """
        return str(self.uuid)

    def __call__(self):
        """ represent a uuid as, well, a uuid """
        return self.uuid

    def __eq__(self, other):
        if hasattr(other, 'uuid'):
            return self.uuid == other.uuid
        else:
            return False

    def __xor__(self, arg):
        """ the xor of two UUIDs """
        temp = self.uuid.int ^ arg.uuid.int
        result = uuid.UUID(int=temp)
        return UUID(result.__str__())