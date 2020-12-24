# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/ifconfig.py
# Compiled at: 2020-01-19 08:12:56
# Size of source mod 2**32: 1861 bytes
import re
from .dependency import Dependency

class Ifconfig(Dependency):
    dependency_required = True
    dependency_name = 'ifconfig'
    dependency_url = 'apt-get install net-tools'

    @classmethod
    def up(cls, interface, args=[]):
        """Put interface up"""
        from ..handlers.process import Process
        command = [
         'ifconfig', interface]
        if type(args) is list:
            command.extend(args)
        else:
            if type(args) is 'str':
                command.append(args)
        command.append('up')
        pid = Process(command)
        pid.wait()
        if pid.poll() != 0:
            raise Exception('Error putting interface %s up:\n%s\n%s' % (
             interface, pid.stdout(), pid.stderr()))

    @classmethod
    def down(cls, interface):
        """Put interface down"""
        from ..handlers.process import Process
        pid = Process(['ifconfig', interface, 'down'])
        pid.wait()
        if pid.poll() != 0:
            raise Exception('Error putting interface %s down:\n%s\n%s' % (
             interface, pid.stdout(), pid.stderr()))

    @classmethod
    def get_mac(cls, interface):
        from ..handlers.process import Process
        output = Process(['ifconfig', interface]).stdout()
        mac_dash_regex = ('[a-zA-Z0-9]{2}-' * 6)[:-1]
        match = re.search(' ({})'.format(mac_dash_regex), output)
        if match:
            return match.group(1).replace('-', ':')
        mac_colon_regex = ('[a-zA-Z0-9]{2}:' * 6)[:-1]
        match = re.search(' ({})'.format(mac_colon_regex), output)
        if match:
            return match.group(1)
        raise Exception('Could not find the mac address for %s' % interface)