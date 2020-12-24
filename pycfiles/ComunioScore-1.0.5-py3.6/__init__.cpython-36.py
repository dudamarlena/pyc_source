# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/__init__.py
# Compiled at: 2020-04-13 09:04:07
# Size of source mod 2**32: 535 bytes
__title__ = 'ComunioScore'
__version_info__ = ('1', '0', '5')
__version__ = '.'.join(__version_info__)
__author__ = 'Christian Bierschneider'
__email__ = 'christian.bierschneider@web.de'
__license__ = 'MIT'
import os
from ComunioScore.dbhandler import DBHandler
from ComunioScore.comunio import Comunio
from ComunioScore.dbagent import DBAgent
from ComunioScore.api import APIHandler
from ComunioScore.comuniodb import ComunioDB
from ComunioScore.sofascoredb import SofascoreDB
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))