# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/browser/addVariation.py
# Compiled at: 2008-05-06 12:38:24
from zope import event
from zope.component import getUtility
from zope.formlib import form
from Products.Archetypes.event import ObjectEditedEvent
from Acquisition import aq_inner
from Products.Five.formlib import formbase
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.form.validators import null_validator
from qi.Goban.interfaces import IAddVariation
from qi.Goban import GobanMessageFactory as _
from qi.Goban.lib.sgf2xml import *
from copy import deepcopy

class AddVariationView(formbase.PageForm):
    """Add a new variation
        """
    __module__ = __name__
    label = _('label_addVariation', default='Add variation')
    form_fields = form.FormFields(IAddVariation)

    @form.action(_('label_addAction', default='Add'))
    def action_add(self, action, data):
        """
                """
        context = aq_inner(self.context)
        try:
            sgfFile = data['varSgf']
            xmlConv = sgf2xml(sgfFile)
            newVarList = xmlConv.variations
            oldVarList = deepcopy(context.variations)
            for key in newVarList.keys():
                newVarList[key] = newVarList[key][0]

            for key in oldVarList.keys():
                oldVarList[key] = oldVarList[key][0]

            newNonDupl = [ varKey for varKey in newVarList.keys() if newVarList[varKey] not in oldVarList.values() ]
            oldNonDupl = [ varKey for varKey in oldVarList.keys() if oldVarList[varKey] not in newVarList.values() ]
            if len(oldNonDupl):
                raise Exception(_('error_origVariationNotFound', default='One or more of the original variations were not found in the file you specified. Please download the original and just add variations withoud editing existing ones.'))
            if not len(newNonDupl):
                raise Exception(_('error_noNewVariationFound', default='No new variations were found.'))
        except Exception, e:
            IStatusMessage(self.request).addStatusMessage(str(e), type='error')
        else:
            fileField = context.getField('sgf')
            filename = fileField.getFilename(context)
            context.setSGF(sgfFile)
            fileField.setFilename(context, filename)
            event.notify(ObjectEditedEvent(context))
            IStatusMessage(self.request).addStatusMessage(_('info_variationAdded', default='Variation(s) added.'), type='info')
            self.request.response.redirect(context.absolute_url())
            return ''

    @form.action(_('label_cancelAction', default='Cancel'), validator=null_validator)
    def action_cancel(self, action, data):
        """Cancel 
                """
        context = aq_inner(self.context)
        confirm = _('info_variationImportCanceled', default='Variation import cancelled.')
        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        self.request.response.redirect(context.absolute_url())
        return ''