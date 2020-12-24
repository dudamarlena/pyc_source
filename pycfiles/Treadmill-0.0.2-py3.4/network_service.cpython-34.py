# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/services/network_service.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 9850 bytes
"""Bridge based network management service."""
import errno, logging, os, subprocess
from .. import logcontext as lc
from .. import netdev
from .. import vipfile
from .. import iptables
from ._base_service import BaseResourceServiceImpl
_LOGGER = lc.ContainerAdapter(logging.getLogger(__name__))

class NetworkResourceService(BaseResourceServiceImpl):
    __doc__ = 'Network link resource service.\n    '
    __slots__ = ('ext_mtu', 'ext_speed', '_bridge_mtu', '_devices', '_vips')
    PAYLOAD_SCHEMA = (
     (
      'environment', True, str),)
    _VIPS_DIR = 'vips'
    _TMBR_DEV = 'br0'
    _TM_DEV0 = 'tm0'
    _TM_DEV1 = 'tm1'
    _TM_IP = '192.168.254.254'

    def __init__(self, ext_device, ext_mtu=None, ext_speed=None):
        super(NetworkResourceService, self).__init__()
        self._vips = None
        self._devices = {}
        self._bridge_mtu = 0
        if ext_mtu is None:
            self.ext_mtu = netdev.dev_mtu(ext_device)
        else:
            self.ext_mtu = ext_mtu
        if ext_speed is None:
            self.ext_speed = netdev.dev_speed(ext_device)
        else:
            self.ext_speed = ext_speed

    def initialize(self, service_dir):
        super(NetworkResourceService, self).initialize(service_dir)
        vips_dir = os.path.join(service_dir, self._VIPS_DIR)
        self._vips = vipfile.VipMgr(vips_dir, self._service_rsrc_dir)
        self._vips.garbage_collect()
        need_init = False
        try:
            netdev.link_set_up(self._TM_DEV0)
            netdev.link_set_up(self._TM_DEV1)
            netdev.link_set_up(self._TMBR_DEV)
        except subprocess.CalledProcessError:
            need_init = True

        if need_init:
            self._bridge_initialize()
            self._vips.initialize()
        netdev.bridge_setfd(self._TMBR_DEV, 0)
        netdev.dev_conf_route_localnet_set(self._TM_DEV0, True)
        self._bridge_mtu = netdev.dev_mtu(self._TMBR_DEV)
        self._devices = {}
        for device in netdev.bridge_brif(self._TMBR_DEV):
            if device == self._TM_DEV1:
                continue
            dev_info = _device_info(device)
            self._devices[dev_info['alias']] = dev_info

        for ip, resource in self._vips.list():
            if resource not in self._devices:
                self._vips.free(resource, ip)
                continue
            self._devices[resource]['ip'] = ip

        for device in self._devices:
            self._devices[device]['stale'] = True

    def synchronize(self):
        modified = False
        for app_unique_name in self._devices.keys():
            if not self._devices[app_unique_name].get('stale', False):
                continue
            modified = True
            self.on_delete_request(app_unique_name)

        if not modified:
            return
        self._bridge_mtu = netdev.dev_mtu(self._TMBR_DEV)

    def report_status(self):
        status = {'bridge_dev': self._TMBR_DEV, 
         'bridge_mtu': self._bridge_mtu, 
         'int_dev': self._TM_DEV0, 
         'int_ip': self._TM_IP, 
         'ext_mtu': self.ext_mtu, 
         'ext_speed': self.ext_speed}
        status['devices'] = self._devices
        return status

    def on_create_request(self, rsrc_id, rsrc_data):
        """
        :returns ``dict``:
            Network IP `vip`, network device `veth`, IP gateway `gateway`.
        """
        with lc.LogContext(_LOGGER, rsrc_id) as (log):
            log.logger.debug('req: %r', rsrc_data)
            app_unique_name = rsrc_id
            environment = rsrc_data['environment']
            assert environment in set(['dev', 'qa', 'uat', 'prod']), 'Unknown environment: %r' % environment
            veth0, veth1 = _devive_from_rsrc_id(app_unique_name)
            if app_unique_name not in self._devices:
                ip = self._vips.alloc(rsrc_id)
                iptables.add_mark_rule(ip, environment)
                netdev.link_add_veth(veth0, veth1)
                netdev.link_set_mtu(veth0, self.ext_mtu)
                netdev.link_set_mtu(veth1, self.ext_mtu)
                netdev.link_set_alias(veth0, rsrc_id)
                netdev.link_set_alias(veth1, rsrc_id)
                netdev.bridge_addif(self._TMBR_DEV, veth0)
                netdev.link_set_up(veth0)
            else:
                ip = self._devices[app_unique_name]['ip']
            self._devices[app_unique_name] = _device_info(veth0)
            self._devices[app_unique_name].update({'ip': ip, 
             'environment': environment})
        result = {'vip': ip, 
         'veth': veth1, 
         'gateway': self._TM_IP}
        return result

    def on_delete_request(self, rsrc_id):
        app_unique_name = rsrc_id
        with lc.LogContext(_LOGGER, rsrc_id):
            veth, _ = _devive_from_rsrc_id(app_unique_name)
            try:
                netdev.dev_state(veth)
                netdev.link_del_veth(veth)
            except (OSError, IOError) as err:
                if err.errno != errno.ENOENT:
                    raise

            dev_info = self._devices.pop(app_unique_name, None)
            if dev_info is not None:
                if 'ip' in dev_info:
                    iptables.delete_mark_rule(dev_info['ip'], dev_info['environment'])
                    self._vips.free(app_unique_name, dev_info['ip'])
        return True

    def _bridge_initialize(self):
        """Reset/initialize the Treadmill node bridge.
        """
        try:
            netdev.link_set_down(self._TM_DEV0)
            netdev.bridge_delete(self._TM_DEV0)
        except subprocess.CalledProcessError:
            pass

        try:
            netdev.link_set_down(self._TM_DEV0)
            netdev.link_del_veth(self._TM_DEV0)
        except subprocess.CalledProcessError:
            pass

        try:
            netdev.link_set_down(self._TMBR_DEV)
            netdev.bridge_delete(self._TMBR_DEV)
        except subprocess.CalledProcessError:
            pass

        netdev.bridge_create(self._TMBR_DEV)
        netdev.bridge_setfd(self._TMBR_DEV, 0)
        netdev.link_add_veth(self._TM_DEV0, self._TM_DEV1)
        netdev.link_set_mtu(self._TM_DEV0, self.ext_mtu)
        netdev.link_set_mtu(self._TM_DEV1, self.ext_mtu)
        netdev.bridge_addif(self._TMBR_DEV, self._TM_DEV1)
        tm_mac = netdev.dev_mac(self._TM_DEV1)
        netdev.link_set_addr(self._TMBR_DEV, tm_mac)
        netdev.link_set_up(self._TMBR_DEV)
        netdev.link_set_up(self._TM_DEV1)
        netdev.addr_add(addr='{ip}/16'.format(ip=self._TM_IP), devname=self._TM_DEV0)
        netdev.dev_conf_route_localnet_set(self._TM_DEV0, True)
        netdev.link_set_up(self._TM_DEV0)


def _device_info(device):
    """Gather a given device information.
    """
    return {'device': device, 
     'mtu': netdev.dev_mtu(device), 
     'speed': netdev.dev_speed(device), 
     'alias': netdev.dev_alias(device)}


def _devive_from_rsrc_id(app_unique_name):
    """Format devices names.

    :returns:
        ``tuple`` - Pair for device names based on the app_unique_name.
    """
    _, uniqueid = app_unique_name.rsplit('-', 1)
    veth0 = '{id:>013s}.0'.format(id=uniqueid)
    veth1 = '{id:>013s}.1'.format(id=uniqueid)
    return (
     veth0, veth1)