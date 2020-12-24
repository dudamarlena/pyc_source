# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat/egg/sc/social/viewcounter/setuphandlers.py
# Compiled at: 2010-08-18 13:21:09
import os
from z3c.saconfig import named_scoped_session
from sc.social.viewcounter.pageview import Base
from sc.social.viewcounter.pageview import SCOPED_SESSION_NAME
import logging
logger = logging.getLogger('sc.social.viewcounter: setuphandlers')
Session = named_scoped_session(SCOPED_SESSION_NAME)

def isNotOurProfile(context):
    return context.readDataFile('sc.social.viewcounter.txt') is None


def create_tables(context):
    """Called at profile import time to create necessary tables
    """
    if isNotOurProfile(context):
        return
    Base.metadata.create_all(bind=Session.bind)