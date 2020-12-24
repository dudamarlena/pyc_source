# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Worker/Pdsh.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 9468 bytes
__doc__ = '\nWorkerPdsh\n\nClusterShell worker for executing commands with LLNL pdsh.\n'
import errno, os, shlex
from ClusterShell.NodeSet import NodeSet
from ClusterShell.Worker.EngineClient import EngineClientError
from ClusterShell.Worker.EngineClient import EngineClientNotSupportedError
from ClusterShell.Worker.Worker import WorkerError
from ClusterShell.Worker.Exec import ExecWorker, ExecClient, CopyClient

class PdshClient(ExecClient):
    """PdshClient"""
    MODE = 'pdsh'

    def __init__(self, node, command, worker, stderr, timeout, autoclose=False, rank=None):
        ExecClient.__init__(self, node, command, worker, stderr, timeout, autoclose, rank)
        self._closed_nodes = NodeSet()

    def _build_cmd(self):
        """
        Build the shell command line to start the commmand.
        Return an array of command and arguments.
        """
        task = self.worker.task
        pdsh_env = {}
        path = task.info('pdsh_path') or 'pdsh'
        cmd_l = [os.path.expanduser(pathc) for pathc in shlex.split(path)]
        cmd_l.append('-b')
        fanout = task.info('fanout', 0)
        if fanout > 0:
            cmd_l.append('-f %d' % fanout)
        connect_timeout = task.info('connect_timeout', 0)
        if connect_timeout > 0:
            pdsh_env['PDSH_SSH_ARGS_APPEND'] = '-o ConnectTimeout=%d' % connect_timeout
        command_timeout = task.info('command_timeout', 0)
        if command_timeout > 0:
            cmd_l.append('-u %d' % command_timeout)
        cmd_l.append('-w %s' % self.key)
        cmd_l.append('%s' % self.command)
        return (
         cmd_l, pdsh_env)

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
            if prc > 0:
                raise WorkerError('Cannot run pdsh (error %d)' % prc)
            self.streams.clear()
            self.invalidate()
            assert timeout and abort, 'abort flag not set on timeout'
            for node in self.key - self._closed_nodes:
                self.worker._on_node_timeout(node)

        else:
            for node in self.key - self._closed_nodes:
                self.worker._on_node_close(node, 0)

        self.worker._check_fini()

    def _parse_line(self, line, sname):
        """
        Parse Pdsh line syntax.
        """
        if line.startswith('pdsh@') or line.startswith('pdcp@') or line.startswith('sending '):
            try:
                words = line.split()
                if self.MODE == 'pdsh':
                    if len(words) == 4:
                        if words[2] == 'command':
                            if words[3] == 'timeout':
                                pass
                    if len(words) == 8:
                        if words[3] == 'exited':
                            if words[7].isdigit():
                                nodename = words[1][:-1].decode()
                                self._closed_nodes.add(nodename)
                                self.worker._on_node_close(nodename, int(words[7]))
                else:
                    if self.MODE == 'pdcp':
                        nodename = words[1][:-1].decode()
                        self._closed_nodes.add(nodename)
                        self.worker._on_node_close(nodename, errno.ENOENT)
            except Exception as exc:
                raise EngineClientError('Pdsh parser error: %s' % exc)

        else:
            nodename, msg = line.split(': ', 1)
            self.worker._on_node_msgline(nodename.decode(), msg, sname)

    def _flush_read(self, sname):
        """Called at close time to flush stream read buffer."""
        pass

    def _handle_read(self, sname):
        """Engine is telling us a read is available."""
        debug = self.worker.task.info('debug', False)
        if debug:
            print_debug = self.worker.task.info('print_debug')
        suffix = ''
        if sname == 'stderr':
            suffix = '@STDERR'
        for msg in self._readlines(sname):
            if debug:
                print_debug(self.worker.task, 'PDSH%s: %s' % (suffix, msg))
            self._parse_line(msg, sname)


class PdcpClient(CopyClient, PdshClient):
    """PdcpClient"""
    MODE = 'pdcp'

    def __init__(self, node, source, dest, worker, stderr, timeout, autoclose, preserve, reverse, rank=None):
        CopyClient.__init__(self, node, source, dest, worker, stderr, timeout, autoclose, preserve, reverse, rank)
        PdshClient.__init__(self, node, None, worker, stderr, timeout, autoclose, rank)

    def _build_cmd(self):
        cmd_l = []
        if self.reverse:
            path = self.worker.task.info('rpdcp_path') or 'rpdcp'
        else:
            path = self.worker.task.info('pdcp_path') or 'pdcp'
        cmd_l = [os.path.expanduser(pathc) for pathc in shlex.split(path)]
        cmd_l.append('-b')
        fanout = self.worker.task.info('fanout', 0)
        if fanout > 0:
            cmd_l.append('-f %d' % fanout)
        connect_timeout = self.worker.task.info('connect_timeout', 0)
        if connect_timeout > 0:
            cmd_l.append('-t %d' % connect_timeout)
        cmd_l.append('-w %s' % self.key)
        if self.isdir:
            cmd_l.append('-r')
        if self.preserve:
            cmd_l.append('-p')
        cmd_l.append(self.source)
        cmd_l.append(self.dest)
        return (
         cmd_l, None)


class WorkerPdsh(ExecWorker):
    """WorkerPdsh"""
    SHELL_CLASS = PdshClient
    COPY_CLASS = PdcpClient

    def _create_clients(self, **kwargs):
        (self._add_client)((self.nodes), **kwargs)

    def write(self, buf):
        """
        Write data to process. Not supported with Pdsh worker.
        """
        raise EngineClientNotSupportedError('writing is not supported by pdsh worker')

    def set_write_eof(self):
        """
        Tell worker to close its writer file descriptor once flushed. Do not
        perform writes after this call.

        Not supported by PDSH Worker.
        """
        raise EngineClientNotSupportedError('writing is not supported by pdsh worker')


WORKER_CLASS = WorkerPdsh