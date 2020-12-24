# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/iwconfig.py
# Compiled at: 2020-01-19 08:13:16
# Size of source mod 2**32: 1271 bytes
from .dependency import Dependency

class Iwconfig(Dependency):
    dependency_required = True
    dependency_name = 'iwconfig'
    dependency_url = 'apt-get install wireless-tools'

    @classmethod
    def mode(cls, iface, mode_name):
        from ..handlers.process import Process
        pid = Process(['iwconfig', iface, 'mode', mode_name])
        pid.wait()
        return pid.poll()

    @classmethod
    def get_interfaces(cls, mode=None):
        from ..handlers.process import Process
        interfaces = set()
        iface = ''
        out, err = Process.call('iwconfig')
        for line in out.split('\n'):
            if len(line) == 0:
                pass
            else:
                iface = line.startswith(' ') or line.split(' ')[0]
                if '\t' in iface:
                    iface = iface.split('\t')[0].strip()
                iface = iface.strip()
                if len(iface) == 0:
                    pass
                else:
                    if mode is None:
                        interfaces.add(iface)
                    if mode is not None and 'Mode:{}'.format(mode) in line and len(iface) > 0:
                        interfaces.add(iface)

        return list(interfaces)