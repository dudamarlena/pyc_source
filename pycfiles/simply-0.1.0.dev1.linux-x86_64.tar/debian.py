# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/simply/frontends/debian.py
# Compiled at: 2016-09-26 10:29:43
from .. import utils
from .linux import UnixFrontend

def get_instance(platform, conf):
    return this_class(platform, conf)


class DebianFrontend(UnixFrontend):

    def install_package(self, *package):
        if self.package_installer_init:
            self.execute('apt-get update && apt-get upgrade -y')
            self.package_installer_init = False
        self.execute(('apt-get install -y {}').format((' ').join(package)))

    def get_version(self, app):
        output = self.execute(('apt-cache policy {}').format(app), user='root')
        try:
            return utils.extract_column(utils.filter_column(output, 0, startswith='Install'), 1, sep=':')[0]
        except IndexError:
            pass


this_class = DebianFrontend