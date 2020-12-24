# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/mailer/templateadapter.py
# Compiled at: 2008-12-22 08:12:48
"""IMailerSMTPAnnotation to IMailerSMTP adapter for the Zope 3 based mailersmtp package

$Id: templateadapter.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.component import getUtility
from interfaces import ITemplateAdaptable, ITemplate
from zope.security.management import getInteraction

def templateadapter(context):

    def f(**kw):
        if 'request' in kw:
            return context.render(**kw)
        else:
            request = getInteraction().participations[0]
            return context.render(request=request, **kw)

    return f


def getTemplate(name, context):
    return ITemplate(getUtility(ITemplateAdaptable, name=name, context=context))