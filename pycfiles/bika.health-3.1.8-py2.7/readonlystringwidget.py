# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/widgets/readonlystringwidget.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import StringWidget
from Products.CMFCore.permissions import View
from zope.component import getMultiAdapter

class ReadonlyStringWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update({'macro': 'bika_health_widgets/readonlystringwidget', 
       'css': 'readonly'})
    security = ClassSecurityInfo()
    security.declareProtected(View, 'readonly')

    def readonly(self, context, request):
        portal_state = getMultiAdapter((context, request), name='plone_portal_state')
        if portal_state.anonymous():
            return
        else:
            return '1'
            return


registerWidget(ReadonlyStringWidget, title='ReadonlyString', description='HTML input text in readonly mode')