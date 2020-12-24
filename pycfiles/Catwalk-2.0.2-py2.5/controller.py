# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/catwalk/tg2/controller.py
# Compiled at: 2009-02-02 23:09:07
"""

Catwalk Module

Classes:
Name                               Description
Catwalk

Copywrite (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""
from tgext.admin import AdminController
from tgext.admin.tgadminconfig import TGAdminConfig
import warnings
from sqlalchemy import MetaData
from sqlalchemy.orm import _mapper_registry
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import ScopedSession

class Catwalk(AdminController):
    config_type = TGAdminConfig

    def __init__(self, models, session=None, metadata=None):
        if isinstance(session, MetaData):
            metadata = session
            session = models
            models = []
        if isinstance(models, (ScopedSession, Session)):
            session = models
            models = []
        if metadata is not None:
            for item in _mapper_registry:
                if item.tables[0] is not None and item.tables[0].bind == session.bind:
                    models.append(item.class_)

            warnings.warn('metadata variable is deprecated and no longer needed.  Please send in a list of models\nor your model module for catwalk to find your models  The new signiture is  Catalk(models, DBSession)')
        super(Catwalk, self).__init__(models, session, config_type=self.config_type)
        return