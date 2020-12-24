# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/inotify.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 13463 bytes
"""Linux inotify(7) API wrapper module
"""
import collections, logging, operator, os, struct, ctypes
from ctypes import c_int, c_char_p, c_uint32
from ctypes.util import find_library
import enum
from functools import reduce
_LOGGER = logging.getLogger(__name__)
_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)
if any([getattr(_LIBC, func_name, None) is None for func_name in ['inotify_init1',
 'inotify_add_watch',
 'inotify_rm_watch']]):
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)
_INOTIFY_INIT1_DECL = ctypes.CFUNCTYPE(c_int, c_int, use_errno=True)
_INOTIFY_INIT1 = _INOTIFY_INIT1_DECL(('inotify_init1', _LIBC))

def inotify_init(flags=0):
    """Initializes a new inotify instance and returns a file descriptor
    associated with a new inotify event queue.

    :param ``INInitFlags`` flags:
        Optional flag to control the inotify_init behavior.
    """
    fileno = _INOTIFY_INIT1(flags)
    if fileno < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), 'inotify_init1(%r)' % flags)
    return fileno


class INInitFlags(enum.IntEnum):
    __doc__ = 'Flags supported by inotify_init(2).'
    NONBLOCK = 2048
    CLOEXEC = 524288


IN_NONBLOCK = INInitFlags.NONBLOCK
IN_CLOEXEC = INInitFlags.CLOEXEC
_INOTIFY_ADD_WATCH_DECL = ctypes.CFUNCTYPE(c_int, c_int, c_char_p, c_uint32, use_errno=True)
_INOTIFY_ADD_WATCH = _INOTIFY_ADD_WATCH_DECL(('inotify_add_watch', _LIBC))

def inotify_add_watch(fileno, path, mask):
    """Add a watch to an initialized inotify instance."""
    watch_id = _INOTIFY_ADD_WATCH(fileno, path.encode('utf-8'), mask)
    if watch_id < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), 'inotify_add_watch(%r, %r, %r)' % (fileno, path, mask))
    return watch_id


class INAddWatchFlags(enum.IntEnum):
    __doc__ = 'Special flags for inotify_add_watch.\n    '
    DONT_FOLLOW = 33554432
    MASK_ADD = 536870912
    ONESHOT = 2147483648
    ONLYDIR = 16777216


IN_DONT_FOLLOW = INAddWatchFlags.DONT_FOLLOW
IN_MASK_ADD = INAddWatchFlags.MASK_ADD
IN_ONESHOT = INAddWatchFlags.ONESHOT
IN_ONLYDIR = INAddWatchFlags.ONLYDIR
_INOTIFY_RM_WATCH_DECL = ctypes.CFUNCTYPE(c_int, c_int, c_uint32, use_errno=True)
_INOTIFY_RM_WATCH = _INOTIFY_RM_WATCH_DECL(('inotify_rm_watch', _LIBC))

def inotify_rm_watch(fileno, watch_id):
    """Remove an existing watch from an inotify instance."""
    res = _INOTIFY_RM_WATCH(fileno, watch_id)
    if res < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), 'inotify_rm_watch(%r, %r)' % (fileno, watch_id))


INOTIFY_EVENT_HDRSIZE = struct.calcsize('iIII')

def _parse_buffer(event_buffer):
    """Parses an inotify event buffer of ``inotify_event`` structs read from
    the inotify socket.

    The inotify_event structure looks like this::

        struct inotify_event {
            __s32 wd;            /* watch descriptor */
            __u32 mask;          /* watch mask */
            __u32 cookie;        /* cookie to synchronize two events */
            __u32 len;           /* length (including nulls) of name */
            char  name[0];       /* stub for possible name */
        };

    The ``cookie`` member of this struct is used to pair two related
    events, for example, it pairs an IN_MOVED_FROM event with an
    IN_MOVED_TO event.
    """
    while len(event_buffer) >= INOTIFY_EVENT_HDRSIZE:
        wd, mask, cookie, length = struct.unpack_from('iIII', event_buffer, 0)
        name = event_buffer[INOTIFY_EVENT_HDRSIZE:INOTIFY_EVENT_HDRSIZE + length]
        name = name.decode().rstrip('\x00')
        event_buffer = event_buffer[INOTIFY_EVENT_HDRSIZE + length:]
        yield (wd, mask, cookie, name)

    assert len(event_buffer) == 0, 'Unparsed bytes left in buffer: %r' % event_buffer


class INEvent(enum.IntEnum):
    __doc__ = 'Inotify events.\n    '
    ACCESS = 1
    ATTRIB = 4
    CLOSE_NOWRITE = 16
    CLOSE_WRITE = 8
    CREATE = 256
    DELETE = 512
    DELETE_SELF = 1024
    MODIFY = 2
    MOVED_FROM = 64
    MOVED_TO = 128
    MOVE_SELF = 2048
    OPEN = 32
    IGNORED = 32768
    ISDIR = 1073741824
    Q_OVERFLOW = 16384
    UNMOUNT = 8192


