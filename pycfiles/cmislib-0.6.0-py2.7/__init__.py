# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/__init__.py
# Compiled at: 2014-04-29 16:41:13
"""
Define package contents so that they are easy to import.
"""
from cmislib.model import CmisClient
from cmislib.domain import Repository, Folder
from cmislib.cmis_services import Binding, RepositoryServiceIfc
__all__ = [
 'Binding', 'CmisClient', 'RepositoryServiceIfc', 'Repository', 'Folder']