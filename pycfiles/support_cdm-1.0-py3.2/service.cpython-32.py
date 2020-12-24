# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/cdm/service.py
# Compiled at: 2013-10-23 08:38:07
"""
Created on Oct 14, 2013
 
@package: support cdm
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Configuration for cdm service
"""
from os import path
from ally.cdm.impl.local_filesystem import IDelivery, HTTPDelivery, LocalFileSystemLinkCDM, LocalFileSystemCDM
from ally.cdm.spec import ICDM
from ally.container import ioc

@ioc.config
def server_uri():
    """ The HTTP server URI, basically the URL where the content should be fetched from"""
    return '/content/'


@ioc.config
def repository_path():
    """ The repository absolute or relative (to the distribution folder) path """
    return path.join('workspace', 'shared', 'cdm')


@ioc.config
def use_linked_cdm():
    """ Set to true when the files should not be copied into cdm"""
    return True


@ioc.entity
def delivery() -> IDelivery:
    d = HTTPDelivery()
    d.serverURI = server_uri()
    d.repositoryPath = repository_path()
    return d


@ioc.entity
def contentDeliveryManager() -> ICDM:
    cdm = LocalFileSystemLinkCDM() if use_linked_cdm() else LocalFileSystemCDM()
    cdm.delivery = delivery()
    return cdm