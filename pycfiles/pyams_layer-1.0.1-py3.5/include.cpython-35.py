# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_layer/include.py
# Compiled at: 2020-02-21 07:39:56
# Size of source mod 2**32: 953 bytes
"""PyAMS_layer.include module

This module is used for Pyramid integration
"""
from pyams_layer.skin import apply_skin, get_skin
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_layer:locales')
    config.add_request_method(apply_skin, 'apply_skin')
    config.add_request_method(get_skin, 'get_skin')
    config.scan()