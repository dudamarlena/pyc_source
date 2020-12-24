# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/__init__.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 2771 bytes
from __future__ import absolute_import, division, print_function
import six, logging
logger = logging.getLogger(__name__)
from logging import NullHandler
logger.addHandler(NullHandler())
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions