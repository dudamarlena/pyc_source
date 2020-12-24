# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/smriprep/wrapper/build/lib/python3.7/tarfile.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 92617 bytes
"""Read from and write to tar format archives.
"""
version = '0.9.0'
__author__ = 'Lars Gustäbel (lars@gustaebel.de)'
__credits__ = 'Gustavo Niemeyer, Niels Gustäbel, Richard Townsend.'
from builtins import open as bltn_open
import sys, os, io, shutil, stat, time, struct, copy, re
try:
    import pwd
except ImportError:
    pwd = None

try:
    import grp
except ImportError:
    grp = None

symlink_exception = (
 AttributeError, NotImplementedError)
try:
    symlink_exception += (OSError,)
except NameError:
    pass

__all__ = [
 'TarFile', 'TarInfo', 'is_tarfile', 'TarError', 'ReadError',
 'CompressionError', 'StreamError', 'ExtractError', 'HeaderError',
 'ENCODING', 'USTAR_FORMAT', 'GNU_FORMAT', 'PAX_FORMAT',
 'DEFAULT_FORMAT', 'open']
NUL = b'\x00'
BLOCKSIZE = 512
RECORDSIZE = BLOCKSIZE * 20
GNU_MAGIC = b'ustar  \x00'
POSIX_MAGIC = b'ustar\x0000'
LENGTH_NAME = 100
LENGTH_LINK = 100
LENGTH_PREFIX = 155
REGTYPE = b'0'
AREGTYPE = b'\x00'
LNKTYPE = b'1'
SYMTYPE = b'2'
CHRTYPE = b'3'
BLKTYPE = b'4'
DIRTYPE = b'5'
FIFOTYPE = b'6'
CONTTYPE = b'7'
GNUTYPE_LONGNAME = b'L'
GNUTYPE_LONGLINK = b'K'
GNUTYPE_SPARSE = b'S'
XHDTYPE = b'x'
XGLTYPE = b'g'
SOLARIS_XHDTYPE = b'X'
USTAR_FORMAT = 0
GNU_FORMAT = 1
PAX_FORMAT = 2
DEFAULT_FORMAT = GNU_FORMAT
SUPPORTED_TYPES = (
 REGTYPE, AREGTYPE, LNKTYPE,
 SYMTYPE, DIRTYPE, FIFOTYPE,
 CONTTYPE, CHRTYPE, BLKTYPE,
 GNUTYPE_LONGNAME, GNUTYPE_LONGLINK,
 GNUTYPE_SPARSE)
REGULAR_TYPES = (
 REGTYPE, AREGTYPE,
 CONTTYPE, GNUTYPE_SPARSE)
GNU_TYPES = (
 GNUTYPE_LONGNAME, GNUTYPE_LONGLINK,
 GNUTYPE_SPARSE)
PAX_FIELDS = ('path', 'linkpath', 'size', 'mtime', 'uid', 'gid', 'uname', 'gname')
PAX_NAME_FIELDS = {
 'path', 'linkpath', 'uname', 'gname'}
PAX_NUMBER_FIELDS = {'atime':float, 
 'ctime':float, 
 'mtime':float, 
 'uid':int, 
 'gid':int, 
 'size':int}
if os.name == 'nt':
    ENCODING = 'utf-8'
else:
    ENCODING = sys.getfilesystemencoding()

def stn(s, length, encoding, errors):
    """Convert a string to a null-terminated bytes object.
    """
    s = s.encode(encoding, errors)
    return s[:length] + (length - len(s)) * NUL


def nts(s, encoding, errors):
    """Convert a null-terminated bytes object to a string.
    """
    p = s.find(b'\x00')
    if p != -1:
        s = s[:p]
    return s.decode(encoding, errors)


def nti(s):
    """Convert a number field to a python number.
    """
    if s[0] in (128, 255):
        n = 0
        for i in range(len(s) - 1):
            n <<= 8
            n += s[(i + 1)]

        if s[0] == 255:
            n = -(256 ** (len(s) - 1) - n)
    else:
        try:
            s = nts(s, 'ascii', 'strict')
            n = int(s.strip() or '0', 8)
        except ValueError:
            raise InvalidHeaderError('invalid header')

    return n


def itn(n, digits=8, format=DEFAULT_FORMAT):
    """Convert a python number to a number field.
    """
    n = int(n)
    if 0 <= n < 8 ** (digits - 1):
        s = bytes('%0*o' % (digits - 1, n), 'ascii') + NUL
    else:
        if format == GNU_FORMAT:
            if -256 ** (digits - 1) <= n < 256 ** (digits - 1):
                if n >= 0:
                    s = bytearray([128])
            else:
                s = bytearray([255])
                n = 256 ** digits + n
            for i in range(digits - 1):
                s.insert(1, n & 255)
                n >>= 8

        else:
            raise ValueError('overflow in number field')
    return s


def calc_chksums(buf):
    """Calculate the checksum for a member's header by summing up all
       characters except for the chksum field which is treated as if
       it was filled with spaces. According to the GNU tar sources,
       some tars (Sun and NeXT) calculate chksum with signed char,
       which will be different if there are chars in the buffer with
       the high bit set. So we calculate two checksums, unsigned and
       signed.
    """
    unsigned_chksum = 256 + sum(struct.unpack_from('148B8x356B', buf))
    signed_chksum = 256 + sum(struct.unpack_from('148b8x356b', buf))
    return (unsigned_chksum, signed_chksum)


def copyfileobj(src, dst, length=None, exception=OSError, bufsize=None):
    """Copy length bytes from fileobj src to fileobj dst.
       If length is None, copy the entire content.
    """
    bufsize = bufsize or 16384
    if length == 0:
        return
    if length is None:
        shutil.copyfileobj(src, dst, bufsize)
        return
    blocks, remainder = divmod(length, bufsize)
    for b in range(blocks):
        buf = src.read(bufsize)
        if len(buf) < bufsize:
            raise exception('unexpected end of data')
        dst.write(buf)

    if remainder != 0:
        buf = src.read(remainder)
        if len(buf) < remainder:
            raise exception('unexpected end of data')
        dst.write(buf)


def filemode(mode):
    """Deprecated in this location; use stat.filemode."""
    import warnings
    warnings.warn('deprecated in favor of stat.filemode', DeprecationWarning, 2)
    return stat.filemode(mode)


def _safe_print(s):
    encoding = getattr(sys.stdout, 'encoding', None)
    if encoding is not None:
        s = s.encode(encoding, 'backslashreplace').decode(encoding)
    print(s, end=' ')


class TarError(Exception):
    __doc__ = 'Base exception.'


class ExtractError(TarError):
    __doc__ = 'General exception for extract errors.'


class ReadError(TarError):
    __doc__ = 'Exception for unreadable tar archives.'


class CompressionError(TarError):
    __doc__ = 'Exception for unavailable compression methods.'


class StreamError(TarError):
    __doc__ = 'Exception for unsupported operations on stream-like TarFiles.'


class HeaderError(TarError):
    __doc__ = 'Base exception for header errors.'


class EmptyHeaderError(HeaderError):
    __doc__ = 'Exception for empty headers.'


class TruncatedHeaderError(HeaderError):
    __doc__ = 'Exception for truncated headers.'


class EOFHeaderError(HeaderError):
    __doc__ = 'Exception for end of file headers.'


class InvalidHeaderError(HeaderError):
    __doc__ = 'Exception for invalid headers.'


class SubsequentHeaderError(HeaderError):
    __doc__ = 'Exception for missing and invalid extended headers.'


class _LowLevelFile:
    __doc__ = 'Low-level file object. Supports reading and writing.\n       It is used instead of a regular file object for streaming\n       access.\n    '

    def __init__(self, name, mode):
        mode = {'r':os.O_RDONLY, 
         'w':os.O_WRONLY | os.O_CREAT | os.O_TRUNC}[mode]
        if hasattr(os, 'O_BINARY'):
            mode |= os.O_BINARY
        self.fd = os.open(name, mode, 438)

    def close(self):
        os.close(self.fd)

    def read(self, size):
        return os.read(self.fd, size)

    def write(self, s):
        os.write(self.fd, s)


class _Stream:
    __doc__ = 'Class that serves as an adapter between TarFile and\n       a stream-like object.  The stream-like object only\n       needs to have a read() or write() method and is accessed\n       blockwise.  Use of gzip or bzip2 compression is possible.\n       A stream-like object could be for example: sys.stdin,\n       sys.stdout, a socket, a tape device etc.\n\n       _Stream is intended to be used only internally.\n    '

    def __init__(self, name, mode, comptype, fileobj, bufsize):
        """Construct a _Stream object.
        """
        self._extfileobj = True
        if fileobj is None:
            fileobj = _LowLevelFile(name, mode)
            self._extfileobj = False
        if comptype == '*':
            fileobj = _StreamProxy(fileobj)
            comptype = fileobj.getcomptype()
        self.name = name or ''
        self.mode = mode
        self.comptype = comptype
        self.fileobj = fileobj
        self.bufsize = bufsize
        self.buf = b''
        self.pos = 0
        self.closed = False
        try:
            if comptype == 'gz':
                try:
                    import zlib
                except ImportError:
                    raise CompressionError('zlib module is not available')

                self.zlib = zlib
                self.crc = zlib.crc32(b'')
                if mode == 'r':
                    self._init_read_gz()
                    self.exception = zlib.error
                else:
                    self._init_write_gz()
            else:
                if comptype == 'bz2':
                    try:
                        import bz2
                    except ImportError:
                        raise CompressionError('bz2 module is not available')

                    if mode == 'r':
                        self.dbuf = b''
                        self.cmp = bz2.BZ2Decompressor()
                        self.exception = OSError
                    else:
                        self.cmp = bz2.BZ2Compressor()
                else:
                    if comptype == 'xz':
                        try:
                            import lzma
                        except ImportError:
                            raise CompressionError('lzma module is not available')

                        if mode == 'r':
                            self.dbuf = b''
                            self.cmp = lzma.LZMADecompressor()
                            self.exception = lzma.LZMAError
                        else:
                            self.cmp = lzma.LZMACompressor()
                    else:
                        if comptype != 'tar':
                            raise CompressionError('unknown compression type %r' % comptype)
        except:
            if not self._extfileobj:
                self.fileobj.close()
            self.closed = True
            raise

    def __del__(self):
        if hasattr(self, 'closed'):
            if not self.closed:
                self.close()

    def _init_write_gz(self):
        """Initialize for writing with gzip compression.
        """
        self.cmp = self.zlib.compressobj(9, self.zlib.DEFLATED, -self.zlib.MAX_WBITS, self.zlib.DEF_MEM_LEVEL, 0)
        timestamp = struct.pack('<L', int(time.time()))
        self._Stream__write(b'\x1f\x8b\x08\x08' + timestamp + b'\x02\xff')
        if self.name.endswith('.gz'):
            self.name = self.name[:-3]
        self._Stream__write(self.name.encode('iso-8859-1', 'replace') + NUL)

    def write(self, s):
        """Write string s to the stream.
        """
        if self.comptype == 'gz':
            self.crc = self.zlib.crc32(s, self.crc)
        self.pos += len(s)
        if self.comptype != 'tar':
            s = self.cmp.compress(s)
        self._Stream__write(s)

    def __write(self, s):
        """Write string s to the stream if a whole new block
           is ready to be written.
        """
        self.buf += s
        while len(self.buf) > self.bufsize:
            self.fileobj.write(self.buf[:self.bufsize])
            self.buf = self.buf[self.bufsize:]

    def close(self):
        """Close the _Stream object. No operation should be
           done on it afterwards.
        """
        if self.closed:
            return
        self.closed = True
        try:
            if self.mode == 'w':
                if self.comptype != 'tar':
                    self.buf += self.cmp.flush()
            if self.mode == 'w':
                if self.buf:
                    self.fileobj.write(self.buf)
                    self.buf = b''
                    if self.comptype == 'gz':
                        self.fileobj.write(struct.pack('<L', self.crc))
                        self.fileobj.write(struct.pack('<L', self.pos & 4294967295))
        finally:
            if not self._extfileobj:
                self.fileobj.close()

    def _init_read_gz(self):
        """Initialize for reading a gzip compressed fileobj.
        """
        self.cmp = self.zlib.decompressobj(-self.zlib.MAX_WBITS)
        self.dbuf = b''
        if self._Stream__read(2) != b'\x1f\x8b':
            raise ReadError('not a gzip file')
        if self._Stream__read(1) != b'\x08':
            raise CompressionError('unsupported compression method')
        flag = ord(self._Stream__read(1))
        self._Stream__read(6)
        if flag & 4:
            xlen = ord(self._Stream__read(1)) + 256 * ord(self._Stream__read(1))
            self.read(xlen)
        if flag & 8:
            while 1:
                s = self._Stream__read(1)
                if not s or s == NUL:
                    break

        if flag & 16:
            while 1:
                s = self._Stream__read(1)
                if not s or s == NUL:
                    break

        if flag & 2:
            self._Stream__read(2)

    def tell(self):
        """Return the stream's file pointer position.
        """
        return self.pos

    def seek(self, pos=0):
        """Set the stream's file pointer to pos. Negative seeking
           is forbidden.
        """
        if pos - self.pos >= 0:
            blocks, remainder = divmod(pos - self.pos, self.bufsize)
            for i in range(blocks):
                self.read(self.bufsize)

            self.read(remainder)
        else:
            raise StreamError('seeking backwards is not allowed')
        return self.pos

    def read(self, size=None):
        """Return the next size number of bytes from the stream.
           If size is not defined, return all bytes of the stream
           up to EOF.
        """
        if size is None:
            t = []
            while True:
                buf = self._read(self.bufsize)
                if not buf:
                    break
                t.append(buf)

            buf = (b'').join(t)
        else:
            buf = self._read(size)
        self.pos += len(buf)
        return buf

    def _read(self, size):
        """Return size bytes from the stream.
        """
        if self.comptype == 'tar':
            return self._Stream__read(size)
        c = len(self.dbuf)
        t = [self.dbuf]
        while c < size:
            buf = self._Stream__read(self.bufsize)
            if not buf:
                break
            try:
                buf = self.cmp.decompress(buf)
            except self.exception:
                raise ReadError('invalid compressed data')

            t.append(buf)
            c += len(buf)

        t = (b'').join(t)
        self.dbuf = t[size:]
        return t[:size]

    def __read(self, size):
        """Return size bytes from stream. If internal buffer is empty,
           read another block from the stream.
        """
        c = len(self.buf)
        t = [self.buf]
        while c < size:
            buf = self.fileobj.read(self.bufsize)
            if not buf:
                break
            t.append(buf)
            c += len(buf)

        t = (b'').join(t)
        self.buf = t[size:]
        return t[:size]


class _StreamProxy(object):
    __doc__ = "Small proxy class that enables transparent compression\n       detection for the Stream interface (mode 'r|*').\n    "

    def __init__(self, fileobj):
        self.fileobj = fileobj
        self.buf = self.fileobj.read(BLOCKSIZE)

    def read(self, size):
        self.read = self.fileobj.read
        return self.buf

    def getcomptype(self):
        if self.buf.startswith(b'\x1f\x8b\x08'):
            return 'gz'
        if self.buf[0:3] == b'BZh':
            if self.buf[4:10] == b'1AY&SY':
                return 'bz2'
        if self.buf.startswith((b']\x00\x00\x80', b'\xfd7zXZ')):
            return 'xz'
        return 'tar'

    def close(self):
        self.fileobj.close()


class _FileInFile(object):
    __doc__ = 'A thin wrapper around an existing file object that\n       provides a part of its data as an individual file\n       object.\n    '

    def __init__(self, fileobj, offset, size, blockinfo=None):
        self.fileobj = fileobj
        self.offset = offset
        self.size = size
        self.position = 0
        self.name = getattr(fileobj, 'name', None)
        self.closed = False
        if blockinfo is None:
            blockinfo = [
             (
              0, size)]
        self.map_index = 0
        self.map = []
        lastpos = 0
        realpos = self.offset
        for offset, size in blockinfo:
            if offset > lastpos:
                self.map.append((False, lastpos, offset, None))
            self.map.append((True, offset, offset + size, realpos))
            realpos += size
            lastpos = offset + size

        if lastpos < self.size:
            self.map.append((False, lastpos, self.size, None))

    def flush(self):
        pass

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return self.fileobj.seekable()

    def tell(self):
        """Return the current file position.
        """
        return self.position

    def seek(self, position, whence=io.SEEK_SET):
        """Seek to a position in the file.
        """
        if whence == io.SEEK_SET:
            self.position = min(max(position, 0), self.size)
        else:
            if whence == io.SEEK_CUR:
                if position < 0:
                    self.position = max(self.position + position, 0)
                else:
                    self.position = min(self.position + position, self.size)
            elif whence == io.SEEK_END:
                self.position = max(min(self.size + position, self.size), 0)
            else:
                raise ValueError('Invalid argument')
        return self.position

    def read(self, size=None):
        """Read data from the file.
        """
        if size is None:
            size = self.size - self.position
        else:
            size = min(size, self.size - self.position)
        buf = b''
        while size > 0:
            while 1:
                data, start, stop, offset = self.map[self.map_index]
                if start <= self.position < stop:
                    break
                else:
                    self.map_index += 1
                    if self.map_index == len(self.map):
                        self.map_index = 0

            length = min(size, stop - self.position)
            if data:
                self.fileobj.seek(offset + (self.position - start))
                b = self.fileobj.read(length)
                if len(b) != length:
                    raise ReadError('unexpected end of data')
                buf += b
            else:
                buf += NUL * length
            size -= length
            self.position += length

        return buf

    def readinto(self, b):
        buf = self.read(len(b))
        b[:len(buf)] = buf
        return len(buf)

    def close(self):
        self.closed = True


class ExFileObject(io.BufferedReader):

    def __init__(self, tarfile, tarinfo):
        fileobj = _FileInFile(tarfile.fileobj, tarinfo.offset_data, tarinfo.size, tarinfo.sparse)
        super().__init__(fileobj)


