# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ftd2xx\_ftd2xx_linux.py
# Compiled at: 2018-05-21 11:04:47
# Size of source mod 2**32: 107364 bytes
from ctypes import *
_libraries = {}
_libraries['libftd2xx.so'] = CDLL('libftd2xx.so')
STRING = c_char_p
FT_OK = 0
PTHREAD_MUTEX_ERRORCHECK_NP = 2
PTHREAD_CANCEL_ASYNCHRONOUS = 1
PTHREAD_MUTEX_ERRORCHECK = 2
PTHREAD_SCOPE_SYSTEM = 0
PTHREAD_MUTEX_FAST_NP = 3
FT_INVALID_BAUD_RATE = 7
FT_DEVICE_2232C = 4
PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP = 2
FT_INVALID_ARGS = 16
PTHREAD_CANCEL_DISABLE = 1
FT_INVALID_PARAMETER = 6
PTHREAD_INHERIT_SCHED = 0
FT_EEPROM_NOT_PROGRAMMED = 15
PTHREAD_CREATE_JOINABLE = 0
FT_DEVICE_BM = 0
FT_INVALID_HANDLE = 1
PTHREAD_PROCESS_PRIVATE = 0
FT_DEVICE_NOT_FOUND = 2
FT_DEVICE_NOT_OPENED_FOR_WRITE = 9
FT_DEVICE_AM = 1
FT_EEPROM_ERASE_FAILED = 13
FT_DEVICE_UNKNOWN = 3
FT_OTHER_ERROR = 18
FT_DEVICE_NOT_OPENED_FOR_ERASE = 8
PTHREAD_MUTEX_NORMAL = 0
PTHREAD_MUTEX_DEFAULT = 0
PTHREAD_SCOPE_PROCESS = 1
PTHREAD_RWLOCK_PREFER_WRITER_NP = 1
PTHREAD_CANCEL_DEFERRED = 0
FT_NOT_SUPPORTED = 17
PTHREAD_RWLOCK_PREFER_READER_NP = 0
FT_DEVICE_232R = 5
PTHREAD_EXPLICIT_SCHED = 1
FT_EEPROM_NOT_PRESENT = 14
FT_INSUFFICIENT_RESOURCES = 5
FT_DEVICE_NOT_OPENED = 3
PTHREAD_MUTEX_ADAPTIVE_NP = 3
PTHREAD_CREATE_DETACHED = 1
PTHREAD_CANCEL_ENABLE = 0
FT_DEVICE_100AX = 2
FT_IO_ERROR = 4
PTHREAD_MUTEX_RECURSIVE = 1
FT_EEPROM_READ_FAILED = 11
PTHREAD_PROCESS_SHARED = 1
FT_FAILED_TO_WRITE_DEVICE = 10
FT_EEPROM_WRITE_FAILED = 12
PTHREAD_MUTEX_TIMED_NP = 0
PTHREAD_MUTEX_RECURSIVE_NP = 1
PTHREAD_RWLOCK_DEFAULT_NP = 1
_TIME_H = 1
MS_RING_ON = 64
FT_PURGE_TX = 2
CLRDTR = 6
_BITS_TYPESIZES_H = 1
__clock_t_defined = 1
SETXOFF = 1
__USE_XOPEN = 1
__USE_LARGEFILE64 = 1
TRUE = 1
__GLIBC_HAVE_LONG_LONG = 1
CSIGNAL = 255
PTHREAD_CANCELED = 0
EV_TXEMPTY = 4
FT_BAUD_460800 = 460800
__defined_schedparam = 1
RESETDEV = 7
_BITS_TYPES_H = 1
__timer_t_defined = 1
FT_PARITY_EVEN = 2
PURGE_RXCLEAR = 8
FT_BAUD_2400 = 2400
FT_BITS_8 = 8
FT_BITS_5 = 5
FT_BITS_7 = 7
FT_BITS_6 = 6
__STDC_IEC_559__ = 1
_BITS_PTHREADTYPES_H = 1
CLONE_STOPPED = 33554432
_PTHREAD_H = 1
FT_EVENT_RXCHAR = 1
_POSIX_SOURCE = 1
CE_FRAME = 8
__GNU_LIBRARY__ = 6
__USE_POSIX = 1
FT_DEFAULT_RX_TIMEOUT = 300
CLONE_THREAD = 65536
FT_FLOW_DTR_DSR = 512
CE_BREAK = 16
EV_EVENT1 = 2048
MS_RLSD_ON = 128
FT_PURGE_RX = 1
FT_EVENT_MODEM_STATUS = 2
CE_RXOVER = 1
PURGE_RXABORT = 2
FT_STOP_BITS_1_5 = 1
__USE_POSIX199309 = 1
FT_BAUD_19200 = 19200
FT_DEFAULT_TX_TIMEOUT = 300
EV_DSR = 16
CE_OVERRUN = 2
EV_CTS = 8
__clockid_t_defined = 1
EV_RXFLAG = 2
_ISOC99_SOURCE = 1
CE_IOE = 1024
FT_BAUD_14400 = 14400
CLONE_PARENT = 32768
CLOCK_MONOTONIC = 1
EV_RX80FULL = 1024
CE_RXPARITY = 4
_SVID_SOURCE = 1
__USE_XOPEN2K = 1
CLONE_FS = 512
_SCHED_H = 1
__FD_SETSIZE = 1024
CLONE_CHILD_CLEARTID = 2097152
__time_t_defined = 1
CLONE_DETACHED = 4194304
EV_RXCHAR = 1
CLONE_VM = 256
EV_BREAK = 64
__timespec_defined = 1
CLONE_CHILD_SETTID = 16777216
__USE_GNU = 1
CLONE_PTRACE = 8192
FT_LIST_ALL = 536870912
__USE_POSIX2 = 1
PTHREAD_ONCE_INIT = 0
CLOCK_THREAD_CPUTIME_ID = 3
FT_STOP_BITS_2 = 2
FT_STOP_BITS_1 = 0
CLOCK_REALTIME = 0
EV_ERR = 128
_POSIX_C_SOURCE = 199506
_SIGSET_H_types = 1
FT_BAUD_230400 = 230400
FT_LIST_BY_INDEX = 1073741824
CLONE_SIGHAND = 2048
SETRTS = 3
__USE_SVID = 1
EV_RING = 256
__USE_UNIX98 = 1
__USE_ANSI = 1
PTHREAD_BARRIER_SERIAL_THREAD = -1
__USE_MISC = 1
__USE_FORTIFY_LEVEL = 0
FT_PARITY_ODD = 1
CE_DNS = 2048
SCHED_RR = 2
FT_BAUD_300 = 300
CE_TXFULL = 256
SETBREAK = 8
FT_PARITY_MARK = 3
CLONE_SETTLS = 524288
SETXON = 2
CLRRTS = 4
PURGE_TXCLEAR = 4
CE_OOP = 4096
FT_BAUD_38400 = 38400
FT_BAUD_57600 = 57600
SCHED_FIFO = 1
FT_PARITY_NONE = 0
__STDC_ISO_10646__ = 200009
__STDC_IEC_559_COMPLEX__ = 1
FT_FLOW_RTS_CTS = 256
FT_BAUD_115200 = 115200
__USE_XOPEN_EXTENDED = 1
FALSE = 0
CLONE_FILES = 1024
__CPU_SETSIZE = 1024
CE_PTO = 512
FT_BAUD_9600 = 9600
__USE_LARGEFILE = 1
EV_EVENT2 = 4096
INVALID_HANDLE_VALUE = 4294967295
_FEATURES_H = 1
MS_DSR_ON = 32
FT_FLOW_XON_XOFF = 1024
FT_FLOW_NONE = 0
__USE_POSIX199506 = 1
CLONE_SYSVSEM = 262144
FT_PARITY_SPACE = 4
__USE_BSD = 1
FT_OPEN_BY_DESCRIPTION = 2
FT_BAUD_4800 = 4800
CLONE_PARENT_SETTID = 1048576
__WORDSIZE_COMPAT32 = 1
PURGE_TXABORT = 1
TIMER_ABSTIME = 1
FT_BAUD_1200 = 1200
FT_OPEN_BY_SERIAL_NUMBER = 1
CLONE_UNTRACED = 8388608
FT_LIST_MASK = 3758096384
EV_PERR = 512
CLOCK_PROCESS_CPUTIME_ID = 2
_XOPEN_SOURCE_EXTENDED = 1
MAX_NUM_DEVICES = 50
CLOCKS_PER_SEC = 1000000
MS_CTS_ON = 16
__WORDSIZE = 64
__NCPUBITS = 64
SCHED_OTHER = 0
_SYS_CDEFS_H = 1
EV_RLSD = 32
_LARGEFILE64_SOURCE = 1
_XOPEN_SOURCE = 600
_SIGSET_NWORDS = 16
CLRBREAK = 9
__GLIBC__ = 2
CE_MODE = 32768
__USE_ISOC99 = 1
_BITS_SIGTHREAD_H = 1
CLONE_NEWNS = 131072
__GLIBC_MINOR__ = 3
_BITS_TIME_H = 1
SETDTR = 5
FT_BAUD_921600 = 921600
CLONE_VFORK = 16384
FT_BAUD_600 = 600
__LT_SPINLOCK_INIT = 0
_BSD_SOURCE = 1
FT_LIST_NUMBER_ONLY = 2147483648
_XLOCALE_H = 1
_LARGEFILE_SOURCE = 1

class _pthread_fastlock(Structure):
    pass


_pthread_fastlock._fields_ = [
 (
  '__status', c_long),
 (
  '__spinlock', c_int)]

class _pthread_descr_struct(Structure):
    pass


_pthread_descr = POINTER(_pthread_descr_struct)
_pthread_descr_struct._fields_ = []

class __pthread_attr_s(Structure):
    pass


class __sched_param(Structure):
    pass


__sched_param._fields_ = [
 (
  '__sched_priority', c_int)]
size_t = c_uint
__pthread_attr_s._fields_ = [
 (
  '__detachstate', c_int),
 (
  '__schedpolicy', c_int),
 (
  '__schedparam', __sched_param),
 (
  '__inheritsched', c_int),
 (
  '__scope', c_int),
 (
  '__guardsize', size_t),
 (
  '__stackaddr_set', c_int),
 (
  '__stackaddr', c_void_p),
 (
  '__stacksize', size_t)]
pthread_attr_t = __pthread_attr_s
__pthread_cond_align_t = c_longlong

class pthread_cond_t(Structure):
    pass


pthread_cond_t._fields_ = [
 (
  '__c_lock', _pthread_fastlock),
 (
  '__c_waiting', _pthread_descr),
 (
  '__padding', c_char * 16),
 (
  '__align', __pthread_cond_align_t)]

class pthread_condattr_t(Structure):
    pass


pthread_condattr_t._fields_ = [
 (
  '__dummy', c_int)]
pthread_key_t = c_uint

class pthread_mutex_t(Structure):
    pass


pthread_mutex_t._fields_ = [
 (
  '__m_reserved', c_int),
 (
  '__m_count', c_int),
 (
  '__m_owner', _pthread_descr),
 (
  '__m_kind', c_int),
 (
  '__m_lock', _pthread_fastlock)]

class pthread_mutexattr_t(Structure):
    pass


pthread_mutexattr_t._fields_ = [
 (
  '__mutexkind', c_int)]
pthread_once_t = c_int

class _pthread_rwlock_t(Structure):
    pass


_pthread_rwlock_t._fields_ = [
 (
  '__rw_lock', _pthread_fastlock),
 (
  '__rw_readers', c_int),
 (
  '__rw_writer', _pthread_descr),
 (
  '__rw_read_waiting', _pthread_descr),
 (
  '__rw_write_waiting', _pthread_descr),
 (
  '__rw_kind', c_int),
 (
  '__rw_pshared', c_int)]
pthread_rwlock_t = _pthread_rwlock_t

class pthread_rwlockattr_t(Structure):
    pass


pthread_rwlockattr_t._fields_ = [
 (
  '__lockkind', c_int),
 (
  '__pshared', c_int)]
pthread_spinlock_t = c_int

class pthread_barrier_t(Structure):
    pass


pthread_barrier_t._fields_ = [
 (
  '__ba_lock', _pthread_fastlock),
 (
  '__ba_required', c_int),
 (
  '__ba_present', c_int),
 (
  '__ba_waiting', _pthread_descr)]

class pthread_barrierattr_t(Structure):
    pass


pthread_barrierattr_t._fields_ = [
 (
  '__pshared', c_int)]
pthread_t = c_ulong

class sched_param(Structure):
    pass


sched_param._fields_ = [
 (
  '__sched_priority', c_int)]
clone = _libraries['libftd2xx.so'].clone
clone.restype = c_int
clone.argtypes = [
 CFUNCTYPE(c_int, c_void_p), c_void_p, c_int, c_void_p]
clone.__doc__ = 'int clone(unknown * __fn, void * __child_stack, int __flags, void * __arg)\n/usr/include/bits/sched.h:72'
__cpu_mask = c_ulong

class cpu_set_t(Structure):
    pass


cpu_set_t._fields_ = [
 (
  '__bits', __cpu_mask * 16)]
__sig_atomic_t = c_int

class __sigset_t(Structure):
    pass


__sigset_t._fields_ = [
 (
  '__val', c_ulong * 16)]
pthread_sigmask = _libraries['libftd2xx.so'].pthread_sigmask
pthread_sigmask.restype = c_int
pthread_sigmask.argtypes = [
 c_int, POINTER(__sigset_t), POINTER(__sigset_t)]
pthread_sigmask.__doc__ = 'int pthread_sigmask(int __how, unknown __newmask, unknown __oldmask)\n/usr/include/bits/sigthread.h:33'
pthread_kill = _libraries['libftd2xx.so'].pthread_kill
pthread_kill.restype = c_int
pthread_kill.argtypes = [
 pthread_t, c_int]
pthread_kill.__doc__ = 'int pthread_kill(pthread_t __threadid, int __signo)\n/usr/include/bits/sigthread.h:36'
__u_char = c_ubyte
__u_short = c_ushort
__u_int = c_uint
__u_long = c_ulong
__int8_t = c_byte
__uint8_t = c_ubyte
__int16_t = c_short
__uint16_t = c_ushort
__int32_t = c_int
__uint32_t = c_uint
__int64_t = c_long
__uint64_t = c_ulong
__quad_t = c_long
__u_quad_t = c_ulong
__dev_t = c_ulong
__uid_t = c_uint
__gid_t = c_uint
__ino_t = c_ulong
__ino64_t = c_ulong
__mode_t = c_uint
__nlink_t = c_ulong
__off_t = c_long
__off64_t = c_long
__pid_t = c_int

class __fsid_t(Structure):
    pass


__fsid_t._fields_ = [
 (
  '__val', c_int * 2)]
__clock_t = c_long
__rlim_t = c_ulong
__rlim64_t = c_ulong
__id_t = c_uint
__time_t = c_long
__useconds_t = c_uint
__suseconds_t = c_long
__daddr_t = c_int
__swblk_t = c_long
__key_t = c_int
__clockid_t = c_int
__timer_t = c_int
__blksize_t = c_long
__blkcnt_t = c_long
__blkcnt64_t = c_long
__fsblkcnt_t = c_ulong
__fsblkcnt64_t = c_ulong
__fsfilcnt_t = c_ulong
__fsfilcnt64_t = c_ulong
__ssize_t = c_long
__loff_t = __off64_t
__qaddr_t = POINTER(__quad_t)
__caddr_t = STRING
__intptr_t = c_long
__socklen_t = c_uint

class _pthread_cleanup_buffer(Structure):
    pass


_pthread_cleanup_buffer._fields_ = [
 (
  '__routine', CFUNCTYPE(None, c_void_p)),
 (
  '__arg', c_void_p),
 (
  '__canceltype', c_int),
 (
  '__prev', POINTER(_pthread_cleanup_buffer))]
