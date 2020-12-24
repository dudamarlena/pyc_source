# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/asyncore_25.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 16791 bytes
"""Basic infrastructure for asynchronous socket service clients and servers.

There are only two ways to have a program on a single processor do "more
than one thing at a time".  Multi-threaded programming is the simplest and
most popular way to do it, but there is another very different technique,
that lets you have nearly all the advantages of multi-threading, without
actually using multiple threads. it's really only practical if your program
is largely I/O bound. If your program is CPU bound, then preemptive
scheduled threads are probably what you really need. Network servers are
rarely CPU-bound, however.

If your operating system supports the select() system call in its I/O
library (and nearly all do), then you can use it to juggle multiple
communication channels at once; doing other work while your I/O is taking
place in the "background."  Although this strategy can seem strange and
complex, especially at first, it is in many ways easier to understand and
control than multi-threaded programming. The module documented here solves
many of the difficult problems for you, making the task of building
sophisticated high-performance network servers and clients a snap.
"""
import select, socket, sys, time, os
from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, ECONNRESET, ENOTCONN, ESHUTDOWN, EINTR, EISCONN, errorcode
from supervisor.compat import as_string, as_bytes
try:
    socket_map
except NameError:
    socket_map = {}
else:

    class ExitNow(Exception):
        pass


    def read(obj):
        try:
            obj.handle_read_event()
        except ExitNow:
            raise
        except:
            obj.handle_error()


    def write(obj):
        try:
            obj.handle_write_event()
        except ExitNow:
            raise
        except:
            obj.handle_error()


    def _exception(obj):
        try:
            obj.handle_expt_event()
        except ExitNow:
            raise
        except:
            obj.handle_error()


    def readwrite(obj, flags):
        try:
            if flags & (select.POLLIN | select.POLLPRI):
                obj.handle_read_event()
            if flags & select.POLLOUT:
                obj.handle_write_event()
            if flags & (select.POLLERR | select.POLLHUP | select.POLLNVAL):
                obj.handle_expt_event()
        except ExitNow:
            raise
        except:
            obj.handle_error()


    def poll--- This code section failed: ---

 L. 106         0  LOAD_FAST                'map'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 107         8  LOAD_GLOBAL              socket_map
               10  STORE_FAST               'map'
             12_0  COME_FROM             6  '6'

 L. 108        12  LOAD_FAST                'map'
            14_16  POP_JUMP_IF_FALSE   376  'to 376'

 L. 109        18  BUILD_LIST_0          0 
               20  STORE_FAST               'r'

 L. 109        22  BUILD_LIST_0          0 
               24  STORE_FAST               'w'

 L. 109        26  BUILD_LIST_0          0 
               28  STORE_FAST               'e'

 L. 110        30  LOAD_FAST                'map'
               32  LOAD_METHOD              items
               34  CALL_METHOD_0         0  ''
               36  GET_ITER         
             38_0  COME_FROM            96  '96'
               38  FOR_ITER            110  'to 110'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'fd'
               44  STORE_FAST               'obj'

 L. 111        46  LOAD_FAST                'obj'
               48  LOAD_METHOD              readable
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'is_r'

 L. 112        54  LOAD_FAST                'obj'
               56  LOAD_METHOD              writable
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'is_w'

 L. 113        62  LOAD_FAST                'is_r'
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L. 114        66  LOAD_FAST                'r'
               68  LOAD_METHOD              append
               70  LOAD_FAST                'fd'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
             76_0  COME_FROM            64  '64'

 L. 115        76  LOAD_FAST                'is_w'
               78  POP_JUMP_IF_FALSE    90  'to 90'

 L. 116        80  LOAD_FAST                'w'
               82  LOAD_METHOD              append
               84  LOAD_FAST                'fd'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
             90_0  COME_FROM            78  '78'

 L. 117        90  LOAD_FAST                'is_r'
               92  POP_JUMP_IF_TRUE     98  'to 98'
               94  LOAD_FAST                'is_w'
               96  POP_JUMP_IF_FALSE    38  'to 38'
             98_0  COME_FROM            92  '92'

 L. 118        98  LOAD_FAST                'e'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'fd'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  JUMP_BACK            38  'to 38'

 L. 119       110  BUILD_LIST_0          0 
              112  LOAD_FAST                'r'
              114  DUP_TOP          
              116  ROT_THREE        
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   140  'to 140'
              122  LOAD_FAST                'w'
              124  DUP_TOP          
              126  ROT_THREE        
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   140  'to 140'
              132  LOAD_FAST                'e'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   156  'to 156'
              138  JUMP_FORWARD        144  'to 144'
            140_0  COME_FROM           130  '130'
            140_1  COME_FROM           120  '120'
              140  POP_TOP          
              142  JUMP_FORWARD        156  'to 156'
            144_0  COME_FROM           138  '138'

 L. 120       144  LOAD_GLOBAL              time
              146  LOAD_METHOD              sleep
              148  LOAD_FAST                'timeout'
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
              154  JUMP_FORWARD        248  'to 248'
            156_0  COME_FROM           142  '142'
            156_1  COME_FROM           136  '136'

 L. 122       156  SETUP_FINALLY       184  'to 184'

 L. 123       158  LOAD_GLOBAL              select
              160  LOAD_METHOD              select
              162  LOAD_FAST                'r'
              164  LOAD_FAST                'w'
              166  LOAD_FAST                'e'
              168  LOAD_FAST                'timeout'
              170  CALL_METHOD_4         4  ''
              172  UNPACK_SEQUENCE_3     3 
              174  STORE_FAST               'r'
              176  STORE_FAST               'w'
              178  STORE_FAST               'e'
              180  POP_BLOCK        
              182  JUMP_FORWARD        248  'to 248'
            184_0  COME_FROM_FINALLY   156  '156'

 L. 124       184  DUP_TOP          
              186  LOAD_GLOBAL              select
              188  LOAD_ATTR                error
              190  COMPARE_OP               exception-match
              192  POP_JUMP_IF_FALSE   246  'to 246'
              194  POP_TOP          
              196  STORE_FAST               'err'
              198  POP_TOP          
              200  SETUP_FINALLY       234  'to 234'

 L. 125       202  LOAD_FAST                'err'
              204  LOAD_ATTR                args
              206  LOAD_CONST               0
              208  BINARY_SUBSCR    
              210  LOAD_GLOBAL              EINTR
              212  COMPARE_OP               !=
              214  POP_JUMP_IF_FALSE   220  'to 220'

 L. 126       216  RAISE_VARARGS_0       0  'reraise'
              218  JUMP_FORWARD        230  'to 230'
            220_0  COME_FROM           214  '214'

 L. 128       220  POP_BLOCK        
              222  POP_EXCEPT       
              224  CALL_FINALLY        234  'to 234'
              226  LOAD_CONST               None
              228  RETURN_VALUE     
            230_0  COME_FROM           218  '218'
              230  POP_BLOCK        
              232  BEGIN_FINALLY    
            234_0  COME_FROM           224  '224'
            234_1  COME_FROM_FINALLY   200  '200'
              234  LOAD_CONST               None
              236  STORE_FAST               'err'
              238  DELETE_FAST              'err'
              240  END_FINALLY      
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           192  '192'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           182  '182'
            248_2  COME_FROM           154  '154'

 L. 130       248  LOAD_FAST                'r'
              250  GET_ITER         
              252  FOR_ITER            288  'to 288'
              254  STORE_FAST               'fd'

 L. 131       256  LOAD_FAST                'map'
              258  LOAD_METHOD              get
              260  LOAD_FAST                'fd'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'obj'

 L. 132       266  LOAD_FAST                'obj'
              268  LOAD_CONST               None
              270  COMPARE_OP               is
          272_274  POP_JUMP_IF_FALSE   278  'to 278'

 L. 133       276  JUMP_BACK           252  'to 252'
            278_0  COME_FROM           272  '272'

 L. 134       278  LOAD_GLOBAL              read
              280  LOAD_FAST                'obj'
              282  CALL_FUNCTION_1       1  ''
              284  POP_TOP          
              286  JUMP_BACK           252  'to 252'

 L. 136       288  LOAD_FAST                'w'
              290  GET_ITER         
              292  FOR_ITER            332  'to 332'
              294  STORE_FAST               'fd'

 L. 137       296  LOAD_FAST                'map'
              298  LOAD_METHOD              get
              300  LOAD_FAST                'fd'
              302  CALL_METHOD_1         1  ''
              304  STORE_FAST               'obj'

 L. 138       306  LOAD_FAST                'obj'
              308  LOAD_CONST               None
              310  COMPARE_OP               is
          312_314  POP_JUMP_IF_FALSE   320  'to 320'

 L. 139   316_318  JUMP_BACK           292  'to 292'
            320_0  COME_FROM           312  '312'

 L. 140       320  LOAD_GLOBAL              write
              322  LOAD_FAST                'obj'
              324  CALL_FUNCTION_1       1  ''
              326  POP_TOP          
          328_330  JUMP_BACK           292  'to 292'

 L. 142       332  LOAD_FAST                'e'
              334  GET_ITER         
              336  FOR_ITER            376  'to 376'
              338  STORE_FAST               'fd'

 L. 143       340  LOAD_FAST                'map'
              342  LOAD_METHOD              get
              344  LOAD_FAST                'fd'
              346  CALL_METHOD_1         1  ''
              348  STORE_FAST               'obj'

 L. 144       350  LOAD_FAST                'obj'
              352  LOAD_CONST               None
              354  COMPARE_OP               is
          356_358  POP_JUMP_IF_FALSE   364  'to 364'

 L. 145   360_362  JUMP_BACK           336  'to 336'
            364_0  COME_FROM           356  '356'

 L. 146       364  LOAD_GLOBAL              _exception
              366  LOAD_FAST                'obj'
              368  CALL_FUNCTION_1       1  ''
              370  POP_TOP          
          372_374  JUMP_BACK           336  'to 336'
            376_0  COME_FROM            14  '14'

