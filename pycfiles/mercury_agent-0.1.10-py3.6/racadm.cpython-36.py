# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/hardware/obm/racadm.py
# Compiled at: 2018-10-04 17:41:36
# Size of source mod 2**32: 1450 bytes
from mercury.common.helpers import cli

class SimpleRACException(Exception):
    pass


class SimpleRAC(object):

    def __init__(self, path='racadm'):
        """

        :param path:
        """
        self.racadm_path = cli.find_in_path(path)
        if not self.racadm_path:
            raise SimpleRACException('Could not find racadm binary')

    def racadm(self, command):
        result = cli.run(('sh {} {}'.format(self.racadm_path, command)), raise_exception=False,
          ignore_error=True)
        if result.returncode:
            raise SimpleRACException('Error running racadm command: {}, code {}'.format(command, result.returncode))
        return result.stdout

    @property
    def getsysinfo(self):
        """
        Simple 'parser' for getsysinfo command
        :return:
        """
        output = self.racadm('getsysinfo')
        sys_info = {}
        key = None
        for line in output.splitlines():
            if not line:
                pass
            else:
                if '=' not in line:
                    if line.strip()[(-1)] == ':':
                        key = line[:-1]
                        sys_info[key] = {}
                        continue
                if key:
                    sub_key, d = [term.strip() for term in line.split('=', 1)]
                    if d == '::':
                        d = None
                    sys_info[key][sub_key] = d

        return sys_info