pthread_create = _libraries['libftd2xx.so'].pthread_create
pthread_create.restype = c_int
pthread_create.argtypes = [
 POINTER(pthread_t), POINTER(pthread_attr_t), CFUNCTYPE(c_void_p, c_void_p), c_void_p]
pthread_create.__doc__ = 'int pthread_create(unknown __threadp, unknown __attr, unknown * __start_routine, unknown __arg)\n/usr/include/pthread.h:166'
pthread_self = _libraries['libftd2xx.so'].pthread_self
pthread_self.restype = pthread_t
pthread_self.argtypes = []
pthread_self.__doc__ = 'pthread_t pthread_self()\n/usr/include/pthread.h:169'
pthread_equal = _libraries['libftd2xx.so'].pthread_equal
pthread_equal.restype = c_int
pthread_equal.argtypes = [
 pthread_t, pthread_t]
pthread_equal.__doc__ = 'int pthread_equal(pthread_t __thread1, pthread_t __thread2)\n/usr/include/pthread.h:172'
pthread_exit = _libraries['libftd2xx.so'].pthread_exit
pthread_exit.restype = None
pthread_exit.argtypes = [
 c_void_p]
pthread_exit.__doc__ = 'void pthread_exit(void * __retval)\n/usr/include/pthread.h:175'
pthread_join = _libraries['libftd2xx.so'].pthread_join
pthread_join.restype = c_int
pthread_join.argtypes = [
 pthread_t, POINTER(c_void_p)]
pthread_join.__doc__ = 'int pthread_join(pthread_t __th, void * * __thread_return)\n/usr/include/pthread.h:180'
pthread_detach = _libraries['libftd2xx.so'].pthread_detach
pthread_detach.restype = c_int
pthread_detach.argtypes = [
 pthread_t]
pthread_detach.__doc__ = 'int pthread_detach(pthread_t __th)\n/usr/include/pthread.h:186'
pthread_attr_init = _libraries['libftd2xx.so'].pthread_attr_init
pthread_attr_init.restype = c_int
pthread_attr_init.argtypes = [
 POINTER(pthread_attr_t)]
pthread_attr_init.__doc__ = 'int pthread_attr_init(pthread_attr_t * __attr)\n/usr/include/pthread.h:194'
pthread_attr_destroy = _libraries['libftd2xx.so'].pthread_attr_destroy
pthread_attr_destroy.restype = c_int
pthread_attr_destroy.argtypes = [
 POINTER(pthread_attr_t)]
pthread_attr_destroy.__doc__ = 'int pthread_attr_destroy(pthread_attr_t * __attr)\n/usr/include/pthread.h:197'
pthread_attr_setdetachstate = _libraries['libftd2xx.so'].pthread_attr_setdetachstate
pthread_attr_setdetachstate.restype = c_int
pthread_attr_setdetachstate.argtypes = [
 POINTER(pthread_attr_t), c_int]
pthread_attr_setdetachstate.__doc__ = 'int pthread_attr_setdetachstate(pthread_attr_t * __attr, int __detachstate)\n/usr/include/pthread.h:201'
pthread_attr_getdetachstate = _libraries['libftd2xx.so'].pthread_attr_getdetachstate
pthread_attr_getdetachstate.restype = c_int
pthread_attr_getdetachstate.argtypes = [
 POINTER(pthread_attr_t), POINTER(c_int)]
pthread_attr_getdetachstate.__doc__ = 'int pthread_attr_getdetachstate(unknown * __attr, int * __detachstate)\n/usr/include/pthread.h:205'
pthread_attr_setschedparam = _libraries['libftd2xx.so'].pthread_attr_setschedparam
pthread_attr_setschedparam.restype = c_int
pthread_attr_setschedparam.argtypes = [
 POINTER(pthread_attr_t), POINTER(sched_param)]
pthread_attr_setschedparam.__doc__ = 'int pthread_attr_setschedparam(unknown __attr, unknown __param)\n/usr/include/pthread.h:210'
pthread_attr_getschedparam = _libraries['libftd2xx.so'].pthread_attr_getschedparam
pthread_attr_getschedparam.restype = c_int
pthread_attr_getschedparam.argtypes = [
 POINTER(pthread_attr_t), POINTER(sched_param)]
pthread_attr_getschedparam.__doc__ = 'int pthread_attr_getschedparam(unknown __attr, unknown __param)\n/usr/include/pthread.h:216'
pthread_attr_setschedpolicy = _libraries['libftd2xx.so'].pthread_attr_setschedpolicy
pthread_attr_setschedpolicy.restype = c_int
pthread_attr_setschedpolicy.argtypes = [
 POINTER(pthread_attr_t), c_int]
pthread_attr_setschedpolicy.__doc__ = 'int pthread_attr_setschedpolicy(pthread_attr_t * __attr, int __policy)\n/usr/include/pthread.h:220'
pthread_attr_getschedpolicy = _libraries['libftd2xx.so'].pthread_attr_getschedpolicy
pthread_attr_getschedpolicy.restype = c_int
pthread_attr_getschedpolicy.argtypes = [
 POINTER(pthread_attr_t), POINTER(c_int)]
pthread_attr_getschedpolicy.__doc__ = 'int pthread_attr_getschedpolicy(unknown __attr, unknown __policy)\n/usr/include/pthread.h:225'
pthread_attr_setinheritsched = _libraries['libftd2xx.so'].pthread_attr_setinheritsched
pthread_attr_setinheritsched.restype = c_int
pthread_attr_setinheritsched.argtypes = [
 POINTER(pthread_attr_t), c_int]
pthread_attr_setinheritsched.__doc__ = 'int pthread_attr_setinheritsched(pthread_attr_t * __attr, int __inherit)\n/usr/include/pthread.h:229'
pthread_attr_getinheritsched = _libraries['libftd2xx.so'].pthread_attr_getinheritsched
pthread_attr_getinheritsched.restype = c_int
pthread_attr_getinheritsched.argtypes = [
 POINTER(pthread_attr_t), POINTER(c_int)]
pthread_attr_getinheritsched.__doc__ = 'int pthread_attr_getinheritsched(unknown __attr, unknown __inherit)\n/usr/include/pthread.h:234'
pthread_attr_setscope = _libraries['libftd2xx.so'].pthread_attr_setscope
pthread_attr_setscope.restype = c_int
pthread_attr_setscope.argtypes = [
 POINTER(pthread_attr_t), c_int]
pthread_attr_setscope.__doc__ = 'int pthread_attr_setscope(pthread_attr_t * __attr, int __scope)\n/usr/include/pthread.h:238'
pthread_attr_getscope = _libraries['libftd2xx.so'].pthread_attr_getscope
pthread_attr_getscope.restype = c_int
pthread_attr_getscope.argtypes = [
 POINTER(pthread_attr_t), POINTER(c_int)]
pthread_attr_getscope.__doc__ = 'int pthread_attr_getscope(unknown __attr, unknown __scope)\n/usr/include/pthread.h:242'
pthread_attr_setguardsize = _libraries['libftd2xx.so'].pthread_attr_setguardsize
pthread_attr_setguardsize.restype = c_int
pthread_attr_setguardsize.argtypes = [
 POINTER(pthread_attr_t), size_t]
pthread_attr_setguardsize.__doc__ = 'int pthread_attr_setguardsize(pthread_attr_t * __attr, size_t __guardsize)\n/usr/include/pthread.h:247'
pthread_attr_getguardsize = _libraries['libftd2xx.so'].pthread_attr_getguardsize
pthread_attr_getguardsize.restype = c_int
pthread_attr_getguardsize.argtypes = [
 POINTER(pthread_attr_t), POINTER(size_t)]
pthread_attr_getguardsize.__doc__ = 'int pthread_attr_getguardsize(unknown __attr, unknown __guardsize)\n/usr/include/pthread.h:252'
pthread_attr_setstackaddr = _libraries['libftd2xx.so'].pthread_attr_setstackaddr
pthread_attr_setstackaddr.restype = c_int
pthread_attr_setstackaddr.argtypes = [
 POINTER(pthread_attr_t), c_void_p]
pthread_attr_setstackaddr.__doc__ = 'int pthread_attr_setstackaddr(pthread_attr_t * __attr, void * __stackaddr)\n/usr/include/pthread.h:260'
pthread_attr_getstackaddr = _libraries['libftd2xx.so'].pthread_attr_getstackaddr
pthread_attr_getstackaddr.restype = c_int
pthread_attr_getstackaddr.argtypes = [
 POINTER(pthread_attr_t), POINTER(c_void_p)]
pthread_attr_getstackaddr.__doc__ = 'int pthread_attr_getstackaddr(unknown __attr, unknown __stackaddr)\n/usr/include/pthread.h:265'
pthread_attr_setstack = _libraries['libftd2xx.so'].pthread_attr_setstack
pthread_attr_setstack.restype = c_int
pthread_attr_setstack.argtypes = [
 POINTER(pthread_attr_t), c_void_p, size_t]
pthread_attr_setstack.__doc__ = 'int pthread_attr_setstack(pthread_attr_t * __attr, void * __stackaddr, size_t __stacksize)\n/usr/include/pthread.h:272'
pthread_attr_getstack = _libraries['libftd2xx.so'].pthread_attr_getstack
pthread_attr_getstack.restype = c_int
pthread_attr_getstack.argtypes = [
 POINTER(pthread_attr_t), POINTER(c_void_p), POINTER(size_t)]
pthread_attr_getstack.__doc__ = 'int pthread_attr_getstack(unknown __attr, unknown __stackaddr, unknown __stacksize)\n/usr/include/pthread.h:277'
pthread_attr_setstacksize = _libraries['libftd2xx.so'].pthread_attr_setstacksize
pthread_attr_setstacksize.restype = c_int
pthread_attr_setstacksize.argtypes = [
 POINTER(pthread_attr_t), size_t]
pthread_attr_setstacksize.__doc__ = 'int pthread_attr_setstacksize(pthread_attr_t * __attr, size_t __stacksize)\n/usr/include/pthread.h:284'
pthread_attr_getstacksize = _libraries['libftd2xx.so'].pthread_attr_getstacksize
pthread_attr_getstacksize.restype = c_int
pthread_attr_getstacksize.argtypes = [
 POINTER(pthread_attr_t), POINTER(size_t)]
pthread_attr_getstacksize.__doc__ = 'int pthread_attr_getstacksize(unknown __attr, unknown __stacksize)\n/usr/include/pthread.h:289'
pthread_getattr_np = _libraries['libftd2xx.so'].pthread_getattr_np
pthread_getattr_np.restype = c_int
pthread_getattr_np.argtypes = [
 pthread_t, POINTER(pthread_attr_t)]
pthread_getattr_np.__doc__ = 'int pthread_getattr_np(pthread_t __th, pthread_attr_t * __attr)\n/usr/include/pthread.h:295'
pthread_setschedparam = _libraries['libftd2xx.so'].pthread_setschedparam
pthread_setschedparam.restype = c_int
pthread_setschedparam.argtypes = [
 pthread_t, c_int, POINTER(sched_param)]
pthread_setschedparam.__doc__ = 'int pthread_setschedparam(pthread_t __target_thread, int __policy, unknown * __param)\n/usr/include/pthread.h:304'
pthread_getschedparam = _libraries['libftd2xx.so'].pthread_getschedparam
pthread_getschedparam.restype = c_int
pthread_getschedparam.argtypes = [
 pthread_t, POINTER(c_int), POINTER(sched_param)]
pthread_getschedparam.__doc__ = 'int pthread_getschedparam(pthread_t __target_thread, unknown __policy, unknown __param)\n/usr/include/pthread.h:310'
pthread_getconcurrency = _libraries['libftd2xx.so'].pthread_getconcurrency
pthread_getconcurrency.restype = c_int
pthread_getconcurrency.argtypes = []
pthread_getconcurrency.__doc__ = 'int pthread_getconcurrency()\n/usr/include/pthread.h:314'
pthread_setconcurrency = _libraries['libftd2xx.so'].pthread_setconcurrency
pthread_setconcurrency.restype = c_int
pthread_setconcurrency.argtypes = [
 c_int]
pthread_setconcurrency.__doc__ = 'int pthread_setconcurrency(int __level)\n/usr/include/pthread.h:317'
pthread_yield = _libraries['libftd2xx.so'].pthread_yield
pthread_yield.restype = c_int
pthread_yield.argtypes = []
pthread_yield.__doc__ = 'int pthread_yield()\n/usr/include/pthread.h:325'
pthread_mutex_init = _libraries['libftd2xx.so'].pthread_mutex_init
pthread_mutex_init.restype = c_int
pthread_mutex_init.argtypes = [
 POINTER(pthread_mutex_t), POINTER(pthread_mutexattr_t)]
pthread_mutex_init.__doc__ = 'int pthread_mutex_init(unknown __mutex, unknown __mutex_attr)\n/usr/include/pthread.h:334'
pthread_mutex_destroy = _libraries['libftd2xx.so'].pthread_mutex_destroy
pthread_mutex_destroy.restype = c_int
pthread_mutex_destroy.argtypes = [
 POINTER(pthread_mutex_t)]
pthread_mutex_destroy.__doc__ = 'int pthread_mutex_destroy(pthread_mutex_t * __mutex)\n/usr/include/pthread.h:337'
pthread_mutex_trylock = _libraries['libftd2xx.so'].pthread_mutex_trylock
pthread_mutex_trylock.restype = c_int
pthread_mutex_trylock.argtypes = [
 POINTER(pthread_mutex_t)]
pthread_mutex_trylock.__doc__ = 'int pthread_mutex_trylock(pthread_mutex_t * __mutex)\n/usr/include/pthread.h:340'
pthread_mutex_lock = _libraries['libftd2xx.so'].pthread_mutex_lock
pthread_mutex_lock.restype = c_int
pthread_mutex_lock.argtypes = [
 POINTER(pthread_mutex_t)]
pthread_mutex_lock.__doc__ = 'int pthread_mutex_lock(pthread_mutex_t * __mutex)\n/usr/include/pthread.h:343'

class timespec(Structure):
    pass


timespec._fields_ = [
 (
  'tv_sec', __time_t),
 (
  'tv_nsec', c_long)]
pthread_mutex_timedlock = _libraries['libftd2xx.so'].pthread_mutex_timedlock
pthread_mutex_timedlock.restype = c_int
pthread_mutex_timedlock.argtypes = [
 POINTER(pthread_mutex_t), POINTER(timespec)]
pthread_mutex_timedlock.__doc__ = 'int pthread_mutex_timedlock(unknown __mutex, unknown __abstime)\n/usr/include/pthread.h:349'
pthread_mutex_unlock = _libraries['libftd2xx.so'].pthread_mutex_unlock
pthread_mutex_unlock.restype = c_int
pthread_mutex_unlock.argtypes = [
 POINTER(pthread_mutex_t)]
pthread_mutex_unlock.__doc__ = 'int pthread_mutex_unlock(pthread_mutex_t * __mutex)\n/usr/include/pthread.h:353'
pthread_mutexattr_init = _libraries['libftd2xx.so'].pthread_mutexattr_init
pthread_mutexattr_init.restype = c_int
pthread_mutexattr_init.argtypes = [
 POINTER(pthread_mutexattr_t)]
pthread_mutexattr_init.__doc__ = 'int pthread_mutexattr_init(pthread_mutexattr_t * __attr)\n/usr/include/pthread.h:360'
pthread_mutexattr_destroy = _libraries['libftd2xx.so'].pthread_mutexattr_destroy
pthread_mutexattr_destroy.restype = c_int
pthread_mutexattr_destroy.argtypes = [
 POINTER(pthread_mutexattr_t)]
