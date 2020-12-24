# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jim/workspace/python_module_helm_values/reckoner_values/meta.py
# Compiled at: 2019-07-17 08:32:22
# Size of source mod 2**32: 624 bytes
from pkg_resources import get_distribution, DistributionNotFound
import re
__version_modifier__ = re.compile('^([0-9]+\\.[0-9]+\\.[0-9]+)\\.(.*)$')
__distribution_name__ = 'reckoner_values'
try:
    __version__ = re.sub(__version_modifier__, '\\g<1>-\\g<2>', get_distribution(__distribution_name__).version)
except DistributionNotFound:
    from pkgutil import get_data
    _raw_ver = get_data(__distribution_name__, 'version.txt').decode('UTF-8', 'ignore').rstrip('\r\n')
    __version__ = re.sub(__version_modifier__, '\\g<1>-\\g<2>', _raw_ver)

__author__ = 'Croud Ltd'