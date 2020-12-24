# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/edc_fabric/fabfile/apache.py
# Compiled at: 2017-04-21 13:52:06
# Size of source mod 2**32: 545 bytes
from fabric.api import sudo, task, env
from .constants import LINUX, MACOSX

@task
def disable_apache(target_os=None, prompt=None):
    target_os = target_os or env.target_os
    if target_os == LINUX:
        sudo('systemctl stop apache2.service', warn_only=True)
        sudo('systemctl disable apache2', warn_only=True)
    else:
        if target_os == MACOSX:
            sudo('launchctl unload -w /System/Library/LaunchDaemons/org.apache.httpd.plist', warn_only=True)
        else:
            raise Exception("Unknown OS/System. Got '{}'".format(target_os))