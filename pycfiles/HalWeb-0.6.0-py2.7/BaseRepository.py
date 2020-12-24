# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/repositories/BaseRepository.py
# Compiled at: 2011-12-27 16:01:55
from google.appengine.ext import db
import models.BaseModels as base

def clearDatastore():
    db.delete(base.Person.all())
    db.delete(base.Role.all())
    db.delete(base.WishList.all())
    db.delete(base.Invitation.all())


def importTestData():
    pass