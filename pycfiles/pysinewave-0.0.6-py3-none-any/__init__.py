# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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