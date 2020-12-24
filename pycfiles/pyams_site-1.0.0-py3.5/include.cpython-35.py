# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_site/include.py
# Compiled at: 2019-12-06 17:41:45
# Size of source mod 2**32: 877 bytes
"""PyAMS_site.include module

This module is used for Pyramid integration
"""
from pyams_site.site import site_factory
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_site:locales')
    config.set_root_factory(site_factory)
    config.scan()