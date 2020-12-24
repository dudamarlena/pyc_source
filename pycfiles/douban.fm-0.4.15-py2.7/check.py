# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/check.py
# Compiled at: 2016-06-22 17:38:57
import xmlrpclib, subprocess, pip
from doubanfm.exceptions import MplayerError

def is_latest(package_name):
    pypi = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
    for dist in pip.get_installed_distributions():
        if dist.project_name == package_name:
            available = pypi.package_releases(dist.project_name)
            if available[0] != dist.version:
                return False
            return True


def update_package(package_name):
    pip.main(['install', package_name, '--upgrade'])


def is_mplayer():
    try:
        subprocess.check_output('mplayer')
    except Exception:
        raise MplayerError()