class TarInfo(object):
    __doc__ = 'Informational class which holds the details about an\n       archive member given by a tar header block.\n       TarInfo objects are returned by TarFile.getmember(),\n       TarFile.getmembers() and TarFile.gettarinfo() and are\n       usually created internally.\n    '
    __slots__ = ('name', 'mode', 'uid', 'gid', 'size', 'mtime', 'chksum', 'type', 'linkname',
                 'uname', 'gname', 'devmajor', 'devminor', 'offset', 'offset_data',
                 'pax_headers', 'sparse', 'tarfile', '_sparse_structs', '_link_target')

    def __init__(self, name=''):
        """Construct a TarInfo object. name is the optional name
           of the member.
        """
        self.name = name
        self.mode = 420
        self.uid = 0
        self.gid = 0
        self.size = 0
        self.mtime = 0
        self.chksum = 0
        self.type = REGTYPE
        self.linkname = ''
        self.uname = ''
        self.gname = ''
        self.devmajor = 0
        self.devminor = 0
        self.offset = 0
        self.offset_data = 0
        self.sparse = None
        self.pax_headers = {}

    @property
    def path(self):
        return self.name

    @path.setter
    def path(self, name):
        self.name = name

    @property
    def linkpath(self):
        return self.linkname

    @linkpath.setter
    def linkpath(self, linkname):
        self.linkname = linkname

    def __repr__(self):
        return '<%s %r at %#x>' % (self.__class__.__name__, self.name, id(self))

    def get_info(self):
        """Return the TarInfo's attributes as a dictionary.
        """
        info = {'name':self.name, 
         'mode':self.mode & 4095, 
         'uid':self.uid, 
         'gid':self.gid, 
         'size':self.size, 
         'mtime':self.mtime, 
         'chksum':self.chksum, 
         'type':self.type, 
         'linkname':self.linkname, 
         'uname':self.uname, 
         'gname':self.gname, 
         'devmajor':self.devmajor, 
         'devminor':self.devminor}
        if info['type'] == DIRTYPE:
            if not info['name'].endswith('/'):
                info['name'] += '/'
        return info

    def tobuf(self, format=DEFAULT_FORMAT, encoding=ENCODING, errors='surrogateescape'):
        """Return a tar header as a string of 512 byte blocks.
        """
        info = self.get_info()
        if format == USTAR_FORMAT:
            return self.create_ustar_header(info, encoding, errors)
        if format == GNU_FORMAT:
            return self.create_gnu_header(info, encoding, errors)
        if format == PAX_FORMAT:
            return self.create_pax_header(info, encoding)
        raise ValueError('invalid format')

    def create_ustar_header(self, info, encoding, errors):
        """Return the object as a ustar header block.
        """
        info['magic'] = POSIX_MAGIC
        if len(info['linkname'].encode(encoding, errors)) > LENGTH_LINK:
            raise ValueError('linkname is too long')
        if len(info['name'].encode(encoding, errors)) > LENGTH_NAME:
            info['prefix'], info['name'] = self._posix_split_name(info['name'], encoding, errors)
        return self._create_header(info, USTAR_FORMAT, encoding, errors)

    def create_gnu_header(self, info, encoding, errors):
        """Return the object as a GNU header block sequence.
        """
        info['magic'] = GNU_MAGIC
        buf = b''
        if len(info['linkname'].encode(encoding, errors)) > LENGTH_LINK:
            buf += self._create_gnu_long_header(info['linkname'], GNUTYPE_LONGLINK, encoding, errors)
        if len(info['name'].encode(encoding, errors)) > LENGTH_NAME:
            buf += self._create_gnu_long_header(info['name'], GNUTYPE_LONGNAME, encoding, errors)
        return buf + self._create_header(info, GNU_FORMAT, encoding, errors)

    def create_pax_header--- This code section failed: ---

 L. 854         0  LOAD_GLOBAL              POSIX_MAGIC
                2  LOAD_FAST                'info'
                4  LOAD_STR                 'magic'
                6  STORE_SUBSCR     

 L. 855         8  LOAD_FAST                'self'
               10  LOAD_ATTR                pax_headers
               12  LOAD_METHOD              copy
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  STORE_FAST               'pax_headers'

 L. 859        18  SETUP_LOOP          152  'to 152'

 L. 860        20  LOAD_STR                 'name'
               22  LOAD_STR                 'path'
               24  LOAD_GLOBAL              LENGTH_NAME
               26  BUILD_TUPLE_3         3 
               28  LOAD_STR                 'linkname'
               30  LOAD_STR                 'linkpath'
               32  LOAD_GLOBAL              LENGTH_LINK
               34  BUILD_TUPLE_3         3 

 L. 861        36  LOAD_CONST               ('uname', 'uname', 32)
               38  LOAD_CONST               ('gname', 'gname', 32)
               40  BUILD_TUPLE_4         4 
               42  GET_ITER         
             44_0  COME_FROM           134  '134'
               44  FOR_ITER            150  'to 150'
               46  UNPACK_SEQUENCE_3     3 
               48  STORE_FAST               'name'
               50  STORE_FAST               'hname'
               52  STORE_FAST               'length'

 L. 863        54  LOAD_FAST                'hname'
               56  LOAD_FAST                'pax_headers'
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    64  'to 64'

 L. 865        62  CONTINUE             44  'to 44'
             64_0  COME_FROM            60  '60'

 L. 868        64  SETUP_EXCEPT         86  'to 86'

 L. 869        66  LOAD_FAST                'info'
               68  LOAD_FAST                'name'
               70  BINARY_SUBSCR    
               72  LOAD_METHOD              encode
               74  LOAD_STR                 'ascii'
               76  LOAD_STR                 'strict'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  POP_TOP          
               82  POP_BLOCK        
               84  JUMP_FORWARD        120  'to 120'
             86_0  COME_FROM_EXCEPT     64  '64'

 L. 870        86  DUP_TOP          
               88  LOAD_GLOBAL              UnicodeEncodeError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   118  'to 118'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 871       100  LOAD_FAST                'info'
              102  LOAD_FAST                'name'
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'pax_headers'
              108  LOAD_FAST                'hname'
              110  STORE_SUBSCR     

 L. 872       112  CONTINUE_LOOP        44  'to 44'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            92  '92'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            84  '84'

 L. 874       120  LOAD_GLOBAL              len
              122  LOAD_FAST                'info'
              124  LOAD_FAST                'name'
              126  BINARY_SUBSCR    
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  LOAD_FAST                'length'
              132  COMPARE_OP               >
              134  POP_JUMP_IF_FALSE    44  'to 44'

 L. 875       136  LOAD_FAST                'info'
              138  LOAD_FAST                'name'
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'pax_headers'
              144  LOAD_FAST                'hname'
              146  STORE_SUBSCR     
              148  JUMP_BACK            44  'to 44'
              150  POP_BLOCK        
            152_0  COME_FROM_LOOP       18  '18'

 L. 879       152  SETUP_LOOP          258  'to 258'
              154  LOAD_CONST               (('uid', 8), ('gid', 8), ('size', 12), ('mtime', 12))
              156  GET_ITER         
            158_0  COME_FROM           232  '232'
              158  FOR_ITER            256  'to 256'
              160  UNPACK_SEQUENCE_2     2 
              162  STORE_FAST               'name'
              164  STORE_FAST               'digits'

 L. 880       166  LOAD_FAST                'name'
              168  LOAD_FAST                'pax_headers'
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   184  'to 184'

 L. 882       174  LOAD_CONST               0
              176  LOAD_FAST                'info'
              178  LOAD_FAST                'name'
              180  STORE_SUBSCR     

 L. 883       182  CONTINUE            158  'to 158'
            184_0  COME_FROM           172  '172'

 L. 885       184  LOAD_FAST                'info'
              186  LOAD_FAST                'name'
              188  BINARY_SUBSCR    
              190  STORE_FAST               'val'

 L. 886       192  LOAD_CONST               0
              194  LOAD_FAST                'val'
              196  DUP_TOP          
              198  ROT_THREE        
              200  COMPARE_OP               <=
              202  POP_JUMP_IF_FALSE   220  'to 220'
              204  LOAD_CONST               8
              206  LOAD_FAST                'digits'
              208  LOAD_CONST               1
              210  BINARY_SUBTRACT  
              212  BINARY_POWER     
              214  COMPARE_OP               <
              216  POP_JUMP_IF_FALSE   234  'to 234'
              218  JUMP_FORWARD        224  'to 224'
            220_0  COME_FROM           202  '202'
              220  POP_TOP          
              222  JUMP_FORWARD        234  'to 234'
            224_0  COME_FROM           218  '218'
              224  LOAD_GLOBAL              isinstance
              226  LOAD_FAST                'val'
              228  LOAD_GLOBAL              float
              230  CALL_FUNCTION_2       2  '2 positional arguments'
              232  POP_JUMP_IF_FALSE   158  'to 158'
            234_0  COME_FROM           222  '222'
            234_1  COME_FROM           216  '216'

 L. 887       234  LOAD_GLOBAL              str
              236  LOAD_FAST                'val'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  LOAD_FAST                'pax_headers'
              242  LOAD_FAST                'name'
              244  STORE_SUBSCR     

 L. 888       246  LOAD_CONST               0
              248  LOAD_FAST                'info'
              250  LOAD_FAST                'name'
              252  STORE_SUBSCR     
              254  JUMP_BACK           158  'to 158'
              256  POP_BLOCK        
            258_0  COME_FROM_LOOP      152  '152'

 L. 891       258  LOAD_FAST                'pax_headers'
          260_262  POP_JUMP_IF_FALSE   280  'to 280'

 L. 892       264  LOAD_FAST                'self'
              266  LOAD_METHOD              _create_pax_generic_header
              268  LOAD_FAST                'pax_headers'
              270  LOAD_GLOBAL              XHDTYPE
              272  LOAD_FAST                'encoding'
              274  CALL_METHOD_3         3  '3 positional arguments'
              276  STORE_FAST               'buf'
              278  JUMP_FORWARD        284  'to 284'
            280_0  COME_FROM           260  '260'

 L. 894       280  LOAD_CONST               b''
              282  STORE_FAST               'buf'
            284_0  COME_FROM           278  '278'

 L. 896       284  LOAD_FAST                'buf'
              286  LOAD_FAST                'self'
              288  LOAD_METHOD              _create_header
              290  LOAD_FAST                'info'
              292  LOAD_GLOBAL              USTAR_FORMAT
              294  LOAD_STR                 'ascii'
              296  LOAD_STR                 'replace'
              298  CALL_METHOD_4         4  '4 positional arguments'
              300  BINARY_ADD       
              302  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 256

    @classmethod
    def create_pax_global_header(cls, pax_headers):
        """Return the object as a pax global header block sequence.
        """
        return cls._create_pax_generic_header(pax_headers, XGLTYPE, 'utf-8')

    def _posix_split_name(self, name, encoding, errors):
        """Split a name longer than 100 chars into a prefix
           and a name part.
        """
        components = name.split('/')
        for i in range(1, len(components)):
            prefix = '/'.join(components[:i])
            name = '/'.join(components[i:])
            if len(prefix.encode(encoding, errors)) <= LENGTH_PREFIX and len(name.encode(encoding, errors)) <= LENGTH_NAME:
                break
        else:
            raise ValueError('name is too long')

        return (prefix, name)

    @staticmethod
    def _create_header(info, format, encoding, errors):
        """Return a header block. info is a dictionary with file
           information, format must be one of the *_FORMAT constants.
        """
        parts = [
         stn(info.get('name', ''), 100, encoding, errors),
         itn(info.get('mode', 0) & 4095, 8, format),
         itn(info.get('uid', 0), 8, format),
         itn(info.get('gid', 0), 8, format),
         itn(info.get('size', 0), 12, format),
         itn(info.get('mtime', 0), 12, format),
         b'        ',
         info.get('type', REGTYPE),
         stn(info.get('linkname', ''), 100, encoding, errors),
         info.get('magic', POSIX_MAGIC),
         stn(info.get('uname', ''), 32, encoding, errors),
         stn(info.get('gname', ''), 32, encoding, errors),
         itn(info.get('devmajor', 0), 8, format),
         itn(info.get('devminor', 0), 8, format),
         stn(info.get('prefix', ''), 155, encoding, errors)]
        buf = struct.pack('%ds' % BLOCKSIZE, (b'').join(parts))
        chksum = calc_chksums(buf[-BLOCKSIZE:])[0]
        buf = buf[:-364] + bytes('%06o\x00' % chksum, 'ascii') + buf[-357:]
        return buf

    @staticmethod
    def _create_payload(payload):
        """Return the string payload filled with zero bytes
           up to the next 512 byte border.
        """
        blocks, remainder = divmod(len(payload), BLOCKSIZE)
        if remainder > 0:
            payload += (BLOCKSIZE - remainder) * NUL
        return payload

    @classmethod
    def _create_gnu_long_header(cls, name, type, encoding, errors):
        """Return a GNUTYPE_LONGNAME or GNUTYPE_LONGLINK sequence
           for name.
        """
        name = name.encode(encoding, errors) + NUL
        info = {}
        info['name'] = '././@LongLink'
        info['type'] = type
        info['size'] = len(name)
        info['magic'] = GNU_MAGIC
        return cls._create_header(info, USTAR_FORMAT, encoding, errors) + cls._create_payload(name)

    @classmethod
    def _create_pax_generic_header(cls, pax_headers, type, encoding):
        """Return a POSIX.1-2008 extended or global header sequence
           that contains a list of keyword, value pairs. The values
           must be strings.
        """
        binary = False
        for keyword, value in pax_headers.items():
            try:
                value.encode('utf-8', 'strict')
            except UnicodeEncodeError:
                binary = True
                break

        records = b''
        if binary:
            records += b'21 hdrcharset=BINARY\n'
        for keyword, value in pax_headers.items():
            keyword = keyword.encode('utf-8')
            if binary:
                value = value.encode(encoding, 'surrogateescape')
            else:
                value = value.encode('utf-8')
            l = len(keyword) + len(value) + 3
            n = p = 0
            while True:
                n = l + len(str(p))
                if n == p:
                    break
                p = n

            records += bytes(str(p), 'ascii') + b' ' + keyword + b'=' + value + b'\n'

        info = {}
        info['name'] = '././@PaxHeader'
        info['type'] = type
        info['size'] = len(records)
        info['magic'] = POSIX_MAGIC
        return cls._create_header(info, USTAR_FORMAT, 'ascii', 'replace') + cls._create_payload(records)

    @classmethod
    def frombuf(cls, buf, encoding, errors):
        """Construct a TarInfo object from a 512 byte bytes object.
        """
        if len(buf) == 0:
            raise EmptyHeaderError('empty header')
        else:
            if len(buf) != BLOCKSIZE:
                raise TruncatedHeaderError('truncated header')
            else:
                if buf.count(NUL) == BLOCKSIZE:
                    raise EOFHeaderError('end of file header')
                chksum = nti(buf[148:156])
                if chksum not in calc_chksums(buf):
                    raise InvalidHeaderError('bad checksum')
                obj = cls()
                obj.name = nts(buf[0:100], encoding, errors)
                obj.mode = nti(buf[100:108])
                obj.uid = nti(buf[108:116])
                obj.gid = nti(buf[116:124])
                obj.size = nti(buf[124:136])
                obj.mtime = nti(buf[136:148])
                obj.chksum = chksum
                obj.type = buf[156:157]
                obj.linkname = nts(buf[157:257], encoding, errors)
                obj.uname = nts(buf[265:297], encoding, errors)
                obj.gname = nts(buf[297:329], encoding, errors)
                obj.devmajor = nti(buf[329:337])
                obj.devminor = nti(buf[337:345])
                prefix = nts(buf[345:500], encoding, errors)
                if obj.type == AREGTYPE and obj.name.endswith('/'):
                    obj.type = DIRTYPE
            if obj.type == GNUTYPE_SPARSE:
                pos = 386
                structs = []
                for i in range(4):
                    try:
                        offset = nti(buf[pos:pos + 12])
                        numbytes = nti(buf[pos + 12:pos + 24])
                    except ValueError:
                        break

                    structs.append((offset, numbytes))
                    pos += 24

                isextended = bool(buf[482])
                origsize = nti(buf[483:495])
                obj._sparse_structs = (structs, isextended, origsize)
            if obj.isdir():
                obj.name = obj.name.rstrip('/')
            if prefix and obj.type not in GNU_TYPES:
                obj.name = prefix + '/' + obj.name
        return obj

    @classmethod
    def fromtarfile(cls, tarfile):
        """Return the next TarInfo object from TarFile object
           tarfile.
        """
        buf = tarfile.fileobj.read(BLOCKSIZE)
        obj = cls.frombuf(buf, tarfile.encoding, tarfile.errors)
        obj.offset = tarfile.fileobj.tell() - BLOCKSIZE
        return obj._proc_member(tarfile)

    def _proc_member(self, tarfile):
        """Choose the right processing method depending on
           the type and call it.
        """
        if self.type in (GNUTYPE_LONGNAME, GNUTYPE_LONGLINK):
            return self._proc_gnulong(tarfile)
        if self.type == GNUTYPE_SPARSE:
            return self._proc_sparse(tarfile)
        if self.type in (XHDTYPE, XGLTYPE, SOLARIS_XHDTYPE):
            return self._proc_pax(tarfile)
        return self._proc_builtin(tarfile)

    def _proc_builtin(self, tarfile):
        """Process a builtin type or an unknown type which
           will be treated as a regular file.
        """
        self.offset_data = tarfile.fileobj.tell()
        offset = self.offset_data
        if self.isreg() or self.type not in SUPPORTED_TYPES:
            offset += self._block(self.size)
        tarfile.offset = offset
        self._apply_pax_info(tarfile.pax_headers, tarfile.encoding, tarfile.errors)
        return self

    def _proc_gnulong(self, tarfile):
        """Process the blocks that hold a GNU longname
           or longlink member.
        """
        buf = tarfile.fileobj.read(self._block(self.size))
        try:
            next = self.fromtarfile(tarfile)
        except HeaderError:
            raise SubsequentHeaderError('missing or bad subsequent header')

        next.offset = self.offset
        if self.type == GNUTYPE_LONGNAME:
            next.name = nts(buf, tarfile.encoding, tarfile.errors)
        else:
            if self.type == GNUTYPE_LONGLINK:
                next.linkname = nts(buf, tarfile.encoding, tarfile.errors)
        return next

    def _proc_sparse(self, tarfile):
        """Process a GNU sparse header plus extra headers.
        """
        structs, isextended, origsize = self._sparse_structs
        del self._sparse_structs
        while isextended:
            buf = tarfile.fileobj.read(BLOCKSIZE)
            pos = 0
            for i in range(21):
                try:
                    offset = nti(buf[pos:pos + 12])
                    numbytes = nti(buf[pos + 12:pos + 24])
                except ValueError:
                    break

                if offset:
                    if numbytes:
                        structs.append((offset, numbytes))
                pos += 24

            isextended = bool(buf[504])

        self.sparse = structs
        self.offset_data = tarfile.fileobj.tell()
        tarfile.offset = self.offset_data + self._block(self.size)
        self.size = origsize
        return self

    def _proc_pax(self, tarfile):
        """Process an extended or global header as described in
           POSIX.1-2008.
        """
        buf = tarfile.fileobj.read(self._block(self.size))
        if self.type == XGLTYPE:
            pax_headers = tarfile.pax_headers
        else:
            pax_headers = tarfile.pax_headers.copy()
        match = re.search(b'\\d+ hdrcharset=([^\\n]+)\\n', buf)
        if match is not None:
            pax_headers['hdrcharset'] = match.group(1).decode('utf-8')
        else:
            hdrcharset = pax_headers.get('hdrcharset')
            if hdrcharset == 'BINARY':
                encoding = tarfile.encoding
            else:
                encoding = 'utf-8'
        regex = re.compile(b'(\\d+) ([^=]+)=')
        pos = 0
        while True:
            match = regex.match(buf, pos)
            if not match:
                break
            else:
                length, keyword = match.groups()
                length = int(length)
                value = buf[match.end(2) + 1:match.start(1) + length - 1]
                keyword = self._decode_pax_field(keyword, 'utf-8', 'utf-8', tarfile.errors)
                if keyword in PAX_NAME_FIELDS:
                    value = self._decode_pax_field(value, encoding, tarfile.encoding, tarfile.errors)
                else:
                    value = self._decode_pax_field(value, 'utf-8', 'utf-8', tarfile.errors)
            pax_headers[keyword] = value
            pos += length

        try:
            next = self.fromtarfile(tarfile)
        except HeaderError:
            raise SubsequentHeaderError('missing or bad subsequent header')

        if 'GNU.sparse.map' in pax_headers:
            self._proc_gnusparse_01(next, pax_headers)
        else:
            if 'GNU.sparse.size' in pax_headers:
                self._proc_gnusparse_00(next, pax_headers, buf)
            else:
                if pax_headers.get('GNU.sparse.major') == '1':
                    if pax_headers.get('GNU.sparse.minor') == '0':
                        self._proc_gnusparse_10(next, pax_headers, tarfile)
                if self.type in (XHDTYPE, SOLARIS_XHDTYPE):
                    next._apply_pax_info(pax_headers, tarfile.encoding, tarfile.errors)
                    next.offset = self.offset
                    if 'size' in pax_headers:
                        offset = next.offset_data
                        if next.isreg() or next.type not in SUPPORTED_TYPES:
                            offset += next._block(next.size)
                        tarfile.offset = offset
                return next

    def _proc_gnusparse_00(self, next, pax_headers, buf):
        """Process a GNU tar extended sparse header, version 0.0.
        """
        offsets = []
        for match in re.finditer(b'\\d+ GNU.sparse.offset=(\\d+)\\n', buf):
            offsets.append(int(match.group(1)))

        numbytes = []
        for match in re.finditer(b'\\d+ GNU.sparse.numbytes=(\\d+)\\n', buf):
            numbytes.append(int(match.group(1)))

        next.sparse = list(zip(offsets, numbytes))

    def _proc_gnusparse_01(self, next, pax_headers):
        """Process a GNU tar extended sparse header, version 0.1.
        """
        sparse = [int(x) for x in pax_headers['GNU.sparse.map'].split(',')]
        next.sparse = list(zip(sparse[::2], sparse[1::2]))

    def _proc_gnusparse_10(self, next, pax_headers, tarfile):
        """Process a GNU tar extended sparse header, version 1.0.
        """
        fields = None
        sparse = []
        buf = tarfile.fileobj.read(BLOCKSIZE)
        fields, buf = buf.split(b'\n', 1)
        fields = int(fields)
        while len(sparse) < fields * 2:
            if b'\n' not in buf:
                buf += tarfile.fileobj.read(BLOCKSIZE)
            number, buf = buf.split(b'\n', 1)
            sparse.append(int(number))

        next.offset_data = tarfile.fileobj.tell()
        next.sparse = list(zip(sparse[::2], sparse[1::2]))

    def _apply_pax_info(self, pax_headers, encoding, errors):
        """Replace fields with supplemental information from a previous
           pax extended or global header.
        """
        for keyword, value in pax_headers.items():
            if keyword == 'GNU.sparse.name':
                setattr(self, 'path', value)
            elif keyword == 'GNU.sparse.size':
                setattr(self, 'size', int(value))
            else:
                if keyword == 'GNU.sparse.realsize':
                    setattr(self, 'size', int(value))

        self.pax_headers = pax_headers.copy()

    def _decode_pax_field(self, value, encoding, fallback_encoding, fallback_errors):
        """Decode a single field from a pax record.
        """
        try:
            return value.decode(encoding, 'strict')
        except UnicodeDecodeError:
            return value.decode(fallback_encoding, fallback_errors)

    def _block(self, count):
        """Round up a byte count by BLOCKSIZE and return it,
           e.g. _block(834) => 1024.
        """
        blocks, remainder = divmod(count, BLOCKSIZE)
        if remainder:
            blocks += 1
        return blocks * BLOCKSIZE

    def isreg(self):
        return self.type in REGULAR_TYPES

    def isfile(self):
        return self.isreg()

    def isdir(self):
        return self.type == DIRTYPE

    def issym(self):
        return self.type == SYMTYPE

    def islnk(self):
        return self.type == LNKTYPE

    def ischr(self):
        return self.type == CHRTYPE

    def isblk(self):
        return self.type == BLKTYPE

    def isfifo(self):
        return self.type == FIFOTYPE

    def issparse(self):
        return self.sparse is not None

    def isdev(self):
        return self.type in (CHRTYPE, BLKTYPE, FIFOTYPE)


