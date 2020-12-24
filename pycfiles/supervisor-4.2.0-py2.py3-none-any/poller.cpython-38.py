# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/poller.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 6703 bytes
import select, errno

class BasePoller:

    def __init__(self, options):
        self.options = options
        self.initialize()

    def initialize(self):
        pass

    def register_readable(self, fd):
        raise NotImplementedError

    def register_writable(self, fd):
        raise NotImplementedError

    def unregister_readable(self, fd):
        raise NotImplementedError

    def unregister_writable(self, fd):
        raise NotImplementedError

    def poll(self, timeout):
        raise NotImplementedError

    def before_daemonize(self):
        pass

    def after_daemonize(self):
        pass

    def close(self):
        pass


class SelectPoller(BasePoller):

    def initialize(self):
        self._select = select
        self._init_fdsets()

    def register_readable(self, fd):
        self.readables.add(fd)

    def register_writable(self, fd):
        self.writables.add(fd)

    def unregister_readable(self, fd):
        self.readables.discard(fd)

    def unregister_writable(self, fd):
        self.writables.discard(fd)

    def unregister_all(self):
        self._init_fdsets()

    def poll--- This code section failed: ---

 L.  60         0  SETUP_FINALLY        34  'to 34'

 L.  61         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _select
                6  LOAD_METHOD              select

 L.  62         8  LOAD_FAST                'self'
               10  LOAD_ATTR                readables

 L.  63        12  LOAD_FAST                'self'
               14  LOAD_ATTR                writables

 L.  64        16  BUILD_LIST_0          0 

 L.  64        18  LOAD_FAST                'timeout'

 L.  61        20  CALL_METHOD_4         4  ''
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'r'
               26  STORE_FAST               'w'
               28  STORE_FAST               'x'
               30  POP_BLOCK        
               32  JUMP_FORWARD        172  'to 172'
             34_0  COME_FROM_FINALLY     0  '0'

 L.  66        34  DUP_TOP          
               36  LOAD_GLOBAL              select
               38  LOAD_ATTR                error
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE   170  'to 170'
               44  POP_TOP          
               46  STORE_FAST               'err'
               48  POP_TOP          
               50  SETUP_FINALLY       158  'to 158'

 L.  67        52  LOAD_FAST                'err'
               54  LOAD_ATTR                args
               56  LOAD_CONST               0
               58  BINARY_SUBSCR    
               60  LOAD_GLOBAL              errno
               62  LOAD_ATTR                EINTR
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    98  'to 98'

 L.  68        68  LOAD_FAST                'self'
               70  LOAD_ATTR                options
               72  LOAD_ATTR                logger
               74  LOAD_METHOD              blather
               76  LOAD_STR                 'EINTR encountered in poll'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L.  69        82  BUILD_LIST_0          0 
               84  BUILD_LIST_0          0 
               86  BUILD_TUPLE_2         2 
               88  ROT_FOUR         
               90  POP_BLOCK        
               92  POP_EXCEPT       
               94  CALL_FINALLY        158  'to 158'
               96  RETURN_VALUE     
             98_0  COME_FROM            66  '66'

 L.  70        98  LOAD_FAST                'err'
              100  LOAD_ATTR                args
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_GLOBAL              errno
              108  LOAD_ATTR                EBADF
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   152  'to 152'

 L.  71       114  LOAD_FAST                'self'
              116  LOAD_ATTR                options
              118  LOAD_ATTR                logger
              120  LOAD_METHOD              blather
              122  LOAD_STR                 'EBADF encountered in poll'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L.  72       128  LOAD_FAST                'self'
              130  LOAD_METHOD              unregister_all
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          

 L.  73       136  BUILD_LIST_0          0 
              138  BUILD_LIST_0          0 
              140  BUILD_TUPLE_2         2 
              142  ROT_FOUR         
              144  POP_BLOCK        
              146  POP_EXCEPT       
              148  CALL_FINALLY        158  'to 158'
              150  RETURN_VALUE     
            152_0  COME_FROM           112  '112'

 L.  74       152  RAISE_VARARGS_0       0  'reraise'
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM           148  '148'
            158_1  COME_FROM            94  '94'
            158_2  COME_FROM_FINALLY    50  '50'
              158  LOAD_CONST               None
              160  STORE_FAST               'err'
              162  DELETE_FAST              'err'
              164  END_FINALLY      
              166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM            42  '42'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM            32  '32'

 L.  75       172  LOAD_FAST                'r'
              174  LOAD_FAST                'w'
              176  BUILD_TUPLE_2         2 
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 90

    def _init_fdsets(self):
        self.readables = set()
        self.writables = set()


