# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/exporter/tex/latex_file.py
# Compiled at: 2020-01-26 13:28:51
# Size of source mod 2**32: 2071 bytes
import logging
from builtins import open
from datetime import datetime
LOGGER = logging.getLogger(__name__)

class LatexFile:
    __doc__ = ' Permit to handle the content of a LatexFile '

    def __init__(self, document_class, document_option=None, header=None, intro=None, footer=None, date=None, **kwargs):
        LOGGER.debug('Creating a document skeleton with document_class=%s, document_option=%s', document_class, document_option)
        self.document_class = document_class
        self.text = ''
        self.document_option = self.set_value(document_option)
        self._header = self.set_value(header)
        self.intro = self.set_value(intro)
        self._footer = self.set_value(footer)
        if date is None:
            date = datetime.now().strftime('%B %d, %Y')
        self.date = date

    def set_value(self, value):
        """ Return the value we need for null text. """
        if value is None:
            return ''
        return value

    @property
    def header(self):
        """ Return the header of a .tex file.

        :rtype: String """
        header = '\\documentclass'
        if self.document_option:
            header += '[{}]'.format(self.document_option)
        header += '{%s}\n' % self.document_class
        header += '\\date{%s}\n' % self.date
        header += '%s\n' % self._header
        header += '\\begin{document}\n'
        header += '%s\n' % self.intro
        return header

    @property
    def footer(self):
        """ Return the footer of a .tex file.

        :rtype: String """
        end = '\n\\end{document}\n'
        if self._footer:
            return self._footer + end
        return end

    def save(self, path):
        """ Save the document on disk. """
        with open(path, 'wb') as (tex_file):
            tex_file.write(self.document.encode('UTF-8'))

    @property
    def document(self):
        """ Return the full text of the LatexFile.

        :rtype: String"""
        return '{}{}{}'.format(self.header, self.text, self.footer)