class TarFile(object):
    __doc__ = 'The TarFile Class provides an interface to tar archives.\n    '
    debug = 0
    dereference = False
    ignore_zeros = False
    errorlevel = 1
    format = DEFAULT_FORMAT
    encoding = ENCODING
    errors = None
    tarinfo = TarInfo
    fileobject = ExFileObject

    def __init__(self, name=None, mode='r', fileobj=None, format=None, tarinfo=None, dereference=None, ignore_zeros=None, encoding=None, errors='surrogateescape', pax_headers=None, debug=None, errorlevel=None, copybufsize=None):
        """Open an (uncompressed) tar archive `name'. `mode' is either 'r' to
           read from an existing archive, 'a' to append data to an existing
           file or 'w' to create a new file overwriting an existing one. `mode'
           defaults to 'r'.
           If `fileobj' is given, it is used for reading or writing data. If it
           can be determined, `mode' is overridden by `fileobj's mode.
           `fileobj' is not closed, when TarFile is closed.
        """
        modes = {'r':'rb', 
         'a':'r+b',  'w':'wb',  'x':'xb'}
        if mode not in modes:
            raise ValueError("mode must be 'r', 'a', 'w' or 'x'")
        self.mode = mode
        self._mode = modes[mode]
        if not fileobj:
            if self.mode == 'a':
                if not os.path.exists(name):
                    self.mode = 'w'
                    self._mode = 'wb'
            fileobj = bltn_open(name, self._mode)
            self._extfileobj = False
        else:
            if name is None:
                if hasattr(fileobj, 'name'):
                    if isinstance(fileobj.name, (str, bytes)):
                        name = fileobj.name
            if hasattr(fileobj, 'mode'):
                self._mode = fileobj.mode
            self._extfileobj = True
        self.name = os.path.abspath(name) if name else None
        self.fileobj = fileobj
        if format is not None:
            self.format = format
        if tarinfo is not None:
            self.tarinfo = tarinfo
        if dereference is not None:
            self.dereference = dereference
        if ignore_zeros is not None:
            self.ignore_zeros = ignore_zeros
        if encoding is not None:
            self.encoding = encoding
        self.errors = errors
        if pax_headers is not None and self.format == PAX_FORMAT:
            self.pax_headers = pax_headers
        else:
            self.pax_headers = {}
        if debug is not None:
            self.debug = debug
        if errorlevel is not None:
            self.errorlevel = errorlevel
        self.copybufsize = copybufsize
        self.closed = False
        self.members = []
        self._loaded = False
        self.offset = self.fileobj.tell()
        self.inodes = {}
        try:
            if self.mode == 'r':
                self.firstmember = None
                self.firstmember = self.next()
            else:
                if self.mode == 'a':
                    while True:
                        self.fileobj.seek(self.offset)
                        try:
                            tarinfo = self.tarinfo.fromtarfile(self)
                            self.members.append(tarinfo)
                        except EOFHeaderError:
                            self.fileobj.seek(self.offset)
                            break
                        except HeaderError as e:
                            try:
                                raise ReadError(str(e))
                            finally:
                                e = None
                                del e

                if self.mode in ('a', 'w', 'x'):
                    self._loaded = True
                    if self.pax_headers:
                        buf = self.tarinfo.create_pax_global_header(self.pax_headers.copy())
                        self.fileobj.write(buf)
                        self.offset += len(buf)
        except:
            if not self._extfileobj:
                self.fileobj.close()
            self.closed = True
            raise

    @classmethod
    def open(cls, name=None, mode='r', fileobj=None, bufsize=RECORDSIZE, **kwargs):
        """Open a tar archive for reading, writing or appending. Return
           an appropriate TarFile class.

           mode:
           'r' or 'r:*' open for reading with transparent compression
           'r:'         open for reading exclusively uncompressed
           'r:gz'       open for reading with gzip compression
           'r:bz2'      open for reading with bzip2 compression
           'r:xz'       open for reading with lzma compression
           'a' or 'a:'  open for appending, creating the file if necessary
           'w' or 'w:'  open for writing without compression
           'w:gz'       open for writing with gzip compression
           'w:bz2'      open for writing with bzip2 compression
           'w:xz'       open for writing with lzma compression

           'x' or 'x:'  create a tarfile exclusively without compression, raise
                        an exception if the file is already created
           'x:gz'       create a gzip compressed tarfile, raise an exception
                        if the file is already created
           'x:bz2'      create a bzip2 compressed tarfile, raise an exception
                        if the file is already created
           'x:xz'       create an lzma compressed tarfile, raise an exception
                        if the file is already created

           'r|*'        open a stream of tar blocks with transparent compression
           'r|'         open an uncompressed stream of tar blocks for reading
           'r|gz'       open a gzip compressed stream of tar blocks
           'r|bz2'      open a bzip2 compressed stream of tar blocks
           'r|xz'       open an lzma compressed stream of tar blocks
           'w|'         open an uncompressed stream for writing
           'w|gz'       open a gzip compressed stream for writing
           'w|bz2'      open a bzip2 compressed stream for writing
           'w|xz'       open an lzma compressed stream for writing
        """
        if not name:
            if not fileobj:
                raise ValueError('nothing to open')
        if mode in ('r', 'r:*'):

            def not_compressed(comptype):
                return cls.OPEN_METH[comptype] == 'taropen'

            for comptype in sorted((cls.OPEN_METH), key=not_compressed):
                func = getattr(cls, cls.OPEN_METH[comptype])
                if fileobj is not None:
                    saved_pos = fileobj.tell()
                try:
                    return func(name, 'r', fileobj, **kwargs)
                except (ReadError, CompressionError):
                    if fileobj is not None:
                        fileobj.seek(saved_pos)
                    continue

            raise ReadError('file could not be opened successfully')
        else:
            if ':' in mode:
                filemode, comptype = mode.split(':', 1)
                filemode = filemode or 'r'
                comptype = comptype or 'tar'
                if comptype in cls.OPEN_METH:
                    func = getattr(cls, cls.OPEN_METH[comptype])
                else:
                    raise CompressionError('unknown compression type %r' % comptype)
                return func(name, filemode, fileobj, **kwargs)
            if '|' in mode:
                filemode, comptype = mode.split('|', 1)
                filemode = filemode or 'r'
                comptype = comptype or 'tar'
                if filemode not in ('r', 'w'):
                    raise ValueError("mode must be 'r' or 'w'")
                stream = _Stream(name, filemode, comptype, fileobj, bufsize)
                try:
                    t = cls(name, filemode, stream, **kwargs)
                except:
                    stream.close()
                    raise

                t._extfileobj = False
                return t
            if mode in ('a', 'w', 'x'):
                return (cls.taropen)(name, mode, fileobj, **kwargs)
            raise ValueError('undiscernible mode')

    @classmethod
    def taropen(cls, name, mode='r', fileobj=None, **kwargs):
        """Open uncompressed tar archive name for reading or writing.
        """
        if mode not in ('r', 'a', 'w', 'x'):
            raise ValueError("mode must be 'r', 'a', 'w' or 'x'")
        return cls(name, mode, fileobj, **kwargs)

    @classmethod
    def gzopen(cls, name, mode='r', fileobj=None, compresslevel=9, **kwargs):
        """Open gzip compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
        if mode not in ('r', 'w', 'x'):
            raise ValueError("mode must be 'r', 'w' or 'x'")
        try:
            import gzip
            gzip.GzipFile
        except (ImportError, AttributeError):
            raise CompressionError('gzip module is not available')

        try:
            fileobj = gzip.GzipFile(name, mode + 'b', compresslevel, fileobj)
        except OSError:
            if fileobj is not None:
                if mode == 'r':
                    raise ReadError('not a gzip file')
            raise

        try:
            t = (cls.taropen)(name, mode, fileobj, **kwargs)
        except OSError:
            fileobj.close()
            if mode == 'r':
                raise ReadError('not a gzip file')
            raise
        except:
            fileobj.close()
            raise

        t._extfileobj = False
        return t

    @classmethod
    def bz2open(cls, name, mode='r', fileobj=None, compresslevel=9, **kwargs):
        """Open bzip2 compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
        if mode not in ('r', 'w', 'x'):
            raise ValueError("mode must be 'r', 'w' or 'x'")
        try:
            import bz2
        except ImportError:
            raise CompressionError('bz2 module is not available')

        fileobj = bz2.BZ2File((fileobj or name), mode, compresslevel=compresslevel)
        try:
            t = (cls.taropen)(name, mode, fileobj, **kwargs)
        except (OSError, EOFError):
            fileobj.close()
            if mode == 'r':
                raise ReadError('not a bzip2 file')
            raise
        except:
            fileobj.close()
            raise

        t._extfileobj = False
        return t

    @classmethod
    def xzopen(cls, name, mode='r', fileobj=None, preset=None, **kwargs):
        """Open lzma compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
        if mode not in ('r', 'w', 'x'):
            raise ValueError("mode must be 'r', 'w' or 'x'")
        try:
            import lzma
        except ImportError:
            raise CompressionError('lzma module is not available')

        fileobj = lzma.LZMAFile((fileobj or name), mode, preset=preset)
        try:
            t = (cls.taropen)(name, mode, fileobj, **kwargs)
        except (lzma.LZMAError, EOFError):
            fileobj.close()
            if mode == 'r':
                raise ReadError('not an lzma file')
            raise
        except:
            fileobj.close()
            raise

        t._extfileobj = False
        return t

    OPEN_METH = {'tar':'taropen', 
     'gz':'gzopen', 
     'bz2':'bz2open', 
     'xz':'xzopen'}

    def close(self):
        """Close the TarFile. In write-mode, two finishing zero blocks are
           appended to the archive.
        """
        if self.closed:
            return
        self.closed = True
        try:
            if self.mode in ('a', 'w', 'x'):
                self.fileobj.write(NUL * (BLOCKSIZE * 2))
                self.offset += BLOCKSIZE * 2
                blocks, remainder = divmod(self.offset, RECORDSIZE)
                if remainder > 0:
                    self.fileobj.write(NUL * (RECORDSIZE - remainder))
        finally:
            if not self._extfileobj:
                self.fileobj.close()

    def getmember(self, name):
        """Return a TarInfo object for member `name'. If `name' can not be
           found in the archive, KeyError is raised. If a member occurs more
           than once in the archive, its last occurrence is assumed to be the
           most up-to-date version.
        """
        tarinfo = self._getmember(name)
        if tarinfo is None:
            raise KeyError('filename %r not found' % name)
        return tarinfo

    def getmembers(self):
        """Return the members of the archive as a list of TarInfo objects. The
           list has the same order as the members in the archive.
        """
        self._check()
        if not self._loaded:
            self._load()
        return self.members

    def getnames(self):
        """Return the members of the archive as a list of their names. It has
           the same order as the list returned by getmembers().
        """
        return [tarinfo.name for tarinfo in self.getmembers()]

    def gettarinfo(self, name=None, arcname=None, fileobj=None):
        """Create a TarInfo object from the result of os.stat or equivalent
           on an existing file. The file is either named by `name', or
           specified as a file object `fileobj' with a file descriptor. If
           given, `arcname' specifies an alternative name for the file in the
           archive, otherwise, the name is taken from the 'name' attribute of
           'fileobj', or the 'name' argument. The name should be a text
           string.
        """
        self._check('awx')
        if fileobj is not None:
            name = fileobj.name
        else:
            if arcname is None:
                arcname = name
            else:
                drv, arcname = os.path.splitdrive(arcname)
                arcname = arcname.replace(os.sep, '/')
                arcname = arcname.lstrip('/')
                tarinfo = self.tarinfo()
                tarinfo.tarfile = self
                if fileobj is None:
                    if hasattr(os, 'lstat'):
                        statres = self.dereference or os.lstat(name)
                    else:
                        statres = os.stat(name)
                else:
                    statres = os.fstat(fileobj.fileno())
            linkname = ''
            stmd = statres.st_mode
            if stat.S_ISREG(stmd):
                inode = (
                 statres.st_ino, statres.st_dev)
                if not self.dereference:
                    if statres.st_nlink > 1 and inode in self.inodes and arcname != self.inodes[inode]:
                        type = LNKTYPE
                        linkname = self.inodes[inode]
                    else:
                        type = REGTYPE
                        if inode[0]:
                            self.inodes[inode] = arcname
                else:
                    if stat.S_ISDIR(stmd):
                        type = DIRTYPE
                    else:
                        if stat.S_ISFIFO(stmd):
                            type = FIFOTYPE
                        else:
                            if stat.S_ISLNK(stmd):
                                type = SYMTYPE
                                linkname = os.readlink(name)
                            else:
                                if stat.S_ISCHR(stmd):
                                    type = CHRTYPE
                                else:
                                    if stat.S_ISBLK(stmd):
                                        type = BLKTYPE
                                    else:
                                        return
                tarinfo.name = arcname
                tarinfo.mode = stmd
                tarinfo.uid = statres.st_uid
                tarinfo.gid = statres.st_gid
                if type == REGTYPE:
                    tarinfo.size = statres.st_size
            else:
                tarinfo.size = 0
        tarinfo.mtime = statres.st_mtime
        tarinfo.type = type
        tarinfo.linkname = linkname
        if pwd:
            try:
                tarinfo.uname = pwd.getpwuid(tarinfo.uid)[0]
            except KeyError:
                pass

        if grp:
            try:
                tarinfo.gname = grp.getgrgid(tarinfo.gid)[0]
            except KeyError:
                pass

        if type in (CHRTYPE, BLKTYPE):
            if hasattr(os, 'major'):
                if hasattr(os, 'minor'):
                    tarinfo.devmajor = os.major(statres.st_rdev)
                    tarinfo.devminor = os.minor(statres.st_rdev)
        return tarinfo

    def list(self, verbose=True, *, members=None):
        """Print a table of contents to sys.stdout. If `verbose' is False, only
           the names of the members are printed. If it is True, an `ls -l'-like
           output is produced. `members' is optional and must be a subset of the
           list returned by getmembers().
        """
        self._check()
        if members is None:
            members = self
        for tarinfo in members:
            if verbose:
                _safe_print(stat.filemode(tarinfo.mode))
                _safe_print('%s/%s' % (tarinfo.uname or tarinfo.uid,
                 tarinfo.gname or tarinfo.gid))
                if tarinfo.ischr() or tarinfo.isblk():
                    _safe_print('%10s' % ('%d,%d' % (tarinfo.devmajor, tarinfo.devminor)))
                else:
                    _safe_print('%10d' % tarinfo.size)
                _safe_print('%d-%02d-%02d %02d:%02d:%02d' % time.localtime(tarinfo.mtime)[:6])
            _safe_print(tarinfo.name + ('/' if tarinfo.isdir() else ''))
            if verbose:
                if tarinfo.issym():
                    _safe_print('-> ' + tarinfo.linkname)
                if tarinfo.islnk():
                    _safe_print('link to ' + tarinfo.linkname)
            print()

    def add(self, name, arcname=None, recursive=True, *, filter=None):
        """Add the file `name' to the archive. `name' may be any type of file
           (directory, fifo, symbolic link, etc.). If given, `arcname'
           specifies an alternative name for the file in the archive.
           Directories are added recursively by default. This can be avoided by
           setting `recursive' to False. `filter' is a function
           that expects a TarInfo object argument and returns the changed
           TarInfo object, if it returns None the TarInfo object will be
           excluded from the archive.
        """
        self._check('awx')
        if arcname is None:
            arcname = name
        elif self.name is not None:
            if os.path.abspath(name) == self.name:
                self._dbg(2, 'tarfile: Skipped %r' % name)
                return
            else:
                self._dbg(1, name)
                tarinfo = self.gettarinfo(name, arcname)
                if tarinfo is None:
                    self._dbg(1, 'tarfile: Unsupported type %r' % name)
                    return
                if filter is not None:
                    tarinfo = filter(tarinfo)
                    if tarinfo is None:
                        self._dbg(2, 'tarfile: Excluded %r' % name)
                        return
            if tarinfo.isreg():
                with bltn_open(name, 'rb') as (f):
                    self.addfile(tarinfo, f)
        elif tarinfo.isdir():
            self.addfile(tarinfo)
            if recursive:
                for f in sorted(os.listdir(name)):
                    self.add((os.path.join(name, f)), (os.path.join(arcname, f)), recursive,
                      filter=filter)

        else:
            self.addfile(tarinfo)

    def addfile(self, tarinfo, fileobj=None):
        """Add the TarInfo object `tarinfo' to the archive. If `fileobj' is
           given, it should be a binary file, and tarinfo.size bytes are read
           from it and added to the archive. You can create TarInfo objects
           directly, or by using gettarinfo().
        """
        self._check('awx')
        tarinfo = copy.copy(tarinfo)
        buf = tarinfo.tobuf(self.format, self.encoding, self.errors)
        self.fileobj.write(buf)
        self.offset += len(buf)
        bufsize = self.copybufsize
        if fileobj is not None:
            copyfileobj(fileobj, (self.fileobj), (tarinfo.size), bufsize=bufsize)
            blocks, remainder = divmod(tarinfo.size, BLOCKSIZE)
            if remainder > 0:
                self.fileobj.write(NUL * (BLOCKSIZE - remainder))
                blocks += 1
            self.offset += blocks * BLOCKSIZE
        self.members.append(tarinfo)

    def extractall(self, path='.', members=None, *, numeric_owner=False):
        """Extract all members from the archive to the current working
           directory and set owner, modification time and permissions on
           directories afterwards. `path' specifies a different directory
           to extract to. `members' is optional and must be a subset of the
           list returned by getmembers(). If `numeric_owner` is True, only
           the numbers for user/group names are used and not the names.
        """
        directories = []
        if members is None:
            members = self
        for tarinfo in members:
            if tarinfo.isdir():
                directories.append(tarinfo)
                tarinfo = copy.copy(tarinfo)
                tarinfo.mode = 448
            self.extract(tarinfo, path, set_attrs=(not tarinfo.isdir()), numeric_owner=numeric_owner)

        directories.sort(key=(lambda a: a.name))
        directories.reverse()
        for tarinfo in directories:
            dirpath = os.path.join(path, tarinfo.name)
            try:
                self.chown(tarinfo, dirpath, numeric_owner=numeric_owner)
                self.utime(tarinfo, dirpath)
                self.chmod(tarinfo, dirpath)
            except ExtractError as e:
                try:
                    if self.errorlevel > 1:
                        raise
                    else:
                        self._dbg(1, 'tarfile: %s' % e)
                finally:
                    e = None
                    del e

    def extract(self, member, path='', set_attrs=True, *, numeric_owner=False):
        """Extract a member from the archive to the current working directory,
           using its full name. Its file information is extracted as accurately
           as possible. `member' may be a filename or a TarInfo object. You can
           specify a different directory using `path'. File attributes (owner,
           mtime, mode) are set unless `set_attrs' is False. If `numeric_owner`
           is True, only the numbers for user/group names are used and not
           the names.
        """
        self._check('r')
        if isinstance(member, str):
            tarinfo = self.getmember(member)
        else:
            tarinfo = member
        if tarinfo.islnk():
            tarinfo._link_target = os.path.join(path, tarinfo.linkname)
        try:
            self._extract_member(tarinfo, (os.path.join(path, tarinfo.name)), set_attrs=set_attrs,
              numeric_owner=numeric_owner)
        except OSError as e:
            try:
                if self.errorlevel > 0:
                    raise
                else:
                    if e.filename is None:
                        self._dbg(1, 'tarfile: %s' % e.strerror)
                    else:
                        self._dbg(1, 'tarfile: %s %r' % (e.strerror, e.filename))
            finally:
                e = None
                del e

        except ExtractError as e:
            try:
                if self.errorlevel > 1:
                    raise
                else:
                    self._dbg(1, 'tarfile: %s' % e)
            finally:
                e = None
                del e

    def extractfile(self, member):
        """Extract a member from the archive as a file object. `member' may be
           a filename or a TarInfo object. If `member' is a regular file or a
           link, an io.BufferedReader object is returned. Otherwise, None is
           returned.
        """
        self._check('r')
        if isinstance(member, str):
            tarinfo = self.getmember(member)
        else:
            tarinfo = member
        if not tarinfo.isreg():
            if tarinfo.type not in SUPPORTED_TYPES:
                return self.fileobject(self, tarinfo)
            if tarinfo.islnk() or tarinfo.issym():
                if isinstance(self.fileobj, _Stream):
                    raise StreamError('cannot extract (sym)link as file object')
                else:
                    return self.extractfile(self._find_link_target(tarinfo))
        else:
            return

    def _extract_member(self, tarinfo, targetpath, set_attrs=True, numeric_owner=False):
        """Extract the TarInfo object tarinfo to a physical
           file called targetpath.
        """
        targetpath = targetpath.rstrip('/')
        targetpath = targetpath.replace('/', os.sep)
        upperdirs = os.path.dirname(targetpath)
        if upperdirs:
            if not os.path.exists(upperdirs):
                os.makedirs(upperdirs)
        elif tarinfo.islnk() or tarinfo.issym():
            self._dbg(1, '%s -> %s' % (tarinfo.name, tarinfo.linkname))
        else:
            self._dbg(1, tarinfo.name)
        if tarinfo.isreg():
            self.makefile(tarinfo, targetpath)
        else:
            if tarinfo.isdir():
                self.makedir(tarinfo, targetpath)
            else:
                if tarinfo.isfifo():
                    self.makefifo(tarinfo, targetpath)
                else:
                    if tarinfo.ischr() or tarinfo.isblk():
                        self.makedev(tarinfo, targetpath)
                    else:
                        if tarinfo.islnk() or tarinfo.issym():
                            self.makelink(tarinfo, targetpath)
                        else:
                            if tarinfo.type not in SUPPORTED_TYPES:
                                self.makeunknown(tarinfo, targetpath)
                            else:
                                self.makefile(tarinfo, targetpath)
        if set_attrs:
            self.chown(tarinfo, targetpath, numeric_owner)
            if not tarinfo.issym():
                self.chmod(tarinfo, targetpath)
                self.utime(tarinfo, targetpath)

    def makedir(self, tarinfo, targetpath):
        """Make a directory called targetpath.
        """
        try:
            os.mkdir(targetpath, 448)
        except FileExistsError:
            pass

    def makefile(self, tarinfo, targetpath):
        """Make a file called targetpath.
        """
        source = self.fileobj
        source.seek(tarinfo.offset_data)
        bufsize = self.copybufsize
        with bltn_open(targetpath, 'wb') as (target):
            if tarinfo.sparse is not None:
                for offset, size in tarinfo.sparse:
                    target.seek(offset)
                    copyfileobj(source, target, size, ReadError, bufsize)

                target.seek(tarinfo.size)
                target.truncate()
            else:
                copyfileobj(source, target, tarinfo.size, ReadError, bufsize)

    def makeunknown(self, tarinfo, targetpath):
        """Make a file from a TarInfo object with an unknown type
           at targetpath.
        """
        self.makefile(tarinfo, targetpath)
        self._dbg(1, 'tarfile: Unknown file type %r, extracted as regular file.' % tarinfo.type)

    def makefifo(self, tarinfo, targetpath):
        """Make a fifo called targetpath.
        """
        if hasattr(os, 'mkfifo'):
            os.mkfifo(targetpath)
        else:
            raise ExtractError('fifo not supported by system')

    def makedev(self, tarinfo, targetpath):
        """Make a character or block device called targetpath.
        """
        if hasattr(os, 'mknod'):
            raise hasattr(os, 'makedev') or ExtractError('special devices not supported by system')
        else:
            mode = tarinfo.mode
            if tarinfo.isblk():
                mode |= stat.S_IFBLK
            else:
                mode |= stat.S_IFCHR
        os.mknod(targetpath, mode, os.makedev(tarinfo.devmajor, tarinfo.devminor))

    def makelink(self, tarinfo, targetpath):
        """Make a (symbolic) link called targetpath. If it cannot be created
          (platform limitation), we try to make a copy of the referenced file
          instead of a link.
        """
        try:
            if tarinfo.issym():
                os.symlink(tarinfo.linkname, targetpath)
            else:
                if os.path.exists(tarinfo._link_target):
                    os.link(tarinfo._link_target, targetpath)
                else:
                    self._extract_member(self._find_link_target(tarinfo), targetpath)
        except symlink_exception:
            try:
                self._extract_member(self._find_link_target(tarinfo), targetpath)
            except KeyError:
                raise ExtractError('unable to resolve link inside archive')

    def chown(self, tarinfo, targetpath, numeric_owner):
        """Set owner of targetpath according to tarinfo. If numeric_owner
           is True, use .gid/.uid instead of .gname/.uname. If numeric_owner
           is False, fall back to .gid/.uid when the search based on name
           fails.
        """
        if hasattr(os, 'geteuid'):
            if os.geteuid() == 0:
                g = tarinfo.gid
                u = tarinfo.uid
                if not numeric_owner:
                    try:
                        if grp:
                            g = grp.getgrnam(tarinfo.gname)[2]
                    except KeyError:
                        pass

                    try:
                        if pwd:
                            u = pwd.getpwnam(tarinfo.uname)[2]
                    except KeyError:
                        pass

                try:
                    if tarinfo.issym() and hasattr(os, 'lchown'):
                        os.lchown(targetpath, u, g)
                    else:
                        os.chown(targetpath, u, g)
                except OSError:
                    raise ExtractError('could not change owner')

    def chmod(self, tarinfo, targetpath):
        """Set file permissions of targetpath according to tarinfo.
        """
        if hasattr(os, 'chmod'):
            try:
                os.chmod(targetpath, tarinfo.mode)
            except OSError:
                raise ExtractError('could not change mode')

    def utime(self, tarinfo, targetpath):
        """Set modification time of targetpath according to tarinfo.
        """
        if not hasattr(os, 'utime'):
            return
        try:
            os.utime(targetpath, (tarinfo.mtime, tarinfo.mtime))
        except OSError:
            raise ExtractError('could not change modification time')

    def next(self):
        """Return the next member of the archive as a TarInfo object, when
           TarFile is opened for reading. Return None if there is no more
           available.
        """
        self._check('ra')
        if self.firstmember is not None:
            m = self.firstmember
            self.firstmember = None
            return m
        if self.offset != self.fileobj.tell():
            self.fileobj.seek(self.offset - 1)
            if not self.fileobj.read(1):
                raise ReadError('unexpected end of data')
        else:
            tarinfo = None
            while True:
                try:
                    tarinfo = self.tarinfo.fromtarfile(self)
                except EOFHeaderError as e:
                    try:
                        if self.ignore_zeros:
                            self._dbg(2, '0x%X: %s' % (self.offset, e))
                            self.offset += BLOCKSIZE
                            continue
                    finally:
                        e = None
                        del e

                except InvalidHeaderError as e:
                    try:
                        if self.ignore_zeros:
                            self._dbg(2, '0x%X: %s' % (self.offset, e))
                            self.offset += BLOCKSIZE
                            continue
                        else:
                            if self.offset == 0:
                                raise ReadError(str(e))
                    finally:
                        e = None
                        del e

                except EmptyHeaderError:
                    if self.offset == 0:
                        raise ReadError('empty file')
                except TruncatedHeaderError as e:
                    try:
                        if self.offset == 0:
                            raise ReadError(str(e))
                    finally:
                        e = None
                        del e

                except SubsequentHeaderError as e:
                    try:
                        raise ReadError(str(e))
                    finally:
                        e = None
                        del e

                break

            if tarinfo is not None:
                self.members.append(tarinfo)
            else:
                self._loaded = True
        return tarinfo

    def _getmember(self, name, tarinfo=None, normalize=False):
        """Find an archive member by name from bottom to top.
           If tarinfo is given, it is used as the starting point.
        """
        members = self.getmembers()
        if tarinfo is not None:
            members = members[:members.index(tarinfo)]
        if normalize:
            name = os.path.normpath(name)
        for member in reversed(members):
            if normalize:
                member_name = os.path.normpath(member.name)
            else:
                member_name = member.name
            if name == member_name:
                return member

    def _load(self):
        """Read through the entire archive file and look for readable
           members.
        """
        while 1:
            tarinfo = self.next()
            if tarinfo is None:
                break

        self._loaded = True

    def _check(self, mode=None):
        """Check if TarFile is still open, and if the operation's mode
           corresponds to TarFile's mode.
        """
        if self.closed:
            raise OSError('%s is closed' % self.__class__.__name__)
        if mode is not None:
            if self.mode not in mode:
                raise OSError('bad operation for mode %r' % self.mode)

    def _find_link_target(self, tarinfo):
        """Find the target member of a symlink or hardlink member in the
           archive.
        """
        if tarinfo.issym():
            linkname = '/'.join(filter(None, (os.path.dirname(tarinfo.name), tarinfo.linkname)))
            limit = None
        else:
            linkname = tarinfo.linkname
            limit = tarinfo
        member = self._getmember(linkname, tarinfo=limit, normalize=True)
        if member is None:
            raise KeyError('linkname %r not found' % linkname)
        return member

    def __iter__(self):
        """Provide an iterator object.
        """
        if self._loaded:
            yield from self.members
            return
        index = 0
        if self.firstmember is not None:
            tarinfo = self.next()
            index += 1
            yield tarinfo
        while True:
            if index < len(self.members):
                tarinfo = self.members[index]
            else:
                if not self._loaded:
                    tarinfo = self.next()
                    self._loaded = tarinfo or True
                    return
                else:
                    return
            index += 1
            yield tarinfo

    def _dbg(self, level, msg):
        """Write debugging output to sys.stderr.
        """
        if level <= self.debug:
            print(msg, file=(sys.stderr))

    def __enter__(self):
        self._check()
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self.close()
        else:
            if not self._extfileobj:
                self.fileobj.close()
            self.closed = True


def is_tarfile(name):
    """Return True if name points to a tar archive that we
       are able to handle, else return False.
    """
    try:
        t = open(name)
        t.close()
        return True
    except TarError:
        return False


open = TarFile.open

def main--- This code section failed: ---

 L.2452         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              argparse
                6  STORE_FAST               'argparse'

 L.2454         8  LOAD_STR                 'A simple command-line interface for tarfile module.'
               10  STORE_FAST               'description'

 L.2455        12  LOAD_FAST                'argparse'
               14  LOAD_ATTR                ArgumentParser
               16  LOAD_FAST                'description'
               18  LOAD_CONST               ('description',)
               20  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               22  STORE_FAST               'parser'

 L.2456        24  LOAD_FAST                'parser'
               26  LOAD_ATTR                add_argument
               28  LOAD_STR                 '-v'
               30  LOAD_STR                 '--verbose'
               32  LOAD_STR                 'store_true'
               34  LOAD_CONST               False

 L.2457        36  LOAD_STR                 'Verbose output'
               38  LOAD_CONST               ('action', 'default', 'help')
               40  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               42  POP_TOP          

 L.2458        44  LOAD_FAST                'parser'
               46  LOAD_ATTR                add_mutually_exclusive_group
               48  LOAD_CONST               True
               50  LOAD_CONST               ('required',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  STORE_FAST               'group'

 L.2459        56  LOAD_FAST                'group'
               58  LOAD_ATTR                add_argument
               60  LOAD_STR                 '-l'
               62  LOAD_STR                 '--list'
               64  LOAD_STR                 '<tarfile>'

 L.2460        66  LOAD_STR                 'Show listing of a tarfile'
               68  LOAD_CONST               ('metavar', 'help')
               70  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               72  POP_TOP          

 L.2461        74  LOAD_FAST                'group'
               76  LOAD_ATTR                add_argument
               78  LOAD_STR                 '-e'
               80  LOAD_STR                 '--extract'
               82  LOAD_STR                 '+'

 L.2462        84  LOAD_CONST               ('<tarfile>', '<output_dir>')

 L.2463        86  LOAD_STR                 'Extract tarfile into target dir'
               88  LOAD_CONST               ('nargs', 'metavar', 'help')
               90  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               92  POP_TOP          

 L.2464        94  LOAD_FAST                'group'
               96  LOAD_ATTR                add_argument
               98  LOAD_STR                 '-c'
              100  LOAD_STR                 '--create'
              102  LOAD_STR                 '+'

 L.2465       104  LOAD_CONST               ('<name>', '<file>')

 L.2466       106  LOAD_STR                 'Create tarfile from sources'
              108  LOAD_CONST               ('nargs', 'metavar', 'help')
              110  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              112  POP_TOP          

 L.2467       114  LOAD_FAST                'group'
              116  LOAD_ATTR                add_argument
              118  LOAD_STR                 '-t'
              120  LOAD_STR                 '--test'
              122  LOAD_STR                 '<tarfile>'

 L.2468       124  LOAD_STR                 'Test if a tarfile is valid'
              126  LOAD_CONST               ('metavar', 'help')
              128  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              130  POP_TOP          

 L.2469       132  LOAD_FAST                'parser'
              134  LOAD_METHOD              parse_args
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  STORE_FAST               'args'

 L.2471       140  LOAD_FAST                'args'
              142  LOAD_ATTR                test
              144  LOAD_CONST               None
              146  COMPARE_OP               is-not
          148_150  POP_JUMP_IF_FALSE   258  'to 258'

 L.2472       152  LOAD_FAST                'args'
              154  LOAD_ATTR                test
              156  STORE_FAST               'src'

 L.2473       158  LOAD_GLOBAL              is_tarfile
              160  LOAD_FAST                'src'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  POP_JUMP_IF_FALSE   236  'to 236'

 L.2474       166  LOAD_GLOBAL              open
              168  LOAD_FAST                'src'
              170  LOAD_STR                 'r'
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  SETUP_WITH          208  'to 208'
              176  STORE_FAST               'tar'

 L.2475       178  LOAD_FAST                'tar'
              180  LOAD_METHOD              getmembers
              182  CALL_METHOD_0         0  '0 positional arguments'
              184  POP_TOP          

 L.2476       186  LOAD_GLOBAL              print
              188  LOAD_FAST                'tar'
              190  LOAD_METHOD              getmembers
              192  CALL_METHOD_0         0  '0 positional arguments'
              194  LOAD_GLOBAL              sys
              196  LOAD_ATTR                stderr
              198  LOAD_CONST               ('file',)
              200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              202  POP_TOP          
              204  POP_BLOCK        
              206  LOAD_CONST               None
            208_0  COME_FROM_WITH      174  '174'
              208  WITH_CLEANUP_START
              210  WITH_CLEANUP_FINISH
              212  END_FINALLY      

 L.2477       214  LOAD_FAST                'args'
              216  LOAD_ATTR                verbose
              218  POP_JUMP_IF_FALSE   254  'to 254'

 L.2478       220  LOAD_GLOBAL              print
              222  LOAD_STR                 '{!r} is a tar archive.'
              224  LOAD_METHOD              format
              226  LOAD_FAST                'src'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  POP_TOP          
              234  JUMP_FORWARD        722  'to 722'
            236_0  COME_FROM           164  '164'

 L.2480       236  LOAD_FAST                'parser'
              238  LOAD_METHOD              exit
              240  LOAD_CONST               1
              242  LOAD_STR                 '{!r} is not a tar archive.\n'
              244  LOAD_METHOD              format
              246  LOAD_FAST                'src'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  CALL_METHOD_2         2  '2 positional arguments'
              252  POP_TOP          
            254_0  COME_FROM           218  '218'
          254_256  JUMP_FORWARD        722  'to 722'
            258_0  COME_FROM           148  '148'

 L.2482       258  LOAD_FAST                'args'
              260  LOAD_ATTR                list
              262  LOAD_CONST               None
              264  COMPARE_OP               is-not
          266_268  POP_JUMP_IF_FALSE   348  'to 348'

 L.2483       270  LOAD_FAST                'args'
              272  LOAD_ATTR                list
              274  STORE_FAST               'src'

 L.2484       276  LOAD_GLOBAL              is_tarfile
              278  LOAD_FAST                'src'
              280  CALL_FUNCTION_1       1  '1 positional argument'
          282_284  POP_JUMP_IF_FALSE   326  'to 326'

 L.2485       286  LOAD_GLOBAL              TarFile
              288  LOAD_METHOD              open
              290  LOAD_FAST                'src'
              292  LOAD_STR                 'r:*'
              294  CALL_METHOD_2         2  '2 positional arguments'
              296  SETUP_WITH          318  'to 318'
              298  STORE_FAST               'tf'

 L.2486       300  LOAD_FAST                'tf'
              302  LOAD_ATTR                list
              304  LOAD_FAST                'args'
              306  LOAD_ATTR                verbose
              308  LOAD_CONST               ('verbose',)
              310  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              312  POP_TOP          
              314  POP_BLOCK        
              316  LOAD_CONST               None
            318_0  COME_FROM_WITH      296  '296'
              318  WITH_CLEANUP_START
              320  WITH_CLEANUP_FINISH
              322  END_FINALLY      
              324  JUMP_FORWARD        722  'to 722'
            326_0  COME_FROM           282  '282'

 L.2488       326  LOAD_FAST                'parser'
              328  LOAD_METHOD              exit
              330  LOAD_CONST               1
              332  LOAD_STR                 '{!r} is not a tar archive.\n'
              334  LOAD_METHOD              format
              336  LOAD_FAST                'src'
              338  CALL_METHOD_1         1  '1 positional argument'
              340  CALL_METHOD_2         2  '2 positional arguments'
              342  POP_TOP          
          344_346  JUMP_FORWARD        722  'to 722'
            348_0  COME_FROM           266  '266'

 L.2490       348  LOAD_FAST                'args'
              350  LOAD_ATTR                extract
              352  LOAD_CONST               None
              354  COMPARE_OP               is-not
          356_358  POP_JUMP_IF_FALSE   556  'to 556'

 L.2491       360  LOAD_GLOBAL              len
              362  LOAD_FAST                'args'
              364  LOAD_ATTR                extract
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  LOAD_CONST               1
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   394  'to 394'

 L.2492       376  LOAD_FAST                'args'
              378  LOAD_ATTR                extract
              380  LOAD_CONST               0
              382  BINARY_SUBSCR    
              384  STORE_FAST               'src'

 L.2493       386  LOAD_GLOBAL              os
              388  LOAD_ATTR                curdir
              390  STORE_FAST               'curdir'
              392  JUMP_FORWARD        438  'to 438'
            394_0  COME_FROM           372  '372'

 L.2494       394  LOAD_GLOBAL              len
              396  LOAD_FAST                'args'
              398  LOAD_ATTR                extract
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  LOAD_CONST               2
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   422  'to 422'

 L.2495       410  LOAD_FAST                'args'
              412  LOAD_ATTR                extract
              414  UNPACK_SEQUENCE_2     2 
              416  STORE_FAST               'src'
              418  STORE_FAST               'curdir'
              420  JUMP_FORWARD        438  'to 438'
            422_0  COME_FROM           406  '406'

 L.2497       422  LOAD_FAST                'parser'
              424  LOAD_METHOD              exit
              426  LOAD_CONST               1
              428  LOAD_FAST                'parser'
              430  LOAD_METHOD              format_help
              432  CALL_METHOD_0         0  '0 positional arguments'
              434  CALL_METHOD_2         2  '2 positional arguments'
              436  POP_TOP          
            438_0  COME_FROM           420  '420'
            438_1  COME_FROM           392  '392'

 L.2499       438  LOAD_GLOBAL              is_tarfile
              440  LOAD_FAST                'src'
              442  CALL_FUNCTION_1       1  '1 positional argument'
          444_446  POP_JUMP_IF_FALSE   536  'to 536'

 L.2500       448  LOAD_GLOBAL              TarFile
              450  LOAD_METHOD              open
              452  LOAD_FAST                'src'
              454  LOAD_STR                 'r:*'
              456  CALL_METHOD_2         2  '2 positional arguments'
              458  SETUP_WITH          478  'to 478'
              460  STORE_FAST               'tf'

 L.2501       462  LOAD_FAST                'tf'
              464  LOAD_ATTR                extractall
              466  LOAD_FAST                'curdir'
              468  LOAD_CONST               ('path',)
              470  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              472  POP_TOP          
              474  POP_BLOCK        
              476  LOAD_CONST               None
            478_0  COME_FROM_WITH      458  '458'
              478  WITH_CLEANUP_START
              480  WITH_CLEANUP_FINISH
              482  END_FINALLY      

 L.2502       484  LOAD_FAST                'args'
              486  LOAD_ATTR                verbose
          488_490  POP_JUMP_IF_FALSE   554  'to 554'

 L.2503       492  LOAD_FAST                'curdir'
              494  LOAD_STR                 '.'
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   514  'to 514'

 L.2504       502  LOAD_STR                 '{!r} file is extracted.'
              504  LOAD_METHOD              format
              506  LOAD_FAST                'src'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  STORE_FAST               'msg'
              512  JUMP_FORWARD        526  'to 526'
            514_0  COME_FROM           498  '498'

 L.2506       514  LOAD_STR                 '{!r} file is extracted into {!r} directory.'
              516  LOAD_METHOD              format

 L.2507       518  LOAD_FAST                'src'
              520  LOAD_FAST                'curdir'
              522  CALL_METHOD_2         2  '2 positional arguments'
              524  STORE_FAST               'msg'
            526_0  COME_FROM           512  '512'

 L.2508       526  LOAD_GLOBAL              print
              528  LOAD_FAST                'msg'
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  POP_TOP          
              534  JUMP_FORWARD        554  'to 554'
            536_0  COME_FROM           444  '444'

 L.2510       536  LOAD_FAST                'parser'
              538  LOAD_METHOD              exit
              540  LOAD_CONST               1
              542  LOAD_STR                 '{!r} is not a tar archive.\n'
              544  LOAD_METHOD              format
              546  LOAD_FAST                'src'
              548  CALL_METHOD_1         1  '1 positional argument'
              550  CALL_METHOD_2         2  '2 positional arguments'
              552  POP_TOP          
            554_0  COME_FROM           534  '534'
            554_1  COME_FROM           488  '488'
              554  JUMP_FORWARD        722  'to 722'
            556_0  COME_FROM           356  '356'

 L.2512       556  LOAD_FAST                'args'
              558  LOAD_ATTR                create
              560  LOAD_CONST               None
              562  COMPARE_OP               is-not
          564_566  POP_JUMP_IF_FALSE   722  'to 722'

 L.2513       568  LOAD_FAST                'args'
              570  LOAD_ATTR                create
              572  LOAD_METHOD              pop
              574  LOAD_CONST               0
              576  CALL_METHOD_1         1  '1 positional argument'
              578  STORE_FAST               'tar_name'

 L.2514       580  LOAD_GLOBAL              os
              582  LOAD_ATTR                path
              584  LOAD_METHOD              splitext
              586  LOAD_FAST                'tar_name'
              588  CALL_METHOD_1         1  '1 positional argument'
              590  UNPACK_SEQUENCE_2     2 
              592  STORE_FAST               '_'
              594  STORE_FAST               'ext'

 L.2517       596  LOAD_STR                 'gz'

 L.2518       598  LOAD_STR                 'gz'

 L.2520       600  LOAD_STR                 'xz'

 L.2521       602  LOAD_STR                 'xz'

 L.2523       604  LOAD_STR                 'bz2'

 L.2524       606  LOAD_STR                 'bz2'

 L.2525       608  LOAD_STR                 'bz2'

 L.2526       610  LOAD_STR                 'bz2'
              612  LOAD_CONST               ('.gz', '.tgz', '.xz', '.txz', '.bz2', '.tbz', '.tbz2', '.tb2')
              614  BUILD_CONST_KEY_MAP_8     8 
              616  STORE_FAST               'compressions'

 L.2528       618  LOAD_FAST                'ext'
              620  LOAD_FAST                'compressions'
              622  COMPARE_OP               in
          624_626  POP_JUMP_IF_FALSE   640  'to 640'
              628  LOAD_STR                 'w:'
              630  LOAD_FAST                'compressions'
              632  LOAD_FAST                'ext'
              634  BINARY_SUBSCR    
              636  BINARY_ADD       
              638  JUMP_FORWARD        642  'to 642'
            640_0  COME_FROM           624  '624'
              640  LOAD_STR                 'w'
            642_0  COME_FROM           638  '638'
              642  STORE_FAST               'tar_mode'

 L.2529       644  LOAD_FAST                'args'
              646  LOAD_ATTR                create
              648  STORE_FAST               'tar_files'

 L.2531       650  LOAD_GLOBAL              TarFile
              652  LOAD_METHOD              open
              654  LOAD_FAST                'tar_name'
              656  LOAD_FAST                'tar_mode'
              658  CALL_METHOD_2         2  '2 positional arguments'
              660  SETUP_WITH          694  'to 694'
              662  STORE_FAST               'tf'

 L.2532       664  SETUP_LOOP          690  'to 690'
              666  LOAD_FAST                'tar_files'
              668  GET_ITER         
              670  FOR_ITER            688  'to 688'
              672  STORE_FAST               'file_name'

 L.2533       674  LOAD_FAST                'tf'
              676  LOAD_METHOD              add
              678  LOAD_FAST                'file_name'
              680  CALL_METHOD_1         1  '1 positional argument'
              682  POP_TOP          
          684_686  JUMP_BACK           670  'to 670'
              688  POP_BLOCK        
            690_0  COME_FROM_LOOP      664  '664'
              690  POP_BLOCK        
              692  LOAD_CONST               None
            694_0  COME_FROM_WITH      660  '660'
              694  WITH_CLEANUP_START
              696  WITH_CLEANUP_FINISH
              698  END_FINALLY      
            700_0  COME_FROM           324  '324'
            700_1  COME_FROM           234  '234'

 L.2535       700  LOAD_FAST                'args'
              702  LOAD_ATTR                verbose
          704_706  POP_JUMP_IF_FALSE   722  'to 722'

 L.2536       708  LOAD_GLOBAL              print
              710  LOAD_STR                 '{!r} file created.'
              712  LOAD_METHOD              format
              714  LOAD_FAST                'tar_name'
              716  CALL_METHOD_1         1  '1 positional argument'
              718  CALL_FUNCTION_1       1  '1 positional argument'
              720  POP_TOP          
            722_0  COME_FROM           704  '704'
            722_1  COME_FROM           564  '564'
            722_2  COME_FROM           554  '554'
            722_3  COME_FROM           344  '344'
            722_4  COME_FROM           254  '254'

Parse error at or near `COME_FROM' instruction at offset 722_3


if __name__ == '__main__':
    main()