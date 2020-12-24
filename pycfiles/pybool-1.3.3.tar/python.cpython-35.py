# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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