Parse error at or near `POP_EXCEPT' instruction at offset 222


    def poll2(timeout=0.0, map=None):
        if map is None:
            map = socket_map
        else:
            if timeout is not None:
                timeout = int(timeout * 1000)
            pollster = select.poll()
            if map:
                for fd, obj in map.items():
                    flags = 0
                    if obj.readable():
                        flags |= select.POLLIN | select.POLLPRI
                    if obj.writable():
                        flags |= select.POLLOUT
                    if flags:
                        flags |= select.POLLERR | select.POLLHUP | select.POLLNVAL
                        pollster.register(fd, flags)
                else:
                    try:
                        r = pollster.polltimeout
                    except select.error as err:
                        try:
                            if err.args[0] != EINTR:
                                raise
                            r = []
                        finally:
                            err = None
                            del err

                    else:
                        for fd, flags in r:
                            obj = map.getfd
                            if obj is None:
                                pass
                            else:
                                readwrite(obj, flags)


    poll3 = poll2

    def loop(timeout=30.0, use_poll=False, map=None, count=None):
        if map is None:
            map = socket_map
        else:
            if use_poll and hasattr(select, 'poll'):
                poll_fun = poll2
            else:
                poll_fun = poll
            if count is None:
                while True:
                    if map:
                        poll_fun(timeout, map)

            else:
                while map:
                    if count > 0:
                        poll_fun(timeout, map)
                        count -= 1


    class dispatcher:
        debug = False
        connected = False
        accepting = False
        closing = False
        addr = None

        def __init__(self, sock=None, map=None):
            if map is None:
                self._map = socket_map
            else:
                self._map = map
            if sock:
                self.set_socket(sock, map)
                self.socket.setblocking0
                self.connected = True
                try:
                    self.addr = sock.getpeername()
                except socket.error:
                    pass

            else:
                self.socket = None

        def __repr__(self):
            status = [self.__class__.__module__ + '.' + self.__class__.__name__]
            if self.accepting and self.addr:
                status.append'listening'
            else:
                if self.connected:
                    status.append'connected'
                elif self.addr is not None:
                    try:
                        status.append('%s:%d' % self.addr)
                    except TypeError:
                        status.appendrepr(self.addr)

                return '<%s at %#x>' % (' '.joinstatus, id(self))

        def add_channel(self, map=None):
            if map is None:
                map = self._map
            map[self._fileno] = self

        def del_channel(self, map=None):
            fd = self._fileno
            if map is None:
                map = self._map
            if fd in map:
                del map[fd]
            self._fileno = None

        def create_socket(self, family, type):
            self.family_and_type = (
             family, type)
            self.socket = socket.socket(family, type)
            self.socket.setblocking0
            self._fileno = self.socket.fileno()
            self.add_channel()

        def set_socket(self, sock, map=None):
            self.socket = sock
            self._fileno = sock.fileno()
            self.add_channelmap

        def set_reuse_addr(self):
            try:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1)
            except socket.error:
                pass

        def readable(self):
            return True

        def writable(self):
            return True

        def listen(self, num):
            self.accepting = True
            if os.name == 'nt':
                if num > 5:
                    num = 1
            return self.socket.listennum

        def bind(self, addr):
            self.addr = addr
            return self.socket.bindaddr

        def connect(self, address):
            self.connected = False
            err = self.socket.connect_exaddress
            if err in (EINPROGRESS, EALREADY, EWOULDBLOCK):
                return
            elif err in (0, EISCONN):
                self.addr = address
                self.connected = True
                self.handle_connect()
            else:
                raise socket.error(err, errorcode[err])

        def accept(self):
            try:
                conn, addr = self.socket.accept()
                return (conn, addr)
                    except socket.error as why:
                try:
                    if why.args[0] == EWOULDBLOCK:
                        pass
                    else:
                        raise
                finally:
                    why = None
                    del why

        def send--- This code section failed: ---

 L. 332         0  SETUP_FINALLY        20  'to 20'

 L. 333         2  LOAD_FAST                'self'
                4  LOAD_ATTR                socket
                6  LOAD_METHOD              send
                8  LOAD_FAST                'data'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'result'

 L. 334        14  LOAD_FAST                'result'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 335        20  DUP_TOP          
               22  LOAD_GLOBAL              socket
               24  LOAD_ATTR                error
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    80  'to 80'
               30  POP_TOP          
               32  STORE_FAST               'why'
               34  POP_TOP          
               36  SETUP_FINALLY        68  'to 68'

 L. 336        38  LOAD_FAST                'why'
               40  LOAD_ATTR                args
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  LOAD_GLOBAL              EWOULDBLOCK
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 337        52  POP_BLOCK        
               54  POP_EXCEPT       
               56  CALL_FINALLY         68  'to 68'
               58  LOAD_CONST               0
               60  RETURN_VALUE     
             62_0  COME_FROM            50  '50'

 L. 339        62  RAISE_VARARGS_0       0  'reraise'
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM            56  '56'
             68_1  COME_FROM_FINALLY    36  '36'
               68  LOAD_CONST               None
               70  STORE_FAST               'why'
               72  DELETE_FAST              'why'
               74  END_FINALLY      
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            28  '28'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'

Parse error at or near `POP_EXCEPT' instruction at offset 54

        def recv--- This code section failed: ---

 L. 342         0  SETUP_FINALLY        42  'to 42'

 L. 343         2  LOAD_FAST                'self'
                4  LOAD_ATTR                socket
                6  LOAD_METHOD              recv
                8  LOAD_FAST                'buffer_size'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'data'

 L. 344        14  LOAD_FAST                'data'
               16  POP_JUMP_IF_TRUE     32  'to 32'

 L. 347        18  LOAD_FAST                'self'
               20  LOAD_METHOD              handle_close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          

 L. 348        26  POP_BLOCK        
               28  LOAD_CONST               b''
               30  RETURN_VALUE     
             32_0  COME_FROM            16  '16'

 L. 350        32  LOAD_FAST                'data'
               34  POP_BLOCK        
               36  RETURN_VALUE     
               38  POP_BLOCK        
               40  JUMP_FORWARD        118  'to 118'
             42_0  COME_FROM_FINALLY     0  '0'

 L. 351        42  DUP_TOP          
               44  LOAD_GLOBAL              socket
               46  LOAD_ATTR                error
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE   116  'to 116'
               52  POP_TOP          
               54  STORE_FAST               'why'
               56  POP_TOP          
               58  SETUP_FINALLY       104  'to 104'

 L. 353        60  LOAD_FAST                'why'
               62  LOAD_ATTR                args
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  LOAD_GLOBAL              ECONNRESET
               70  LOAD_GLOBAL              ENOTCONN
               72  LOAD_GLOBAL              ESHUTDOWN
               74  BUILD_TUPLE_3         3 
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE    98  'to 98'

 L. 354        80  LOAD_FAST                'self'
               82  LOAD_METHOD              handle_close
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          

 L. 355        88  POP_BLOCK        
               90  POP_EXCEPT       
               92  CALL_FINALLY        104  'to 104'
               94  LOAD_STR                 ''
               96  RETURN_VALUE     
             98_0  COME_FROM            78  '78'

 L. 357        98  RAISE_VARARGS_0       0  'reraise'
              100  POP_BLOCK        
              102  BEGIN_FINALLY    
            104_0  COME_FROM            92  '92'
            104_1  COME_FROM_FINALLY    58  '58'
              104  LOAD_CONST               None
              106  STORE_FAST               'why'
              108  DELETE_FAST              'why'
              110  END_FINALLY      
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            50  '50'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            40  '40'

