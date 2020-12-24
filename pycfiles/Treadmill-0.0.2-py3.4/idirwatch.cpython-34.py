# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/idirwatch.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 6656 bytes
"""Watches a directory for changes using inotify and generates events.

Usage:

    def on_created(path):
        pass

    def on_deleted(path):
        pass

    def main():
        watch = DirWatcher('/tmp')
        watch.on_created = on_created
        watch.on_deleted = on_deleted

        if watch.wait_for_events(timeout):
            watch.process_events()
"""
import sys, errno, collections, logging, os, select, enum
if os.name == 'nt':
    from .syscall import readdirchange
else:
    from .syscall import inotify
_LOGGER = logging.getLogger(__name__)

class DirWatcherEvent(enum.Enum):
    __doc__ = "DirWatcher's emitted event types.\n    "
    CREATED = 'created'
    DELETED = 'deleted'
    MODIFIED = 'modified'
    MORE_PENDING = 'more events pending'


class DirWatcher(object):
    __doc__ = 'Directory watcher, invoking callbacks on file create/delete events.'
    __slots__ = ('event_list', 'inotify', 'on_created', 'on_deleted', 'on_modified',
                 'poll', '_watches')

    def __init__(self, watch_dir=None):
        if os.name == 'nt':
            self.inotify = readdirchange.ReadDirChange()
        else:
            self.inotify = inotify.Inotify(inotify.IN_CLOEXEC)
        self._watches = {}
        self.event_list = collections.deque()
        self.poll = select.poll()
        self.poll.register(self.inotify, select.POLLIN)
        self.on_created = self._noop
        self.on_deleted = self._noop
        self.on_modified = self._noop
        if watch_dir is not None:
            self.add_dir(watch_dir)

    def add_dir(self, directory):
        """Add `directory` to the list of watched directories.
        """
        watch_dir = os.path.realpath(directory)
        if os.name == 'nt':
            wid = self.inotify.add_watch(watch_dir)
        else:
            wid = self.inotify.add_watch(watch_dir, event_mask=inotify.IN_ATTRIB | inotify.IN_CREATE | inotify.IN_DELETE | inotify.IN_DELETE_SELF | inotify.IN_MODIFY | inotify.IN_MOVE)
        _LOGGER.info('Watching directoy %r (id: %r)', watch_dir, wid)
        self._watches[wid] = watch_dir

    def remove_dir(self, directory):
        """Remove `directory` from the list of watched directories.
        """
        watch_dir = os.path.realpath(directory)
        for wid, w_dir in self._watches.items():
            if w_dir == watch_dir:
                break
        else:
            wid = None
            _LOGGER.warn('Directoy %r not currently watched', watch_dir)
            return

        _LOGGER.info('Unwatching directoy %r (id: %r)', watch_dir, wid)
        del self._watches[wid]
        self.inotify.remove_watch(wid)

    def _noop(self, event_src):
        """Default NOOP callback"""
        _LOGGER.debug('event on %r', event_src)

    def wait_for_events(self, timeout=-1):
        """Wait for directory change event for up to ``timeout`` seconds.

        :param timeout:
            Time in seconds to wait for an event (-1 means forever)
        :returns:
            ``True`` if events were received, ``False`` otherwise.
        """
        if self.event_list:
            return True
        if timeout != -1:
            timeout *= 1000
        try:
            rc = self.poll.poll(timeout)
            return bool(rc)
        except select.error as err:
            if err.errno == errno.EINTR:
                return False
            raise

    def process_events(self, max_events=0, resume=False):
        """Process events received.

        This function will parse all received events and invoke the registered
        callbacks accordingly.

        :param ``int`` max_events:
            Maximum number of events to process
        :param ``bool`` resume:
            Continue processing any event that was still in the queue (do not
            read new ones).
        :returns ``list``:
            List of ``(DirWatcherEvent, <path>, <callback_return>)``.
        """
        if max_events <= 0:
            max_events = sys.maxsize
        if not self.event_list:
            if not resume:
                try:
                    self.event_list.extend(self.inotify.read_events())
                except OSError as err:
                    if err.errno == errno.EINTR:
                        return []
                    raise

        results = []
        step = 0
        while self.event_list:
            if step >= max_events:
                results.append((
                 DirWatcherEvent.MORE_PENDING,
                 None,
                 None))
                break
            step += 1
            event = self.event_list.popleft()
            if event.is_modify or event.is_attrib:
                res = self.on_modified(event.src_path)
                results.append((
                 DirWatcherEvent.MODIFIED,
                 event.src_path,
                 res))
            elif event.is_delete or event.is_moved_from or event.is_delete_self:
                res = self.on_deleted(event.src_path)
                results.append((
                 DirWatcherEvent.DELETED,
                 event.src_path,
                 res))
            elif event.is_create or event.is_moved_to:
                res = self.on_created(event.src_path)
                results.append((
                 DirWatcherEvent.CREATED,
                 event.src_path,
                 res))
            elif event.mask == inotify.IN_IGNORED:
                if self._watches.pop(event.wd, None):
                    _LOGGER.info('Watch on %r auto-removed', event.src_path)
                else:
                    continue

        return results