# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyjon/reports/template.py
# Compiled at: 2010-06-14 10:29:11
import time, os, tempfile, codecs
from genshi.template import Template, MarkupTemplate
from z3c.rml import rml2pdf, document, interfaces
import logging
logger = logging.getLogger()

class ReportTemplate(MarkupTemplate):

    def write(self, target_file, **kwargs):
        for status in self.process_write(target_file, **kwargs):
            if not status:
                raise Exception, 'Error in file writing'

        if 'should_close' in kwargs and kwargs['should_close']:
            target_file.close()

    def __generate_tempfile(self):
        (fd, fname) = tempfile.mkstemp()
        os.close(fd)
        return fname

    def __clean_tempfile(self, filename):
        os.unlink(filename)

    def process_write(self, target_file, **kwargs):
        """ Do the process of writing the RML file while yielding statuses... """
        flow = self.generate(**kwargs)
        for markup in flow.serialize():
            target_file.write(markup)
            yield True

    def render(self, outfilename, **kwargs):
        """ Renders the report template to pdf with the given kwargs.
        
        Warning: This function does a sleep between genshi rendering and PDF gen
        to avoid crash of rml2pdf.
        
        @param outfilename: the filename of the pdf to write.
        @type outfilename: string
        
        @kwargs: all the vars you want to pass to genshi context
        """
        temp_fname = self.__generate_tempfile()
        temp_file = codecs.open(temp_fname, 'wb+', 'utf-8')
        self.write(temp_file, should_close=True, **kwargs)
        time.sleep(0.1)
        result = rml2pdf.go(temp_fname, outfilename)
        self.__clean_tempfile(temp_fname)
        return result

    def render_flow(self, outfilename, **kwargs):
        """ Renders the report template to pdf with the given kwargs while
        yielding statuses.
        
        Warning: This function does a sleep between genshi rendering and PDF gen
        to avoid crash of rml2pdf.
        
        @param outfilename: the filename of the pdf to write.
        @type outfilename: string
        
        @kwargs: all the vars you want to pass to genshi context
        """
        temp_fname = self.__generate_tempfile()
        temp_file = codecs.open(temp_fname, 'wb+', 'utf-8')
        yield True
        for status in self.process_write(temp_file, **kwargs):
            yield status

        temp_file.close()
        yield True
        time.sleep(0.1)
        rml2pdf.go(temp_fname, outfilename)
        yield True
        self.__clean_tempfile(temp_fname)
        yield True