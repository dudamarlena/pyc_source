# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Worker/Worker.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 26898 bytes
__doc__ = '\nClusterShell worker interface.\n\nA worker is a generic object which provides "grouped" work in a specific task.\n'
try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec

import warnings
from ClusterShell.Worker.EngineClient import EngineClient
from ClusterShell.NodeSet import NodeSet
from ClusterShell.Engine.Engine import FANOUT_UNLIMITED, FANOUT_DEFAULT

def _eh_sigspec_invoke_compat(method, argc_legacy, *args):
    """
    Helper function to invoke an event handler method, with legacy
    signature compatibility if actual argc does match argc_legacy.
    This should be removed when old signatures (< 1.8) aren't supported
    anymore (in 2.x).
    """
    argc_actual = len(getfullargspec(method)[0])
    if argc_actual == argc_legacy:
        return method(*args[0:argc_legacy - 1])
    else:
        return method(*args)


def _eh_sigspec_ev_read_17(ev_read):
    """Helper function to check whether ev_read has the old 1.7 signature."""
    return len(getfullargspec(ev_read)[0]) == 2


class WorkerException(Exception):
    """WorkerException"""
    pass


class WorkerError(WorkerException):
    """WorkerError"""
    pass


WorkerBadArgumentError = ValueError

class Worker(object):
    """Worker"""
    SNAME_STDIN = 'stdin'
    SNAME_STDOUT = 'stdout'
    SNAME_STDERR = 'stderr'

    def __init__(self, handler):
        """Initializer. Should be called from derived classes."""
        self.eh = handler
        self._fanout = FANOUT_DEFAULT
        self._update_task_rc = True
        self.task = None
        self.started = False
        self.metaworker = None
        self.metarefcnt = 0
        self.current_node = None
        self.current_msg = None
        self.current_errmsg = None
        self.current_rc = 0
        self.current_sname = None

    def _set_task(self, task):
        """Bind worker to task. Called by task.schedule()."""
        if self.task is not None:
            raise WorkerError('worker has already been scheduled')
        self.task = task

    def _task_bound_check(self):
        """Helper method to check that worker is bound to a task."""
        if not self.task:
            raise WorkerError('worker is not task bound')

    def _engine_clients(self):
        """Return a list of underlying engine clients."""
        raise NotImplementedError('Derived classes must implement.')

    def _on_start(self, key):
        """Called on command start."""
        self.current_node = key
        if not self.started:
            self.started = True
            if self.eh is not None:
                self.eh.ev_start(self)
        if self.eh is not None:
            _eh_sigspec_invoke_compat(self.eh.ev_pickup, 2, self, key)

    def _on_close(self, key, rc=None):
        """Called to generate events when the Worker is closing."""
        if self._update_task_rc:
            if rc is not None:
                self.task._rc_set(self, key, rc)
        self.current_node = key
        self.current_rc = rc
        if self.eh is not None:
            _eh_sigspec_invoke_compat(self.eh.ev_hup, 2, self, key, rc)

    def _on_written(self, key, bytes_count, sname):
        """Notification of bytes written."""
        self.current_node = key
        self.current_sname = sname
        if self.eh is not None:
            _eh_sigspec_invoke_compat(self.eh.ev_written, 5, self, key, sname, bytes_count)

    def last_read(self):
        """
        Get last read message from event handler.
        [DEPRECATED] use current_msg
        """
        raise NotImplementedError('Derived classes must implement.')

    def last_error(self):
        """
        Get last error message from event handler.
        [DEPRECATED] use current_errmsg
        """
        raise NotImplementedError('Derived classes must implement.')

    def did_timeout(self):
        """Return whether this worker has aborted due to timeout."""
        self._task_bound_check()
        return self.task._num_timeout_by_worker(self) > 0

    def read(self, node=None, sname='stdout'):
        """Read worker stream buffer.

        Return stream read buffer of current worker.

        Arguments:
            node -- node name; can also be set to None for simple worker
                    having worker.key defined (default is None)
            sname -- stream name (default is 'stdout')
        """
        self._task_bound_check()
        return self.task._msg_by_source(self, node, sname)

    def abort(self):
        """Abort processing any action by this worker.

        Safe to call on an already closing or aborting worker.
        """
        raise NotImplementedError('Derived classes must implement.')

    def flush_buffers(self):
        """Flush any messages associated to this worker."""
        self._task_bound_check()
        self.task._flush_buffers_by_worker(self)

    def flush_errors(self):
        """Flush any error messages associated to this worker."""
        self._task_bound_check()
        self.task._flush_errors_by_worker(self)


