# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/repositories/cmsRepository.py
# Compiled at: 2011-12-27 16:02:08
from google.appengine.ext import db
from models.cmsModels import *

def clearDatastore():
    db.delete(CMSContent.all())
    db.delete(CMSLink.all())
    db.delete(ContentTag.all())
    db.delete(Menu.all())


def importTestData():
    pass