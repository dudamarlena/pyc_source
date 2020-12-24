# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Worker/Exec.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 13377 bytes
__doc__ = '\nClusterShell base worker for process-based workers.\n\nThis module manages the worker class to spawn local commands, possibly using\na nodeset to behave like a distant worker. Like other workers it can run\ncommands or copy files, locally.\n\nThis is the base class for most of other distant workers.\n'
import os
from string import Template
from ClusterShell.NodeSet import NodeSet
from ClusterShell.Worker.EngineClient import EngineClient
from ClusterShell.Worker.Worker import WorkerError, DistantWorker
from ClusterShell.Worker.Worker import _eh_sigspec_invoke_compat

def _replace_cmd(pattern, node, rank):
    """
    Replace keywords in `pattern' with value from `node' and `rank'.

    %h, %host map `node'
    %n, %rank map `rank'
    """
    variables = {'h':node, 
     'host':node, 
     'hosts':node, 
     'n':rank or 0, 
     'rank':rank or 0}

    class Replacer(Template):
        delimiter = '%'

    try:
        cmd = Replacer(pattern).substitute(variables)
    except (KeyError, ValueError) as error:
        msg = "%s is not a valid pattern, use '%%%%' to escape '%%'" % error
        raise WorkerError(msg)

    return cmd


class ExecClient(EngineClient):
    """ExecClient"""

    def __init__(self, node, command, worker, stderr, timeout, autoclose=False, rank=None):
        """
        Create an EngineClient-type instance to locally run `command'.

        :param node: will be used as key.
        """
        EngineClient.__init__(self, worker, node, stderr, timeout, autoclose)
        self.rank = rank
        self.command = command
        self.popen = None
        self.streams.set_writer((worker.SNAME_STDIN), None, retain=True)

    def _build_cmd(self):
        """
        Build the shell command line to start the commmand.

        Return a tuple containing command and arguments as a string or a list
        of string, and a dict of additional environment variables. None could
        be returned if no environment change is required.
        """
        return (
         _replace_cmd(self.command, self.key, self.rank), None)

    def _start(self):
        """Prepare command and start client."""
        cmd, cmd_env = self._build_cmd()
        shell = isinstance(cmd, str)
        task = self.worker.task
        if task.info('debug', False):
            name = self.__class__.__name__.upper().split('.')[(-1)]
            if shell:
                task.info('print_debug')(task, '%s: %s' % (name, cmd))
            else:
                task.info('print_debug')(task, '%s: %s' % (name, ' '.join(cmd)))
        self.popen = self._exec_nonblock(cmd, env=cmd_env, shell=shell)
        self._on_nodeset_start(self.key)
        return self

    def _close(self, abort, timeout):
        """Close client. See EngineClient._close()."""
        if abort:
            prc = self.popen.poll()
            if prc is None:
                try:
                    self.popen.kill()
                except OSError:
                    pass

        prc = self.popen.wait()
        self.streams.clear()
        self.invalidate()
        if prc >= 0:
            self._on_nodeset_close(self.key, prc)
        else:
            if timeout:
                assert abort, 'abort flag not set on timeout'
                self.worker._on_node_timeout(self.key)
            else:
                if not abort:
                    self._on_nodeset_close(self.key, 128 + -prc)
        self.worker._check_fini()

    def _on_nodeset_start(self, nodes):
        """local wrapper over _on_start that can also handle nodeset"""
        if isinstance(nodes, NodeSet):
            for node in nodes:
                self.worker._on_start(node)

        else:
            self.worker._on_start(nodes)

    def _on_nodeset_close(self, nodes, rc):
        """local wrapper over _on_node_rc that can also handle nodeset"""
        if isinstance(nodes, NodeSet):
            for node in nodes:
                self.worker._on_node_close(node, rc)

        else:
            self.worker._on_node_close(nodes, rc)

    def _on_nodeset_msgline(self, nodes, msg, sname):
        """local wrapper over _on_node_msgline that can also handle nodeset"""
        if isinstance(nodes, NodeSet):
            for node in nodes:
                self.worker._on_node_msgline(node, msg, sname)

        else:
            self.worker._on_node_msgline(nodes, msg, sname)

    def _flush_read(self, sname):
        """Called at close time to flush stream read buffer."""
        stream = self.streams[sname]
        if stream.readable():
            if stream.rbuf:
                self._on_nodeset_msgline(self.key, stream.rbuf, sname)

    def _handle_read(self, sname):
        """
        Handle a read notification. Called by the engine as the result of an
        event indicating that a read is available.
        """
        worker = self.worker
        task = worker.task
        key = self.key
        node_msgline = self._on_nodeset_msgline
        debug = task.info('debug', False)
        if debug:
            print_debug = task.info('print_debug')
        for msg in self._readlines(sname):
            if debug:
                print_debug(task, '%s: %s' % (key, msg))
            node_msgline(key, msg, sname)


