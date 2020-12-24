# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/utils/installer.py
# Compiled at: 2015-11-10 03:56:22
import subprocess
from coreinit.utils.exceptions import *
from coreinit.logger import Logger

def install_pip(packages):
    for package in packages:
        Logger.info('Pip install %s' % package)
        r = subprocess.call(['pip',
         'install',
         package])
        if r != 0:
            raise ConfigurationException('failed to install %s by pip' % package)


def install_system(packages):
    for package in packages:
        Logger.info('System install %s' % package)
        r = subprocess.call(['apt-get',
         'install', '--yes', '--force-yes',
         package])
        if r != 0:
            raise ConfigurationException('failed to install %s by apt-get' % package)