pthread_mutexattr_destroy.__doc__ = 'int pthread_mutexattr_destroy(pthread_mutexattr_t * __attr)\n/usr/include/pthread.h:363'
pthread_mutexattr_getpshared = _libraries['libftd2xx.so'].pthread_mutexattr_getpshared
pthread_mutexattr_getpshared.restype = c_int
pthread_mutexattr_getpshared.argtypes = [
 POINTER(pthread_mutexattr_t), POINTER(c_int)]
pthread_mutexattr_getpshared.__doc__ = 'int pthread_mutexattr_getpshared(unknown __attr, unknown __pshared)\n/usr/include/pthread.h:368'
pthread_mutexattr_setpshared = _libraries['libftd2xx.so'].pthread_mutexattr_setpshared
pthread_mutexattr_setpshared.restype = c_int
pthread_mutexattr_setpshared.argtypes = [
 POINTER(pthread_mutexattr_t), c_int]
pthread_mutexattr_setpshared.__doc__ = 'int pthread_mutexattr_setpshared(pthread_mutexattr_t * __attr, int __pshared)\n/usr/include/pthread.h:372'
pthread_mutexattr_settype = _libraries['libftd2xx.so'].pthread_mutexattr_settype
pthread_mutexattr_settype.restype = c_int
pthread_mutexattr_settype.argtypes = [
 POINTER(pthread_mutexattr_t), c_int]
pthread_mutexattr_settype.__doc__ = 'int pthread_mutexattr_settype(pthread_mutexattr_t * __attr, int __kind)\n/usr/include/pthread.h:379'
pthread_mutexattr_gettype = _libraries['libftd2xx.so'].pthread_mutexattr_gettype
pthread_mutexattr_gettype.restype = c_int
pthread_mutexattr_gettype.argtypes = [
 POINTER(pthread_mutexattr_t), POINTER(c_int)]
pthread_mutexattr_gettype.__doc__ = 'int pthread_mutexattr_gettype(unknown __attr, unknown __kind)\n/usr/include/pthread.h:383'
pthread_cond_init = _libraries['libftd2xx.so'].pthread_cond_init
pthread_cond_init.restype = c_int
pthread_cond_init.argtypes = [
 POINTER(pthread_cond_t), POINTER(pthread_condattr_t)]
pthread_cond_init.__doc__ = 'int pthread_cond_init(unknown __cond, unknown __cond_attr)\n/usr/include/pthread.h:393'
pthread_cond_destroy = _libraries['libftd2xx.so'].pthread_cond_destroy
pthread_cond_destroy.restype = c_int
pthread_cond_destroy.argtypes = [
 POINTER(pthread_cond_t)]
pthread_cond_destroy.__doc__ = 'int pthread_cond_destroy(pthread_cond_t * __cond)\n/usr/include/pthread.h:396'
pthread_cond_signal = _libraries['libftd2xx.so'].pthread_cond_signal
pthread_cond_signal.restype = c_int
pthread_cond_signal.argtypes = [
 POINTER(pthread_cond_t)]
pthread_cond_signal.__doc__ = 'int pthread_cond_signal(pthread_cond_t * __cond)\n/usr/include/pthread.h:399'
pthread_cond_broadcast = _libraries['libftd2xx.so'].pthread_cond_broadcast
pthread_cond_broadcast.restype = c_int
pthread_cond_broadcast.argtypes = [
 POINTER(pthread_cond_t)]
pthread_cond_broadcast.__doc__ = 'int pthread_cond_broadcast(pthread_cond_t * __cond)\n/usr/include/pthread.h:402'
pthread_cond_wait = _libraries['libftd2xx.so'].pthread_cond_wait
pthread_cond_wait.restype = c_int
pthread_cond_wait.argtypes = [
 POINTER(pthread_cond_t), POINTER(pthread_mutex_t)]
pthread_cond_wait.__doc__ = 'int pthread_cond_wait(unknown __cond, unknown __mutex)\n/usr/include/pthread.h:407'
pthread_cond_timedwait = _libraries['libftd2xx.so'].pthread_cond_timedwait
pthread_cond_timedwait.restype = c_int
pthread_cond_timedwait.argtypes = [
 POINTER(pthread_cond_t), POINTER(pthread_mutex_t), POINTER(timespec)]
pthread_cond_timedwait.__doc__ = 'int pthread_cond_timedwait(unknown __cond, unknown __mutex, unknown __abstime)\n/usr/include/pthread.h:416'
pthread_condattr_init = _libraries['libftd2xx.so'].pthread_condattr_init
pthread_condattr_init.restype = c_int
pthread_condattr_init.argtypes = [
 POINTER(pthread_condattr_t)]
pthread_condattr_init.__doc__ = 'int pthread_condattr_init(pthread_condattr_t * __attr)\n/usr/include/pthread.h:421'
pthread_condattr_destroy = _libraries['libftd2xx.so'].pthread_condattr_destroy
pthread_condattr_destroy.restype = c_int
pthread_condattr_destroy.argtypes = [
 POINTER(pthread_condattr_t)]
pthread_condattr_destroy.__doc__ = 'int pthread_condattr_destroy(pthread_condattr_t * __attr)\n/usr/include/pthread.h:424'
pthread_condattr_getpshared = _libraries['libftd2xx.so'].pthread_condattr_getpshared
pthread_condattr_getpshared.restype = c_int
pthread_condattr_getpshared.argtypes = [
 POINTER(pthread_condattr_t), POINTER(c_int)]
pthread_condattr_getpshared.__doc__ = 'int pthread_condattr_getpshared(unknown __attr, unknown __pshared)\n/usr/include/pthread.h:429'
pthread_condattr_setpshared = _libraries['libftd2xx.so'].pthread_condattr_setpshared
pthread_condattr_setpshared.restype = c_int
pthread_condattr_setpshared.argtypes = [
 POINTER(pthread_condattr_t), c_int]
pthread_condattr_setpshared.__doc__ = 'int pthread_condattr_setpshared(pthread_condattr_t * __attr, int __pshared)\n/usr/include/pthread.h:433'
pthread_rwlock_init = _libraries['libftd2xx.so'].pthread_rwlock_init
pthread_rwlock_init.restype = c_int
pthread_rwlock_init.argtypes = [
 POINTER(pthread_rwlock_t), POINTER(pthread_rwlockattr_t)]
pthread_rwlock_init.__doc__ = 'int pthread_rwlock_init(unknown __rwlock, unknown __attr)\n/usr/include/pthread.h:443'
pthread_rwlock_destroy = _libraries['libftd2xx.so'].pthread_rwlock_destroy
pthread_rwlock_destroy.restype = c_int
pthread_rwlock_destroy.argtypes = [
 POINTER(pthread_rwlock_t)]
pthread_rwlock_destroy.__doc__ = 'int pthread_rwlock_destroy(pthread_rwlock_t * __rwlock)\n/usr/include/pthread.h:446'
pthread_rwlock_rdlock = _libraries['libftd2xx.so'].pthread_rwlock_rdlock
pthread_rwlock_rdlock.restype = c_int
pthread_rwlock_rdlock.argtypes = [
 POINTER(pthread_rwlock_t)]
pthread_rwlock_rdlock.__doc__ = 'int pthread_rwlock_rdlock(pthread_rwlock_t * __rwlock)\n/usr/include/pthread.h:449'
pthread_rwlock_tryrdlock = _libraries['libftd2xx.so'].pthread_rwlock_tryrdlock
pthread_rwlock_tryrdlock.restype = c_int
pthread_rwlock_tryrdlock.argtypes = [
 POINTER(pthread_rwlock_t)]
pthread_rwlock_tryrdlock.__doc__ = 'int pthread_rwlock_tryrdlock(pthread_rwlock_t * __rwlock)\n/usr/include/pthread.h:452'
pthread_rwlock_timedrdlock = _libraries['libftd2xx.so'].pthread_rwlock_timedrdlock
pthread_rwlock_timedrdlock.restype = c_int
pthread_rwlock_timedrdlock.argtypes = [
 POINTER(pthread_rwlock_t), POINTER(timespec)]
pthread_rwlock_timedrdlock.__doc__ = 'int pthread_rwlock_timedrdlock(unknown __rwlock, unknown __abstime)\n/usr/include/pthread.h:458'
pthread_rwlock_wrlock = _libraries['libftd2xx.so'].pthread_rwlock_wrlock
pthread_rwlock_wrlock.restype = c_int
pthread_rwlock_wrlock.argtypes = [
 POINTER(pthread_rwlock_t)]
pthread_rwlock_wrlock.__doc__ = 'int pthread_rwlock_wrlock(pthread_rwlock_t * __rwlock)\n/usr/include/pthread.h:462'
pthread_rwlock_trywrlock = _libraries['libftd2xx.so'].pthread_rwlock_trywrlock
pthread_rwlock_trywrlock.restype = c_int
pthread_rwlock_trywrlock.argtypes = [
 POINTER(pthread_rwlock_t)]
pthread_rwlock_trywrlock.__doc__ = 'int pthread_rwlock_trywrlock(pthread_rwlock_t * __rwlock)\n/usr/include/pthread.h:465'
pthread_rwlock_timedwrlock = _libraries['libftd2xx.so'].pthread_rwlock_timedwrlock
pthread_rwlock_timedwrlock.restype = c_int
pthread_rwlock_timedwrlock.argtypes = [
 POINTER(pthread_rwlock_t), POINTER(timespec)]
pthread_rwlock_timedwrlock.__doc__ = 'int pthread_rwlock_timedwrlock(unknown __rwlock, unknown __abstime)\n/usr/include/pthread.h:471'
pthread_rwlock_unlock = _libraries['libftd2xx.so'].pthread_rwlock_unlock
pthread_rwlock_unlock.restype = c_int
pthread_rwlock_unlock.argtypes = [
 POINTER(pthread_rwlock_t)]
pthread_rwlock_unlock.__doc__ = 'int pthread_rwlock_unlock(pthread_rwlock_t * __rwlock)\n/usr/include/pthread.h:475'
pthread_rwlockattr_init = _libraries['libftd2xx.so'].pthread_rwlockattr_init
pthread_rwlockattr_init.restype = c_int
pthread_rwlockattr_init.argtypes = [
 POINTER(pthread_rwlockattr_t)]
pthread_rwlockattr_init.__doc__ = 'int pthread_rwlockattr_init(pthread_rwlockattr_t * __attr)\n/usr/include/pthread.h:481'
pthread_rwlockattr_destroy = _libraries['libftd2xx.so'].pthread_rwlockattr_destroy
pthread_rwlockattr_destroy.restype = c_int
pthread_rwlockattr_destroy.argtypes = [
 POINTER(pthread_rwlockattr_t)]
pthread_rwlockattr_destroy.__doc__ = 'int pthread_rwlockattr_destroy(pthread_rwlockattr_t * __attr)\n/usr/include/pthread.h:484'
pthread_rwlockattr_getpshared = _libraries['libftd2xx.so'].pthread_rwlockattr_getpshared
pthread_rwlockattr_getpshared.restype = c_int
pthread_rwlockattr_getpshared.argtypes = [
 POINTER(pthread_rwlockattr_t), POINTER(c_int)]
pthread_rwlockattr_getpshared.__doc__ = 'int pthread_rwlockattr_getpshared(unknown __attr, unknown __pshared)\n/usr/include/pthread.h:489'
pthread_rwlockattr_setpshared = _libraries['libftd2xx.so'].pthread_rwlockattr_setpshared
pthread_rwlockattr_setpshared.restype = c_int
pthread_rwlockattr_setpshared.argtypes = [
 POINTER(pthread_rwlockattr_t), c_int]
pthread_rwlockattr_setpshared.__doc__ = 'int pthread_rwlockattr_setpshared(pthread_rwlockattr_t * __attr, int __pshared)\n/usr/include/pthread.h:493'
pthread_rwlockattr_getkind_np = _libraries['libftd2xx.so'].pthread_rwlockattr_getkind_np
pthread_rwlockattr_getkind_np.restype = c_int
pthread_rwlockattr_getkind_np.argtypes = [
 POINTER(pthread_rwlockattr_t), POINTER(c_int)]
pthread_rwlockattr_getkind_np.__doc__ = 'int pthread_rwlockattr_getkind_np(unknown * __attr, int * __pref)\n/usr/include/pthread.h:497'
pthread_rwlockattr_setkind_np = _libraries['libftd2xx.so'].pthread_rwlockattr_setkind_np
pthread_rwlockattr_setkind_np.restype = c_int
pthread_rwlockattr_setkind_np.argtypes = [
 POINTER(pthread_rwlockattr_t), c_int]
pthread_rwlockattr_setkind_np.__doc__ = 'int pthread_rwlockattr_setkind_np(pthread_rwlockattr_t * __attr, int __pref)\n/usr/include/pthread.h:501'
pthread_spin_init = _libraries['libftd2xx.so'].pthread_spin_init
pthread_spin_init.restype = c_int
pthread_spin_init.argtypes = [
 POINTER(pthread_spinlock_t), c_int]
pthread_spin_init.__doc__ = 'int pthread_spin_init(pthread_spinlock_t * __lock, int __pshared)\n/usr/include/pthread.h:511'
pthread_spin_destroy = _libraries['libftd2xx.so'].pthread_spin_destroy
pthread_spin_destroy.restype = c_int
pthread_spin_destroy.argtypes = [
 POINTER(pthread_spinlock_t)]
pthread_spin_destroy.__doc__ = 'int pthread_spin_destroy(pthread_spinlock_t * __lock)\n/usr/include/pthread.h:514'
pthread_spin_lock = _libraries['libftd2xx.so'].pthread_spin_lock
pthread_spin_lock.restype = c_int
pthread_spin_lock.argtypes = [
 POINTER(pthread_spinlock_t)]
pthread_spin_lock.__doc__ = 'int pthread_spin_lock(pthread_spinlock_t * __lock)\n/usr/include/pthread.h:517'
pthread_spin_trylock = _libraries['libftd2xx.so'].pthread_spin_trylock
pthread_spin_trylock.restype = c_int
pthread_spin_trylock.argtypes = [
 POINTER(pthread_spinlock_t)]
pthread_spin_trylock.__doc__ = 'int pthread_spin_trylock(pthread_spinlock_t * __lock)\n/usr/include/pthread.h:520'
pthread_spin_unlock = _libraries['libftd2xx.so'].pthread_spin_unlock
pthread_spin_unlock.restype = c_int
pthread_spin_unlock.argtypes = [
 POINTER(pthread_spinlock_t)]
pthread_spin_unlock.__doc__ = 'int pthread_spin_unlock(pthread_spinlock_t * __lock)\n/usr/include/pthread.h:523'
pthread_barrier_init = _libraries['libftd2xx.so'].pthread_barrier_init
pthread_barrier_init.restype = c_int
pthread_barrier_init.argtypes = [
 POINTER(pthread_barrier_t), POINTER(pthread_barrierattr_t), c_uint]
pthread_barrier_init.__doc__ = 'int pthread_barrier_init(unknown __barrier, unknown __attr, unsigned int __count)\n/usr/include/pthread.h:530'
pthread_barrier_destroy = _libraries['libftd2xx.so'].pthread_barrier_destroy
pthread_barrier_destroy.restype = c_int
pthread_barrier_destroy.argtypes = [
 POINTER(pthread_barrier_t)]
pthread_barrier_destroy.__doc__ = 'int pthread_barrier_destroy(pthread_barrier_t * __barrier)\n/usr/include/pthread.h:532'
pthread_barrierattr_init = _libraries['libftd2xx.so'].pthread_barrierattr_init
pthread_barrierattr_init.restype = c_int
pthread_barrierattr_init.argtypes = [
 POINTER(pthread_barrierattr_t)]
pthread_barrierattr_init.__doc__ = 'int pthread_barrierattr_init(pthread_barrierattr_t * __attr)\n/usr/include/pthread.h:534'
pthread_barrierattr_destroy = _libraries['libftd2xx.so'].pthread_barrierattr_destroy
pthread_barrierattr_destroy.restype = c_int
pthread_barrierattr_destroy.argtypes = [
 POINTER(pthread_barrierattr_t)]
