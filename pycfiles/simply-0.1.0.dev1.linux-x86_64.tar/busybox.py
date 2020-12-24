# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/simply/frontends/busybox.py
# Compiled at: 2016-09-26 10:29:43
from .linux import UnixFrontend

def get_instance(platform, conf):
    return this_class(platform, conf)


class BusyboxFrontend(UnixFrontend):

    def install_package(self, *package):
        self.execute(('opkg-install {}').format((' ').join(package)))

    def get_version(self, app):
        raise RuntimeError("Method 'get_versio'n is not available")


this_class = BusyboxFrontend