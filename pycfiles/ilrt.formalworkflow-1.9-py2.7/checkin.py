# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/formalworkflow/browser/checkin.py
# Compiled at: 2013-06-23 12:02:23
from plone.app.iterate.browser.checkin import Checkin as BaseCheckin
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Checkin(BaseCheckin):
    """ This seems to be the only way to override the template 
        because its set in the base class and so the zcml template directive
        is unusable
    """
    template = ViewPageTemplateFile('checkin.pt')