class CopyClient(ExecClient):
    """CopyClient"""

    def __init__(self, node, source, dest, worker, stderr, timeout, autoclose, preserve, reverse, rank=None):
        """Create an EngineClient-type instance to locally run 'cp'."""
        ExecClient.__init__(self, node, None, worker, stderr, timeout, autoclose, rank)
        self.source = source
        self.dest = dest
        self.preserve = preserve
        self.reverse = reverse
        if self.reverse:
            self.isdir = os.path.isdir(self.dest)
            if not self.isdir:
                raise ValueError('reverse copy dest must be a directory')
        else:
            self.isdir = os.path.isdir(self.source)

    def _build_cmd(self):
        """
        Build the shell command line to start the rcp commmand.
        Return an array of command and arguments.
        """
        source = _replace_cmd(self.source, self.key, self.rank)
        dest = _replace_cmd(self.dest, self.key, self.rank)
        cmd_l = [
         'cp']
        if self.isdir:
            cmd_l.append('-r')
        else:
            if self.preserve:
                cmd_l.append('-p')
            if self.reverse:
                cmd_l.append(dest)
                cmd_l.append(source)
            else:
                cmd_l.append(source)
                cmd_l.append(dest)
        return (cmd_l, None)


class ExecWorker(DistantWorker):
    """ExecWorker"""
    SHELL_CLASS = ExecClient
    COPY_CLASS = CopyClient

    def __init__(self, nodes, handler, timeout=None, **kwargs):
        """Create an ExecWorker and its engine client instances."""
        DistantWorker.__init__(self, handler)
        self._close_count = 0
        self._has_timeout = False
        self._clients = []
        self.nodes = NodeSet(nodes)
        self.command = kwargs.get('command')
        self.source = kwargs.get('source')
        self.dest = kwargs.get('dest')
        (self._create_clients)(timeout=timeout, **kwargs)

    def _create_clients(self, **kwargs):
        """
        Create several shell and copy engine client instances based on worker
        properties.

        Additional arguments in `kwargs' will be used for client creation.
        There will be one client per node in self.nodes
        """
        if self.command:
            if '%hosts' in self.command or '%{hosts}' in self.command:
                (self._add_client)(self.nodes, rank=None, **kwargs)
        else:
            for rank, node in enumerate(self.nodes):
                (self._add_client)(node, rank=rank, **kwargs)

    def _add_client(self, nodes, **kwargs):
        """Create one shell or copy client."""
        autoclose = kwargs.get('autoclose', False)
        stderr = kwargs.get('stderr', False)
        rank = kwargs.get('rank')
        timeout = kwargs.get('timeout')
        if self.command is not None:
            cls = self.__class__.SHELL_CLASS
            self._clients.append(cls(nodes, self.command, self, stderr, timeout, autoclose, rank))
        else:
            if self.source:
                cls = self.__class__.COPY_CLASS
                self._clients.append(cls(nodes, self.source, self.dest, self, stderr, timeout, autoclose, kwargs.get('preserve', False), kwargs.get('reverse', False), rank))
            else:
                raise ValueError('missing command or source parameter in worker constructor')

    def _engine_clients(self):
        """
        Used by upper layer to get the list of underlying created engine
        clients.
        """
        return self._clients

    def write(self, buf, sname=None):
        """Write to worker clients."""
        sname = sname or self.SNAME_STDIN
        for client in self._clients:
            if sname in client.streams:
                client._write(sname, buf)

    def set_write_eof(self, sname=None):
        """
        Tell worker to close its writer file descriptors once flushed. Do not
        perform writes after this call.
        """
        for client in self._clients:
            client._set_write_eof(sname or self.SNAME_STDIN)

    def abort(self):
        """Abort processing any action by this worker."""
        for client in self._clients:
            client.abort()

    def _on_node_timeout(self, node):
        DistantWorker._on_node_timeout(self, node)
        self._has_timeout = True

    def _check_fini(self):
        """
        Must be called by each client when closing.

        If they are all closed, trigger the required events.
        """
        self._close_count += 1
        if not self._close_count <= len(self._clients):
            raise AssertionError
        else:
            if self._close_count == len(self._clients):
                if self.eh is not None:
                    if self._has_timeout:
                        if hasattr(self.eh, 'ev_timeout'):
                            self.eh.ev_timeout(self)
                    _eh_sigspec_invoke_compat(self.eh.ev_close, 2, self, self._has_timeout)


WORKER_CLASS = ExecWorker