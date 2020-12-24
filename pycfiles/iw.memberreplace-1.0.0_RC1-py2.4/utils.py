# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/memberreplace/utils.py
# Compiled at: 2009-03-07 19:02:29
"""
Misc utilities
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from logging import getLogger
from zope.i18nmessageid import MessageFactory
from iw.memberreplace.config import PRODUCTNAME, I18N_DOMAIN
logger = getLogger(PRODUCTNAME)
LOG = logger.info
IwMemberReplaceMessageFactory = MessageFactory(I18N_DOMAIN)