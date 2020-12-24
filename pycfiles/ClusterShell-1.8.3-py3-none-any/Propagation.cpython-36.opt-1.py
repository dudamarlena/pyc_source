# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/Propagation.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 16446 bytes
"""
ClusterShell Propagation module. Use the topology tree to send commands
through gateways and gather results.
"""
from collections import deque
import logging
from ClusterShell.Defaults import DEFAULTS
from ClusterShell.NodeSet import NodeSet
from ClusterShell.Communication import Channel
from ClusterShell.Communication import ControlMessage, StdOutMessage
from ClusterShell.Communication import StdErrMessage, RetcodeMessage
from ClusterShell.Communication import StartMessage, EndMessage
from ClusterShell.Communication import RoutedMessageBase, ErrorMessage
from ClusterShell.Communication import ConfigurationMessage, TimeoutMessage
from ClusterShell.Topology import TopologyError

class RouteResolvingError(Exception):
    __doc__ = 'error raised on invalid conditions during routing operations'


class PropagationTreeRouter(object):
    __doc__ = 'performs routes resolving operations within a propagation tree.\n    This object provides a next_hop method, that will look for the best\n    directly connected node to use to forward a message to a remote\n    node.\n\n    Upon instanciation, the router will parse the topology tree to\n    generate its routing table.\n    '

    def __init__(self, root, topology, fanout=0):
        self.root = root
        self.topology = topology
        self.fanout = fanout
        self.nodes_fanin = {}
        self.table = None
        self.table_generate(root, topology)
        self._unreachable_hosts = NodeSet()

    def table_generate(self, root, topology):
        """The router relies on a routing table. The keys are the
        destination nodes and the values are the next hop gateways to
        use to reach these nodes.
        """
        try:
            root_group = topology.find_nodegroup(root)
        except TopologyError:
            msgfmt = 'Invalid root or gateway node: %s'
            raise RouteResolvingError(msgfmt % root)

        self.table = []
        for group in root_group.children():
            dest = NodeSet()
            stack = [group]
            while len(stack) > 0:
                curr = stack.pop()
                dest.update(curr.children_ns())
                stack += curr.children()

            self.table.append((dest, group.nodeset))

    def dispatch(self, dst):
        """dispatch nodes from a target nodeset to the directly
        connected gateways.

        The method acts as an iterator, returning a gateway and the
        associated hosts. It should provide a rather good load balancing
        between the gateways.
        """
        for network, _ in self.table:
            dst_inter = network & dst
            dst.difference_update(dst_inter)
            for host in dst_inter.nsiter():
                yield (
                 self.next_hop(host), host)

        if dst:
            yield (
             dst, dst)

    def next_hop(self, dst):
        """perform the next hop resolution. If several hops are
        available, then, the one with the least number of current jobs
        will be returned
        """
        if dst in self._unreachable_hosts:
            raise RouteResolvingError('Invalid destination: %s, host is unreachable' % dst)
        if self.root == dst:
            raise RouteResolvingError('Invalid resolution request: %s -> %s' % (self.root, dst))
        for network, nexthops in self.table:
            if dst in network:
                res = self._best_next_hop(nexthops)
                if res is None:
                    raise RouteResolvingError('No route available to %s' % str(dst))
                self.nodes_fanin[res] += len(dst)
                return res
            if dst in nexthops:
                return dst

        raise RouteResolvingError('No route from %s to host %s' % (self.root, dst))

    def mark_unreachable(self, dst):
        """mark node dst as unreachable and don't advertise routes
        through it anymore. The cache will be updated only when
        necessary to avoid performing expensive traversals.
        """
        self._unreachable_hosts.add(dst)

    def _best_next_hop(self, candidates):
        """find out a good next hop gateway"""
        backup = None
        backup_connections = float('inf')
        candidates = candidates.difference(self._unreachable_hosts)
        for host in candidates:
            connections = self.nodes_fanin.setdefault(host, 0)
            if backup_connections > connections:
                backup = host
                backup_connections = connections

        return backup


