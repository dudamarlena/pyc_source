# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\pm\src\epcpm\__init__.py
# Compiled at: 2020-05-13 16:13:04
# Size of source mod 2**32: 238 bytes
import epcpm._build
from ._version import get_versions
__version__ = get_versions()['version']
__sha__ = get_versions()['full-revisionid']
del get_versions
__version_tag__ = 'v{}'.format(__version__)
__build_tag__ = epcpm._build.job_id