Parse error at or near `RETURN_VALUE' instruction at offset 30

        def close(self):
            self.del_channel()
            self.socket.close()

        def __getattr__(self, attr):
            return getattr(self.socket, attr)

        def log(self, message):
            sys.stderr.write('log: %s\n' % str(message))

        def log_info(self, message, type='info'):
            if True or type != 'info':
                print('%s: %s' % (type, message))

        def handle_read_event(self):
            if self.accepting:
                if not self.connected:
                    self.connected = True
                self.handle_accept()
            else:
                if not self.connected:
                    self.handle_connect()
                    self.connected = True
                    self.handle_read()
                else:
                    self.handle_read()

        def handle_write_event(self):
            if not self.connected:
                self.handle_connect()
                self.connected = True
            self.handle_write()

        def handle_expt_event(self):
            self.handle_expt()

        def handle_error(self):
            nil, t, v, tbinfo = compact_traceback()
            try:
                self_repr = repr(self)
            except:
                self_repr = '<__repr__(self) failed for object at %0x>' % id(self)
            else:
                self.log_info('uncaptured python exception, closing channel %s (%s:%s %s)' % (
                 self_repr,
                 t,
                 v,
                 tbinfo), 'error')
                self.close()

        def handle_expt(self):
            self.log_info('unhandled exception', 'warning')

        def handle_read(self):
            self.log_info('unhandled read event', 'warning')

        def handle_write(self):
            self.log_info('unhandled write event', 'warning')

        def handle_connect(self):
            self.log_info('unhandled connect event', 'warning')

        def handle_accept(self):
            self.log_info('unhandled accept event', 'warning')

        def handle_close(self):
            self.log_info('unhandled close event', 'warning')
            self.close()


    class dispatcher_with_send(dispatcher):

        def __init__(self, sock=None, map=None):
            dispatcher.__init__(self, sock, map)
            self.out_buffer = b''

        def initiate_send(self):
            num_sent = dispatcher.send(self, self.out_buffer[:512])
            self.out_buffer = self.out_buffer[num_sent:]

        def handle_write(self):
            self.initiate_send()

        def writable(self):
            return not self.connected or len(self.out_buffer)

        def send(self, data):
            if self.debug:
                self.log_info('sending %s' % repr(data))
            self.out_buffer = self.out_buffer + data
            self.initiate_send()


    def compact_traceback():
        t, v, tb = sys.exc_info()
        tbinfo = []
        if not tb:
            raise AssertionError
        else:
            while True:
                if tb:
                    tbinfo.append(
                     tb.tb_frame.f_code.co_filename,
                     tb.tb_frame.f_code.co_name,
                     str(tb.tb_lineno))
                    tb = tb.tb_next

        del tb
        file, function, line = tbinfo[(-1)]
        info = ' '.join['[%s|%s|%s]' % x for x in tbinfo]
        return ((file, function, line), t, v, info)


    def close_all(map=None):
        if map is None:
            map = socket_map
        for x in map.values():
            x.socket.close()
        else:
            map.clear()


    if os.name == 'posix':
        import fcntl

        class file_wrapper:

            def __init__(self, fd):
                self.fd = fd

            def recv(self, buffersize):
                return as_string(os.read(self.fd, buffersize))

            def send(self, s):
                return os.write(self.fd, as_bytes(s))

            read = recv
            write = send

            def close(self):
                os.closeself.fd

            def fileno(self):
                return self.fd


        class file_dispatcher(dispatcher):

            def __init__(self, fd, map=None):
                dispatcher.__init__(self, None, map)
                self.connected = True
                self.set_filefd
                flags = fcntl.fcntl(fd, fcntl.F_GETFL, 0)
                flags |= os.O_NONBLOCK
                fcntl.fcntl(fd, fcntl.F_SETFL, flags)

            def set_file(self, fd):
                self._fileno = fd
                self.socket = file_wrapper(fd)
                self.add_channel()