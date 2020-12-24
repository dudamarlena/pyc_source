# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/virt/drivers/geatslocal.py
# Compiled at: 2013-07-03 00:54:28
from ..exceptions import DriverException
import subprocess, json, os

def local_call(action, **kwargs):
    p = subprocess.Popen(['geats_jsonagent'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    request = json.dumps({'action': action, 'data': kwargs})
    p.stdin.write(request)
    p.stdin.close()
    result = p.stdout.read()
    exit_code = p.wait()
    if exit_code == 0:
        jresult = json.loads(result)
        assert type(jresult) == dict
        if jresult.get('success', False):
            return jresult.get('data', None)
        errorcode = jresult.get('errorcode', 'undefined')
        message = jresult.get('message', 'check logs')
        exceptionmsg = '%s: %s' % (errorcode, message)
        raise DriverException(exceptionmsg)
    else:
        raise DriverException('geats_jsonagent exited with %d' % (exit_code,))
    return


class GeatsLocal(object):
    """
    Driver to talk to a local Geats install.
    """

    def __init__(self, manager, local_config):
        self.config = local_config

    def _call(self, action, node=None, timeout=60, **kwargs):
        return local_call(action, **kwargs)

    def _call_single(self, action, node, vm, timeout=60, **kwargs):
        vm_name = vm.node_id
        return local_call(action, vm_name=vm.node_id, **kwargs)

    _call_single_exc = _call_single

    def _call_boolean(self, action, node, vm, timeout=60, **kwargs):
        result = self._call_single(action, node, vm, timeout, **kwargs)
        return True

    def provision(self, node, vm):
        """Request a node to define & provision a VM"""
        return self._call_single_exc('provision', node, vm, definition=vm.definition)

    def define(self, node, vm):
        """Request node to define a VM"""
        return self._call_single_exc('define', node, vm, definition=vm.definition)

    def undefine(self, node, vm):
        """Request node to undefine a VM"""
        return self._call_boolean('undefine', node, vm)

    def deprovision(self, node, vm):
        """Request node to undefine & deprovision a VM"""
        return self._call_boolean('deprovision', node, vm)

    def start(self, node, vm):
        """Request node to start the VM"""
        return self._call_boolean('start', node, vm, timeout=10)

    def reboot(self, node, vm):
        """Request node to reboot the VM"""
        return self._call_boolean('reboot', node, vm, timeout=10)

    def stop(self, node, vm):
        """Request node to stop (forcefully) the VM"""
        return self._call_boolean('stop', node, vm, timeout=10)

    def shutdown(self, node, vm):
        """Request node to shutdown (nicely) the VM"""
        return self._call_boolean('shutdown', node, vm, timeout=10)

    def info(self, node, vm):
        """Request information about the given VM from the node"""
        info = self._call_single_exc('info', node, vm, timeout=5)
        if info:
            info['node'] = unicode(node.node_id)
        return info

    def status(self, node=None):
        """Request information about all VMs from the node"""
        res = self._call('status', node, timeout=5)
        if len(res) == 0:
            raise DriverException('No results received for %s' % node)
        nodes = []
        node_name = os.uname()[1]
        if node is None:
            pass
        else:
            if node.node_id != node_name:
                raise DriverException("Cannot contact remote node '%s' using GeatsLocal driver" % (node.node_id,))
            for vm in res['vms'].values():
                vm['_parent'] = node_name
                vm['_name'] = vm['definition']['name']
                vm['_type'] = 'vm'
                nodes.append(vm)

        hv = res.get('status', {})
        hv['_parent'] = None
        hv['_name'] = node_name
        hv['_type'] = 'hv'
        nodes.append(hv)
        return nodes

    def migrate(self, node, vm, destination_node):
        """Request the node to migrate the given VM to the destination node"""
        return NotImplemented