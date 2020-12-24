# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/Gateway.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 14422 bytes
"""
ClusterShell agent launched on remote gateway nodes. This script reads messages
on stdin via the SSH connection, interprets them, takes decisions, and prints
out replies on stdout.
"""
import logging, os, sys, traceback
from ClusterShell.Event import EventHandler
from ClusterShell.NodeSet import NodeSet
from ClusterShell.Task import task_self, _getshorthostname
from ClusterShell.Engine.Engine import EngineAbortException
from ClusterShell.Worker.fastsubprocess import set_nonblock_flag
from ClusterShell.Worker.Worker import StreamWorker, FANOUT_UNLIMITED
from ClusterShell.Worker.Tree import TreeWorker
from ClusterShell.Communication import Channel, ConfigurationMessage, ControlMessage, ACKMessage, ErrorMessage, StartMessage, EndMessage, StdOutMessage, StdErrMessage, RetcodeMessage, TimeoutMessage, MessageProcessingError

def _gw_print_debug(task, line):
    """Default gateway task debug printing function"""
    logging.getLogger(__name__).debug(line)


def gateway_excepthook(exc_type, exc_value, tb):
    """
    Default excepthook for Gateway to redirect any unhandled exception
    to logger instead of stderr.
    """
    tbexc = traceback.format_exception(exc_type, exc_value, tb)
    logging.getLogger(__name__).error(''.join(tbexc))


class TreeWorkerResponder(EventHandler):
    __doc__ = 'Gateway TreeWorker handler'

    def __init__(self, task, gwchan, srcwkr):
        EventHandler.__init__(self)
        self.gwchan = gwchan
        self.srcwkr = srcwkr
        self.worker = None
        self.retcodes = {}
        self.logger = logging.getLogger(__name__)
        self.timer = None
        qdelay = task.info('grooming_delay')
        if qdelay > 0.001:
            task.set_default('stdout_msgtree', True)
            task.set_default('stderr_msgtree', True)
            self.timer = task.timer(qdelay, self, qdelay, autoclose=True)
        self.logger.debug('TreeWorkerResponder initialized grooming=%f', qdelay)

    def ev_start(self, worker):
        self.logger.debug('TreeWorkerResponder: ev_start')
        self.worker = worker

    def ev_timer(self, timer):
        """perform gateway traffic grooming"""
        if not self.worker:
            return
        logger = self.logger
        for msg_elem, nodes in self.worker.iter_errors():
            logger.debug('iter(stderr): %s: %d bytes', nodes, len(msg_elem.message()))
            self.gwchan.send(StdErrMessage(nodes, msg_elem.message(), self.srcwkr))

        for msg_elem, nodes in self.worker.iter_buffers():
            logger.debug('iter(stdout): %s: %d bytes', nodes, len(msg_elem.message()))
            self.gwchan.send(StdOutMessage(nodes, msg_elem.message(), self.srcwkr))

        self.worker.flush_buffers()
        self.worker.flush_errors()
        for rc, nodes in self.retcodes.items():
            self.logger.debug('iter(rc): %s: rc=%d', nodes, rc)
            self.gwchan.send(RetcodeMessage(nodes, rc, self.srcwkr))

        self.retcodes.clear()

    def ev_read(self, worker, node, sname, msg):
        """message received"""
        if sname == worker.SNAME_STDOUT:
            msg_class = StdOutMessage
        else:
            if sname == worker.SNAME_STDERR:
                msg_class = StdErrMessage
                self.logger.debug('TreeWorkerResponder: ev_error %s %s', node, msg)
        if self.timer is None:
            self.gwchan.send(msg_class(node, msg, self.srcwkr))

    def ev_hup(self, worker, node, rc):
        """Received end of command from one node"""
        if self.timer is None:
            self.gwchan.send(RetcodeMessage(node, rc, self.srcwkr))
        else:
            if rc in self.retcodes:
                self.retcodes[rc].add(node)
            else:
                self.retcodes[rc] = NodeSet(node)

    def ev_close(self, worker, timedout):
        """End of CTL responder"""
        self.logger.debug('TreeWorkerResponder: ev_close timedout=%s', timedout)
        if timedout:
            msg = TimeoutMessage(NodeSet._fromlist1(worker.iter_keys_timeout()), self.srcwkr)
            self.gwchan.send(msg)
        if self.timer is not None:
            self.ev_timer(None)
            self.timer.invalidate()


