# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/installers/ubuntu/apache.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1929 bytes
from boto.pyami.installers.ubuntu.installer import Installer

class Apache(Installer):
    """Apache"""

    def install(self):
        self.run('apt-get update')
        self.run('apt-get -y install apache2', notify=True, exit_on_error=True)
        self.run('apt-get -y install libapache2-mod-python', notify=True, exit_on_error=True)
        self.run('a2enmod rewrite', notify=True, exit_on_error=True)
        self.run('a2enmod ssl', notify=True, exit_on_error=True)
        self.run('a2enmod proxy', notify=True, exit_on_error=True)
        self.run('a2enmod proxy_ajp', notify=True, exit_on_error=True)
        self.stop('apache2')
        self.start('apache2')

    def main(self):
        self.install()