class DistantWorker(Worker):
    """DistantWorker"""

    def _on_node_msgline(self, node, msg, sname):
        """Message received from node, update last* stuffs."""
        task = self.task
        assert not isinstance(node, NodeSet)
        task._msg_add(self, node, sname, msg)
        self.current_sname = sname
        self.current_node = node
        if sname == self.SNAME_STDERR:
            self.current_errmsg = msg
            if self.eh is not None:
                if hasattr(self.eh, 'ev_error'):
                    self.eh.ev_error(self)
                if not _eh_sigspec_ev_read_17(self.eh.ev_read):
                    self.eh.ev_read(self, node, sname, msg)
        else:
            self.current_msg = msg
        if self.eh is not None:
            if _eh_sigspec_ev_read_17(self.eh.ev_read):
                self.eh.ev_read(self)
            else:
                self.eh.ev_read(self, node, sname, msg)

    def _on_node_close(self, node, rc):
        """Command return code received."""
        Worker._on_close(self, node, rc)

    def _on_node_timeout(self, node):
        """Update on node timeout."""
        self.current_node = node
        self.task._timeout_add(self, node)

    def last_node(self):
        """
        Get last node, useful to get the node in an EventHandler
        callback like ev_read().
        [DEPRECATED] use current_node
        """
        warnings.warn('use current_node instead', DeprecationWarning)
        return self.current_node

    def last_read(self):
        """
        Get last (node, buffer), useful in an EventHandler.ev_read()
        [DEPRECATED] use (current_node, current_msg)
        """
        warnings.warn('use current_node and current_msg instead', DeprecationWarning)
        return (
         self.current_node, self.current_msg)

    def last_error(self):
        """
        Get last (node, error_buffer), useful in an EventHandler.ev_error()
        [DEPRECATED] use (current_node, current_errmsg)
        """
        warnings.warn('use current_node and current_errmsg instead', DeprecationWarning)
        return (
         self.current_node, self.current_errmsg)

    def last_retcode(self):
        """
        Get last (node, rc), useful in an EventHandler.ev_hup()
        [DEPRECATED] use (current_node, current_rc)
        """
        warnings.warn('use current_node and current_rc instead', DeprecationWarning)
        return (
         self.current_node, self.current_rc)

    def node_buffer(self, node):
        """Get specific node buffer."""
        return self.read(node, self.SNAME_STDOUT)

    def node_error(self, node):
        """Get specific node error buffer."""
        return self.read(node, self.SNAME_STDERR)

    node_error_buffer = node_error

    def node_retcode(self, node):
        """
        Get specific node return code.

        :raises KeyError: command on node has not yet finished (no return code
            available), or this node is not known by this worker
        """
        self._task_bound_check()
        try:
            rc = self.task._rc_by_source(self, node)
        except KeyError:
            raise KeyError(node)

        return rc

    node_rc = node_retcode

    def iter_buffers(self, match_keys=None):
        """
        Returns an iterator over available buffers and associated
        NodeSet. If the optional parameter match_keys is defined, only
        keys found in match_keys are returned.
        """
        self._task_bound_check()
        for msg, keys in self.task._call_tree_matcher(self.task._msgtree(self.SNAME_STDOUT).walk, match_keys, self):
            yield (
             msg, NodeSet.fromlist(keys))

    def iter_errors(self, match_keys=None):
        """
        Returns an iterator over available error buffers and associated
        NodeSet. If the optional parameter match_keys is defined, only
        keys found in match_keys are returned.
        """
        self._task_bound_check()
        for msg, keys in self.task._call_tree_matcher(self.task._msgtree(self.SNAME_STDERR).walk, match_keys, self):
            yield (
             msg, NodeSet.fromlist(keys))

    def iter_node_buffers(self, match_keys=None):
        """
        Returns an iterator over each node and associated buffer.
        """
        self._task_bound_check()
        return self.task._call_tree_matcher(self.task._msgtree(self.SNAME_STDOUT).items, match_keys, self)

    def iter_node_errors(self, match_keys=None):
        """
        Returns an iterator over each node and associated error buffer.
        """
        self._task_bound_check()
        return self.task._call_tree_matcher(self.task._msgtree(self.SNAME_STDERR).items, match_keys, self)

    def iter_retcodes(self, match_keys=None):
        """
        Returns an iterator over return codes and associated NodeSet.
        If the optional parameter match_keys is defined, only keys
        found in match_keys are returned.
        """
        self._task_bound_check()
        for rc, keys in self.task._rc_iter_by_worker(self, match_keys):
            yield (
             rc, NodeSet.fromlist(keys))

    def iter_node_retcodes(self):
        """
        Returns an iterator over each node and associated return code.
        """
        self._task_bound_check()
        return self.task._krc_iter_by_worker(self)

    def num_timeout(self):
        """
        Return the number of timed out "keys" (ie. nodes) for this worker.
        """
        self._task_bound_check()
        return self.task._num_timeout_by_worker(self)

    def iter_keys_timeout(self):
        """
        Iterate over timed out keys (ie. nodes) for a specific worker.
        """
        self._task_bound_check()
        return self.task._iter_keys_timeout_by_worker(self)


