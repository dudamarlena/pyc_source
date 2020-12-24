# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/__init__.py
# Compiled at: 2016-07-14 12:19:26
# Size of source mod 2**32: 1217 bytes
"""
8888888b.   d8b                                          888    888        d8888  .d8888b.   .d8888b.
888  "Y88b  Y8P                                          888    888       d88888 d88P  Y88b d88P  Y88b
888    888                                               888    888      d88P888 888    888 Y88b.
888    888 8888  8888b.  88888b.   .d88b.   .d88b.       8888888888     d88P 888 888         "Y888b.
888    888 "888     "88b 888 "88b d88P"88b d88""88b      888    888    d88P  888 888            "Y88b.
888    888  888 .d888888 888  888 888  888 888  888      888    888   d88P   888 888    888       "888
888  .d88P  888 888  888 888  888 Y88b 888 Y88..88P      888    888  d8888888888 Y88b  d88P Y88b  d88P
8888888P"   888 "Y888888 888  888  "Y88888  "Y88P"       888    888 d88P     888  "Y8888P"   "Y8888P"
            888                        888
           d88P                   Y8b d88P
         888P"                     "Y88P"
"""
try:
    from django.utils.version import get_version
except ImportError:
    from hacs.django_utils_version import get_version

VERSION = (1, 0, 0, 'beta', 1)
default_app_config = 'hacs.apps.HACSConfig'
__version__ = get_version(VERSION)