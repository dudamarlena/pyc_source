# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/doc/watermark.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import CoilsException
from coils.core.logic import ActionCommand
from coils.foundation.api.pypdf import PdfFileWriter, PdfFileReader

class WatermarkPDFAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'watermark-pdf'
    __aliases__ = ['watermarkPDF', 'watermarkPDFAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'application/pdf'

    def get_document_from_path(self, number, path):
        project = self._ctx.run_command('project::get', number=number)
        if not project:
            raise CoilsException(('Unable to marshall project "{0}" specified in path to watermark.').format(number))
        document = self._ctx.run_command('project::get-path', path=path, project=project)
        if not document:
            raise CoilsException(('Unable to marshall watermark document from path "{0}" in projectId#{1}').format(path, project.object_id))
        return document

    def do_action(self):
        if self.input_message.mimetype != 'application/pdf':
            raise CoilsException('Input message for PDF watermarking is not PDF')
        if self._document_id is None:
            watermark_d = self.get_document_from_path(self._project_number, self._project_path)
        else:
            watermark_d = self._ctx.run_command('document::get', id=self._document_id)
            if watermark_d is None:
                raise CoilsException(('Unable to retrieve documentId#{0}').format(self._document_id))
        watermark_h = self._ctx.run_command('document::get-handle', document=watermark_d)
        if watermark_h is None:
            raise CoilsException(('Unable to retrieve handle for contents of documentId#{0}').format(self._document_id))
        watermark_r = PdfFileReader(watermark_h)
        input_r = PdfFileReader(self._rfile)
        output_w = PdfFileWriter()
        for i in range(0, input_r.numPages):
            page_in = input_r.getPage(i)
            rect = page_in.mediaBox
            page_out = output_w.addBlankPage(width=rect.getWidth(), height=rect.getHeight())
            page_out.mergePage(watermark_r.getPage(0))
            page_out.mergePage(page_in)

        output_w.write(self._wfile)
        return

    def parse_action_parameters(self):
        document_id = self.action_parameters.get('documentId', None)
        if document_id is None:
            path_to_watermark = self.action_parameters.get('path', None)
            if path_to_watermark is None:
                raise CoilsException('No watermark document specified')
            tmp = path_to_watermark.split(':')
            if len(tmp) != 2:
                raise CoilsException('Path to watermark document cannot be parsed.')
            else:
                self._document_id = None
                self._project_number = tmp[0]
                self._project_path = tmp[1]
        else:
            try:
                document_id = self.process_label_substitutions(document_id)
                self._document_id = int(document_id)
            except:
                raise CoilsException(('Watermark documentId of "{0}" is not a valid objectId').format(document_id))

            return

    def do_epilogue(self):
        pass