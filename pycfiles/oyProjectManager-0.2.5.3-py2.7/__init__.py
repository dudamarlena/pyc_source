# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/__init__.py
# Compiled at: 2012-10-23 06:33:01
__version__ = '0.2.5.3'
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S')
logging.info('Init oyProjectManager')
from oyProjectManager import config
conf = config.Config()
from oyProjectManager.models.asset import Asset
from oyProjectManager.models.auth import Client, User
from oyProjectManager.models.entity import VersionableBase, EnvironmentBase
from oyProjectManager.models.errors import CircularDependencyError
from oyProjectManager.models.link import FileLink
from oyProjectManager.models.mixins import IOMixin
from oyProjectManager.models.project import Project
from oyProjectManager.models.repository import Repository
from oyProjectManager.models.sequence import Sequence
from oyProjectManager.models.shot import Shot
from oyProjectManager.models.version import Version, VersionType, VersionTypeEnvironments, VersionStatusComparator, Version_References