# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/OleFileIO.py
# Compiled at: 2007-09-25 20:00:35
import string, StringIO

def i16(c, o=0):
    return ord(c[o]) + (ord(c[(o + 1)]) << 8)


def i32(c, o=0):
    return ord(c[o]) + (ord(c[(o + 1)]) << 8) + (ord(c[(o + 2)]) << 16) + (ord(c[(o + 3)]) << 24)


MAGIC = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
VT_EMPTY = 0
VT_NULL = 1
VT_I2 = 2
VT_I4 = 3
VT_R4 = 4
VT_R8 = 5
VT_CY = 6
VT_DATE = 7
VT_BSTR = 8
VT_DISPATCH = 9
VT_ERROR = 10
VT_BOOL = 11
VT_VARIANT = 12
VT_UNKNOWN = 13
VT_DECIMAL = 14
VT_I1 = 16
VT_UI1 = 17
VT_UI2 = 18
VT_UI4 = 19
VT_I8 = 20
VT_UI8 = 21
VT_INT = 22
VT_UINT = 23
VT_VOID = 24
VT_HRESULT = 25
VT_PTR = 26
VT_SAFEARRAY = 27
VT_CARRAY = 28
VT_USERDEFINED = 29
VT_LPSTR = 30
VT_LPWSTR = 31
VT_FILETIME = 64
VT_BLOB = 65
VT_STREAM = 66
VT_STORAGE = 67
VT_STREAMED_OBJECT = 68
VT_STORED_OBJECT = 69
VT_BLOB_OBJECT = 70
VT_CF = 71
VT_CLSID = 72
VT_VECTOR = 4096
VT = {}
for (k, v) in vars().items():
    if k[:3] == 'VT_':
        VT[v] = k

WORD_CLSID = '00020900-0000-0000-C000-000000000046'

class _OleStream(StringIO.StringIO):
    """OLE2 Stream

    Returns a read-only file object which can be used to read
    the contents of a OLE stream.  To open a stream, use the
    openstream method in the OleFile class.

    This function can be used with either ordinary streams,
    or ministreams, depending on the offset, sectorsize, and
    fat table arguments.
    """

    def __init__(self, fp, sect, size, offset, sectorsize, fat):
        data = []
        while sect != -2:
            fp.seek(offset + sectorsize * sect)
            data.append(fp.read(sectorsize))
            sect = fat[sect]

        data = string.join(data, '')
        StringIO.StringIO.__init__(self, data[:size])


class _OleDirectoryEntry():
    """OLE2 Directory Entry

    Encapsulates a stream directory entry.  Note that the
    constructor builds a tree of all subentries, so we only
    have to call it with the root object.
    """

    def __init__(self, sidlist, sid):
        (name, type, sect, size, sids, clsid) = sidlist[sid]
        self.sid = sid
        self.name = name
        self.type = type
        self.sect = sect
        self.size = size
        self.clsid = clsid
        self.kids = []
        sid = sidlist[sid][4][2]
        if sid != -1:
            stack = [
             self.sid]
            (left, right, child) = sidlist[sid][4]
            while left != -1:
                stack.append(sid)
                sid = left
                (left, right, child) = sidlist[sid][4]

            while sid != self.sid:
                self.kids.append(_OleDirectoryEntry(sidlist, sid))
                (left, right, child) = sidlist[sid][4]
                if right != -1:
                    sid = right
                    while 1:
                        (left, right, child) = sidlist[sid][4]
                        if left == -1:
                            break
                        stack.append(sid)
                        sid = left

                else:
                    while 1:
                        ptr = stack[(-1)]
                        del stack[-1]
                        (left, right, child) = sidlist[ptr][4]
                        if right != sid:
                            break
                        sid = right

                    (left, right, child) = sidlist[sid][4]
                    if right != ptr:
                        sid = ptr

            self.kids.sort()

    def __cmp__(self, other):
        """Compare entries by name"""
        return cmp(self.name, other.name)

    def dump(self, tab=0):
        """Dump this entry, and all its subentries (for debug purposes only)"""
        TYPES = [
         '(invalid)', '(storage)', '(stream)', '(lockbytes)',
         '(property)', '(root)']
        print ' ' * tab + repr(self.name), TYPES[self.type],
        if self.type in (2, 5):
            print self.size, 'bytes',
        print
        if self.type in (1, 5) and self.clsid:
            print ' ' * tab + '{%s}' % self.clsid
        for kid in self.kids:
            kid.dump(tab + 2)


