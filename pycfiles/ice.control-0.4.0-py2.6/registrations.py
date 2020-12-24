# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/details/localregistry/registrations.py
# Compiled at: 2010-08-27 06:32:04
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.component.browser.registration import SiteRegistrationView

class LocalRegistrations(SiteRegistrationView):
    render = ViewPageTemplateFile('registrations.pt')