class PollPoller(BasePoller):

    def initialize(self):
        self._poller = select.poll()
        self.READ = select.POLLIN | select.POLLPRI | select.POLLHUP
        self.WRITE = select.POLLOUT
        self.readables = set()
        self.writables = set()

    def register_readable(self, fd):
        self._poller.register(fd, self.READ)
        self.readables.add(fd)

    def register_writable(self, fd):
        self._poller.register(fd, self.WRITE)
        self.writables.add(fd)

    def unregister_readable(self, fd):
        self.readables.discard(fd)
        self._poller.unregister(fd)
        if fd in self.writables:
            self._poller.register(fd, self.WRITE)

    def unregister_writable(self, fd):
        self.writables.discard(fd)
        self._poller.unregister(fd)
        if fd in self.readables:
            self._poller.register(fd, self.READ)

    def poll(self, timeout):
        fds = self._poll_fds(timeout)
        readables, writables = [], []
        for fd, eventmask in fds:
            if self._ignore_invalid(fd, eventmask):
                pass
            else:
                if eventmask & self.READ:
                    readables.append(fd)
                if eventmask & self.WRITE:
                    writables.append(fd)
                return (
                 readables, writables)

    def _poll_fds--- This code section failed: ---

 L. 123         0  SETUP_FINALLY        20  'to 20'

 L. 124         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _poller
                6  LOAD_METHOD              poll
                8  LOAD_FAST                'timeout'
               10  LOAD_CONST               1000
               12  BINARY_MULTIPLY  
               14  CALL_METHOD_1         1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 125        20  DUP_TOP          
               22  LOAD_GLOBAL              select
               24  LOAD_ATTR                error
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    98  'to 98'
               30  POP_TOP          
               32  STORE_FAST               'err'
               34  POP_TOP          
               36  SETUP_FINALLY        86  'to 86'

 L. 126        38  LOAD_FAST                'err'
               40  LOAD_ATTR                args
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  LOAD_GLOBAL              errno
               48  LOAD_ATTR                EINTR
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    80  'to 80'

 L. 127        54  LOAD_FAST                'self'
               56  LOAD_ATTR                options
               58  LOAD_ATTR                logger
               60  LOAD_METHOD              blather
               62  LOAD_STR                 'EINTR encountered in poll'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 128        68  BUILD_LIST_0          0 
               70  ROT_FOUR         
               72  POP_BLOCK        
               74  POP_EXCEPT       
               76  CALL_FINALLY         86  'to 86'
               78  RETURN_VALUE     
             80_0  COME_FROM            52  '52'

 L. 129        80  RAISE_VARARGS_0       0  'reraise'
               82  POP_BLOCK        
               84  BEGIN_FINALLY    
             86_0  COME_FROM            76  '76'
             86_1  COME_FROM_FINALLY    36  '36'
               86  LOAD_CONST               None
               88  STORE_FAST               'err'
               90  DELETE_FAST              'err'
               92  END_FINALLY      
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            28  '28'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'

