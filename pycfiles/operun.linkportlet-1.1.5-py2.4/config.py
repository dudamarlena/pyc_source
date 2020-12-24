# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/operun/linkportlet/config.py
# Compiled at: 2009-04-08 09:06:23
"""Common configuration constants
"""
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('operun.linkportlet')
PROJECTNAME = 'operun.linkportlet'
ADD_PERMISSIONS = {'operun Link Area': 'operun: Add operun Link Area', 'operun Link Folder': 'operun: Add operun Link Folder', 'operun Link': 'operun: Add operun Link'}
LINK_TYPE_VOCABULARY = [
 (
  'internal', _('internal', default='Internal link')), ('external', _('external', default='External link'))]
LINK_TARGET_VOCABULARY = [
 (
  'same', _('same_window', default='Same browser window')), ('new', _('new_window', default='New browser window'))]