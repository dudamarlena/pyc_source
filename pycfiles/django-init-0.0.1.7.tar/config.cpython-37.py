# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/projects/django-init/django_init/utils/config.py
# Compiled at: 2020-01-11 18:41:43
# Size of source mod 2**32: 677 bytes
import sys, argparse, configparser, os

def get_package_namespace():
    return 'django_init'


def get_init_namespace():
    return '%s.init' % get_package_namespace()


def get_version():
    """
    Return the django-init version, which should be correct for all built-in
    commands. User-supplied commands can override this method to
    return their own version.
    """
    version = '11111'
    return version