Parse error at or near `POP_BLOCK' instruction at offset 72

    def _ignore_invalid(self, fd, eventmask):
        if eventmask & select.POLLNVAL:
            self._poller.unregister(fd)
            self.readables.discard(fd)
            self.writables.discard(fd)
            return True
        return False


class KQueuePoller(BasePoller):
    __doc__ = '\n    Wrapper for select.kqueue()/kevent()\n    '
    max_events = 1000

    def initialize(self):
        self._kqueue = select.kqueue()
        self.readables = set()
        self.writables = set()

    def register_readable(self, fd):
        self.readables.add(fd)
        kevent = select.kevent(fd, filter=(select.KQ_FILTER_READ), flags=(select.KQ_EV_ADD))
        self._kqueue_control(fd, kevent)

    def register_writable(self, fd):
        self.writables.add(fd)
        kevent = select.kevent(fd, filter=(select.KQ_FILTER_WRITE), flags=(select.KQ_EV_ADD))
        self._kqueue_control(fd, kevent)

    def unregister_readable(self, fd):
        kevent = select.kevent(fd, filter=(select.KQ_FILTER_READ), flags=(select.KQ_EV_DELETE))
        self.readables.discard(fd)
        self._kqueue_control(fd, kevent)

    def unregister_writable(self, fd):
        kevent = select.kevent(fd, filter=(select.KQ_FILTER_WRITE), flags=(select.KQ_EV_DELETE))
        self.writables.discard(fd)
        self._kqueue_control(fd, kevent)

    def _kqueue_control(self, fd, kevent):
        try:
            self._kqueue.control([kevent], 0)
        except OSError as error:
            try:
                if error.errno == errno.EBADF:
                    self.options.logger.blather('EBADF encountered in kqueue. Invalid file descriptor %s' % fd)
                else:
                    raise
            finally:
                error = None
                del error

    def poll--- This code section failed: ---

 L. 190         0  BUILD_LIST_0          0 
                2  BUILD_LIST_0          0 
                4  ROT_TWO          
                6  STORE_FAST               'readables'
                8  STORE_FAST               'writables'

 L. 192        10  SETUP_FINALLY        34  'to 34'

 L. 193        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _kqueue
               16  LOAD_METHOD              control
               18  LOAD_CONST               None
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                max_events
               24  LOAD_FAST                'timeout'
               26  CALL_METHOD_3         3  ''
               28  STORE_FAST               'kevents'
               30  POP_BLOCK        
               32  JUMP_FORWARD        112  'to 112'
             34_0  COME_FROM_FINALLY    10  '10'

 L. 194        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE   110  'to 110'
               42  POP_TOP          
               44  STORE_FAST               'error'
               46  POP_TOP          
               48  SETUP_FINALLY        98  'to 98'

 L. 195        50  LOAD_FAST                'error'
               52  LOAD_ATTR                errno
               54  LOAD_GLOBAL              errno
               56  LOAD_ATTR                EINTR
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    92  'to 92'

 L. 196        62  LOAD_FAST                'self'
               64  LOAD_ATTR                options
               66  LOAD_ATTR                logger
               68  LOAD_METHOD              blather
               70  LOAD_STR                 'EINTR encountered in poll'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L. 197        76  LOAD_FAST                'readables'
               78  LOAD_FAST                'writables'
               80  BUILD_TUPLE_2         2 
               82  ROT_FOUR         
               84  POP_BLOCK        
               86  POP_EXCEPT       
               88  CALL_FINALLY         98  'to 98'
               90  RETURN_VALUE     
             92_0  COME_FROM            60  '60'

 L. 198        92  RAISE_VARARGS_0       0  'reraise'
               94  POP_BLOCK        
               96  BEGIN_FINALLY    
             98_0  COME_FROM            88  '88'
             98_1  COME_FROM_FINALLY    48  '48'
               98  LOAD_CONST               None
              100  STORE_FAST               'error'
              102  DELETE_FAST              'error'
              104  END_FINALLY      
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            40  '40'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            32  '32'

 L. 200       112  LOAD_FAST                'kevents'
              114  GET_ITER         
            116_0  COME_FROM           154  '154'
              116  FOR_ITER            170  'to 170'
              118  STORE_FAST               'kevent'

 L. 201       120  LOAD_FAST                'kevent'
              122  LOAD_ATTR                filter
              124  LOAD_GLOBAL              select
              126  LOAD_ATTR                KQ_FILTER_READ
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   144  'to 144'

 L. 202       132  LOAD_FAST                'readables'
              134  LOAD_METHOD              append
              136  LOAD_FAST                'kevent'
              138  LOAD_ATTR                ident
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           130  '130'

 L. 203       144  LOAD_FAST                'kevent'
              146  LOAD_ATTR                filter
              148  LOAD_GLOBAL              select
              150  LOAD_ATTR                KQ_FILTER_WRITE
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   116  'to 116'

 L. 204       156  LOAD_FAST                'writables'
              158  LOAD_METHOD              append
              160  LOAD_FAST                'kevent'
              162  LOAD_ATTR                ident
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  JUMP_BACK           116  'to 116'

 L. 206       170  LOAD_FAST                'readables'
              172  LOAD_FAST                'writables'
              174  BUILD_TUPLE_2         2 
              176  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 84

    def before_daemonize(self):
        self.close()

    def after_daemonize(self):
        self._kqueue = select.kqueue()
        for fd in self.readables:
            self.register_readable(fd)
        else:
            for fd in self.writables:
                self.register_writable(fd)

    def close(self):
        self._kqueue.close()
        self._kqueue = None


def implements_poll():
    return hasattr(select, 'poll')


def implements_kqueue():
    return hasattr(select, 'kqueue')


if implements_kqueue():
    Poller = KQueuePoller
else:
    if implements_poll():
        Poller = PollPoller
    else:
        Poller = SelectPoller