pthread_barrierattr_destroy.__doc__ = 'int pthread_barrierattr_destroy(pthread_barrierattr_t * __attr)\n/usr/include/pthread.h:536'
pthread_barrierattr_getpshared = _libraries['libftd2xx.so'].pthread_barrierattr_getpshared
pthread_barrierattr_getpshared.restype = c_int
pthread_barrierattr_getpshared.argtypes = [
 POINTER(pthread_barrierattr_t), POINTER(c_int)]
pthread_barrierattr_getpshared.__doc__ = 'int pthread_barrierattr_getpshared(unknown __attr, unknown __pshared)\n/usr/include/pthread.h:540'
pthread_barrierattr_setpshared = _libraries['libftd2xx.so'].pthread_barrierattr_setpshared
pthread_barrierattr_setpshared.restype = c_int
pthread_barrierattr_setpshared.argtypes = [
 POINTER(pthread_barrierattr_t), c_int]
pthread_barrierattr_setpshared.__doc__ = 'int pthread_barrierattr_setpshared(pthread_barrierattr_t * __attr, int __pshared)\n/usr/include/pthread.h:543'
pthread_barrier_wait = _libraries['libftd2xx.so'].pthread_barrier_wait
pthread_barrier_wait.restype = c_int
pthread_barrier_wait.argtypes = [
 POINTER(pthread_barrier_t)]
pthread_barrier_wait.__doc__ = 'int pthread_barrier_wait(pthread_barrier_t * __barrier)\n/usr/include/pthread.h:545'
pthread_key_create = _libraries['libftd2xx.so'].pthread_key_create
pthread_key_create.restype = c_int
pthread_key_create.argtypes = [
 POINTER(pthread_key_t), CFUNCTYPE(None, c_void_p)]
pthread_key_create.__doc__ = 'int pthread_key_create(pthread_key_t * __key, unknown * __destr_function)\n/usr/include/pthread.h:558'
pthread_key_delete = _libraries['libftd2xx.so'].pthread_key_delete
pthread_key_delete.restype = c_int
pthread_key_delete.argtypes = [
 pthread_key_t]
pthread_key_delete.__doc__ = 'int pthread_key_delete(pthread_key_t __key)\n/usr/include/pthread.h:561'
pthread_setspecific = _libraries['libftd2xx.so'].pthread_setspecific
pthread_setspecific.restype = c_int
pthread_setspecific.argtypes = [
 pthread_key_t, c_void_p]
pthread_setspecific.__doc__ = 'int pthread_setspecific(pthread_key_t __key, unknown * __pointer)\n/usr/include/pthread.h:565'
pthread_getspecific = _libraries['libftd2xx.so'].pthread_getspecific
pthread_getspecific.restype = c_void_p
pthread_getspecific.argtypes = [
 pthread_key_t]
pthread_getspecific.__doc__ = 'void * pthread_getspecific(pthread_key_t __key)\n/usr/include/pthread.h:568'
pthread_once = _libraries['libftd2xx.so'].pthread_once
pthread_once.restype = c_int
pthread_once.argtypes = [
 POINTER(pthread_once_t), CFUNCTYPE(None)]
pthread_once.__doc__ = 'int pthread_once(pthread_once_t * __once_control, unknown * __init_routine)\n/usr/include/pthread.h:581'
pthread_setcancelstate = _libraries['libftd2xx.so'].pthread_setcancelstate
pthread_setcancelstate.restype = c_int
pthread_setcancelstate.argtypes = [
 c_int, POINTER(c_int)]
pthread_setcancelstate.__doc__ = 'int pthread_setcancelstate(int __state, int * __oldstate)\n/usr/include/pthread.h:588'
pthread_setcanceltype = _libraries['libftd2xx.so'].pthread_setcanceltype
pthread_setcanceltype.restype = c_int
pthread_setcanceltype.argtypes = [
 c_int, POINTER(c_int)]
pthread_setcanceltype.__doc__ = 'int pthread_setcanceltype(int __type, int * __oldtype)\n/usr/include/pthread.h:592'
pthread_cancel = _libraries['libftd2xx.so'].pthread_cancel
pthread_cancel.restype = c_int
pthread_cancel.argtypes = [
 pthread_t]
pthread_cancel.__doc__ = 'int pthread_cancel(pthread_t __cancelthread)\n/usr/include/pthread.h:595'
pthread_testcancel = _libraries['libftd2xx.so'].pthread_testcancel
pthread_testcancel.restype = None
pthread_testcancel.argtypes = []
pthread_testcancel.__doc__ = 'void pthread_testcancel()\n/usr/include/pthread.h:600'
_pthread_cleanup_push = _libraries['libftd2xx.so']._pthread_cleanup_push
_pthread_cleanup_push.restype = None
_pthread_cleanup_push.argtypes = [
 POINTER(_pthread_cleanup_buffer), CFUNCTYPE(None, c_void_p), c_void_p]
_pthread_cleanup_push.__doc__ = 'void _pthread_cleanup_push(_pthread_cleanup_buffer * __buffer, unknown * __routine, void * __arg)\n/usr/include/pthread.h:616'
_pthread_cleanup_pop = _libraries['libftd2xx.so']._pthread_cleanup_pop
_pthread_cleanup_pop.restype = None
_pthread_cleanup_pop.argtypes = [
 POINTER(_pthread_cleanup_buffer), c_int]
_pthread_cleanup_pop.__doc__ = 'void _pthread_cleanup_pop(_pthread_cleanup_buffer * __buffer, int __execute)\n/usr/include/pthread.h:625'
_pthread_cleanup_push_defer = _libraries['libftd2xx.so']._pthread_cleanup_push_defer
_pthread_cleanup_push_defer.restype = None
_pthread_cleanup_push_defer.argtypes = [
 POINTER(_pthread_cleanup_buffer), CFUNCTYPE(None, c_void_p), c_void_p]
_pthread_cleanup_push_defer.__doc__ = 'void _pthread_cleanup_push_defer(_pthread_cleanup_buffer * __buffer, unknown * __routine, void * __arg)\n/usr/include/pthread.h:637'
_pthread_cleanup_pop_restore = _libraries['libftd2xx.so']._pthread_cleanup_pop_restore
_pthread_cleanup_pop_restore.restype = None
_pthread_cleanup_pop_restore.argtypes = [
 POINTER(_pthread_cleanup_buffer), c_int]
_pthread_cleanup_pop_restore.__doc__ = 'void _pthread_cleanup_pop_restore(_pthread_cleanup_buffer * __buffer, int __execute)\n/usr/include/pthread.h:647'
pthread_getcpuclockid = _libraries['libftd2xx.so'].pthread_getcpuclockid
pthread_getcpuclockid.restype = c_int
pthread_getcpuclockid.argtypes = [
 pthread_t, POINTER(__clockid_t)]
pthread_getcpuclockid.__doc__ = 'int pthread_getcpuclockid(pthread_t __thread_id, __clockid_t * __clock_id)\n/usr/include/pthread.h:654'
sched_setparam = _libraries['libftd2xx.so'].sched_setparam
sched_setparam.restype = c_int
sched_setparam.argtypes = [
 __pid_t, POINTER(sched_param)]
sched_setparam.__doc__ = 'int sched_setparam(__pid_t __pid, unknown * __param)\n/usr/include/sched.h:41'
sched_getparam = _libraries['libftd2xx.so'].sched_getparam
sched_getparam.restype = c_int
sched_getparam.argtypes = [
 __pid_t, POINTER(sched_param)]
sched_getparam.__doc__ = 'int sched_getparam(__pid_t __pid, sched_param * __param)\n/usr/include/sched.h:44'
sched_setscheduler = _libraries['libftd2xx.so'].sched_setscheduler
sched_setscheduler.restype = c_int
sched_setscheduler.argtypes = [
 __pid_t, c_int, POINTER(sched_param)]
sched_setscheduler.__doc__ = 'int sched_setscheduler(__pid_t __pid, int __policy, unknown * __param)\n/usr/include/sched.h:48'
sched_getscheduler = _libraries['libftd2xx.so'].sched_getscheduler
sched_getscheduler.restype = c_int
sched_getscheduler.argtypes = [
 __pid_t]
sched_getscheduler.__doc__ = 'int sched_getscheduler(__pid_t __pid)\n/usr/include/sched.h:51'
sched_yield = _libraries['libftd2xx.so'].sched_yield
sched_yield.restype = c_int
sched_yield.argtypes = []
sched_yield.__doc__ = 'int sched_yield()\n/usr/include/sched.h:54'
sched_get_priority_max = _libraries['libftd2xx.so'].sched_get_priority_max
sched_get_priority_max.restype = c_int
sched_get_priority_max.argtypes = [
 c_int]
sched_get_priority_max.__doc__ = 'int sched_get_priority_max(int __algorithm)\n/usr/include/sched.h:57'
sched_get_priority_min = _libraries['libftd2xx.so'].sched_get_priority_min
sched_get_priority_min.restype = c_int
sched_get_priority_min.argtypes = [
 c_int]
sched_get_priority_min.__doc__ = 'int sched_get_priority_min(int __algorithm)\n/usr/include/sched.h:60'
sched_rr_get_interval = _libraries['libftd2xx.so'].sched_rr_get_interval
sched_rr_get_interval.restype = c_int
sched_rr_get_interval.argtypes = [
 __pid_t, POINTER(timespec)]
sched_rr_get_interval.__doc__ = 'int sched_rr_get_interval(__pid_t __pid, timespec * __t)\n/usr/include/sched.h:63'
sched_setaffinity = _libraries['libftd2xx.so'].sched_setaffinity
sched_setaffinity.restype = c_int
sched_setaffinity.argtypes = [
 __pid_t, size_t, POINTER(cpu_set_t)]
sched_setaffinity.__doc__ = 'int sched_setaffinity(__pid_t __pid, size_t __cpusetsize, unknown * __cpuset)\n/usr/include/sched.h:77'
sched_getaffinity = _libraries['libftd2xx.so'].sched_getaffinity
sched_getaffinity.restype = c_int
sched_getaffinity.argtypes = [
 __pid_t, size_t, POINTER(cpu_set_t)]
sched_getaffinity.__doc__ = 'int sched_getaffinity(__pid_t __pid, size_t __cpusetsize, cpu_set_t * __cpuset)\n/usr/include/sched.h:81'
sigset_t = __sigset_t
clock_t = __clock_t
time_t = __time_t
clockid_t = __clockid_t
timer_t = __timer_t

class tm(Structure):
    pass


tm._fields_ = [
 (
  'tm_sec', c_int),
 (
  'tm_min', c_int),
 (
  'tm_hour', c_int),
 (
  'tm_mday', c_int),
 (
  'tm_mon', c_int),
 (
  'tm_year', c_int),
 (
  'tm_wday', c_int),
 (
  'tm_yday', c_int),
 (
  'tm_isdst', c_int),
 (
  'tm_gmtoff', c_long),
 (
  'tm_zone', STRING)]

class itimerspec(Structure):
    pass


itimerspec._fields_ = [
 (
  'it_interval', timespec),
 (
  'it_value', timespec)]

class sigevent(Structure):
    pass


sigevent._fields_ = []
pid_t = __pid_t
clock = _libraries['libftd2xx.so'].clock
clock.restype = clock_t
clock.argtypes = []
clock.__doc__ = 'clock_t clock()\n/usr/include/time.h:181'
time = _libraries['libftd2xx.so'].time
time.restype = time_t
time.argtypes = [
 POINTER(time_t)]
time.__doc__ = 'time_t time(time_t * __timer)\n/usr/include/time.h:184'
difftime = _libraries['libftd2xx.so'].difftime
difftime.restype = c_double
difftime.argtypes = [
 time_t, time_t]
difftime.__doc__ = 'double difftime(time_t __time1, time_t __time0)\n/usr/include/time.h:188'
mktime = _libraries['libftd2xx.so'].mktime
mktime.restype = time_t
mktime.argtypes = [
 POINTER(tm)]
mktime.__doc__ = 'time_t mktime(tm * __tp)\n/usr/include/time.h:191'
strftime = _libraries['libftd2xx.so'].strftime
strftime.restype = size_t
strftime.argtypes = [
 STRING, size_t, STRING, POINTER(tm)]
strftime.__doc__ = 'size_t strftime(unknown __s, size_t __maxsize, unknown __format, unknown __tp)\n/usr/include/time.h:199'
strptime = _libraries['libftd2xx.so'].strptime
strptime.restype = STRING
strptime.argtypes = [
 STRING, STRING, POINTER(tm)]
strptime.__doc__ = 'char * strptime(unknown __s, unknown __fmt, tm * __tp)\n/usr/include/time.h:207'

class __locale_struct(Structure):
    pass


__locale_t = POINTER(__locale_struct)
strftime_l = _libraries['libftd2xx.so'].strftime_l
strftime_l.restype = size_t
strftime_l.argtypes = [
 STRING, size_t, STRING, POINTER(tm), __locale_t]
strftime_l.__doc__ = 'size_t strftime_l(unknown __s, size_t __maxsize, unknown __format, unknown __tp, __locale_t __loc)\n/usr/include/time.h:218'
strptime_l = _libraries['libftd2xx.so'].strptime_l
strptime_l.restype = STRING
strptime_l.argtypes = [
 STRING, STRING, POINTER(tm), __locale_t]
strptime_l.__doc__ = 'char * strptime_l(unknown __s, unknown __fmt, tm * __tp, __locale_t __loc)\n/usr/include/time.h:222'
gmtime = _libraries['libftd2xx.so'].gmtime
gmtime.restype = POINTER(tm)
gmtime.argtypes = [
 POINTER(time_t)]
gmtime.__doc__ = 'tm * gmtime(unknown * __timer)\n/usr/include/time.h:229'
localtime = _libraries['libftd2xx.so'].localtime
localtime.restype = POINTER(tm)
localtime.argtypes = [
 POINTER(time_t)]
localtime.__doc__ = 'tm * localtime(unknown * __timer)\n/usr/include/time.h:233'
gmtime_r = _libraries['libftd2xx.so'].gmtime_r
gmtime_r.restype = POINTER(tm)
gmtime_r.argtypes = [
 POINTER(time_t), POINTER(tm)]
gmtime_r.__doc__ = 'tm * gmtime_r(unknown __timer, unknown __tp)\n/usr/include/time.h:240'
localtime_r = _libraries['libftd2xx.so'].localtime_r
localtime_r.restype = POINTER(tm)
localtime_r.argtypes = [
 POINTER(time_t), POINTER(tm)]
localtime_r.__doc__ = 'tm * localtime_r(unknown __timer, unknown __tp)\n/usr/include/time.h:245'
asctime = _libraries['libftd2xx.so'].asctime
asctime.restype = STRING
asctime.argtypes = [
 POINTER(tm)]
asctime.__doc__ = 'char * asctime(unknown * __tp)\n/usr/include/time.h:251'
ctime = _libraries['libftd2xx.so'].ctime
ctime.restype = STRING
ctime.argtypes = [
 POINTER(time_t)]
ctime.__doc__ = 'char * ctime(unknown * __timer)\n/usr/include/time.h:254'
asctime_r = _libraries['libftd2xx.so'].asctime_r
asctime_r.restype = STRING
asctime_r.argtypes = [
 POINTER(tm), STRING]
asctime_r.__doc__ = 'char * asctime_r(unknown __tp, unknown __buf)\n/usr/include/time.h:263'
ctime_r = _libraries['libftd2xx.so'].ctime_r
ctime_r.restype = STRING
ctime_r.argtypes = [
 POINTER(time_t), STRING]
ctime_r.__doc__ = 'char * ctime_r(unknown __timer, unknown __buf)\n/usr/include/time.h:267'
tzset = _libraries['libftd2xx.so'].tzset
tzset.restype = None
tzset.argtypes = []
tzset.__doc__ = 'void tzset()\n/usr/include/time.h:283'
stime = _libraries['libftd2xx.so'].stime
stime.restype = c_int
stime.argtypes = [
 POINTER(time_t)]
stime.__doc__ = 'int stime(unknown * __when)\n/usr/include/time.h:294'
timegm = _libraries['libftd2xx.so'].timegm
timegm.restype = time_t
timegm.argtypes = [
 POINTER(tm)]
timegm.__doc__ = 'time_t timegm(tm * __tp)\n/usr/include/time.h:309'
timelocal = _libraries['libftd2xx.so'].timelocal
timelocal.restype = time_t
timelocal.argtypes = [
 POINTER(tm)]
timelocal.__doc__ = 'time_t timelocal(tm * __tp)\n/usr/include/time.h:312'
dysize = _libraries['libftd2xx.so'].dysize
dysize.restype = c_int
dysize.argtypes = [
 c_int]
dysize.__doc__ = 'int dysize(int __year)\n/usr/include/time.h:315'
nanosleep = _libraries['libftd2xx.so'].nanosleep
nanosleep.restype = c_int
nanosleep.argtypes = [
 POINTER(timespec), POINTER(timespec)]
nanosleep.__doc__ = 'int nanosleep(unknown * __requested_time, timespec * __remaining)\n/usr/include/time.h:325'
getdate = _libraries['libftd2xx.so'].getdate
getdate.restype = POINTER(tm)
getdate.argtypes = [
 STRING]
getdate.__doc__ = 'tm * getdate(unknown * __string)\n/usr/include/time.h:395'
getdate_r = _libraries['libftd2xx.so'].getdate_r
getdate_r.restype = c_int
getdate_r.argtypes = [
 STRING, POINTER(tm)]
getdate_r.__doc__ = 'int getdate_r(unknown __string, unknown __resbufp)\n/usr/include/time.h:410'

class locale_data(Structure):
    pass


__locale_struct._fields_ = [
 (
  '__locales', POINTER(locale_data) * 13),
 (
  '__ctype_b', POINTER(c_ushort)),
 (
  '__ctype_tolower', POINTER(c_int)),
 (
  '__ctype_toupper', POINTER(c_int)),
 (
  '__names', STRING * 13)]
locale_data._fields_ = []
DWORD = c_ulong
ULONG = c_ulong
USHORT = c_ushort
SHORT = c_short
UCHAR = c_ubyte
WORD = c_ushort
BYTE = c_ubyte
LPBYTE = POINTER(c_ubyte)
BOOL = c_int
BOOLEAN = c_char
CHAR = c_char
LPBOOL = POINTER(c_int)
PUCHAR = POINTER(c_ubyte)
LPCSTR = STRING
PCHAR = STRING
PVOID = c_void_p
HANDLE = c_void_p
LONG = c_long
INT = c_int
UINT = c_uint
LPSTR = STRING
LPTSTR = STRING
LPDWORD = POINTER(DWORD)
LPWORD = POINTER(WORD)
PULONG = POINTER(ULONG)
LPVOID = PVOID
VOID = None
ULONGLONG = c_ulonglong

class _OVERLAPPED(Structure):
    pass


_OVERLAPPED._fields_ = [
 (
  'Internal', DWORD),
 (
  'InternalHigh', DWORD),
 (
  'Offset', DWORD),
 (
  'OffsetHigh', DWORD),
 (
  'hEvent', HANDLE)]
LPOVERLAPPED = POINTER(_OVERLAPPED)
OVERLAPPED = _OVERLAPPED

class _SECURITY_ATTRIBUTES(Structure):
    pass


_SECURITY_ATTRIBUTES._fields_ = [
 (
  'nLength', DWORD),
 (
  'lpSecurityDescriptor', LPVOID),
 (
  'bInheritHandle', BOOL)]
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES

class timeval(Structure):
    pass


SYSTEMTIME = timeval
timeval._fields_ = []
FILETIME = timeval

class _EVENT_HANDLE(Structure):
    pass


_EVENT_HANDLE._fields_ = [
 (
  'eCondVar', pthread_cond_t),
 (
  'eMutex', pthread_mutex_t),
 (
  'iVar', c_int)]
EVENT_HANDLE = _EVENT_HANDLE
FT_HANDLE = POINTER(DWORD)
FT_STATUS = ULONG
PFT_EVENT_HANDLER = CFUNCTYPE(None, c_ulong, c_ulong)
FT_DEVICE = ULONG
FT_Open = _libraries['libftd2xx.so'].FT_Open
FT_Open.restype = FT_STATUS
FT_Open.argtypes = [
 c_int, POINTER(FT_HANDLE)]
FT_Open.__doc__ = 'FT_STATUS FT_Open(int deviceNumber, FT_HANDLE * pHandle)\nftd2xx_linux.h:220'
FT_OpenEx = _libraries['libftd2xx.so'].FT_OpenEx
FT_OpenEx.restype = FT_STATUS
FT_OpenEx.argtypes = [
 PVOID, DWORD, POINTER(FT_HANDLE)]
FT_OpenEx.__doc__ = 'FT_STATUS FT_OpenEx(PVOID pArg1, DWORD Flags, FT_HANDLE * pHandle)\nftd2xx_linux.h:227'
FT_ListDevices = _libraries['libftd2xx.so'].FT_ListDevices
FT_ListDevices.restype = FT_STATUS
FT_ListDevices.argtypes = [
 PVOID, PVOID, DWORD]
FT_ListDevices.__doc__ = 'FT_STATUS FT_ListDevices(PVOID pArg1, PVOID pArg2, DWORD Flags)\nftd2xx_linux.h:234'
FT_SetVIDPID = _libraries['libftd2xx.so'].FT_SetVIDPID
FT_SetVIDPID.restype = FT_STATUS
FT_SetVIDPID.argtypes = [
 DWORD, DWORD]
FT_SetVIDPID.__doc__ = 'FT_STATUS FT_SetVIDPID(DWORD dwVID, DWORD dwPID)\nftd2xx_linux.h:240'
FT_GetVIDPID = _libraries['libftd2xx.so'].FT_GetVIDPID
FT_GetVIDPID.restype = FT_STATUS
FT_GetVIDPID.argtypes = [
 POINTER(DWORD), POINTER(DWORD)]
FT_GetVIDPID.__doc__ = 'FT_STATUS FT_GetVIDPID(DWORD * pdwVID, DWORD * pdwPID)\nftd2xx_linux.h:246'
FT_Close = _libraries['libftd2xx.so'].FT_Close
FT_Close.restype = FT_STATUS
FT_Close.argtypes = [
 FT_HANDLE]
FT_Close.__doc__ = 'FT_STATUS FT_Close(FT_HANDLE ftHandle)\nftd2xx_linux.h:251'
FT_Read = _libraries['libftd2xx.so'].FT_Read
FT_Read.restype = FT_STATUS
FT_Read.argtypes = [
 FT_HANDLE, LPVOID, DWORD, LPDWORD]
FT_Read.__doc__ = 'FT_STATUS FT_Read(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD nBufferSize, LPDWORD lpBytesReturned)\nftd2xx_linux.h:259'
FT_Write = _libraries['libftd2xx.so'].FT_Write
FT_Write.restype = FT_STATUS
FT_Write.argtypes = [
 FT_HANDLE, LPVOID, DWORD, LPDWORD]
