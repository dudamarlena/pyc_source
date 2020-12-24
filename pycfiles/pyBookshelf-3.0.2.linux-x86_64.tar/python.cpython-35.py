# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/python.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 347 bytes
from fabric.api import sudo, settings, run, hide

def update_system_pip_to_latest_pip():
    """ install the latest pip """
    sudo('pip install --quiet --upgrade pip')


def update_to_latest_pip():
    """ install the latest pip """
    run('pip install --quiet --upgrade pip')