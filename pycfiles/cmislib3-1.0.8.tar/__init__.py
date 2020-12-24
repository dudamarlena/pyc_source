# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/__init__.py
# Compiled at: 2014-04-29 16:41:13
__doc__ = '\nDefine package contents so that they are easy to import.\n'
from cmislib.model import CmisClient
from cmislib.domain import Repository, Folder
from cmislib.cmis_services import Binding, RepositoryServiceIfc
__all__ = [
 'Binding', 'CmisClient', 'RepositoryServiceIfc', 'Repository', 'Folder']