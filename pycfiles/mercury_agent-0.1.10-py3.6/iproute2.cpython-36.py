# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/hwlib/iproute2.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 2040 bytes
"""
Bare minimum to get system routing information
"""
from mercury.common.helpers import cli

class IPRoute2(object):

    def __init__(self, path='ip'):
        self.ip_path = cli.find_in_path(path)
        self.raw_table = self.get_table()
        self.table = []
        self.parse_table()

    def ip(self, args):
        command = '%s %s' % (self.ip_path, args)
        return cli.run(command)

    @staticmethod
    def _dzip(l):
        _d = {}
        length = len(l)
        if length % 2:
            raise Exception('The list length is ODD, cannot unzip')
        for idx in range(0, len(l), 2):
            _d[l[idx]] = l[(idx + 1)]

        return _d

    def parse_table(self):
        singletons = [
         'dead', 'onlink', 'pervasive', 'offload', 'notify', 'linkdown']
        for line in self.raw_table.splitlines():
            if line:
                line = line.split()
                route = {'destination': line[0]}
                for singleton in singletons:
                    if singleton in line:
                        route[singleton] = True
                        line.remove(singleton)

                route.update(self._dzip(line[1:]))
                self.table.append(route)

    def get_table(self):
        return self.ip('route show')


if __name__ == '__main__':
    ip_route = IPRoute2()
    from pprint import pprint
    pprint(ip_route.table)