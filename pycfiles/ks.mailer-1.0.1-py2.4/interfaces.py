# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/mailer/interfaces.py
# Compiled at: 2008-12-22 08:12:48
"""Interfaces for the Zope 3 based mailer package

$Id: interfaces.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.interface import Interface
from zope.schema import Choice
from ks.mailer import _

class IMailer(Interface):
    __module__ = __name__
    template = Choice(title=_('Template'), vocabulary='Message Template Vocabulary')

    def execute(**kw):
        pass


class ITemplateAdaptable(Interface):
    __module__ = __name__


class ITemplate(ITemplateAdaptable):
    __module__ = __name__

    def __call__(**kw):
        pass