# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Worker/Tree.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 22823 bytes
__doc__ = '\nClusterShell v2 tree propagation worker\n'
import base64, logging, os
from os.path import basename, dirname, isfile, normpath
import sys, tarfile, tempfile
from ClusterShell.Event import EventHandler
from ClusterShell.NodeSet import NodeSet
from ClusterShell.Worker.Worker import DistantWorker, WorkerError
from ClusterShell.Worker.Worker import _eh_sigspec_invoke_compat
from ClusterShell.Worker.Exec import ExecWorker
from ClusterShell.Propagation import PropagationTreeRouter

class MetaWorkerEventHandler(EventHandler):
    """MetaWorkerEventHandler"""

    def __init__(self, metaworker):
        self.metaworker = metaworker
        self.logger = logging.getLogger(__name__)

    def ev_start(self, worker):
        """
        Called to indicate that a worker has just started.
        """
        self.logger.debug('MetaWorkerEventHandler: ev_start')
        self.metaworker._start_count += 1
        self.metaworker._check_ini()

    def ev_read(self, worker, node, sname, msg):
        """
        Called to indicate that a worker has data to read.
        """
        self.metaworker._on_node_msgline(node, msg, sname)

    def ev_written(self, worker, node, sname, size):
        """
        Called to indicate that writing has been done.
        """
        metaworker = self.metaworker
        metaworker.current_node = node
        metaworker.current_sname = sname
        if metaworker.eh:
            metaworker.eh.ev_written(metaworker, node, sname, size)

    def ev_hup(self, worker, node, rc):
        """
        Called to indicate that a worker's connection has been closed.
        """
        self.metaworker._on_node_close(node, rc)

    def ev_close(self, worker, timedout):
        """
        Called to indicate that a worker has just finished. It may have failed
        on timeout if timedout is set.
        """
        self.logger.debug('MetaWorkerEventHandler: ev_close, timedout=%s', timedout)
        if timedout:
            for node in NodeSet._fromlist1(worker.iter_keys_timeout()):
                self.metaworker._on_node_timeout(node)

        self.metaworker._check_fini()


