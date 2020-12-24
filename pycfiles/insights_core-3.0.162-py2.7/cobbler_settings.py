# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/cobbler_settings.py
# Compiled at: 2019-05-16 13:41:33
"""
Cobbler settings - ``/etc/cobbler/settings`` file
=================================================

The Cobbler settings file is a **YAML** file and the standard Python ``yaml``
library is used to parse it.

Sample input::

    kernel_options:
        ksdevice: bootif
        lang: ' '
        text: ~

Examples:

    >>> cobbler = shared[CobblerSettings]
    >>> 'kernel_options' in cobbler.data
    True
    >>> cobbler.data['kernel_options']['ksdevice']
    'bootif'

"""
from .. import YAMLParser, parser
from insights.specs import Specs

@parser(Specs.cobbler_settings)
class CobblerSettings(YAMLParser):
    """
    Read the ``/etc/cobbler/settings`` YAML file.
    """
    pass