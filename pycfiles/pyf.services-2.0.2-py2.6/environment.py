# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/config/environment.py
# Compiled at: 2010-05-21 08:57:50
"""WSGI environment setup for pyf.services."""
from pyf.services.config.app_cfg import base_config
__all__ = [
 'load_environment']
load_environment = base_config.make_load_environment()