class TreeWorker(DistantWorker):
    """TreeWorker"""
    UNTAR_CMD_FMT = "tar -xf - -C '%s'"
    TAR_CMD_FMT = 'tar -cf - -C \'%s\' --transform "s,^\\([^/]*\\)[/]*,\\1.$(hostname -s)/," \'%s\' | base64 -w 65536'

    def __init__(self, nodes, handler, timeout, **kwargs):
        """
        Initialize Tree worker instance.

        :param nodes: Targeted nodeset.
        :param handler: Worker EventHandler.
        :param timeout: Timeout value for worker.
        :param command: Command to execute.
        :param topology: Force specific TopologyTree.
        :param newroot: Root node of TopologyTree.
        """
        DistantWorker.__init__(self, handler)
        self.logger = logging.getLogger(__name__)
        self.workers = []
        self.nodes = NodeSet(nodes)
        self.timeout = timeout
        self.command = kwargs.get('command')
        self.source = kwargs.get('source')
        self.dest = kwargs.get('dest')
        autoclose = kwargs.get('autoclose', False)
        self.stderr = kwargs.get('stderr', False)
        self.logger.debug('stderr=%s', self.stderr)
        self.remote = kwargs.get('remote', True)
        self.preserve = kwargs.get('preserve', None)
        self.reverse = kwargs.get('reverse', False)
        self._rcopy_bufs = {}
        self._rcopy_tars = {}
        self._close_count = 0
        self._start_count = 0
        self._child_count = 0
        self._target_count = 0
        self._has_timeout = False
        if self.command is None:
            if self.source is None:
                raise ValueError('missing command or source parameter in TreeWorker constructor')
        else:
            if self.source:
                if self.reverse:
                    self.stderr = True
            invoke_gw_args = []
            for envname in ('PYTHONPATH', 'CLUSTERSHELL_GW_PYTHON_EXECUTABLE', 'CLUSTERSHELL_GW_LOG_DIR',
                            'CLUSTERSHELL_GW_LOG_LEVEL', 'CLUSTERSHELL_GW_B64_LINE_LENGTH'):
                envval = os.getenv(envname)
                if envval:
                    invoke_gw_args.append('%s=%s' % (envname, envval))

            python_executable = os.getenv('CLUSTERSHELL_GW_PYTHON_EXECUTABLE', basename(sys.executable or 'python'))
            invoke_gw_args.append(python_executable)
            invoke_gw_args.extend(['-m', 'ClusterShell.Gateway', '-Bu'])
            self.invoke_gateway = ' '.join(invoke_gw_args)
            self.topology = kwargs.get('topology')
            if self.topology is not None:
                self.newroot = kwargs.get('newroot') or str(self.topology.root.nodeset)
                self.router = PropagationTreeRouter(self.newroot, self.topology)
            else:
                self.router = None
        self.upchannel = None
        self.metahandler = MetaWorkerEventHandler(self)
        self.gwtargets = {}

    def _set_task(self, task):
        """
        Bind worker to task. Called by task.schedule().
        TreeWorker metaworker: override to schedule sub-workers.
        """
        DistantWorker._set_task(self, task)
        self.topology = self.topology or task.topology
        self.router = self.router or task._default_router()
        self._launch(self.nodes)
        self._check_ini()

    def _launch(self, nodes):
        self.logger.debug('TreeWorker._launch on %s (fanout=%d)', nodes, self.task.info('fanout'))
        destdir = None
        if self.source:
            if self.reverse:
                self.logger.debug('rcopy source=%s, dest=%s', self.source, self.dest)
                destdir = self.dest
            else:
                self.logger.debug('copy source=%s, dest=%s', self.source, self.dest)
                if isfile(self.source):
                    arcname = basename(self.dest) or basename(normpath(self.source))
                    destdir = dirname(self.dest)
                else:
                    if self.dest[(-1)] == '/':
                        arcname = basename(self.source)
                    else:
                        arcname = basename(self.dest)
                    destdir = dirname(self.dest)
                self.logger.debug('copy arcname=%s destdir=%s', arcname, destdir)
        next_hops = self._distribute(self.task.info('fanout'), nodes.copy())
        self.logger.debug('next_hops=%s' % [(str(n), str(v)) for n, v in next_hops])
        for gw, targets in next_hops:
            if gw == targets:
                self.logger.debug('task.shell cmd=%s source=%s nodes=%s timeout=%s remote=%s', self.command, self.source, nodes, self.timeout, self.remote)
                self._child_count += 1
                self._target_count += len(targets)
                if self.remote:
                    if self.source:
                        self.logger.debug('_launch copy r=%s source=%s dest=%s', self.reverse, self.source, self.dest)
                        worker = self.task.copy((self.source), (self.dest), targets, handler=(self.metahandler),
                          stderr=(self.stderr),
                          timeout=(self.timeout),
                          preserve=(self.preserve),
                          reverse=(self.reverse),
                          tree=False)
                    else:
                        worker = self.task.shell((self.command), nodes=targets,
                          timeout=(self.timeout),
                          handler=(self.metahandler),
                          stderr=(self.stderr),
                          tree=False)
                else:
                    assert self.source is None
                    worker = ExecWorker(nodes=targets, command=(self.command),
                      handler=(self.metahandler),
                      timeout=(self.timeout),
                      stderr=(self.stderr))
                    self.task.schedule(worker)
                self.workers.append(worker)
                self.logger.debug('added child worker %s count=%d', worker, len(self.workers))
            else:
                self.logger.debug('trying gateway %s to reach %s', gw, targets)
                if self.source:
                    self._copy_remote(self.source, destdir, targets, gw, self.timeout, self.reverse)
                else:
                    self._execute_remote(self.command, targets, gw, self.timeout)

        if self.source:
            if not self.reverse:
                try:
                    tmptar = tempfile.TemporaryFile()
                    tar = tarfile.open(fileobj=tmptar, mode='w:')
                    tar.add((self.source), arcname=arcname)
                    tar.close()
                    tmptar.flush()
                    tmptar.seek(0)
                    rbuf = tmptar.read(32768)
                    while len(rbuf) > 0:
                        self._write_remote(rbuf)
                        rbuf = tmptar.read(32768)

                except OSError as exc:
                    raise WorkerError(exc)

    def _distribute(self, fanout, dst_nodeset):
        """distribute target nodes between next hop gateways"""
        self.router.fanout = fanout
        distribution = {}
        for gw, dstset in self.router.dispatch(dst_nodeset):
            distribution.setdefault(str(gw), NodeSet()).add(dstset)

        return tuple((NodeSet(k), v) for k, v in distribution.items())

    def _copy_remote(self, source, dest, targets, gateway, timeout, reverse):
        """run a remote copy in tree mode (using gateway)"""
        self.logger.debug('_copy_remote gateway=%s source=%s dest=%s reverse=%s', gateway, source, dest, reverse)
        self._target_count += len(targets)
        self.gwtargets.setdefault(str(gateway), NodeSet()).add(targets)
        if reverse:
            srcdir = dirname(source).replace("'", '\'"\'"\'')
            srcbase = basename(normpath(self.source)).replace("'", '\'"\'"\'')
            cmd = self.TAR_CMD_FMT % (srcdir, srcbase)
        else:
            cmd = self.UNTAR_CMD_FMT % dest.replace("'", '\'"\'"\'')
        self.logger.debug('_copy_remote: tar cmd: %s', cmd)
        pchan = self.task._pchannel(gateway, self)
        pchan.shell(nodes=targets, command=cmd, worker=self, timeout=timeout, stderr=(self.stderr),
          gw_invoke_cmd=(self.invoke_gateway),
          remote=(self.remote))

    def _execute_remote(self, cmd, targets, gateway, timeout):
        """run command against a remote node via a gateway"""
        self.logger.debug('_execute_remote gateway=%s cmd=%s targets=%s', gateway, cmd, targets)
        self._target_count += len(targets)
        self.gwtargets.setdefault(str(gateway), NodeSet()).add(targets)
        pchan = self.task._pchannel(gateway, self)
        pchan.shell(nodes=targets, command=cmd, worker=self, timeout=timeout, stderr=(self.stderr),
          gw_invoke_cmd=(self.invoke_gateway),
          remote=(self.remote))

    def _relaunch(self, previous_gateway):
        """Redistribute and relaunch commands on targets that were running
        on previous_gateway (which is probably marked unreachable by now)

        NOTE: Relaunch is always called after failed remote execution, so
        previous_gateway must be defined. However, it is not guaranteed that
        the relaunch is going to be performed using gateways (that's a feature).
        """
        targets = self.gwtargets[previous_gateway].copy()
        self.logger.debug('_relaunch on targets %s from previous_gateway %s', targets, previous_gateway)
        for target in targets:
            self.gwtargets[previous_gateway].remove(target)

        self._check_fini(previous_gateway)
        self._target_count -= len(targets)
        self._launch(targets)

    def _engine_clients(self):
        """
        Access underlying engine clients.
        """
        return []

    def _on_remote_node_msgline(self, node, msg, sname, gateway):
        """remote msg received"""
        if not self.source or not self.reverse or sname != 'stdout':
            DistantWorker._on_node_msgline(self, node, msg, sname)
            return
        encoded = self._rcopy_bufs.setdefault(node, '') + msg
        if node not in self._rcopy_tars:
            self._rcopy_tars[node] = tempfile.TemporaryFile()
        encoded_sz = len(encoded) // 4 * 4
        self._rcopy_tars[node].write(base64.b64decode(encoded[0:encoded_sz]))
        self._rcopy_bufs[node] = encoded[encoded_sz:]

    def _on_remote_node_close(self, node, rc, gateway):
        """remote node closing with return code"""
        DistantWorker._on_node_close(self, node, rc)
        self.logger.debug('_on_remote_node_close %s %s via gw %s', node, self._close_count, gateway)
        if self.source and self.reverse:
            for bnode, buf in self._rcopy_bufs.items():
                tarfileobj = self._rcopy_tars[bnode]
                if len(buf) > 0:
                    self.logger.debug('flushing node %s buf %d bytes', bnode, len(buf))
                    tarfileobj.write(buf)
                tarfileobj.flush()
                tarfileobj.seek(0)
                tmptar = tarfile.open(fileobj=tarfileobj)
                try:
                    try:
                        self.logger.debug('%s extracting %d members in dest %s', bnode, len(tmptar.getmembers()), self.dest)
                        tmptar.extractall(path=(self.dest))
                    except IOError as ex:
                        self._on_remote_node_msgline(bnode, ex, 'stderr', gateway)

                finally:
                    tmptar.close()

            self._rcopy_bufs = {}
            self._rcopy_tars = {}
        self.gwtargets[str(gateway)].remove(node)
        self._close_count += 1
        self._check_fini(gateway)

    def _on_remote_node_timeout(self, node, gateway):
        """remote node timeout received"""
        DistantWorker._on_node_timeout(self, node)
        self.logger.debug('_on_remote_node_timeout %s via gw %s', node, gateway)
        self._close_count += 1
        self._has_timeout = True
        self.gwtargets[str(gateway)].remove(node)
        self._check_fini(gateway)

    def _on_node_close(self, node, rc):
        DistantWorker._on_node_close(self, node, rc)
        self.logger.debug('_on_node_close %s %s (%s)', node, rc, self._close_count)
        self._close_count += 1

    def _on_node_timeout(self, node):
        DistantWorker._on_node_timeout(self, node)
        self._close_count += 1
        self._has_timeout = True

    def _check_ini(self):
        self.logger.debug('TreeWorker: _check_ini (%d, %d)', self._start_count, self._child_count)
        if self.eh:
            if self._start_count >= self._child_count:
                self.eh.ev_start(self)
                for node in self.nodes:
                    _eh_sigspec_invoke_compat(self.eh.ev_pickup, 2, self, node)

    def _check_fini(self, gateway=None):
        self.logger.debug('check_fini %s %s', self._close_count, self._target_count)
        if self._close_count >= self._target_count:
            handler = self.eh
            if handler:
                if self._has_timeout:
                    if hasattr(handler, 'ev_timeout'):
                        handler.ev_timeout(self)
                _eh_sigspec_invoke_compat(handler.ev_close, 2, self, self._has_timeout)
        if gateway:
            targets = self.gwtargets[str(gateway)]
            if not targets:
                self.logger.debug('TreeWorker._check_fini %s call pchannel_release for gw %s', self, gateway)
                self.task._pchannel_release(gateway, self)
                del self.gwtargets[str(gateway)]

    def _write_remote(self, buf):
        """Write buf to remote clients only."""
        for gateway, targets in self.gwtargets.items():
            assert len(targets) > 0
            self.task._pchannel(gateway, self).write(nodes=targets, buf=buf, worker=self)

    def write(self, buf):
        """Write to worker clients."""
        osexc = None
        for worker in self.workers:
            try:
                worker.write(buf)
            except OSError as exc:
                osexc = exc

        self._write_remote(buf)
        if osexc:
            raise osexc

    def set_write_eof(self):
        """
        Tell worker to close its writer file descriptor once flushed. Do not
        perform writes after this call.
        """
        for worker in self.workers:
            worker.set_write_eof()

        for gateway, targets in self.gwtargets.items():
            assert len(targets) > 0
            self.task._pchannel(gateway, self).set_write_eof(nodes=targets, worker=self)

    def abort(self):
        """Abort processing any action by this worker."""
        raise NotImplementedError('see github issue #229')


WorkerTree = TreeWorker