class StreamClient(EngineClient):
    """StreamClient"""

    def _start(self):
        """Called on EngineClient start."""
        assert not self.worker.started
        self.worker._on_start(self.key)
        return self

    def _read(self, sname, size=65536):
        """Read data from process."""
        return EngineClient._read(self, sname, size)

    def _close(self, abort, timeout):
        """Close client. See EngineClient._close()."""
        EngineClient._close(self, abort, timeout)
        if timeout:
            assert abort, 'abort flag not set on timeout'
            self.worker._on_timeout(self.key)
        self.worker._on_close(self.key)
        if self.worker.eh:
            _eh_sigspec_invoke_compat(self.worker.eh.ev_close, 2, self, timeout)

    def _handle_read(self, sname):
        """Engine is telling us there is data available for reading."""
        task = self.worker.task
        msgline = self.worker._on_msgline
        debug = task.info('debug', False)
        if debug:
            print_debug = task.info('print_debug')
            for msg in self._readlines(sname):
                print_debug(task, 'LINE %s' % msg)
                msgline(self.key, msg, sname)

        else:
            for msg in self._readlines(sname):
                msgline(self.key, msg, sname)

    def _flush_read(self, sname):
        """Called at close time to flush stream read buffer."""
        stream = self.streams[sname]
        if stream.readable():
            if stream.rbuf:
                self.worker._on_msgline(self.key, stream.rbuf, sname)

    def write(self, buf, sname=None):
        """Write to writable stream(s)."""
        if sname is not None:
            self._write(sname, buf)
            return
        for writer in self.streams.writers():
            self._write(writer.name, buf)

    def set_write_eof(self, sname=None):
        """Set EOF flag to writable stream(s)."""
        if sname is not None:
            self._set_write_eof(sname)
            return
        for writer in self.streams.writers():
            self._set_write_eof(writer.name)


