# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_pagelet/include.py
# Compiled at: 2020-02-20 08:01:50
# Size of source mod 2**32: 771 bytes
"""PyAMS_pagelet.include module

This module is used for Pyramid integration
"""
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_pagelet:locales')
    config.scan()