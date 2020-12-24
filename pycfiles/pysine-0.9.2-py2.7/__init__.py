# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysine/__init__.py
# Compiled at: 2017-08-28 11:27:25
from ._version import __version_info__, __version__
__author__ = 'Leonhard Neuhaus <neuhaus@lkb.upmc.fr>'
__license__ = 'GNU General Public License 3 (GPLv3)'
import logging
logging.basicConfig()
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.INFO)
from .pysine import *