IN_ACCESS = INEvent.ACCESS
IN_ATTRIB = INEvent.ATTRIB
IN_CLOSE_NOWRITE = INEvent.CLOSE_NOWRITE
IN_CLOSE_WRITE = INEvent.CLOSE_WRITE
IN_CREATE = INEvent.CREATE
IN_DELETE = INEvent.DELETE
IN_DELETE_SELF = INEvent.DELETE_SELF
IN_MODIFY = INEvent.MODIFY
IN_MOVED_FROM = INEvent.MOVED_FROM
IN_MOVED_TO = INEvent.MOVED_TO
IN_MOVE_SELF = INEvent.MOVE_SELF
IN_OPEN = INEvent.OPEN
IN_IGNORED = INEvent.IGNORED
IN_ISDIR = INEvent.ISDIR
IN_Q_OVERFLOW = INEvent.Q_OVERFLOW
IN_UNMOUNT = INEvent.UNMOUNT
IN_CLOSE = IN_CLOSE_WRITE | IN_CLOSE_NOWRITE
IN_MOVE = IN_MOVED_FROM | IN_MOVED_TO
IN_ALL_EVENTS = reduce(operator.or_, [
 IN_ACCESS,
 IN_ATTRIB,
 IN_CLOSE_NOWRITE,
 IN_CLOSE_WRITE,
 IN_CREATE,
 IN_DELETE,
 IN_DELETE_SELF,
 IN_MODIFY,
 IN_MOVED_FROM,
 IN_MOVED_TO,
 IN_MOVE_SELF,
 IN_OPEN])

def _fmt_mask(mask):
    """Parse an Inotify event mask into indivitual event flags."""
    masks = []
    for event in INEvent:
        if mask & event:
            masks.append(event.name)
            mask ^= event
            continue

    if mask:
        masks.append(hex(mask))
    return masks


class InotifyEvent(collections.namedtuple('InotifyEvent', 'wd mask cookie src_path')):
    __doc__ = '\n    Inotify event struct wrapper.\n\n    :param wd:\n        Watch descriptor\n    :param mask:\n        Event mask\n    :param cookie:\n        Event cookie\n    :param src_path:\n        Event source path\n    '
    __slots__ = ()

    @property
    def is_modify(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_MODIFY)

    @property
    def is_close_write(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_CLOSE_WRITE)

    @property
    def is_close_nowrite(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_CLOSE_NOWRITE)

    @property
    def is_access(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_ACCESS)

    @property
    def is_delete(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_DELETE)

    @property
    def is_delete_self(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_DELETE_SELF)

    @property
    def is_create(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_CREATE)

    @property
    def is_moved_from(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_MOVED_FROM)

    @property
    def is_moved_to(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_MOVED_TO)

    @property
    def is_move(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_MOVE)

    @property
    def is_move_self(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_MOVE_SELF)

    @property
    def is_attrib(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_ATTRIB)

    @property
    def is_ignored(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_IGNORED)

    @property
    def is_directory(self):
        """Test mask shorthand."""
        return bool(self.mask & IN_ISDIR)

    def __repr__(self):
        masks = _fmt_mask(self.mask)
        return '<InotifyEvent: src_path=%s, wd=%d, mask=%s, cookie=%d>' % (
         self.src_path,
         self.wd,
         '|'.join(masks),
         self.cookie)


DEFAULT_NUM_EVENTS = 2048
DEFAULT_EVENT_BUFFER_SIZE = DEFAULT_NUM_EVENTS * INOTIFY_EVENT_HDRSIZE
DEFAULT_EVENTS = IN_ALL_EVENTS

class Inotify(object):
    __doc__ = 'Inotify system interface.'

    def __init__(self, flags):
        """Initialize a new Inotify object.
        """
        inotify_fd = inotify_init(flags)
        self._inotify_fd = inotify_fd
        self._paths = {}

    def fileno(self):
        """The file descriptor associated with the inotify instance."""
        return self._inotify_fd

    def close(self):
        """Close the inotify filedescriptor.

        NOTE: After call this, this object will be unusable.
        """
        os.close(self._inotify_fd)

    def add_watch(self, path, event_mask=DEFAULT_EVENTS):
        """
        Adds a watch for the given path to monitor events specified by the
        mask.

        :param path:
            Path to monitor
        :type path:
            ``str``
        :param event_mask:
            *optional* Bit mask of the request events.
        :type event_mask:
            ``int``
        :returns:
            Unique watch descriptor identifier
        :rtype:
            ``int``
        """
        path = os.path.normpath(path)
        watch_id = inotify_add_watch(self._inotify_fd, path, event_mask | IN_MASK_ADD)
        self._paths[watch_id] = path
        return watch_id

    def remove_watch(self, watch_id):
        """
        Removes a watch.

        :param watch_id:
            Watch descriptor returned by :meth:`~Inotify.add_watch`
        :type watch_id:
            ``int``
        :returns:
            ``None``
        """
        inotify_rm_watch(self._inotify_fd, watch_id)

    def read_events(self, event_buffer_size=DEFAULT_EVENT_BUFFER_SIZE):
        """
        Reads events from inotify and yields them.

        :param event_buffer_size:
            *optional* Buffer size while reading the inotify socket
        :type event_buffer_size:
            ``int``
        :returns:
            List of :class:`InotifyEvent` instances
        :rtype:
            ``list``
        """
        if not self._paths:
            return []
        event_buffer = os.read(self._inotify_fd, event_buffer_size)
        event_list = []
        for wd, mask, cookie, name in _parse_buffer(event_buffer):
            wd_path = self._paths[wd]
            src_path = os.path.normpath(os.path.join(wd_path, name))
            inotify_event = InotifyEvent(wd, mask, cookie, src_path)
            _LOGGER.debug('Received event %r', inotify_event)
            if inotify_event.mask & IN_IGNORED:
                del self._paths[wd]
            event_list.append(inotify_event)

        return event_list