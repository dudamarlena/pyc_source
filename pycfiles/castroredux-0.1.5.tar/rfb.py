# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/pyvnc2swf/rfb.py
# Compiled at: 2011-03-28 15:09:52
import sys, time, socket
from struct import pack, unpack
from d3des import decrypt_passwd, generate_response
from image import IMG_SOLID, IMG_RAW
from .. import messageboard as mb
stderr = sys.stderr
lowerbound = max

def byte2bit(s):
    return ('').join([ chr(ord(s[(i >> 3)]) >> (7 - i & 7) & 1) for i in xrange(len(s) * 8) ])


class RFBError(Exception):
    pass


class RFBAuthError(RFBError):
    pass


class RFBProtocolError(RFBError):
    pass


class RFBFrameBuffer():

    def init_screen(self, width, height, name):
        raise NotImplementedError

    def set_converter(self, convert_pixels, convert_color1):
        self.convert_pixels = convert_pixels
        self.convert_color1 = convert_color1

    def process_pixels(self, x, y, width, height, data):
        raise NotImplementedError

    def process_solid(self, x, y, width, height, data):
        raise NotImplementedError

    def update_screen(self, t):
        raise NotImplementedError

    def change_cursor(self, width, height, data):
        raise NotImplementedError

    def move_cursor(self, x, y):
        raise NotImplementedError

    def close(self):
        pass


