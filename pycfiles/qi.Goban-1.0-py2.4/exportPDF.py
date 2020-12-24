# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/browser/exportPDF.py
# Compiled at: 2008-05-05 04:02:00
from zope.component import getUtility
from zope.formlib import form
from Acquisition import aq_inner
from Products.Five.formlib import formbase
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.form.validators import null_validator
from qi.Goban.interfaces import IPDFDiagram
from qi.Goban import GobanMessageFactory as _

class ExportPDFView(formbase.PageForm):
    """Export game to pdf
        """
    __module__ = __name__
    label = _('label_exportPDF', default='Export PDF')
    form_fields = form.FormFields(IPDFDiagram)

    @form.action(_('label_exportAction', default='Export'))
    def action_export(self, action, data):
        """Export pdf file
                """
        context = aq_inner(self.context)
        try:
            args = '-movesPerDiagram %s' % data['movesPerDiagram']
            if data['ignoreVariations']:
                args = args + ' -ignoreVariations'
            if data['ignoreLetters']:
                args = args + ' -ignoreLetters'
            if data['ignoreMarks']:
                args = args + ' -ignoreMarks'
            from os import popen2
            (stin, stout) = popen2('sgf2dg %s -converter PDF -o STDOUT ' % args)
            stin.write(str(context.sgf))
            stin.close()
            pdf = stout.read()
            stout.close()
            self.request.response.setHeader('Content-type', 'application/pdf')
            self.request.response.setHeader('Content-disposition', 'inline;filename="diagram.pdf"')
            IStatusMessage(self.request).addStatusMessage(_('info_diagramExported', default='Diagram exported.'), type='info')
            return pdf
        except Exception, e:
            IStatusMessage(self.request).addStatusMessage(str(e), type='error')

    @form.action(_('label_cancelAction', default='Cancel'), validator=null_validator)
    def action_cancel(self, action, data):
        """Cancel the pdf export
                """
        context = aq_inner(self.context)
        confirm = _('info_pdfExportCancel', default='PDF export cancelled.')
        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        self.request.response.redirect(context.absolute_url())
        return ''