FT_Write.__doc__ = 'FT_STATUS FT_Write(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD nBufferSize, LPDWORD lpBytesWritten)\nftd2xx_linux.h:267'
FT_IoCtl = _libraries['libftd2xx.so'].FT_IoCtl
FT_IoCtl.restype = FT_STATUS
FT_IoCtl.argtypes = [
 FT_HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
FT_IoCtl.__doc__ = 'FT_STATUS FT_IoCtl(FT_HANDLE ftHandle, DWORD dwIoControlCode, LPVOID lpInBuf, DWORD nInBufSize, LPVOID lpOutBuf, DWORD nOutBufSize, LPDWORD lpBytesReturned, LPOVERLAPPED lpOverlapped)\nftd2xx_linux.h:279'
FT_SetBaudRate = _libraries['libftd2xx.so'].FT_SetBaudRate
FT_SetBaudRate.restype = FT_STATUS
FT_SetBaudRate.argtypes = [
 FT_HANDLE, ULONG]
FT_SetBaudRate.__doc__ = 'FT_STATUS FT_SetBaudRate(FT_HANDLE ftHandle, ULONG BaudRate)\nftd2xx_linux.h:285'
FT_SetDivisor = _libraries['libftd2xx.so'].FT_SetDivisor
FT_SetDivisor.restype = FT_STATUS
FT_SetDivisor.argtypes = [
 FT_HANDLE, USHORT]
FT_SetDivisor.__doc__ = 'FT_STATUS FT_SetDivisor(FT_HANDLE ftHandle, USHORT Divisor)\nftd2xx_linux.h:291'
FT_SetDataCharacteristics = _libraries['libftd2xx.so'].FT_SetDataCharacteristics
FT_SetDataCharacteristics.restype = FT_STATUS
FT_SetDataCharacteristics.argtypes = [
 FT_HANDLE, UCHAR, UCHAR, UCHAR]
FT_SetDataCharacteristics.__doc__ = 'FT_STATUS FT_SetDataCharacteristics(FT_HANDLE ftHandle, UCHAR WordLength, UCHAR StopBits, UCHAR Parity)\nftd2xx_linux.h:299'
FT_SetFlowControl = _libraries['libftd2xx.so'].FT_SetFlowControl
FT_SetFlowControl.restype = FT_STATUS
FT_SetFlowControl.argtypes = [
 FT_HANDLE, USHORT, UCHAR, UCHAR]
FT_SetFlowControl.__doc__ = 'FT_STATUS FT_SetFlowControl(FT_HANDLE ftHandle, USHORT FlowControl, UCHAR XonChar, UCHAR XoffChar)\nftd2xx_linux.h:307'
FT_ResetDevice = _libraries['libftd2xx.so'].FT_ResetDevice
FT_ResetDevice.restype = FT_STATUS
FT_ResetDevice.argtypes = [
 FT_HANDLE]
FT_ResetDevice.__doc__ = 'FT_STATUS FT_ResetDevice(FT_HANDLE ftHandle)\nftd2xx_linux.h:312'
FT_SetDtr = _libraries['libftd2xx.so'].FT_SetDtr
FT_SetDtr.restype = FT_STATUS
FT_SetDtr.argtypes = [
 FT_HANDLE]
FT_SetDtr.__doc__ = 'FT_STATUS FT_SetDtr(FT_HANDLE ftHandle)\nftd2xx_linux.h:317'
FT_ClrDtr = _libraries['libftd2xx.so'].FT_ClrDtr
FT_ClrDtr.restype = FT_STATUS
FT_ClrDtr.argtypes = [
 FT_HANDLE]
FT_ClrDtr.__doc__ = 'FT_STATUS FT_ClrDtr(FT_HANDLE ftHandle)\nftd2xx_linux.h:322'
FT_SetRts = _libraries['libftd2xx.so'].FT_SetRts
FT_SetRts.restype = FT_STATUS
FT_SetRts.argtypes = [
 FT_HANDLE]
FT_SetRts.__doc__ = 'FT_STATUS FT_SetRts(FT_HANDLE ftHandle)\nftd2xx_linux.h:327'
FT_ClrRts = _libraries['libftd2xx.so'].FT_ClrRts
FT_ClrRts.restype = FT_STATUS
FT_ClrRts.argtypes = [
 FT_HANDLE]
FT_ClrRts.__doc__ = 'FT_STATUS FT_ClrRts(FT_HANDLE ftHandle)\nftd2xx_linux.h:332'
FT_GetModemStatus = _libraries['libftd2xx.so'].FT_GetModemStatus
FT_GetModemStatus.restype = FT_STATUS
FT_GetModemStatus.argtypes = [
 FT_HANDLE, POINTER(ULONG)]
FT_GetModemStatus.__doc__ = 'FT_STATUS FT_GetModemStatus(FT_HANDLE ftHandle, ULONG * pModemStatus)\nftd2xx_linux.h:338'
FT_SetChars = _libraries['libftd2xx.so'].FT_SetChars
FT_SetChars.restype = FT_STATUS
FT_SetChars.argtypes = [
 FT_HANDLE, UCHAR, UCHAR, UCHAR, UCHAR]
FT_SetChars.__doc__ = 'FT_STATUS FT_SetChars(FT_HANDLE ftHandle, UCHAR EventChar, UCHAR EventCharEnabled, UCHAR ErrorChar, UCHAR ErrorCharEnabled)\nftd2xx_linux.h:347'
FT_Purge = _libraries['libftd2xx.so'].FT_Purge
FT_Purge.restype = FT_STATUS
FT_Purge.argtypes = [
 FT_HANDLE, ULONG]
FT_Purge.__doc__ = 'FT_STATUS FT_Purge(FT_HANDLE ftHandle, ULONG Mask)\nftd2xx_linux.h:353'
FT_SetTimeouts = _libraries['libftd2xx.so'].FT_SetTimeouts
FT_SetTimeouts.restype = FT_STATUS
FT_SetTimeouts.argtypes = [
 FT_HANDLE, ULONG, ULONG]
FT_SetTimeouts.__doc__ = 'FT_STATUS FT_SetTimeouts(FT_HANDLE ftHandle, ULONG ReadTimeout, ULONG WriteTimeout)\nftd2xx_linux.h:360'
FT_GetQueueStatus = _libraries['libftd2xx.so'].FT_GetQueueStatus
FT_GetQueueStatus.restype = FT_STATUS
FT_GetQueueStatus.argtypes = [
 FT_HANDLE, POINTER(DWORD)]
FT_GetQueueStatus.__doc__ = 'FT_STATUS FT_GetQueueStatus(FT_HANDLE ftHandle, DWORD * dwRxBytes)\nftd2xx_linux.h:366'
FT_SetEventNotification = _libraries['libftd2xx.so'].FT_SetEventNotification
FT_SetEventNotification.restype = FT_STATUS
FT_SetEventNotification.argtypes = [
 FT_HANDLE, DWORD, PVOID]
FT_SetEventNotification.__doc__ = 'FT_STATUS FT_SetEventNotification(FT_HANDLE ftHandle, DWORD Mask, PVOID Param)\nftd2xx_linux.h:373'
FT_GetStatus = _libraries['libftd2xx.so'].FT_GetStatus
FT_GetStatus.restype = FT_STATUS
FT_GetStatus.argtypes = [
 FT_HANDLE, POINTER(DWORD), POINTER(DWORD), POINTER(DWORD)]
FT_GetStatus.__doc__ = 'FT_STATUS FT_GetStatus(FT_HANDLE ftHandle, DWORD * dwRxBytes, DWORD * dwTxBytes, DWORD * dwEventDWord)\nftd2xx_linux.h:381'
FT_SetBreakOn = _libraries['libftd2xx.so'].FT_SetBreakOn
FT_SetBreakOn.restype = FT_STATUS
FT_SetBreakOn.argtypes = [
 FT_HANDLE]
FT_SetBreakOn.__doc__ = 'FT_STATUS FT_SetBreakOn(FT_HANDLE ftHandle)\nftd2xx_linux.h:386'
FT_SetBreakOff = _libraries['libftd2xx.so'].FT_SetBreakOff
FT_SetBreakOff.restype = FT_STATUS
FT_SetBreakOff.argtypes = [
 FT_HANDLE]
FT_SetBreakOff.__doc__ = 'FT_STATUS FT_SetBreakOff(FT_HANDLE ftHandle)\nftd2xx_linux.h:391'
FT_SetWaitMask = _libraries['libftd2xx.so'].FT_SetWaitMask
FT_SetWaitMask.restype = FT_STATUS
FT_SetWaitMask.argtypes = [
 FT_HANDLE, DWORD]
FT_SetWaitMask.__doc__ = 'FT_STATUS FT_SetWaitMask(FT_HANDLE ftHandle, DWORD Mask)\nftd2xx_linux.h:397'
FT_WaitOnMask = _libraries['libftd2xx.so'].FT_WaitOnMask
FT_WaitOnMask.restype = FT_STATUS
FT_WaitOnMask.argtypes = [
 FT_HANDLE, POINTER(DWORD)]
FT_WaitOnMask.__doc__ = 'FT_STATUS FT_WaitOnMask(FT_HANDLE ftHandle, DWORD * Mask)\nftd2xx_linux.h:403'
FT_GetEventStatus = _libraries['libftd2xx.so'].FT_GetEventStatus
FT_GetEventStatus.restype = FT_STATUS
FT_GetEventStatus.argtypes = [
 FT_HANDLE, POINTER(DWORD)]
FT_GetEventStatus.__doc__ = 'FT_STATUS FT_GetEventStatus(FT_HANDLE ftHandle, DWORD * dwEventDWord)\nftd2xx_linux.h:409'
FT_ReadEE = _libraries['libftd2xx.so'].FT_ReadEE
FT_ReadEE.restype = FT_STATUS
FT_ReadEE.argtypes = [
 FT_HANDLE, DWORD, LPWORD]
FT_ReadEE.__doc__ = 'FT_STATUS FT_ReadEE(FT_HANDLE ftHandle, DWORD dwWordOffset, LPWORD lpwValue)\nftd2xx_linux.h:416'
FT_WriteEE = _libraries['libftd2xx.so'].FT_WriteEE
FT_WriteEE.restype = FT_STATUS
FT_WriteEE.argtypes = [
 FT_HANDLE, DWORD, WORD]
FT_WriteEE.__doc__ = 'FT_STATUS FT_WriteEE(FT_HANDLE ftHandle, DWORD dwWordOffset, WORD wValue)\nftd2xx_linux.h:423'
FT_EraseEE = _libraries['libftd2xx.so'].FT_EraseEE
FT_EraseEE.restype = FT_STATUS
FT_EraseEE.argtypes = [
 FT_HANDLE]
FT_EraseEE.__doc__ = 'FT_STATUS FT_EraseEE(FT_HANDLE ftHandle)\nftd2xx_linux.h:428'

class ft_program_data(Structure):
    pass


ft_program_data._fields_ = [
 (
  'Signature1', DWORD),
 (
  'Signature2', DWORD),
 (
  'Version', DWORD),
 (
  'VendorId', WORD),
 (
  'ProductId', WORD),
 (
  'Manufacturer', STRING),
 (
  'ManufacturerId', STRING),
 (
  'Description', STRING),
 (
  'SerialNumber', STRING),
 (
  'MaxPower', WORD),
 (
  'PnP', WORD),
 (
  'SelfPowered', WORD),
 (
  'RemoteWakeup', WORD),
 (
  'Rev4', UCHAR),
 (
  'IsoIn', UCHAR),
 (
  'IsoOut', UCHAR),
 (
  'PullDownEnable', UCHAR),
 (
  'SerNumEnable', UCHAR),
 (
  'USBVersionEnable', UCHAR),
 (
  'USBVersion', WORD),
 (
  'Rev5', UCHAR),
 (
  'IsoInA', UCHAR),
 (
  'IsoInB', UCHAR),
 (
  'IsoOutA', UCHAR),
 (
  'IsoOutB', UCHAR),
 (
  'PullDownEnable5', UCHAR),
 (
  'SerNumEnable5', UCHAR),
 (
  'USBVersionEnable5', UCHAR),
 (
  'USBVersion5', WORD),
 (
  'AIsHighCurrent', UCHAR),
 (
  'BIsHighCurrent', UCHAR),
 (
  'IFAIsFifo', UCHAR),
 (
  'IFAIsFifoTar', UCHAR),
 (
  'IFAIsFastSer', UCHAR),
 (
  'AIsVCP', UCHAR),
 (
  'IFBIsFifo', UCHAR),
 (
  'IFBIsFifoTar', UCHAR),
 (
  'IFBIsFastSer', UCHAR),
 (
  'BIsVCP', UCHAR),
 (
  'UseExtOsc', UCHAR),
 (
  'HighDriveIOs', UCHAR),
 (
  'EndpointSize', UCHAR),
 (
  'PullDownEnableR', UCHAR),
 (
  'SerNumEnableR', UCHAR),
 (
  'InvertTXD', UCHAR),
 (
  'InvertRXD', UCHAR),
 (
  'InvertRTS', UCHAR),
 (
  'InvertCTS', UCHAR),
 (
  'InvertDTR', UCHAR),
 (
  'InvertDSR', UCHAR),
 (
  'InvertDCD', UCHAR),
 (
  'InvertRI', UCHAR),
 (
  'Cbus0', UCHAR),
 (
  'Cbus1', UCHAR),
 (
  'Cbus2', UCHAR),
 (
  'Cbus3', UCHAR),
 (
  'Cbus4', UCHAR),
 (
  'RIsVCP', UCHAR)]
PFT_PROGRAM_DATA = POINTER(ft_program_data)
FT_PROGRAM_DATA = ft_program_data
FT_EE_Program = _libraries['libftd2xx.so'].FT_EE_Program
FT_EE_Program.restype = FT_STATUS
FT_EE_Program.argtypes = [
 FT_HANDLE, PFT_PROGRAM_DATA]
FT_EE_Program.__doc__ = 'FT_STATUS FT_EE_Program(FT_HANDLE ftHandle, PFT_PROGRAM_DATA pData)\nftd2xx_linux.h:518'
FT_EE_ProgramEx = _libraries['libftd2xx.so'].FT_EE_ProgramEx
FT_EE_ProgramEx.restype = FT_STATUS
FT_EE_ProgramEx.argtypes = [
 FT_HANDLE, PFT_PROGRAM_DATA, STRING, STRING, STRING, STRING]
FT_EE_ProgramEx.__doc__ = 'FT_STATUS FT_EE_ProgramEx(FT_HANDLE ftHandle, PFT_PROGRAM_DATA lpData, char * Manufacturer, char * ManufacturerId, char * Description, char * SerialNumber)\nftd2xx_linux.h:528'
FT_EE_Read = _libraries['libftd2xx.so'].FT_EE_Read
FT_EE_Read.restype = FT_STATUS
FT_EE_Read.argtypes = [
 FT_HANDLE, PFT_PROGRAM_DATA]
FT_EE_Read.__doc__ = 'FT_STATUS FT_EE_Read(FT_HANDLE ftHandle, PFT_PROGRAM_DATA pData)\nftd2xx_linux.h:534'
FT_EE_ReadEx = _libraries['libftd2xx.so'].FT_EE_ReadEx
FT_EE_ReadEx.restype = FT_STATUS
FT_EE_ReadEx.argtypes = [
 FT_HANDLE, PFT_PROGRAM_DATA, STRING, STRING, STRING, STRING]
FT_EE_ReadEx.__doc__ = 'FT_STATUS FT_EE_ReadEx(FT_HANDLE ftHandle, PFT_PROGRAM_DATA lpData, char * Manufacturer, char * ManufacturerId, char * Description, char * SerialNumber)\nftd2xx_linux.h:544'
FT_EE_UASize = _libraries['libftd2xx.so'].FT_EE_UASize
FT_EE_UASize.restype = FT_STATUS
FT_EE_UASize.argtypes = [
 FT_HANDLE, LPDWORD]
FT_EE_UASize.__doc__ = 'FT_STATUS FT_EE_UASize(FT_HANDLE ftHandle, LPDWORD lpdwSize)\nftd2xx_linux.h:550'
FT_EE_UAWrite = _libraries['libftd2xx.so'].FT_EE_UAWrite
FT_EE_UAWrite.restype = FT_STATUS
FT_EE_UAWrite.argtypes = [
 FT_HANDLE, PUCHAR, DWORD]
FT_EE_UAWrite.__doc__ = 'FT_STATUS FT_EE_UAWrite(FT_HANDLE ftHandle, PUCHAR pucData, DWORD dwDataLen)\nftd2xx_linux.h:557'
FT_EE_UARead = _libraries['libftd2xx.so'].FT_EE_UARead
FT_EE_UARead.restype = FT_STATUS
FT_EE_UARead.argtypes = [
 FT_HANDLE, PUCHAR, DWORD, LPDWORD]
FT_EE_UARead.__doc__ = 'FT_STATUS FT_EE_UARead(FT_HANDLE ftHandle, PUCHAR pucData, DWORD dwDataLen, LPDWORD lpdwBytesRead)\nftd2xx_linux.h:565'
FT_SetLatencyTimer = _libraries['libftd2xx.so'].FT_SetLatencyTimer
FT_SetLatencyTimer.restype = FT_STATUS
FT_SetLatencyTimer.argtypes = [
 FT_HANDLE, UCHAR]
FT_SetLatencyTimer.__doc__ = 'FT_STATUS FT_SetLatencyTimer(FT_HANDLE ftHandle, UCHAR ucLatency)\nftd2xx_linux.h:571'
FT_GetLatencyTimer = _libraries['libftd2xx.so'].FT_GetLatencyTimer
FT_GetLatencyTimer.restype = FT_STATUS
FT_GetLatencyTimer.argtypes = [
 FT_HANDLE, PUCHAR]
FT_GetLatencyTimer.__doc__ = 'FT_STATUS FT_GetLatencyTimer(FT_HANDLE ftHandle, PUCHAR pucLatency)\nftd2xx_linux.h:577'
FT_SetBitMode = _libraries['libftd2xx.so'].FT_SetBitMode
FT_SetBitMode.restype = FT_STATUS
FT_SetBitMode.argtypes = [
 FT_HANDLE, UCHAR, UCHAR]
FT_SetBitMode.__doc__ = 'FT_STATUS FT_SetBitMode(FT_HANDLE ftHandle, UCHAR ucMask, UCHAR ucEnable)\nftd2xx_linux.h:584'
FT_GetBitMode = _libraries['libftd2xx.so'].FT_GetBitMode
FT_GetBitMode.restype = FT_STATUS
FT_GetBitMode.argtypes = [
 FT_HANDLE, PUCHAR]
FT_GetBitMode.__doc__ = 'FT_STATUS FT_GetBitMode(FT_HANDLE ftHandle, PUCHAR pucMode)\nftd2xx_linux.h:590'
FT_SetUSBParameters = _libraries['libftd2xx.so'].FT_SetUSBParameters
FT_SetUSBParameters.restype = FT_STATUS
FT_SetUSBParameters.argtypes = [
 FT_HANDLE, ULONG, ULONG]
FT_SetUSBParameters.__doc__ = 'FT_STATUS FT_SetUSBParameters(FT_HANDLE ftHandle, ULONG ulInTransferSize, ULONG ulOutTransferSize)\nftd2xx_linux.h:597'
FT_SetDeadmanTimeout = _libraries['libftd2xx.so'].FT_SetDeadmanTimeout
FT_SetDeadmanTimeout.restype = FT_STATUS
FT_SetDeadmanTimeout.argtypes = [
 FT_HANDLE, ULONG]
FT_SetDeadmanTimeout.__doc__ = 'FT_STATUS FT_SetDeadmanTimeout(FT_HANDLE ftHandle, ULONG ulDeadmanTimeout)\nftd2xx_linux.h:603'
FT_GetDeviceInfo = _libraries['libftd2xx.so'].FT_GetDeviceInfo
FT_GetDeviceInfo.restype = FT_STATUS
FT_GetDeviceInfo.argtypes = [
 FT_HANDLE, POINTER(FT_DEVICE), LPDWORD, PCHAR, PCHAR, LPVOID]
FT_GetDeviceInfo.__doc__ = 'FT_STATUS FT_GetDeviceInfo(FT_HANDLE ftHandle, FT_DEVICE * lpftDevice, LPDWORD lpdwID, PCHAR SerialNumber, PCHAR Description, LPVOID Dummy)\nftd2xx_linux.h:613'
FT_StopInTask = _libraries['libftd2xx.so'].FT_StopInTask
FT_StopInTask.restype = FT_STATUS
FT_StopInTask.argtypes = [
 FT_HANDLE]
FT_StopInTask.__doc__ = 'FT_STATUS FT_StopInTask(FT_HANDLE ftHandle)\nftd2xx_linux.h:618'
FT_RestartInTask = _libraries['libftd2xx.so'].FT_RestartInTask
FT_RestartInTask.restype = FT_STATUS
FT_RestartInTask.argtypes = [
 FT_HANDLE]
FT_RestartInTask.__doc__ = 'FT_STATUS FT_RestartInTask(FT_HANDLE ftHandle)\nftd2xx_linux.h:623'
FT_SetResetPipeRetryCount = _libraries['libftd2xx.so'].FT_SetResetPipeRetryCount
FT_SetResetPipeRetryCount.restype = FT_STATUS
FT_SetResetPipeRetryCount.argtypes = [
 FT_HANDLE, DWORD]
FT_SetResetPipeRetryCount.__doc__ = 'FT_STATUS FT_SetResetPipeRetryCount(FT_HANDLE ftHandle, DWORD dwCount)\nftd2xx_linux.h:629'
FT_ResetPort = _libraries['libftd2xx.so'].FT_ResetPort
FT_ResetPort.restype = FT_STATUS
FT_ResetPort.argtypes = [
 FT_HANDLE]
FT_ResetPort.__doc__ = 'FT_STATUS FT_ResetPort(FT_HANDLE ftHandle)\nftd2xx_linux.h:634'
FT_CyclePort = _libraries['libftd2xx.so'].FT_CyclePort
FT_CyclePort.restype = FT_STATUS
FT_CyclePort.argtypes = [
 FT_HANDLE]
FT_CyclePort.__doc__ = 'FT_STATUS FT_CyclePort(FT_HANDLE ftHandle)\nftd2xx_linux.h:639'
FT_W32_CreateFile = _libraries['libftd2xx.so'].FT_W32_CreateFile
FT_W32_CreateFile.restype = FT_HANDLE
FT_W32_CreateFile.argtypes = [
 LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]
FT_W32_CreateFile.__doc__ = 'FT_HANDLE FT_W32_CreateFile(LPCSTR lpszName, DWORD dwAccess, DWORD dwShareMode, LPSECURITY_ATTRIBUTES lpSecurityAttributes, DWORD dwCreate, DWORD dwAttrsAndFlags, HANDLE hTemplate)\nftd2xx_linux.h:655'
FT_W32_CloseHandle = _libraries['libftd2xx.so'].FT_W32_CloseHandle
FT_W32_CloseHandle.restype = BOOL
FT_W32_CloseHandle.argtypes = [
 FT_HANDLE]
FT_W32_CloseHandle.__doc__ = 'BOOL FT_W32_CloseHandle(FT_HANDLE ftHandle)\nftd2xx_linux.h:660'
FT_W32_ReadFile = _libraries['libftd2xx.so'].FT_W32_ReadFile
FT_W32_ReadFile.restype = BOOL
FT_W32_ReadFile.argtypes = [
 FT_HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
FT_W32_ReadFile.__doc__ = 'BOOL FT_W32_ReadFile(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD nBufferSize, LPDWORD lpBytesReturned, LPOVERLAPPED lpOverlapped)\nftd2xx_linux.h:669'
FT_W32_WriteFile = _libraries['libftd2xx.so'].FT_W32_WriteFile
FT_W32_WriteFile.restype = BOOL
FT_W32_WriteFile.argtypes = [
 FT_HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
FT_W32_WriteFile.__doc__ = 'BOOL FT_W32_WriteFile(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD nBufferSize, LPDWORD lpBytesWritten, LPOVERLAPPED lpOverlapped)\nftd2xx_linux.h:678'
FT_W32_GetLastError = _libraries['libftd2xx.so'].FT_W32_GetLastError
FT_W32_GetLastError.restype = DWORD
FT_W32_GetLastError.argtypes = [
 FT_HANDLE]
FT_W32_GetLastError.__doc__ = 'DWORD FT_W32_GetLastError(FT_HANDLE ftHandle)\nftd2xx_linux.h:683'
FT_W32_GetOverlappedResult = _libraries['libftd2xx.so'].FT_W32_GetOverlappedResult
FT_W32_GetOverlappedResult.restype = BOOL
FT_W32_GetOverlappedResult.argtypes = [
 FT_HANDLE, LPOVERLAPPED, LPDWORD, BOOL]
FT_W32_GetOverlappedResult.__doc__ = 'BOOL FT_W32_GetOverlappedResult(FT_HANDLE ftHandle, LPOVERLAPPED lpOverlapped, LPDWORD lpdwBytesTransferred, BOOL bWait)\nftd2xx_linux.h:691'
FT_W32_CancelIo = _libraries['libftd2xx.so'].FT_W32_CancelIo
FT_W32_CancelIo.restype = BOOL
FT_W32_CancelIo.argtypes = [
 FT_HANDLE]
FT_W32_CancelIo.__doc__ = 'BOOL FT_W32_CancelIo(FT_HANDLE ftHandle)\nftd2xx_linux.h:696'

class _FTCOMSTAT(Structure):
    pass


_FTCOMSTAT._fields_ = [
 (
  'fCtsHold', DWORD, 1),
 (
  'fDsrHold', DWORD, 1),
 (
  'fRlsdHold', DWORD, 1),
 (
  'fXoffHold', DWORD, 1),
 (
  'fXoffSent', DWORD, 1),
 (
  'fEof', DWORD, 1),
 (
  'fTxim', DWORD, 1),
 (
  'fReserved', DWORD, 25),
 (
  'cbInQue', DWORD),
 (
  'cbOutQue', DWORD)]
LPFTCOMSTAT = POINTER(_FTCOMSTAT)
FTCOMSTAT = _FTCOMSTAT

class _FTDCB(Structure):
    pass


_FTDCB._fields_ = [
 (
  'DCBlength', DWORD),
 (
  'BaudRate', DWORD),
 (
  'fBinary', DWORD, 1),
 (
  'fParity', DWORD, 1),
 (
  'fOutxCtsFlow', DWORD, 1),
 (
  'fOutxDsrFlow', DWORD, 1),
 (
  'fDtrControl', DWORD, 2),
 (
  'fDsrSensitivity', DWORD, 1),
 (
  'fTXContinueOnXoff', DWORD, 1),
 (
  'fOutX', DWORD, 1),
 (
  'fInX', DWORD, 1),
 (
  'fErrorChar', DWORD, 1),
 (
  'fNull', DWORD, 1),
 (
  'fRtsControl', DWORD, 2),
 (
  'fAbortOnError', DWORD, 1),
 (
  'fDummy2', DWORD, 17),
 (
  'wReserved', WORD),
 (
  'XonLim', WORD),
 (
  'XoffLim', WORD),
 (
  'ByteSize', BYTE),
 (
  'Parity', BYTE),
 (
  'StopBits', BYTE),
 (
  'XonChar', c_char),
 (
  'XoffChar', c_char),
 (
  'ErrorChar', c_char),
 (
  'EofChar', c_char),
 (
  'EvtChar', c_char),
 (
  'wReserved1', WORD)]
LPFTDCB = POINTER(_FTDCB)
FTDCB = _FTDCB

class _FTTIMEOUTS(Structure):
    pass


_FTTIMEOUTS._fields_ = [
 (
  'ReadIntervalTimeout', DWORD),
 (
  'ReadTotalTimeoutMultiplier', DWORD),
 (
  'ReadTotalTimeoutConstant', DWORD),
 (
  'WriteTotalTimeoutMultiplier', DWORD),
 (
  'WriteTotalTimeoutConstant', DWORD)]
FTTIMEOUTS = _FTTIMEOUTS
LPFTTIMEOUTS = POINTER(_FTTIMEOUTS)
FT_W32_ClearCommBreak = _libraries['libftd2xx.so'].FT_W32_ClearCommBreak
FT_W32_ClearCommBreak.restype = BOOL
FT_W32_ClearCommBreak.argtypes = [
 FT_HANDLE]
FT_W32_ClearCommBreak.__doc__ = 'BOOL FT_W32_ClearCommBreak(FT_HANDLE ftHandle)\nftd2xx_linux.h:758'
FT_W32_ClearCommError = _libraries['libftd2xx.so'].FT_W32_ClearCommError
FT_W32_ClearCommError.restype = BOOL
FT_W32_ClearCommError.argtypes = [
 FT_HANDLE, LPDWORD, LPFTCOMSTAT]
FT_W32_ClearCommError.__doc__ = 'BOOL FT_W32_ClearCommError(FT_HANDLE ftHandle, LPDWORD lpdwErrors, LPFTCOMSTAT lpftComstat)\nftd2xx_linux.h:765'
FT_W32_EscapeCommFunction = _libraries['libftd2xx.so'].FT_W32_EscapeCommFunction
FT_W32_EscapeCommFunction.restype = BOOL
FT_W32_EscapeCommFunction.argtypes = [
 FT_HANDLE, DWORD]
FT_W32_EscapeCommFunction.__doc__ = 'BOOL FT_W32_EscapeCommFunction(FT_HANDLE ftHandle, DWORD dwFunc)\nftd2xx_linux.h:771'
FT_W32_GetCommModemStatus = _libraries['libftd2xx.so'].FT_W32_GetCommModemStatus
FT_W32_GetCommModemStatus.restype = BOOL
FT_W32_GetCommModemStatus.argtypes = [
 FT_HANDLE, LPDWORD]
FT_W32_GetCommModemStatus.__doc__ = 'BOOL FT_W32_GetCommModemStatus(FT_HANDLE ftHandle, LPDWORD lpdwModemStatus)\nftd2xx_linux.h:777'
FT_W32_GetCommState = _libraries['libftd2xx.so'].FT_W32_GetCommState
FT_W32_GetCommState.restype = BOOL
FT_W32_GetCommState.argtypes = [
 FT_HANDLE, LPFTDCB]
FT_W32_GetCommState.__doc__ = 'BOOL FT_W32_GetCommState(FT_HANDLE ftHandle, LPFTDCB lpftDcb)\nftd2xx_linux.h:783'
FT_W32_GetCommTimeouts = _libraries['libftd2xx.so'].FT_W32_GetCommTimeouts
FT_W32_GetCommTimeouts.restype = BOOL
FT_W32_GetCommTimeouts.argtypes = [
 FT_HANDLE, POINTER(FTTIMEOUTS)]
FT_W32_GetCommTimeouts.__doc__ = 'BOOL FT_W32_GetCommTimeouts(FT_HANDLE ftHandle, FTTIMEOUTS * pTimeouts)\nftd2xx_linux.h:789'
FT_W32_PurgeComm = _libraries['libftd2xx.so'].FT_W32_PurgeComm
FT_W32_PurgeComm.restype = BOOL
FT_W32_PurgeComm.argtypes = [
 FT_HANDLE, DWORD]
FT_W32_PurgeComm.__doc__ = 'BOOL FT_W32_PurgeComm(FT_HANDLE ftHandle, DWORD dwMask)\nftd2xx_linux.h:795'
FT_W32_SetCommBreak = _libraries['libftd2xx.so'].FT_W32_SetCommBreak
FT_W32_SetCommBreak.restype = BOOL
FT_W32_SetCommBreak.argtypes = [
 FT_HANDLE]
FT_W32_SetCommBreak.__doc__ = 'BOOL FT_W32_SetCommBreak(FT_HANDLE ftHandle)\nftd2xx_linux.h:800'
FT_W32_SetCommMask = _libraries['libftd2xx.so'].FT_W32_SetCommMask
FT_W32_SetCommMask.restype = BOOL
FT_W32_SetCommMask.argtypes = [
 FT_HANDLE, ULONG]
FT_W32_SetCommMask.__doc__ = 'BOOL FT_W32_SetCommMask(FT_HANDLE ftHandle, ULONG ulEventMask)\nftd2xx_linux.h:806'
FT_W32_SetCommState = _libraries['libftd2xx.so'].FT_W32_SetCommState
FT_W32_SetCommState.restype = BOOL
FT_W32_SetCommState.argtypes = [
 FT_HANDLE, LPFTDCB]
FT_W32_SetCommState.__doc__ = 'BOOL FT_W32_SetCommState(FT_HANDLE ftHandle, LPFTDCB lpftDcb)\nftd2xx_linux.h:812'
FT_W32_SetCommTimeouts = _libraries['libftd2xx.so'].FT_W32_SetCommTimeouts
FT_W32_SetCommTimeouts.restype = BOOL
FT_W32_SetCommTimeouts.argtypes = [
 FT_HANDLE, POINTER(FTTIMEOUTS)]
FT_W32_SetCommTimeouts.__doc__ = 'BOOL FT_W32_SetCommTimeouts(FT_HANDLE ftHandle, FTTIMEOUTS * pTimeouts)\nftd2xx_linux.h:818'
FT_W32_SetupComm = _libraries['libftd2xx.so'].FT_W32_SetupComm
FT_W32_SetupComm.restype = BOOL
FT_W32_SetupComm.argtypes = [
 FT_HANDLE, DWORD, DWORD]
FT_W32_SetupComm.__doc__ = 'BOOL FT_W32_SetupComm(FT_HANDLE ftHandle, DWORD dwReadBufferSize, DWORD dwWriteBufferSize)\nftd2xx_linux.h:825'
FT_W32_WaitCommEvent = _libraries['libftd2xx.so'].FT_W32_WaitCommEvent
FT_W32_WaitCommEvent.restype = BOOL
FT_W32_WaitCommEvent.argtypes = [
 FT_HANDLE, PULONG, LPOVERLAPPED]
FT_W32_WaitCommEvent.__doc__ = 'BOOL FT_W32_WaitCommEvent(FT_HANDLE ftHandle, PULONG pulEvent, LPOVERLAPPED lpOverlapped)\nftd2xx_linux.h:832'

class _ft_device_list_info_node(Structure):
    pass


_ft_device_list_info_node._fields_ = [
 (
  'Flags', ULONG),
 (
  'Type', ULONG),
 (
  'ID', ULONG),
 (
  'LocId', DWORD),
 (
  'SerialNumber', c_char * 16),
 (
  'Description', c_char * 64),
 (
  'ftHandle', FT_HANDLE)]
FT_DEVICE_LIST_INFO_NODE = _ft_device_list_info_node
FT_CreateDeviceInfoList = _libraries['libftd2xx.so'].FT_CreateDeviceInfoList
FT_CreateDeviceInfoList.restype = FT_STATUS
FT_CreateDeviceInfoList.argtypes = [
 LPDWORD]
FT_CreateDeviceInfoList.__doc__ = 'FT_STATUS FT_CreateDeviceInfoList(LPDWORD lpdwNumDevs)\nftd2xx_linux.h:851'
FT_GetDeviceInfoList = _libraries['libftd2xx.so'].FT_GetDeviceInfoList
FT_GetDeviceInfoList.restype = FT_STATUS
FT_GetDeviceInfoList.argtypes = [
 POINTER(FT_DEVICE_LIST_INFO_NODE), LPDWORD]
FT_GetDeviceInfoList.__doc__ = 'FT_STATUS FT_GetDeviceInfoList(FT_DEVICE_LIST_INFO_NODE * pDest, LPDWORD lpdwNumDevs)\nftd2xx_linux.h:857'
FT_GetDeviceInfoDetail = _libraries['libftd2xx.so'].FT_GetDeviceInfoDetail
FT_GetDeviceInfoDetail.restype = FT_STATUS
FT_GetDeviceInfoDetail.argtypes = [
 DWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPVOID, LPVOID, POINTER(FT_HANDLE)]
FT_GetDeviceInfoDetail.__doc__ = 'FT_STATUS FT_GetDeviceInfoDetail(DWORD dwIndex, LPDWORD lpdwFlags, LPDWORD lpdwType, LPDWORD lpdwID, LPDWORD lpdwLocId, LPVOID lpSerialNumber, LPVOID lpDescription, FT_HANDLE * pftHandle)\nftd2xx_linux.h:869'
FT_GetDriverVersion = _libraries['libftd2xx.so'].FT_GetDriverVersion
FT_GetDriverVersion.restype = FT_STATUS
FT_GetDriverVersion.argtypes = [
 FT_HANDLE, LPDWORD]
FT_GetDriverVersion.__doc__ = 'FT_STATUS FT_GetDriverVersion(FT_HANDLE ftHandle, LPDWORD lpdwVersion)\nftd2xx_linux.h:875'
FT_GetLibraryVersion = _libraries['libftd2xx.so'].FT_GetLibraryVersion
FT_GetLibraryVersion.restype = FT_STATUS
FT_GetLibraryVersion.argtypes = [
 LPDWORD]
FT_GetLibraryVersion.__doc__ = 'FT_STATUS FT_GetLibraryVersion(LPDWORD lpdwVersion)\nftd2xx_linux.h:880'
__all__ = ['FT_STATUS', 'cpu_set_t', '__int16_t',
 'pthread_mutex_lock', 'CLRDTR', 'FT_DEFAULT_RX_TIMEOUT',
 'pthread_condattr_getpshared', '__off64_t',
 'FT_GetLibraryVersion', 'pthread_getconcurrency',
 'FT_SetFlowControl', 'CE_RXPARITY', 'pthread_testcancel',
 'FT_StopInTask', 'pthread_attr_getscope', 'LPSTR',
 'strptime', 'sched_getaffinity', 'sched_setparam', 'tm',
 '__cpu_mask', 'VOID', 'localtime', '_pthread_descr_struct',
 'FT_BAUD_2400', 'FT_BITS_8', 'FT_ResetPort', 'FT_BITS_5',
 'FT_BITS_7', 'FT_BITS_6', 'FT_SetDataCharacteristics',
 'FT_GetModemStatus', '__time_t_defined', '__time_t',
 'pthread_barrier_destroy', 'FT_SetChars', 'FT_SetVIDPID',
 '_POSIX_SOURCE', 'sched_get_priority_max', '_PTHREAD_H',
 'pthread_rwlock_t', 'timer_t', 'PTHREAD_CREATE_JOINABLE',
 'pthread_spin_trylock', '__uint64_t', 'timespec', 'CE_PTO',
 'MS_RLSD_ON', 'FT_PURGE_RX', '__USE_POSIX199309',
 '__clockid_t', 'FT_BAUD_19200', 'clock',
 'pthread_spin_destroy', 'FT_SetRts', 'CLONE_SYSVSEM',
 'getdate_r', 'pthread_detach',
 'pthread_attr_setdetachstate', 'localtime_r', 'gmtime',
 'pthread_attr_init', 'CLONE_DETACHED', '__u_long',
 'EV_BREAK', 'CLONE_CHILD_SETTID', 'INT', 'FT_SetDivisor',
 'CLOCK_THREAD_CPUTIME_ID', 'FT_GetDeviceInfo',
 'FT_EEPROM_NOT_PROGRAMMED', 'FT_STOP_BITS_2',
 'FT_STOP_BITS_1', 'EV_ERR', 'FT_EE_ProgramEx',
 'pthread_mutexattr_gettype', 'FT_SetDtr', '__mode_t',
 'FT_SetUSBParameters', 'FT_LIST_BY_INDEX', 'SETRTS',
 'sched_rr_get_interval', '__off_t', 'CLONE_UNTRACED',
 'pthread_yield', 'pthread_equal',
 'FT_INSUFFICIENT_RESOURCES', 'FT_PARITY_ODD',
 'PTHREAD_CREATE_DETACHED', 'SCHED_RR', 'CE_TXFULL',
 'FT_PARITY_MARK', 'SECURITY_ATTRIBUTES', '_pthread_descr',
 'CLRRTS', '__USE_FORTIFY_LEVEL', '__int8_t',
 '__fsblkcnt64_t', 'pthread_cond_broadcast',
 'FT_BAUD_38400', 'SCHED_FIFO', 'FT_PARITY_NONE',
 'pthread_sigmask', 'pthread_rwlockattr_setpshared',
 'pthread_barrierattr_t', '__USE_XOPEN_EXTENDED', 'pid_t',
 'FT_EEPROM_READ_FAILED', 'FT_INVALID_PARAMETER',
 '__CPU_SETSIZE', '__fsfilcnt64_t', 'FT_W32_SetCommBreak',
 'pthread_key_t', 'EVENT_HANDLE', '__locale_struct',
 '__pthread_cond_align_t', 'pthread_spin_lock',
 'FT_PARITY_SPACE', 'LPFTCOMSTAT', 'FT_BAUD_4800',
 'CLONE_PARENT_SETTID', 'FT_BAUD_1200', '__fsblkcnt_t',
 '__locale_t', 'pthread_rwlockattr_setkind_np',
 'pthread_getspecific', '_SECURITY_ATTRIBUTES',
 'FT_LIST_MASK', 'FT_W32_ClearCommBreak',
 'FT_GetDriverVersion', 'CSIGNAL', 'EV_TXEMPTY',
 '__WORDSIZE', '__NCPUBITS', 'pthread_rwlockattr_destroy',
 '_pthread_cleanup_push_defer', '_XOPEN_SOURCE', 'clone',
 '_OVERLAPPED', 'pthread_condattr_setpshared',
 'pthread_rwlock_wrlock', 'pthread_join', '__GLIBC__',
 'pthread_rwlockattr_t', '__USE_ISOC99',
 'pthread_rwlockattr_getpshared', 'CLONE_NEWNS',
 'FT_DEVICE_UNKNOWN', 'pthread_attr_setschedpolicy',
 '__u_int', 'FT_BAUD_600', 'FT_OK', '__clock_t',
 'pthread_rwlock_timedwrlock', '__fsfilcnt_t',
 'FT_GetLatencyTimer', 'SYSTEMTIME',
 'FT_SetEventNotification', 'pthread_mutexattr_t',
 'SETXOFF', '__USE_XOPEN', 'PTHREAD_MUTEX_FAST_NP', 'TRUE',
 'FT_INVALID_ARGS', 'CLONE_VM', '__USE_POSIX2', 'LONG',
 'PFT_PROGRAM_DATA', 'FT_PARITY_EVEN', '__qaddr_t',
 'PURGE_RXCLEAR', 'pthread_mutexattr_setpshared',
 'pthread_mutex_timedlock', 'sched_setaffinity',
 'sched_get_priority_min', 'FT_GetStatus',
 '__pthread_attr_s', 'FT_EEPROM_WRITE_FAILED',
 'LPFTTIMEOUTS', 'PTHREAD_CANCEL_DISABLE', 'sigset_t',
 'LPVOID', 'pthread_attr_getschedparam', 'CE_FRAME',
 'pthread_cancel', '__int32_t', 'FT_W32_CancelIo',
 'PTHREAD_MUTEX_RECURSIVE_NP', '__USE_POSIX',
 '_pthread_cleanup_pop', 'CE_BREAK', 'sigevent',
 'FT_FAILED_TO_WRITE_DEVICE', 'FT_DEVICE_BM',
 'pthread_attr_setstack', 'pthread_cond_signal',
 'FT_ReadEE', 'clock_t', '_pthread_cleanup_pop_restore',
 'pthread_cond_wait', '__useconds_t',
 'FT_GetDeviceInfoList', '__GLIBC_MINOR__', 'FT_EE_UARead',
 'pthread_condattr_destroy', 'FT_W32_GetCommState',
 '__clockid_t_defined', 'pthread_key_delete', 'EV_RXFLAG',
 'FT_BAUD_14400', 'FT_DEVICE_NOT_OPENED_FOR_ERASE',
 'pthread_attr_setstacksize', 'pthread_setcancelstate',
 'pthread_barrierattr_setpshared', 'pthread_barrier_t',
 'pthread_rwlock_destroy', 'tzset',
 '_pthread_cleanup_buffer', 'PTHREAD_MUTEX_DEFAULT',
 'PTHREAD_PROCESS_PRIVATE', 'asctime_r',
 'FT_W32_GetOverlappedResult', 'OVERLAPPED', '__USE_GNU',
 'FT_LIST_ALL', 'PTHREAD_RWLOCK_PREFER_READER_NP',
 'pthread_attr_t', '__ino_t', '__rlim64_t', 'SETDTR',
 'pthread_condattr_init', '_POSIX_C_SOURCE', 'LPWORD',
 'FT_Read', 'pthread_attr_getstacksize', 'CHAR',
 '__blksize_t', '__USE_SVID', 'pthread_spinlock_t',
 '__USE_ANSI', 'PTHREAD_PROCESS_SHARED',
 '_pthread_fastlock', 'FT_W32_SetupComm', 'WORD', '__uid_t',
 'FT_W32_PurgeComm', 'PTHREAD_EXPLICIT_SCHED', 'HANDLE',
 'PURGE_TXCLEAR', 'SCHED_OTHER', '__u_char',
 'FT_BAUD_57600', 'strftime_l', '__caddr_t', '__blkcnt64_t',
 '__STDC_ISO_10646__', 'FT_PROGRAM_DATA',
 'FT_EEPROM_NOT_PRESENT', 'FT_BAUD_115200', 'FALSE',
 'CLONE_FILES', '__USE_LARGEFILE', 'FT_W32_WriteFile',
 'pthread_setcanceltype', 'BOOLEAN', '_FEATURES_H',
 'MS_DSR_ON', 'sched_param', 'FT_FLOW_XON_XOFF',
 'PTHREAD_RWLOCK_PREFER_WRITER_NP', 'pthread_cond_t',
 'FT_SetLatencyTimer', 'CLONE_SETTLS', 'UINT',
 'pthread_attr_getstackaddr', '__WORDSIZE_COMPAT32',
 'TIMER_ABSTIME', 'itimerspec', 'pthread_once', 'DWORD',
 'LPBOOL', '__rlim_t', 'PTHREAD_MUTEX_TIMED_NP',
 '__uint8_t', '_XOPEN_SOURCE_EXTENDED', 'LPCSTR', 'timeval',
 'MAX_NUM_DEVICES', 'pthread_attr_destroy', 'MS_CTS_ON',
 '_ISOC99_SOURCE', 'FT_ResetDevice',
 'FT_W32_EscapeCommFunction', 'FT_GetQueueStatus',
 'pthread_barrier_init', 'sched_yield', 'FT_WaitOnMask',
 'FT_SetTimeouts', '_XLOCALE_H', 'pthread_cond_init',
 'pthread_barrierattr_init', 'FT_EE_UASize',
 '_pthread_rwlock_t', 'pthread_rwlock_tryrdlock',
 'FT_BAUD_921600', 'pthread_barrierattr_destroy',
 '__quad_t', '__LT_SPINLOCK_INIT', '__key_t', 'FT_DEVICE',
 'FT_W32_ClearCommError', 'pthread_attr_getdetachstate',
 'PVOID', '__uint16_t', 'pthread_getattr_np',
 'PTHREAD_CANCELED', 'FT_PURGE_TX', 'timegm',
 '__GNU_LIBRARY__', '_BITS_TYPESIZES_H', '__swblk_t',
 'pthread_setconcurrency', 'PURGE_RXABORT',
 '__USE_LARGEFILE64', 'FT_OpenEx', 'FT_BAUD_460800',
 '__defined_schedparam', 'pthread_mutex_init',
 'LPSECURITY_ATTRIBUTES', 'pthread_mutex_trylock', 'PUCHAR',
 '__loff_t', '_FTDCB', 'FT_Close', 'FT_W32_CreateFile',
 '__GLIBC_HAVE_LONG_LONG', 'FT_Write',
 'FT_W32_GetCommModemStatus', 'pthread_getschedparam',
 'FT_SetBreakOff', 'PTHREAD_SCOPE_SYSTEM',
 '_pthread_cleanup_push', 'pthread_mutexattr_init',
 'FT_SetBaudRate', 'dysize', 'pthread_rwlock_timedrdlock',
 'FTTIMEOUTS', '__timer_t', 'SHORT', '__ssize_t',
 'pthread_attr_getinheritsched', 'pthread_kill',
 'FT_EVENT_MODEM_STATUS', 'size_t', 'CE_RXOVER',
 'FT_NOT_SUPPORTED', '__sigset_t', 'FT_DEFAULT_TX_TIMEOUT',
 'pthread_barrier_wait', 'EV_DSR', 'FT_EE_Read', 'EV_CTS',
 'PTHREAD_RWLOCK_DEFAULT_NP', 'CE_IOE', 'FT_SetBitMode',
 'FT_HANDLE', 'CLONE_PARENT', 'FT_W32_GetLastError',
 '__USE_XOPEN2K', '_SCHED_H', '__FD_SETSIZE', 'timelocal',
 'stime', 'EV_RXCHAR', '__intptr_t',
 'pthread_attr_setguardsize', '__timespec_defined',
 'CLONE_PTRACE', 'PTHREAD_ONCE_INIT', '__blkcnt_t',
 'clockid_t', 'strftime', 'gmtime_r', 'FT_BAUD_230400',
 'CLONE_SIGHAND', 'PFT_EVENT_HANDLER', '__USE_MISC',
 'pthread_spin_init', 'CE_DNS', 'FT_EE_ReadEx', 'nanosleep',
 'PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP',
 'FT_BAUD_300', 'PTHREAD_BARRIER_SERIAL_THREAD',
 '_BITS_TYPES_H', 'SETXON', 'FT_SetDeadmanTimeout',
 'mktime', 'FT_DEVICE_LIST_INFO_NODE', 'CE_OOP',
 'FT_W32_WaitCommEvent', 'pthread_attr_setinheritsched',
 'FT_GetEventStatus', '__dev_t',
 'pthread_attr_setschedparam', 'BYTE', 'FT_FLOW_RTS_CTS',
 'pthread_attr_setstackaddr', 'CLONE_STOPPED',
 '__suseconds_t', 'FT_STOP_BITS_1_5',
 'pthread_mutex_destroy', 'LPDWORD', 'INVALID_HANDLE_VALUE',
 'pthread_attr_getschedpolicy', 'FT_IoCtl', 'FT_EE_UAWrite',
 'FT_FLOW_NONE', 'pthread_rwlock_unlock',
 'PTHREAD_MUTEX_ERRORCHECK_NP', '__USE_POSIX199506',
 'PTHREAD_MUTEX_NORMAL', 'FT_OPEN_BY_DESCRIPTION', 'LPTSTR',
 'pthread_getcpuclockid', 'FT_OPEN_BY_SERIAL_NUMBER',
 'pthread_attr_setscope', 'time_t', 'pthread_t',
 'sched_getparam', 'FT_IO_ERROR', 'FT_INVALID_HANDLE',
 'FT_EEPROM_ERASE_FAILED', '_SYS_CDEFS_H',
 'pthread_rwlock_rdlock', 'FT_GetVIDPID',
 'pthread_attr_getstack', 'FT_W32_SetCommState', 'SETBREAK',
 'pthread_attr_getguardsize', 'PTHREAD_CANCEL_ASYNCHRONOUS',
 '_BITS_TIME_H', 'FT_ClrRts', 'pthread_mutex_t',
 '__int64_t', 'FT_LIST_NUMBER_ONLY', 'ft_program_data',
 '_LARGEFILE_SOURCE', 'FT_DEVICE_232R', '_TIME_H',
 'MS_RING_ON', 'FTCOMSTAT', 'pthread_condattr_t',
 'pthread_once_t', '__fsid_t',
 'pthread_mutexattr_getpshared', 'LPOVERLAPPED',
 '__uint32_t', 'CLOCKS_PER_SEC', '_FTCOMSTAT', 'RESETDEV',
 'FT_DEVICE_100AX', '__ino64_t', 'strptime_l',
 'pthread_rwlockattr_init', 'FT_W32_ReadFile',
 '__STDC_IEC_559__', 'PTHREAD_MUTEX_ERRORCHECK',
 '_BITS_PTHREADTYPES_H', 'FT_EVENT_RXCHAR', 'ctime',
 '_FTTIMEOUTS', 'FT_SetBreakOn', 'FT_DEVICE_NOT_OPENED',
 'PTHREAD_SCOPE_PROCESS', '__nlink_t', 'CLONE_THREAD',
 'FT_FLOW_DTR_DSR', '__clock_t_defined',
 '_LARGEFILE64_SOURCE', '__id_t',
 'PTHREAD_MUTEX_ADAPTIVE_NP', '_BITS_SIGTHREAD_H',
 'CE_OVERRUN', 'FT_DEVICE_2232C', 'FT_CreateDeviceInfoList',
 '__timer_t_defined', 'FT_DEVICE_AM', 'pthread_setspecific',
 'asctime', 'FT_EE_Program', 'pthread_exit',
 'CLOCK_MONOTONIC', 'EV_RX80FULL',
 'pthread_rwlock_trywrlock', 'UCHAR', '_SVID_SOURCE',
 'CLONE_FS', 'CLONE_CHILD_CLEARTID', 'LPFTDCB',
 'PTHREAD_CANCEL_ENABLE', 'FT_DEVICE_NOT_FOUND',
 'PTHREAD_MUTEX_RECURSIVE', 'pthread_spin_unlock',
 'FT_GetBitMode', '__USE_BSD', 'PULONG', 'CLOCK_REALTIME',
 'FT_ClrDtr', '_SIGSET_H_types', 'PTHREAD_INHERIT_SCHED',
 'LPBYTE', 'EV_RING', '__USE_UNIX98', 'FT_ListDevices',
 'pthread_create', 'FT_W32_GetCommTimeouts', '__gid_t',
 'FT_WriteEE', '_EVENT_HANDLE', 'pthread_key_create',
 '__daddr_t', 'pthread_mutexattr_destroy', '__sig_atomic_t',
 'pthread_cond_timedwait', 'FT_CyclePort',
 'pthread_rwlockattr_getkind_np', 'FTDCB',
 'FT_GetDeviceInfoDetail', 'pthread_setschedparam',
 'FILETIME', 'FT_W32_CloseHandle', 'pthread_mutex_unlock',
 '_ft_device_list_info_node', '__STDC_IEC_559_COMPLEX__',
 'getdate', 'FT_RestartInTask', 'locale_data', 'USHORT',
 'EV_EVENT1', 'FT_BAUD_9600', 'EV_EVENT2',
 'sched_setscheduler', 'BOOL', 'ctime_r',
 'pthread_rwlock_init', 'FT_DEVICE_NOT_OPENED_FOR_WRITE',
 'pthread_barrierattr_getpshared', 'FT_Purge',
 'PURGE_TXABORT', 'pthread_mutexattr_settype',
 'PTHREAD_CANCEL_DEFERRED', 'pthread_cond_destroy',
 'FT_W32_SetCommMask', 'EV_PERR',
 'CLOCK_PROCESS_CPUTIME_ID', '__u_quad_t', '__u_short',
 '_BSD_SOURCE', 'EV_RLSD', 'PCHAR', '__pid_t', 'ULONGLONG',
 'FT_SetResetPipeRetryCount', 'sched_getscheduler',
 'FT_W32_SetCommTimeouts', '_SIGSET_NWORDS', 'FT_EraseEE',
 'CLRBREAK', '__sched_param', 'FT_INVALID_BAUD_RATE',
 'CE_MODE', 'FT_SetWaitMask', 'ULONG', '__socklen_t',
 'difftime', 'CLONE_VFORK', 'time', 'FT_OTHER_ERROR',
 'pthread_self', 'FT_Open']