class RFBProxy():
    """Abstract class of RFB clients."""

    def __init__(self, fb=None, pwdfile=None, preferred_encoding=(5, 0), debug=0):
        self.fb = fb
        self.debug = debug
        self.pwdfile = pwdfile
        self.pwdcache = None
        self.preferred_encoding = preferred_encoding
        return

    FASTEST_FORMAT = (32, 8, 1, 1, 255, 255, 255, 24, 16, 8)

    def preferred_format(self, bitsperpixel, depth, bigendian, truecolour, red_max, green_max, blue_max, red_shift, green_shift, blue_shift):
        if self.fb:
            self.fb.set_converter(lambda data: data, lambda data: unpack('BBBx', data))
        return self.FASTEST_FORMAT

    def send(self, s):
        """Send data s to the server."""
        raise NotImplementedError

    def recv(self, n):
        """Receive n-bytes data from the server."""
        raise NotImplementedError

    def recv_relay(self, n):
        """Same as recv() except the received data is also passed to self.relay.recv_framedata."""
        return self.recv(n)

    def recv_byte_with_timeout(self):
        return self.recv_relay(1)

    def write(self, n):
        pass

    def request_update(self):
        """Send a request to the server."""
        raise NotImplementedError

    def finish_update(self):
        if self.fb:
            self.fb.update_screen(time.time())

    def init(self):
        server_version = self.recv(12)
        self.protocol_version = 3
        if server_version.startswith('RFB 003.007'):
            self.protocol_version = 7
        elif server_version.startswith('RFB 003.008'):
            self.protocol_version = 8
        self.send('RFB 003.%03d\n' % self.protocol_version)
        if self.debug:
            print >> stderr, 'protocol_version: 3.%d' % self.protocol_version
        return self

    def getpass(self):
        raise NotImplementedError

    def auth(self):

        def crauth():
            if self.pwdcache:
                p = self.pwdcache
            elif self.pwdfile:
                fp = file(self.pwdfile)
                s = fp.read()
                fp.close()
                p = decrypt_passwd(s)
            elif not self.pwdcache:
                p = self.getpass()
            if not p:
                raise RFBError('Auth cancelled')
            challange = self.recv(16)
            if self.debug:
                print >> stderr, 'challange: %r' % challange
            response = generate_response(p, challange)
            if self.debug:
                print >> stderr, 'response: %r' % response
            self.send(response)
            (result,) = unpack('>L', self.recv(4))
            return (
             p, result)

        (p, server_result) = (None, 0)
        if self.protocol_version == 3:
            (server_security,) = unpack('>L', self.recv(4))
            if self.debug:
                print >> stderr, 'server_security: %r' % server_security
            if server_security == 0:
                (reason_length,) = unpack('>L', self.recv(4))
                reason = self.recv(reason_length)
                raise RFBAuthError('Auth Error: %s' % reason)
            elif server_security == 1:
                pass
            else:
                (p, server_result) = crauth()
        else:
            (nsecurities,) = unpack('>B', self.recv(1))
            server_securities = self.recv(nsecurities)
            if self.debug:
                print >> stderr, 'server_securities: %r' % server_securities
            if '\x01' in server_securities:
                self.send('\x01')
                if self.protocol_version == 8:
                    (server_result,) = unpack('>L', self.recv(4))
                else:
                    server_result = 0
            elif '\x02' in server_securities:
                self.send('\x02')
                (p, server_result) = crauth()
        if self.debug:
            print >> stderr, 'server_result: %r' % server_result
        if server_result != 0:
            if self.protocol_version != 3:
                (reason_length,) = unpack('>L', self.recv(4))
                reason = self.recv(reason_length)
            else:
                reason = server_result
            raise RFBAuthError('Auth Error: %s' % reason)
        self.pwdcache = p
        self.send('\x01')
        return self

    def start(self):
        server_init = self.recv(24)
        (width, height, pixelformat, namelen) = unpack('>HH16sL', server_init)
        self.name = self.recv(namelen)
        (bitsperpixel, depth, bigendian, truecolour, red_max, green_max, blue_max, red_shift, green_shift, blue_shift) = unpack('>BBBBHHHBBBxxx', pixelformat)
        if self.debug:
            print >> stderr, 'Server Encoding:'
            print >> stderr, ' width=%d, height=%d, name=%r' % (width, height, self.name)
            print >> stderr, ' pixelformat=', (bitsperpixel, depth, bigendian, truecolour)
            print >> stderr, ' rgbmax=', (red_max, green_max, blue_max)
            print >> stderr, ' rgbshift=', (red_shift, green_shift, blue_shift)
        self.send('\x00\x00\x00\x00')
        (bitsperpixel, depth, bigendian, truecolour, red_max, green_max, blue_max, red_shift, green_shift, blue_shift) = self.preferred_format(bitsperpixel, depth, bigendian, truecolour, red_max, green_max, blue_max, red_shift, green_shift, blue_shift)
        self.bytesperpixel = bitsperpixel / 8
        pixelformat = pack('>BBBBHHHBBBxxx', bitsperpixel, depth, bigendian, truecolour, red_max, green_max, blue_max, red_shift, green_shift, blue_shift)
        self.send(pixelformat)
        self.write(pack('>HH16sL', width, height, pixelformat, namelen))
        self.write(self.name)
        if self.fb:
            self.clipping = self.fb.init_screen(width, height, self.name)
        else:
            self.clipping = (
             0, 0, width, height)
        self.send('\x02\x00' + pack('>H', len(self.preferred_encoding)))
        for e in self.preferred_encoding:
            self.send(pack('>l', e))

        return self

    def loop1(self):
        self.request_update()
        c = self.recv_byte_with_timeout()
        if c == '':
            return False
        if c == None:
            pass
        else:
            if c == '\x00':
                (nrects,) = unpack('>xH', self.recv_relay(3))
                if self.debug:
                    print >> stderr, 'FrameBufferUpdate: nrects=%d' % nrects
                for rectindex in xrange(nrects):
                    (x0, y0, width, height, t) = unpack('>HHHHl', self.recv_relay(12))
                    if self.debug:
                        print >> stderr, ' %d: %d x %d at (%d,%d), type=%d' % (rectindex, width, height, x0, y0, t)
                    if t == 0:
                        l = width * height * self.bytesperpixel
                        data = self.recv_relay(l)
                        if self.debug:
                            print >> stderr, ' RawEncoding: len=%d, received=%d' % (l, len(data))
                        if self.fb:
                            self.fb.process_pixels(x0, y0, width, height, data)
                    elif t == 1:
                        raise RFBProtocolError('unsupported: CopyRectEncoding')
                    elif t == 2:
                        (nsubrects,) = unpack('>L', self.recv_relay(4))
                        bgcolor = self.recv_relay(self.bytesperpixel)
                        if self.debug:
                            print >> stderr, ' RREEncoding: subrects=%d, bgcolor=%r' % (nsubrects, bgcolor)
                        if self.fb:
                            self.fb.process_solid(x0, y0, width, height, bgcolor)
                        for i in xrange(nsubrects):
                            fgcolor = self.recv_relay(self.bytesperpixel)
                            (x, y, w, h) = unpack('>HHHH', self.recv_relay(8))
                            if self.fb:
                                self.fb.process_solid(x0 + x, y0 + y, w, h, fgcolor)
                            if 2 <= self.debug:
                                print >> stderr, ' RREEncoding: ', (x, y, w, h, fgcolor)

                    elif t == 4:
                        (nsubrects,) = unpack('>L', self.recv_relay(4))
                        bgcolor = self.recv_relay(self.bytesperpixel)
                        if self.debug:
                            print >> stderr, ' CoRREEncoding: subrects=%d, bgcolor=%r' % (nsubrects, bgcolor)
                        if self.fb:
                            self.fb.process_solid(x0, y0, width, height, bgcolor)
                        for i in xrange(nsubrects):
                            fgcolor = self.recv_relay(self.bytesperpixel)
                            (x, y, w, h) = unpack('>BBBB', self.recv_relay(4))
                            if self.fb:
                                self.fb.process_solid(x0 + x, y0 + y, w, h, fgcolor)
                            if 2 <= self.debug:
                                print >> stderr, ' CoRREEncoding: ', (x, y, w, h, fgcolor)

                    elif t == 5:
                        if self.debug:
                            print >> stderr, ' HextileEncoding'
                        (fgcolor, bgcolor) = (None, None)
                        for y in xrange(0, height, 16):
                            for x in xrange(0, width, 16):
                                w = min(width - x, 16)
                                h = min(height - y, 16)
                                c = ord(self.recv_relay(1))
                                assert c < 32
                                if c & 1:
                                    l = w * h * self.bytesperpixel
                                    data = self.recv_relay(l)
                                    if self.fb:
                                        self.fb.process_pixels(x0 + x, y0 + y, w, h, data)
                                    if 2 <= self.debug:
                                        print >> stderr, '  Raw:', l
                                    continue
                                if c & 2:
                                    bgcolor = self.recv_relay(self.bytesperpixel)
                                if c & 4:
                                    fgcolor = self.recv_relay(self.bytesperpixel)
                                if self.fb:
                                    self.fb.process_solid(x0 + x, y0 + y, w, h, bgcolor)
                                if not c & 8:
                                    if 2 <= self.debug:
                                        print >> stderr, '  Solid:', repr(bgcolor)
                                    continue
                                nsubrects = ord(self.recv_relay(1))
                                if c & 16:
                                    if 2 <= self.debug:
                                        print >> stderr, '  SubrectsColoured:', nsubrects, repr(bgcolor)
                                    for i in xrange(nsubrects):
                                        color = self.recv_relay(self.bytesperpixel)
                                        (xy, wh) = unpack('>BB', self.recv_relay(2))
                                        if self.fb:
                                            self.fb.process_solid(x0 + x + (xy >> 4), y0 + y + (xy & 15), (wh >> 4) + 1, (wh & 15) + 1, color)
                                        if 3 <= self.debug:
                                            print >> stderr, '   ', repr(color), (xy, wh)

                                else:
                                    if 2 <= self.debug:
                                        print >> stderr, '  NoSubrectsColoured:', nsubrects, repr(bgcolor)
                                    for i in xrange(nsubrects):
                                        (xy, wh) = unpack('>BB', self.recv_relay(2))
                                        if self.fb:
                                            self.fb.process_solid(x0 + x + (xy >> 4), y0 + y + (xy & 15), (wh >> 4) + 1, (wh & 15) + 1, fgcolor)
                                        if 3 <= self.debug:
                                            print >> stderr, '  ', (xy, wh)

                    elif t == 16:
                        raise RFBProtocolError('unsupported: ZRLEEncoding')
                    elif t == -239:
                        if width and height:
                            rowbytes = (width + 7) / 8
                            data = self.recv_relay(width * height * self.bytesperpixel)
                            mask = self.recv_relay(rowbytes * height)
                            if self.debug:
                                print >> stderr, 'RichCursor: %dx%d at %d,%d' % (width, height, x0, y0)
                            if self.fb:
                                data = self.fb.convert_pixels(data)
                                mask = ('').join([ byte2bit(mask[p:p + rowbytes])[:width] for p in xrange(0, height * rowbytes, rowbytes)
                                                 ])

                                def conv1(i):
                                    if mask[(i / 4)] == '\x01':
                                        return b'\xff' + data[i] + data[(i + 1)] + data[(i + 2)]
                                    else:
                                        return '\x00\x00\x00\x00'

                                data = ('').join([ conv1(i) for i in xrange(0, len(data), 4) ])
                                self.fb.change_cursor(width, height, x0, y0, data)
                    elif t == -240:
                        if width and height:
                            rowbytes = (width + 7) / 8
                            fgcolor = self.recv_relay(3)
                            bgcolor = self.recv_relay(3)
                            data = self.recv_relay(rowbytes * height)
                            mask = self.recv_relay(rowbytes * height)
                            if self.debug:
                                print >> stderr, 'XCursor: %dx%d at %d,%d' % (width, height, x0, y0)
                            if self.fb:
                                data = ('').join([ byte2bit(data[p:p + rowbytes])[:width] for p in xrange(0, height * rowbytes, rowbytes)
                                                 ])
                                mask = ('').join([ byte2bit(mask[p:p + rowbytes])[:width] for p in xrange(0, height * rowbytes, rowbytes)
                                                 ])

                                def conv1(i):
                                    if mask[i] == '\x01':
                                        if data[i] == '\x01':
                                            return b'\xff' + fgcolor
                                        else:
                                            return b'\xff' + bgcolor
                                    else:
                                        return '\x00\x00\x00\x00'

                                data = ('').join([ conv1(i) for i in xrange(len(data)) ])
                                self.fb.change_cursor(width, height, x0, y0, data)
                    elif t == -232:
                        if self.debug:
                            print >> stderr, 'CursorPos: %d,%d' % (x0, y0)
                        if self.fb:
                            self.fb.move_cursor(x0, y0)
                    else:
                        raise RFBProtocolError('Illegal encoding: 0x%02x' % t)

                self.finish_update()
            elif c == '\x01':
                (first, ncolours) = unpack('>xHH', self.recv_relay(11))
                if self.debug:
                    print >> stderr, 'SetColourMapEntries: first=%d, ncolours=%d' % (first, ncolours)
                for i in ncolours:
                    self.recv_relay(6)

            elif c == '\x02':
                if self.debug:
                    print >> stderr, 'Bell'
            elif c == '\x03':
                (length,) = unpack('>3xL', self.recv_relay(7))
                data = self.recv_relay(length)
                if self.debug:
                    print >> stderr, 'ServerCutText: %r' % data
            else:
                raise RFBProtocolError('Unsupported msg: %d' % ord(c))
            return True

    def set_loop(self):
        mb.recording_should_continue.write(True)
        self.do_another_loop = True

    def get_loop(self):
        self.do_another_loop = mb.recording_should_continue.read()
        return self.do_another_loop

    def loop(self):
        self.set_loop()
        while self.do_another_loop == True:
            if not self.loop1():
                break
            self.get_loop()

        self.finish_update()
        return self

    def close(self):
        if self.fb:
            self.fb.close()


