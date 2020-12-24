# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/env_platforms.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 3264 bytes
"""This module contains mappings to construct platform-specific
identifying information that will be used by the EnvGetter to apply
the appoprirate specific subsections of the pdk_environment files.

By its nature, this information is expected to be site-specific.
Users may need or wish to tailor it for their specific test situation."""
import platform
hierarchy = [
 'os',
 'osver',
 'cpu',
 'hostname']
cpudict = dict(i386='x86', i686='x86')

class PlatformType(object):
    __doc__ = 'Base class from which specific sub-classes that need special\n    handling can be instantiated.'

    def __init__(self):
        """Constructor takes no arguments because it will call platform
        routines."""
        self.os = platform.system().lower()
        self.osver = None
        self.cpu = None
        self.hostname = platform.node().split('.')[0]
        self.processor = platform.processor().lower()
        self.uname = [x.lower() for x in platform.uname()]
        self.dist = [x.lower() for x in platform.dist()]
        self.arch = platform.architecture()[0].lower()
        self.makecpu()
        self.makeosver()

    def makecpu(self):
        self.cpu = cpudict.get(self.processor, self.processor)
        if self.os in ('sunos', ):
            self.cpu = ''.join([self.cpu, self.arch])

    def makeosver(self):
        if self.os in ('linux', ):
            ver = self.dist[1].split('.')[0]
            self.osver = ''.join([self.dist[0], ver])
        else:
            if self.os in ('darwin', ):
                ver = self.uname[2].split('.')[0]
                self.osver = ''.join([self.uname[0], ver])
            if self.os in ('sunos', ):
                ver = self.uname[2].split('.')[1]
                self.osver = ''.join([self.uname[0], ver])

    def __iter__(self):
        """Iterates through the relevant attributes in the order given by
        the hierarchy, and returns the section name. This is expected to
        be the primary interface used by envgetter."""
        for i, item in enumerate(hierarchy):
            yield self.getsecname(i)

    def query(self):
        """For debugging purposes"""
        print(self.os)
        print(self.osver)
        print(self.cpu)
        print(self.hostname)

    def getsecname(self, index):
        """The real UI: returns the section name corresponding to the ith
        element of the ordered list. This section name will be matched to
        the environment file."""
        item = hierarchy[index]
        secname = '%s=%s' % (item, self.__getattribute__(item))
        return secname


if __name__ == '__main__':
    p = PlatformType()
    for i in range(4):
        print(p.getsecname(i))