# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/gacontext/browser/browser.py
# Compiled at: 2008-05-20 05:21:26
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 60982 $'
__version__ = '$Revision: 60982 $'[11:-2]
from plone.fieldsets.fieldsets import FormFieldsets
from Products.Five.formlib import formbase
from Products.Five.browser import BrowserView
from collective.gacontext.interfaces import IGACode
from collective.gacontext.interfaces import IGAContextMarker

class GAForm(formbase.EditForm):
    """ Edit annotations form """
    __module__ = __name__
    form_fields = FormFieldsets(IGACode)


class GACondition(BrowserView):
    """Returns True or False depending on whether the current context is GA aware.
    """
    __module__ = __name__

    @property
    def _action_condition(self):
        context = self.context
        return IGAContextMarker.providedBy(context)

    def __call__(self):
        return self._action_condition