class RFBNetworkClient(RFBProxy):

    def __init__(self, host, port, fb=None, pwdfile=None, preferred_encoding=(0, 5), debug=0):
        RFBProxy.__init__(self, fb=fb, pwdfile=pwdfile, preferred_encoding=preferred_encoding, debug=debug)
        self.host = host
        self.port = port

    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        x = RFBProxy.init(self)
        print >> stderr, 'Connected: %s:%d, protocol_version=3.%d, preferred_encoding=%s' % (
         self.host, self.port, self.protocol_version, self.preferred_encoding)
        return x

    def recv(self, n):
        buf = ''
        n0 = n
        while n:
            x = self.sock.recv(n)
            if not x:
                raise RFBProtocolError('Connection closed unexpectedly.')
            buf += x
            n -= len(x)

        return buf

    def recv_byte_with_timeout(self):
        self.sock.settimeout(0.05)
        try:
            c = self.recv_relay(1)
        except socket.timeout:
            c = None

        self.sock.settimeout(None)
        return c

    def send(self, s):
        return self.sock.send(s)

    def getpass(self):
        import getpass
        return getpass.getpass('Password for %s:%d: ' % (self.host, self.port))

    def request_update(self):
        if self.debug:
            print >> stderr, 'FrameBufferUpdateRequest'
        self.send('\x03\x01' + pack('>HHHH', *self.clipping))

    def close(self):
        RFBProxy.close(self)
        self.sock.close()


