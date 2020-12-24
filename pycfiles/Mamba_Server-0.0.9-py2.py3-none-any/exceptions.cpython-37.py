# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/exceptions.py
# Compiled at: 2020-05-12 02:33:25
# Size of source mod 2**32: 493 bytes
"""
Mamba core exceptions
These exceptions are documented in docs/topics/exceptions.rst. Please don't add
new exceptions here without documenting them there.
"""

class ComponentConfigException(Exception):
    __doc__ = 'Indicates a missing configuration situation'


class LaunchFileException(Exception):
    __doc__ = 'Indicates a wrong launch file situation'


class ComponentSettingsException(Exception):
    __doc__ = 'Indicates a wrongly formed setting situation'