class PropagationChannel(Channel):
    __doc__ = 'Admin node propagation logic. Instances are able to handle\n    incoming messages from a directly connected gateway, process them\n    and reply.\n\n    In order to take decisions, the instance acts as a finite states\n    machine, whose current state evolves according to received data.\n\n    -- INTERNALS --\n    Instance can be in one of the 4 different states:\n      - init (implicit)\n        This is the very first state. The instance enters the init\n        state at start() method, and will then send the configuration\n        to the remote node.  Once the configuration is sent away, the\n        state changes to cfg.\n\n      - cfg\n        During this second state, the instance will wait for a valid\n        acknowledgement from the gateway to the previously sent\n        configuration message. If such a message is delivered, the\n        control message (the one that contains the actions to perform)\n        is sent, and the state is set to ctl.\n\n      - ctl\n        Third state, the instance is waiting for a valid ack for from\n        the gateway to the ctl packet. Then, the state switch to gtr\n        (gather).\n\n      - gtr\n        Final state: wait for results from the subtree and store them.\n    '

    def __init__(self, task, gateway):
        """
        """
        Channel.__init__(self, initiator=True)
        self.task = task
        self.gateway = gateway
        self.workers = {}
        self._cfg_write_hist = deque()
        self._sendq = deque()
        self._rc = None
        self.logger = logging.getLogger(__name__)

    def send_queued(self, ctl):
        """helper used to send a message, using msg queue if needed"""
        if self.setup:
            if not self._sendq:
                self.send(ctl)
        else:
            self.logger.debug('send_queued: %d', len(self._sendq))
            self._sendq.appendleft(ctl)

    def send_dequeue(self):
        """helper used to send one queued message (if any)"""
        if self._sendq:
            ctl = self._sendq.pop()
            self.logger.debug('dequeuing sendq: %s', ctl)
            self.send(ctl)

    def start(self):
        """start propagation channel"""
        self._init()
        self._open()
        cfg = ConfigurationMessage(self.gateway)
        cfg.data_encode(self.task.topology)
        self.send(cfg)

    def recv(self, msg):
        """process incoming messages"""
        self.logger.debug('recv: %s', msg)
        if msg.type == EndMessage.ident:
            self.logger.debug('got EndMessage; closing')
            self.worker.abort()
        elif msg.type == StdErrMessage.ident and msg.srcid == 0:
            nodeset = NodeSet(msg.nodes)
            decoded = msg.data_decode() + b'\n'
            for metaworker in self.workers.values():
                for line in decoded.splitlines():
                    for node in nodeset:
                        metaworker._on_remote_node_msgline(node, line, 'stderr', self.gateway)

        else:
            if self.setup:
                self.recv_ctl(msg)
            else:
                if self.opened:
                    self.recv_cfg(msg)
                else:
                    if msg.type == StartMessage.ident:
                        self.opened = True
                        self.logger.debug('channel started (version %s on remote gateway)', self._xml_reader.version)
                    else:
                        self.logger.error('unexpected message: %s', str(msg))

    def shell(self, nodes, command, worker, timeout, stderr, gw_invoke_cmd, remote):
        """command execution through channel"""
        self.logger.debug('shell nodes=%s timeout=%s worker=%s remote=%s', nodes, timeout, id(worker), remote)
        self.workers[id(worker)] = worker
        ctl = ControlMessage(id(worker))
        ctl.action = 'shell'
        ctl.target = nodes
        info = dict((k, v) for k, v in self.task._info.items() if k not in DEFAULTS._task_info_pkeys_bl)
        ctl_data = {'cmd':command, 
         'invoke_gateway':gw_invoke_cmd, 
         'taskinfo':info, 
         'stderr':stderr, 
         'timeout':timeout, 
         'remote':remote}
        ctl.data_encode(ctl_data)
        self.send_queued(ctl)

    def write(self, nodes, buf, worker):
        """write buffer through channel to nodes on standard input"""
        self.logger.debug('write buflen=%d', len(buf))
        assert id(worker) in self.workers
        ctl = ControlMessage(id(worker))
        ctl.action = 'write'
        ctl.target = nodes
        ctl_data = {'buf': buf}
        ctl.data_encode(ctl_data)
        self._cfg_write_hist.appendleft((ctl.msgid, nodes, len(buf), worker))
        self.send_queued(ctl)

    def set_write_eof(self, nodes, worker):
        """send EOF through channel to specified nodes"""
        self.logger.debug('set_write_eof')
        assert id(worker) in self.workers
        ctl = ControlMessage(id(worker))
        ctl.action = 'eof'
        ctl.target = nodes
        self.send_queued(ctl)

    def recv_cfg(self, msg):
        """handle incoming messages for state 'propagate configuration'"""
        self.logger.debug('recv_cfg')
        if msg.type == 'ACK':
            self.logger.debug('CTL - connection with gateway fully established')
            self.setup = True
            self.send_dequeue()
        else:
            self.logger.debug('_state_config error (msg=%s)', msg)

    def recv_ctl(self, msg):
        """handle incoming messages for state 'control'"""
        if msg.type == 'ACK':
            self.logger.debug('got ack (%s)', msg.type)
            if self._cfg_write_hist:
                if msg.ack == self._cfg_write_hist[(-1)][0]:
                    _, nodes, bytes_count, metaworker = self._cfg_write_hist.pop()
                    for node in nodes:
                        metaworker._on_written(node, bytes_count, 'stdin')

            self.send_dequeue()
        else:
            if isinstance(msg, RoutedMessageBase):
                metaworker = self.workers[msg.srcid]
                if msg.type == StdOutMessage.ident:
                    nodeset = NodeSet(msg.nodes)
                    decoded = msg.data_decode() + b'\n'
                    for line in decoded.splitlines():
                        for node in nodeset:
                            metaworker._on_remote_node_msgline(node, line, 'stdout', self.gateway)

                else:
                    if msg.type == StdErrMessage.ident:
                        nodeset = NodeSet(msg.nodes)
                        decoded = msg.data_decode() + b'\n'
                        for line in decoded.splitlines():
                            for node in nodeset:
                                metaworker._on_remote_node_msgline(node, line, 'stderr', self.gateway)

                    else:
                        if msg.type == RetcodeMessage.ident:
                            rc = msg.retcode
                            for node in NodeSet(msg.nodes):
                                metaworker._on_remote_node_close(node, rc, self.gateway)

                        else:
                            if msg.type == TimeoutMessage.ident:
                                self.logger.debug('TimeoutMessage for %s', msg.nodes)
                                for node in NodeSet(msg.nodes):
                                    metaworker._on_remote_node_timeout(node, self.gateway)

            else:
                if msg.type == ErrorMessage.ident:
                    raise TopologyError('%s: %s' % (self.gateway, msg.reason))
                else:
                    self.logger.debug('recv_ctl: unhandled msg %s', msg)

    def ev_hup(self, worker, node, rc):
        """Channel command is closing"""
        self._rc = rc

    def ev_close(self, worker, timedout):
        """Channel is closing"""
        gateway = str(worker.nodes)
        self.logger.debug('ev_close gateway=%s %s', gateway, self)
        self.logger.debug('ev_close rc=%s', self._rc)
        if self._rc != 0:
            self.logger.debug('error on gateway %s (setup=%s)', gateway, self.setup)
            self.task.router.mark_unreachable(gateway)
            self.logger.debug('gateway %s now set as unreachable', gateway)
            if not self.setup:
                for mw in set(self.task.gateways[gateway][1]):
                    mw._relaunch(gateway)