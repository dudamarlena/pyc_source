# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/newnet.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 4586 bytes
"""Creates new network subsystem with virtual eth device."""
import errno, os, logging, multiprocessing
from . import utils
from . import iptables
from . import netdev
from .syscall import unshare
_LOGGER = logging.getLogger(__name__)

def create_newnet(veth, dev_ip, gateway_ip, service_ip=None):
    """Unshares network subsystem and setup virtual interface in the given
    container network namespace.

    The steps are:

    - Fork a child (child shares original network)
    - Unshare network subsystem namespace
    - Signal to the child that we are ready
    - Child creates virtual eth device and moves one end to the new namespace
    - Child exits

    :param dev_ip:
        IP address of the node side of the virtual interface
    :type dev_ip:
        ``str``
    :param gateway_ip:
        Gateway IP address for the node side of the virtual interface
    :type gateway_ip:
        ``str``
    :param service_ip:
        Service IP address of the host the container is running on
        (tm_env.host_ip). If ``None`` that indicates not to use the host IP for
        the container.
    :type service_ip:
        ``str``
    """
    pid = os.getpid()
    unshared_event = multiprocessing.Event()
    childpid = os.fork()
    if childpid:
        unshare.unshare(unshare.CLONE_NEWNET)
        unshared_event.set()
        while True:
            try:
                _pid, _status = os.waitpid(childpid, 0)
                break
            except OSError as exc:
                if exc.errno == errno.EINTR:
                    _LOGGER.info('waitpid interrupted, cont.')
                else:
                    _LOGGER.exception('unhandled waitpid exception')
                    raise

        _configure_veth(veth, dev_ip, gateway_ip, service_ip)
    else:
        unshared_event.wait()
        unshared_event = None
        netdev.link_set_netns(veth, pid)
        utils.sys_exit(0)


def _configure_veth(veth, dev_ip, gateway_ip, service_ip=None):
    """Configures the network interface of the container.

    The function should be invoked in the context of unshared network
    subsystem.

    TODO: should we check that ifconfig is empty before proceeding?
    """
    _LOGGER.info('configure container: %s ip = %r(%r), gateway_ip = %r', veth, dev_ip, service_ip, gateway_ip)
    netdev.link_set_up('lo')
    netdev.link_set_name(veth, 'eth0')
    netdev.dev_conf_arp_ignore_set('eth0', netdev.ARP_IGNORE_DO_NOT_REPLY_ANY_ON_HOST)
    if service_ip is not None:
        netdev.addr_add('{ip}/32'.format(ip=service_ip), 'eth0', addr_scope='host')
    netdev.addr_add('{ip}/32'.format(ip=dev_ip), 'eth0', addr_scope='link')
    netdev.link_set_up('eth0')
    netdev.route_add(gateway_ip, devname='eth0', route_scope='link')
    if service_ip is None:
        route_src = dev_ip
    else:
        route_src = service_ip
    netdev.route_add('default', via=gateway_ip, src=route_src)
    iptables.initialize_container()
    if service_ip is not None:
        iptables.add_raw_rule('nat', 'PREROUTING', '-i eth0 -j DNAT --to-destination {service_ip}'.format(service_ip=service_ip))
        iptables.add_raw_rule('nat', 'POSTROUTING', '-o eth0  -j SNAT --to-source {container_ip}'.format(container_ip=dev_ip))