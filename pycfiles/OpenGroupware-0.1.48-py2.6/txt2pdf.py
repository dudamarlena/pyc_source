# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/doc/txt2pdf.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand
from django1778 import pyText2Pdf

class TextToPDFAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'text-to-pdf'
    __aliases__ = ['textToPDF', 'textToPDFAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'application/pdf'

    def do_action(self):
        if self._do_ffs:
            self.log.debug('FFs in input will cause page breaks')
        self.log.debug(('Columns: {0} TabWidth: {1} Size: {2}').format(self._columns, self._tab_width, self._font_size))
        pdf = pyText2Pdf(self.rfile, self.wfile, title=self._title, font=self._font, ptSize=self._font_size, tab=self._tab_width, cols=self._columns, do_ffs=self._do_ffs)
        pdf.Convert()

    def parse_action_parameters(self):
        self._columns = int(self.process_label_substitutions(self.action_parameters.get('columns', '80'), default='80'))
        self._title = self.process_label_substitutions(self.action_parameters.get('title', ''), default='')
        self._font_size = int(self.process_label_substitutions(self.action_parameters.get('pointSize', '10'), default='10'))
        self._tab_width = int(self.process_label_substitutions(self.action_parameters.get('tabWidth', '4'), default='4'))
        self._font = self.process_label_substitutions(self.action_parameters.get('font', '/Courier'), default='/Courier')
        self._do_ffs = self.process_label_substitutions(self.action_parameters.get('doFormFeeds', 'NO'), default='NO')
        if self._do_ffs.upper() == 'YES':
            self._do_ffs = 1
        else:
            self._do_ffs = 0

    def do_epilogue(self):
        pass