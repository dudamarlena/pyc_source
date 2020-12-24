# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/inventory/hooks.py
# Compiled at: 2019-04-01 12:39:10
# Size of source mod 2**32: 3137 bytes
import logging
log = logging.getLogger(__name__)

class HookException(Exception):
    pass


class Hook(object):
    __doc__ = '\n    Base Hook class. Hooks provide a way to manage inventory data before or\n    after it is inserted or updated in the database and run additional \n    processes if needed.\n    '

    def __init__(self, data, *args, **kwargs):
        self.data = data

    def run(self):
        pass


class InterfaceHook(Hook):
    __doc__ = '\n    Interface data handler, this should run when updating interface data for\n    a given inventory record.\n    '

    def process_data(self):
        """
        Convert interface data to mongodb dot notation in order to update the 
        inventory record without erasing data collected asynchronously.
        """
        interfaces = self.data.pop('interfaces', [])
        for i, interface in enumerate(interfaces):
            for key, value in interface.items():
                new_key = 'interfaces.{}.{}'.format(i, key)
                self.data[new_key] = value

    def run(self):
        self.process_data()


class LLDPHook(Hook):
    __doc__ = '\n    Interface LLDP data handler, this should run when updating LLDP data for\n    a given inventory interface.\n    '

    def process_data(self):
        """
        Convert interface LLDP data to mongodb dot notation in order to update
        the interface specified by the 'interface_index' key.
        """
        try:
            lldp = self.data.pop('lldp')
            interface_index = lldp.pop('interface_index')
        except KeyError:
            raise HookException('Missing LLDP data')

        lldp_key = 'interfaces.{}.lldp'.format(interface_index)
        self.data[lldp_key] = lldp

    def run(self):
        self.process_data()


HOOK_MAP = {'interfaces':InterfaceHook, 
 'lldp':LLDPHook}

def run_hooks(hooks, data):
    """
    Calls the run method for each hook in the hooks dict.
    
    :param hooks: A dict of keys/hook classes
    :param data: Inventory data dict
    :return: 
    """
    for hook_key, hook_class in hooks.items():
        hook = hook_class(data)
        log.info('Running {} hook'.format(hook_key))
        hook.run()


def get_hooks_from_data(data):
    """
    Returns a dict of hooks based on the keys present in the data dict
    
    :param data: Inventory data dict
    :return: dict 
    """
    keys = set(data.keys()) & set(HOOK_MAP.keys())
    hooks = {key:HOOK_MAP[key] for key in keys}
    return hooks