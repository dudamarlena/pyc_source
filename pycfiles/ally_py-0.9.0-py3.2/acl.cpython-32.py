# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/internationalization/acl.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jan 14, 2013

@package: superdesk user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Setup for the access control layer.
"""
from ..acl import acl
from ..acl.acl import aclRight
from ally.container import ioc
from ally.internationalization import NC_
from internationalization.api.file import IFileService
from internationalization.api.json_locale import IJSONLocaleFileService
from internationalization.api.message import IMessageService
from internationalization.api.po_file import IPOFileService
from internationalization.api.source import ISourceService

@ioc.entity
def rightTranslationAccess():
    return aclRight(NC_('security', 'Translation access'), NC_('security', '\n    Allows read only access to the translation files.'))


@ioc.entity
def rightTranslationManage():
    return aclRight(NC_('security', 'Translation manage'), NC_('security', '\n    Allows for the modification of translatable messages that the application uses.'))


@ioc.entity
def rightTranslationModify():
    return aclRight(NC_('security', 'Translation modify'), NC_('security', '\n    Allows for the modification of translation files by the upload of updated PO files.'))


@acl.setup
def updateAcl():
    rightTranslationAccess().allGet(IPOFileService, IJSONLocaleFileService)
    rightTranslationManage().all(IFileService, ISourceService, IMessageService)
    rightTranslationModify().all(IPOFileService)