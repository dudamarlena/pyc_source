# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/tests/sampledata.py
# Compiled at: 2009-05-04 14:30:04
from zope.interface import implements
from zope.app.component.hooks import setSite
from zope.component import queryUtility, provideUtility
from z3c.sampledata.interfaces import ISampleDataPlugin
from ice.template import ITemplates, Templates

class MailTemplatesPlugin(object):
    __module__ = __name__
    implements(ISampleDataPlugin)
    name = 'templates.mail'
    dependencies = []
    schema = None

    def generate(self, context, param={}, dataSource=None, seed=None):
        setSite(context)
        templates = queryUtility(ITemplates, 'templates.mail')
        if templates is None:
            templates = Templates()
            sm = context.getSiteManager()
            sm['mail-templates'] = templates
            sm.registerUtility(templates, ITemplates, 'templates.mail')
        return templates


class SkinTemplatesPlugin(object):
    __module__ = __name__
    implements(ISampleDataPlugin)
    name = 'templates.skin'
    dependencies = []
    schema = None

    def generate(self, context, param={}, dataSource=None, seed=None):
        setSite(context)
        templates = queryUtility(ITemplates, 'templates.skin')
        if templates is None:
            templates = Templates()
            sm = context.getSiteManager()
            sm['skin-templates'] = templates
            sm.registerUtility(templates, ITemplates, 'templates.skin')
        return templates