class RFBNetworkClientForRecording(RFBNetworkClient):

    def __init__(self, host, port, fp, pwdfile=None, preferred_encoding=(5, 0), debug=0):
        RFBNetworkClient.__init__(self, host, port, fb=None, pwdfile=pwdfile, preferred_encoding=preferred_encoding, debug=debug)
        print >> stderr, 'Creating vncrec: %r: vncLog0.0' % fp
        self.fp = fp
        self.write('vncLog0.0')
        self.write('RFB 003.003\n')
        self.write('\x00\x00\x00\x01')
        self.updated = True
        return

    def write(self, x):
        self.fp.write(x)

    def request_update(self):
        if self.updated:
            self.updated = False
            t = time.time()
            self.write(pack('>LL', int(t), int((t - int(t)) * 1000000)))
            RFBNetworkClient.request_update(self)

    def finish_update(self):
        self.updated = True

    def recv_relay(self, n):
        data = self.recv(n)
        self.write(data)
        return data


class RFBFileParser(RFBProxy):

    def __init__(self, fp, fb=None, debug=0):
        RFBProxy.__init__(self, fb=fb, debug=debug)
        if self.fb:
            self.fb.change_format = False
        self.fp = fp

    def preferred_format(self, bitsperpixel, depth, bigendian, truecolour, red_max, green_max, blue_max, red_shift, green_shift, blue_shift):
        if (
         bitsperpixel, depth, bigendian, truecolour,
         red_max, green_max, blue_max,
         red_shift, green_shift, blue_shift) == self.FASTEST_FORMAT:
            return RFBProxy.preferred_format(self, bitsperpixel, depth, bigendian, truecolour, red_max, green_max, blue_max, red_shift, green_shift, blue_shift)
        if self.fb:
            if bigendian:
                endian = '>'
            else:
                endian = '<'
            try:
                length = {8: 'B', 16: 'H', 32: 'L'}[bitsperpixel]
            except KeyError:
                raise 'invalid bitsperpixel: %d' % bitsperpixel
            else:
                unpackstr = endian + length
                nbytes = bitsperpixel / 8
                bits = {1: 1, 3: 2, 7: 3, 15: 4, 31: 5, 63: 6, 127: 7, 255: 8}
                try:
                    e = 'lambda p: (((p>>%d)&%d)<<%d, ((p>>%d)&%d)<<%d, ((p>>%d)&%d)<<%d)' % (
                     red_shift, red_max, 8 - bits[red_max],
                     green_shift, green_max, 8 - bits[green_max],
                     blue_shift, blue_max, 8 - bits[blue_max])
                except KeyError:
                    raise 'invalid {red,green,blue}_max: %d, %d or %d' % (red_max, green_max, blue_max)
                else:
                    getrgb = eval(e)
                    unpack_pixels = eval('lambda data: unpack("%s%%d%s" %% (len(data)/%d), data)' % (endian, length, nbytes))
                    unpack_color1 = eval('lambda data: unpack("%s", data)' % unpackstr)
                    self.fb.set_converter(lambda data: ('').join([ pack('>BBB', *getrgb(p)) for p in unpack_pixels(data) ]), lambda data: getrgb(unpack_color1(data)[0]))
        return (
         bitsperpixel, depth, bigendian, truecolour,
         red_max, green_max, blue_max,
         red_shift, green_shift, blue_shift)

    def seek(self, pos):
        self.fp.seek(pos)

    def tell(self):
        return self.fp.tell()

    def init(self):
        self.curtime = 0
        version = self.fp.read(9)
        print >> stderr, 'Reading vncrec file: %s, version=%r...' % (self.fp, version)
        if version != 'vncLog0.0':
            raise RFBProtocolError('Unsupported vncrec version: %r' % version)
        return RFBProxy.init(self)

    def recv(self, n):
        x = self.fp.read(n)
        if len(x) != n:
            raise EOFError
        return x

    def send(self, s):
        pass

    def auth(self):
        if self.protocol_version == 3 or True:
            (server_security,) = unpack('>L', self.recv(4))
            if self.debug:
                print >> stderr, 'server_security: %r' % server_security
            if server_security == 2:
                self.recv(20)
        else:
            RFBProxy.auth(self)
        return self

    def request_update(self):
        (sec, usec) = unpack('>LL', self.recv(8))
        self.curtime = sec + usec / 1000000.0

    def finish_update(self):
        if self.fb:
            self.fb.update_screen(self.curtime)

    def loop(self, endpos=0):
        try:
            while self.loop1():
                if endpos and endpos <= self.tell():
                    break

        except EOFError:
            self.finish_update()

        return self

    def close(self):
        RFBProxy.close(self)
        self.fp.close()