class OleFileIO():
    """OLE container object

    This class encapsulates the interface to an OLE 2 structured
    storage file.  Use the listdir and openstream methods to access
    the contents of this file.

    Object names are given as a list of strings, one for each subentry
    level.  The root entry should be omitted.  For example, the following
    code extracts all image streams from a Microsoft Image Composer file:

        ole = OleFileIO("fan.mic")

        for entry in ole.listdir():
            if entry[1:2] == "Image":
                fin = ole.openstream(entry)
                fout = open(entry[0:1], "wb")
                while 1:
                    s = fin.read(8192)
                    if not s:
                        break
                    fout.write(s)

    You can use the viewer application provided with the Python Imaging
    Library to view the resulting files (which happens to be standard
    TIFF files).
    """

    def __init__(self, filename=None):
        if filename:
            self.open(filename)

    def open(self, filename):
        """Open an OLE2 file"""
        if type(filename) == type(''):
            self.fp = open(filename, 'rb')
        else:
            self.fp = filename
        header = self.fp.read(512)
        if len(header) != 512 or header[:8] != MAGIC:
            raise IOError, 'not an OLE2 structured storage file'
        clsid = self._clsid(header[8:24])
        self.sectorsize = 1 << i16(header, 30)
        self.minisectorsize = 1 << i16(header, 32)
        self.minisectorcutoff = i32(header, 56)
        self.loadfat(header)
        self.loaddirectory(i32(header, 48))
        self.ministream = None
        self.minifatsect = i32(header, 60)
        return

    def loadfat(self, header):
        sect = header[76:512]
        fat = []
        for i in range(0, len(sect), 4):
            ix = i32(sect, i)
            if ix == -2 or ix == -1:
                break
            s = self.getsect(ix)
            fat = fat + map(lambda i, s=s: i32(s, i), range(0, len(s), 4))

        self.fat = fat

    def loadminifat(self):
        s = self._open(self.minifatsect).read()
        self.minifat = map(lambda i, s=s: i32(s, i), range(0, len(s), 4))

    def getsect(self, sect):
        self.fp.seek(512 + self.sectorsize * sect)
        return self.fp.read(self.sectorsize)

    def _unicode(self, s):
        return filter(ord, s)

    def loaddirectory(self, sect):
        fp = self._open(sect)
        self.sidlist = []
        while 1:
            entry = fp.read(128)
            if not entry:
                break
            type = ord(entry[66])
            name = self._unicode(entry[0:0 + i16(entry, 64)])
            ptrs = (i32(entry, 68), i32(entry, 72), i32(entry, 76))
            sect, size = i32(entry, 116), i32(entry, 120)
            clsid = self._clsid(entry[80:96])
            self.sidlist.append((name, type, sect, size, ptrs, clsid))

        self.root = _OleDirectoryEntry(self.sidlist, 0)

    def dumpdirectory(self):
        self.root.dump()

    def _clsid(self, clsid):
        if clsid == '\x00' * len(clsid):
            return ''
        return ('%08X-%04X-%04X-%02X%02X-' + '%02X' * 6) % ((
         i32(clsid, 0), i16(clsid, 4), i16(clsid, 6)) + tuple(map(ord, clsid[8:16])))

    def _list(self, files, prefix, node):
        prefix = prefix + [node.name]
        for entry in node.kids:
            if entry.kids:
                self._list(files, prefix, entry)
            else:
                files.append(prefix[1:] + [entry.name])

    def _find(self, filename):
        node = self.root
        for name in filename:
            for kid in node.kids:
                if kid.name == name:
                    break
            else:
                raise IOError, 'file not found'

            node = kid

        return node.sid

    def _open(self, start, size=2147483647):
        if size < self.minisectorcutoff:
            if not self.ministream:
                self.loadminifat()
                self.ministream = self._open(self.sidlist[0][2])
            return _OleStream(self.ministream, start, size, 0, self.minisectorsize, self.minifat)
        return _OleStream(self.fp, start, size, 512, self.sectorsize, self.fat)

    def listdir(self):
        """Return a list of streams stored in this file"""
        files = []
        self._list(files, [], self.root)
        return files

    def openstream(self, filename):
        """Open a stream as a read-only file object"""
        slot = self._find(filename)
        (name, type, sect, size, sids, clsid) = self.sidlist[slot]
        if type != 2:
            raise IOError, 'this file is not a stream'
        return self._open(sect, size)

    def getproperties(self, filename):
        """Return properties described in substream"""
        fp = self.openstream(filename)
        data = {}
        s = fp.read(28)
        clsid = self._clsid(s[8:24])
        s = fp.read(20)
        fmtid = self._clsid(s[:16])
        fp.seek(i32(s, 16))
        s = '****' + fp.read(i32(fp.read(4)) - 4)
        for i in range(i32(s, 4)):
            id = i32(s, 8 + i * 8)
            offset = i32(s, 12 + i * 8)
            type = i32(s, offset)
            if type == VT_I2:
                value = i16(s, offset + 4)
                if value >= 32768:
                    value = value - 65536
            elif type == VT_UI2:
                value = i16(s, offset + 4)
            elif type in (VT_I4, VT_ERROR):
                value = i32(s, offset + 4)
            elif type == VT_UI4:
                value = i32(s, offset + 4)
            elif type in (VT_BSTR, VT_LPSTR):
                count = i32(s, offset + 4)
                value = s[offset + 8:offset + 8 + count - 1]
            elif type == VT_BLOB:
                count = i32(s, offset + 4)
                value = s[offset + 8:offset + 8 + count]
            elif type == VT_LPWSTR:
                count = i32(s, offset + 4)
                value = self._unicode(s[offset + 8:offset + 8 + count * 2])
            elif type == VT_FILETIME:
                value = long(i32(s, offset + 4)) + (long(i32(s, offset + 8)) << 32)
                value = value / 10000000
            elif type == VT_UI1:
                value = ord(s[(offset + 4)])
            elif type == VT_CLSID:
                value = self._clsid(s[offset + 4:offset + 20])
            elif type == VT_CF:
                count = i32(s, offset + 4)
                value = s[offset + 8:offset + 8 + count]
            else:
                value = None
            data[id] = value

        return data


if __name__ == '__main__':
    import sys
    for file in sys.argv[1:]:
        try:
            ole = OleFileIO(file)
            print '-' * 68
            print file
            print '-' * 68
            ole.dumpdirectory()
            for file in ole.listdir():
                if file[(-1)][0] == '\x05':
                    print file
                    props = ole.getproperties(file)
                    props = props.items()
                    props.sort()
                    for (k, v) in props:
                        print '   ', k, v

        except IOError, v:
            print '***', 'cannot read', file, '-', v