class GatewayChannel(Channel):
    __doc__ = 'high level logic for gateways'

    def __init__(self, task):
        Channel.__init__(self)
        self.task = task
        self.nodename = None
        self.topology = None
        self.propagation = None
        self.logger = logging.getLogger(__name__)

    def start(self):
        """initialization"""
        self._init()
        self.logger.debug('ready to accept channel communication')

    def close(self):
        """close gw channel"""
        self.logger.debug('closing gateway channel')
        self._close()

    def recv(self, msg):
        """handle incoming message"""
        try:
            self.logger.debug('handling incoming message: %s', str(msg))
            if msg.type == EndMessage.ident:
                self.logger.debug('recv: got EndMessage')
                self._close()
            else:
                if self.setup:
                    self.recv_ctl(msg)
                else:
                    if self.opened:
                        self.recv_cfg(msg)
                    else:
                        if msg.type == StartMessage.ident:
                            self.logger.debug('got start message %s', msg)
                            self.opened = True
                            self._open()
                            self.logger.debug('channel started (version %s on remote end)', self._xml_reader.version)
                        else:
                            self.logger.error('unexpected message: %s', str(msg))
                            raise MessageProcessingError('unexpected message: %s' % msg)
        except MessageProcessingError as ex:
            self.logger.error('on recv(): %s', str(ex))
            self.send(ErrorMessage(str(ex)))
            self._close()
        except EngineAbortException:
            raise
        except Exception as ex:
            self.logger.exception('on recv(): %s', str(ex))
            self.send(ErrorMessage(str(ex)))
            self._close()

    def recv_cfg(self, msg):
        """receive cfg/topology configuration"""
        if msg.type != ConfigurationMessage.ident:
            raise MessageProcessingError('unexpected message: %s' % msg)
        else:
            self.logger.debug('got channel configuration')
            hostname = _getshorthostname()
            if not msg.gateway:
                self.nodename = hostname
                self.logger.warn('gw name not provided, using system hostname %s', self.nodename)
            else:
                self.nodename = msg.gateway
        self.logger.debug('using gateway node name %s', self.nodename)
        if self.nodename.lower() != hostname.lower():
            self.logger.debug('gw name %s does not match system hostname %s', self.nodename, hostname)
        task_self().topology = self.topology = msg.data_decode()
        self.logger.debug('decoded propagation tree')
        self.logger.debug('\n%s', self.topology)
        self.setup = True
        self._ack(msg)

    def recv_ctl(self, msg):
        """receive control message with actions to perform"""
        if msg.type == ControlMessage.ident:
            self.logger.debug('GatewayChannel._state_ctl')
            if msg.action == 'shell':
                data = msg.data_decode()
                cmd = data['cmd']
                stderr = data['stderr']
                timeout = data['timeout']
                remote = data['remote']
                self.logger.debug('decoded gw invoke (%s)', data['invoke_gateway'])
                taskinfo = data['taskinfo']
                self.logger.debug('assigning task infos (%s)', data['taskinfo'])
                task = task_self()
                task._info.update(taskinfo)
                task.set_info('print_debug', _gw_print_debug)
                if task.info('debug'):
                    self.logger.setLevel(logging.DEBUG)
                self.logger.debug('inherited fanout value=%d', task.info('fanout'))
                self.logger.debug('launching execution/enter gathering state')
                responder = TreeWorkerResponder(task, self, msg.srcid)
                self.propagation = TreeWorker((msg.target), responder, timeout, command=cmd,
                  topology=(self.topology),
                  newroot=(self.nodename),
                  stderr=stderr,
                  remote=remote)
                responder.worker = self.propagation
                self.propagation.upchannel = self
                task.schedule(self.propagation)
                self.logger.debug('TreeWorker scheduled')
                self._ack(msg)
            else:
                if msg.action == 'write':
                    data = msg.data_decode()
                    self.logger.debug('GatewayChannel write: %d bytes', len(data['buf']))
                    self.propagation.write(data['buf'])
                    self._ack(msg)
                else:
                    if msg.action == 'eof':
                        self.logger.debug('GatewayChannel eof')
                        self.propagation.set_write_eof()
                        self._ack(msg)
                    else:
                        self.logger.error('unexpected CTL action: %s', msg.action)
        else:
            self.logger.error('unexpected message: %s', str(msg))

    def _ack(self, msg):
        """acknowledge a received message"""
        self.send(ACKMessage(msg.msgid))

    def ev_close(self, worker, timedout):
        """Gateway (parent) channel is closing.

        We abort the whole gateway task to stop other running workers.
        This avoids any unwanted remaining processes on gateways.
        """
        self.logger.debug('GatewayChannel: ev_close')
        self.worker.task.abort()


def gateway_main():
    """ClusterShell gateway entry point"""
    host = _getshorthostname()
    logdir = os.path.expanduser(os.environ.get('CLUSTERSHELL_GW_LOG_DIR', '/tmp'))
    loglevel = os.environ.get('CLUSTERSHELL_GW_LOG_LEVEL', 'INFO')
    try:
        log_level = getattr(logging, loglevel.upper(), logging.INFO)
        log_fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
        logging.basicConfig(level=log_level, format=log_fmt, filename=(os.path.join(logdir, '%s.gw.log' % host)))
    except (IOError, OSError):
        pass

    logger = logging.getLogger(__name__)
    sys.excepthook = gateway_excepthook
    logger.debug('Starting gateway on %s', host)
    logger.debug('environ=%s', os.environ)
    set_nonblock_flag(sys.stdin.fileno())
    set_nonblock_flag(sys.stdout.fileno())
    set_nonblock_flag(sys.stderr.fileno())
    task = task_self()
    task.set_default('stdout_msgtree', False)
    task.set_default('stderr_msgtree', False)
    if sys.stdin.isatty():
        logger.critical('Gateway failure: sys.stdin.isatty() is True')
        sys.exit(1)
    gateway = GatewayChannel(task)
    worker = StreamWorker(handler=gateway)
    worker._fanout = FANOUT_UNLIMITED
    worker.set_reader(gateway.SNAME_READER, sys.stdin)
    worker.set_writer((gateway.SNAME_WRITER), (sys.stdout), retain=False)
    task.schedule(worker)
    logger.debug('Starting task')
    try:
        task.resume()
        logger.debug('Task performed')
    except EngineAbortException as exc:
        logger.debug('EngineAbortException')
    except IOError as exc:
        logger.debug('Broken pipe (%s)', exc)
        raise
    except Exception as exc:
        logger.exception('Gateway failure: %s', exc)

    logger.debug('-------- The End --------')


if __name__ == '__main__':
    __name__ = 'ClusterShell.Gateway'
    gateway_main()