class StreamWorker(Worker):
    """StreamWorker"""

    def __init__(self, handler, key=None, stderr=False, timeout=-1, autoclose=False, client_class=StreamClient):
        Worker.__init__(self, handler)
        if key is None:
            key = self
        self.clients = [
         client_class(self, key, stderr, timeout, autoclose)]

    def set_reader(self, sname, sfile, retain=True, closefd=True):
        """Add a readable stream to StreamWorker.

        Arguments:
            sname   -- the name of the stream (string)
            sfile   -- the stream file or file descriptor
            retain  -- whether the stream retains engine client
                       (default is True)
            closefd -- whether to close fd when the stream is closed
                       (default is True)
        """
        if not self.clients[0].registered:
            self.clients[0].streams.set_reader(sname, sfile, retain, closefd)
        else:
            raise WorkerError('cannot add new stream at runtime')

    def set_writer(self, sname, sfile, retain=True, closefd=True):
        """Set a writable stream to StreamWorker.

        Arguments:
            sname -- the name of the stream (string)
            sfile -- the stream file or file descriptor
            retain  -- whether the stream retains engine client
                       (default is True)
            closefd -- whether to close fd when the stream is closed
                       (default is True)
        """
        if not self.clients[0].registered:
            self.clients[0].streams.set_writer(sname, sfile, retain, closefd)
        else:
            raise WorkerError('cannot add new stream at runtime')

    def _engine_clients(self):
        """Return a list of underlying engine clients."""
        return self.clients

    def set_key(self, key):
        """Source key for this worker is free for use.

        Use this method to set the custom source key for this worker.
        """
        self.clients[0].key = key

    def _on_msgline(self, key, msg, sname):
        """Add a message."""
        self.task._msg_add(self, key, sname, msg)
        self.current_sname = sname
        if sname == 'stderr':
            self.current_errmsg = msg
            if self.eh is not None:
                if hasattr(self.eh, 'ev_error'):
                    self.eh.ev_error(self)
                if not _eh_sigspec_ev_read_17(self.eh.ev_read):
                    self.eh.ev_read(self, key, sname, msg)
        else:
            self.current_msg = msg
        if self.eh is not None:
            if _eh_sigspec_ev_read_17(self.eh.ev_read):
                self.eh.ev_read(self)
            else:
                self.eh.ev_read(self, key, sname, msg)

    def _on_timeout(self, key):
        """Update on timeout."""
        self.task._timeout_add(self, key)
        if self.eh:
            if hasattr(self.eh, 'ev_timeout'):
                self.eh.ev_timeout(self)

    def abort(self):
        """Abort processing any action by this worker.

        Safe to call on an already closing or aborting worker.
        """
        self.clients[0].abort()

    def read(self, node=None, sname='stdout'):
        """Read worker stream buffer.

        Return stream read buffer of current worker.

        Arguments:
            node -- node name; can also be set to None for simple worker
                    having worker.key defined (default is None)
            sname -- stream name (default is 'stdout')
        """
        return Worker.read(self, node or self.clients[0].key, sname)

    def write(self, buf, sname=None):
        """Write to worker.

        If sname is specified, write to the associated stream,
        otherwise write to all writable streams.
        """
        self.clients[0].write(buf, sname)

    def set_write_eof(self, sname=None):
        """
        Tell worker to close its writer file descriptor once flushed.

        Do not perform writes after this call. Like write(), sname can
        be optionally specified to target a specific writable stream,
        otherwise all writable streams are marked as EOF.
        """
        self.clients[0].set_write_eof(sname)


class WorkerSimple(StreamWorker):
    """WorkerSimple"""

    def __init__(self, file_reader, file_writer, file_error, key, handler, stderr=False, timeout=-1, autoclose=False, closefd=True, client_class=StreamClient):
        """Initialize WorkerSimple worker."""
        StreamWorker.__init__(self, handler, key, stderr, timeout, autoclose, client_class=client_class)
        if file_reader:
            self.set_reader('stdout', file_reader, closefd=closefd)
        if file_error:
            self.set_reader('stderr', file_error, closefd=closefd)
        if file_writer:
            self.set_writer('stdin', file_writer, closefd=closefd)
        self._filerefs = (file_reader, file_writer, file_error)

    def error_fileno(self):
        """Return the standard error reader file descriptor (integer)."""
        return self.clients[0].streams['stderr'].fd

    def reader_fileno(self):
        """Return the reader file descriptor (integer)."""
        return self.clients[0].streams['stdout'].fd

    def writer_fileno(self):
        """Return the writer file descriptor as an integer."""
        return self.clients[0].streams['stdin'].fd

    def last_read(self):
        """
        Get last read message.

        [DEPRECATED] use current_msg
        """
        warnings.warn('use current_msg instead', DeprecationWarning)
        return self.current_msg

    def last_error(self):
        """
        Get last error message.

        [DEPRECATED] use current_errmsg
        """
        warnings.warn('use current_errmsg instead', DeprecationWarning)
        return self.current_errmsg

    def error(self):
        """Read worker error buffer."""
        return self.read(sname='stderr')

    def _on_start(self, key):
        """Called on command start."""
        if not self.started:
            self.started = True
            if self.eh is not None:
                self.eh.ev_start(self)
        elif self.eh is not None:
            _eh_sigspec_invoke_compat(self.eh.ev_pickup, 2, self, key)

    def _on_close(self, key, rc=None):
        """Called to generate events when the Worker is closing."""
        self.current_rc = rc
        if rc is not None:
            self.task._rc_set(self, key, rc)
        if self.eh is not None:
            _eh_sigspec_invoke_compat(self.eh.ev_hup, 2, self, key, rc)

    def _on_written(self, key, bytes_count, sname):
        """Notification of bytes written."""
        self.current_sname = sname
        if self.eh is not None:
            _eh_sigspec_invoke_compat(self.eh.ev_written, 5, self, key, sname, bytes_count)