class RFBConverter(RFBFrameBuffer):

    def __init__(self, info, debug=0):
        self.debug = debug
        self.info = info

    def init_screen(self, width, height, name):
        print >> stderr, 'VNC Screen: size=%dx%d, name=%r' % (width, height, name)
        self.info.set_defaults(width, height)
        self.images = []
        self.cursor_image = None
        self.cursor_pos = None
        self.t0 = 0
        return self.info.clipping

    def process_pixels(self, x, y, width, height, data):
        self.images.append(((x, y), (width, height, (IMG_RAW, self.convert_pixels(data)))))

    def process_solid(self, x, y, width, height, data):
        self.images.append(((x, y), (width, height, (IMG_SOLID, self.convert_color1(data)))))

    def move_cursor(self, x, y):
        self.cursor_pos = (
         x, y)

    def change_cursor(self, width, height, dx, dy, data):
        if width and height:
            self.cursor_image = (
             width, height, dx, dy, data)

    def calc_frames(self, t):
        if not self.t0:
            self.t0 = t
        return int((t - self.t0) * self.info.framerate) + 1


class RFBMovieConverter(RFBConverter):

    def __init__(self, movie, debug=0):
        RFBConverter.__init__(self, movie.info, debug)
        self.movie = movie
        self.frameinfo = []

    def process_pixels(self, x, y, width, height, data):
        if self.processing:
            RFBConverter.process_pixels(self, x, y, width, height, data)

    def process_solid(self, x, y, width, height, data):
        if self.processing:
            RFBConverter.process_solid(self, x, y, width, height, data)

    def update_screen(self, t):
        if not self.processing:
            frames = RFBConverter.calc_frames(self, t)
            done = False
            while len(self.frameinfo) < frames:
                if done:
                    self.frameinfo.append((self.beginpos, -1))
                else:
                    endpos = self.rfbparser.tell()
                    self.frameinfo.append((self.beginpos, endpos))
                    if self.debug:
                        print >> stderr, 'scan:', self.beginpos, endpos
                    self.beginpos = endpos
                    done = True

    def open(self, fname):
        self.processing = False
        fp = file(fname, 'rb')
        self.rfbparser = RFBFileParser(fp, self, self.debug)
        self.rfbparser.init().auth().start()
        self.beginpos = self.rfbparser.tell()
        self.rfbparser.loop()

    def parse_frame(self, i):
        (pos, endpos) = self.frameinfo[i]
        if self.debug:
            print >> stderr, 'seek:', i, pos, endpos
        self.rfbparser.seek(pos)
        self.images = []
        self.processing = True
        self.cursor_image = None
        self.cursor_pos = None
        self.rfbparser.loop(endpos)
        return (
         self.images, [], (self.cursor_image, self.cursor_pos))


class RFBStreamConverter(RFBConverter):

    def __init__(self, info, stream, debug=0):
        RFBConverter.__init__(self, info, debug)
        self.stream = stream
        self.stream_opened = False

    def init_screen(self, width, height, name):
        clipping = RFBConverter.init_screen(self, width, height, name)
        if not self.stream_opened:
            self.stream.open()
            self.stream_opened = True
        self.nframes = 0
        return clipping

    def update_screen(self, t):
        frames = RFBConverter.calc_frames(self, t)
        if self.nframes < frames:
            while self.nframes < frames - 1:
                self.stream.next_frame()
                self.nframes += 1

            self.stream.paint_frame((self.images, [], (self.cursor_image, self.cursor_pos)))
            self.images = []
            self.cursor_image = None
            self.cursor_pos = None
            self.stream.next_frame()
            self.nframes += 1
        return