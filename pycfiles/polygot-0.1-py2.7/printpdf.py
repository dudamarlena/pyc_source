# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/printpdf.py
# Compiled at: 2016-10-08 10:29:41
"""
*Print webpages to PDF*

:Author:
    David Young

:Date Created:
    September 28, 2015
"""
import sys, os
os.environ['TERM'] = 'vt100'
import readline, glob, pickle, re, codecs
from subprocess import Popen, PIPE, STDOUT
from docopt import docopt
from fundamentals import tools, times
from polygot import authenticate
import codecs

def handler(e):
    return (
     ' ', e.start + 1)


codecs.register_error('dryx', handler)

class printpdf:
    """
    *PDF printer*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``url`` -- the webpage url
        - ``title`` -- title of pdf
        - ``folderpath`` -- path at which to save pdf
        - ``append`` -- append this at the end of the file name (not title)
        - ``readability`` -- clean text with readability

    **Usage:**

        To print a webpage to PDF without any cleaning of the content using the title of the webpage as filename:

        .. code-block:: python 

            from polygot import printpdf
            pdf = printpdf(
                log=log,
                settings=settings,
                url="https://en.wikipedia.org/wiki/Volkswagen",
                folderpath="/path/to/output",
                readability=False
            ).get()

        To give the PDF an alternative title use:

        .. code-block:: python 

            from polygot import printpdf
            pdf = printpdf(
                log=log,
                settings=settings,
                url="https://en.wikipedia.org/wiki/Volkswagen",
                folderpath="/path/to/output",
                title="Cars",
                readability=False
            ).get()

        Or to append a string to the end of the filename before *.pdf* extension (useful for indexing or adding date created etc):

        .. code-block:: python 

            from datetime import datetime, date, time
            now = datetime.now()
            now = now.strftime("%Y%m%dt%H%M%S")

            from polygot import printpdf
            pdf = printpdf(
                log=log,
                settings=settings,
                url="https://en.wikipedia.org/wiki/Volkswagen",
                folderpath="/path/to/output",
                append="_"+now,
                readability=False
            ).get()

        To clean the content using the readability parser and apply some simple styling and pretty fonts:

        .. code-block:: python 

            from polygot import printpdf
            pdf = printpdf(
                log=log,
                settings=settings,
                url="https://en.wikipedia.org/wiki/Volkswagen",
                folderpath=pathToOutputDir,
                readability=True
            ).get()

    """

    def __init__(self, log, settings=False, url=False, title=False, folderpath=False, append=False, readability=True):
        self.log = log
        log.debug("instansiating a new 'print' object")
        self.settings = settings
        self.url = url
        self.folderpath = folderpath
        self.title = title
        self.append = append
        self.readability = readability
        self.parserClient = authenticate.authenticate(log=self.log, settings=self.settings).get()
        return

    def get(self):
        """
        *get the PDF*

        **Return:**
            - ``pdfPath`` -- the path to the generated PDF
        """
        self.log.info('starting the ``get`` method')
        if not self.append:
            self.append = ''
        if not self.readability:
            return self._print_original_webpage()
        else:
            return self._print_parsed_webpage()

        self.log.info('completed the ``get`` method')
        return pdfPath

    def _print_original_webpage(self):
        """*print the original webpage*

        **Return:**
            - ``pdfPath`` -- the path to the generated PDF
        """
        self.log.info('starting the ``_print_original_webpage`` method')
        if not self.title:
            from polygot import htmlCleaner
            cleaner = htmlCleaner(log=self.log, settings=self.settings, url=self.url, outputDirectory=self.folderpath, title=self.title, style=True, metadata=True, h1=True)
            htmlFile = cleaner.clean()
            basename = os.path.basename(htmlFile)
            title = basename.replace('.html', '')
            os.remove(htmlFile)
        else:
            title = self.title
        url = self.url
        pdfPath = self.folderpath + '/' + title + self.append + '.pdf'
        electron = self.settings['polygot']['electron path']
        cmd = '%(electron)s -i "%(url)s" -o "%(pdfPath)s" --printBackground ' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        self.log.debug('output: %(stdout)s' % locals())
        if len(stderr):
            print stderr
        exists = os.path.exists(pdfPath)
        if not exists:
            print '%(pdfPath)s was not generated for some reason - please investigate' % locals()
            sys.exit(0)
        self.log.info('completed the ``_print_original_webpage`` method')
        return pdfPath

    def _print_parsed_webpage(self):
        """*print the parsed/cleaned webpage*

        **Return:**
            - ``pdfPath`` -- the path to the generated PDF
        """
        self.log.info('starting the ``_print_parsed_webpage()`` method')
        from polygot import htmlCleaner
        cleaner = htmlCleaner(log=self.log, settings=self.settings, url=self.url, outputDirectory=self.folderpath, title=self.title, style=True, metadata=True, h1=True)
        htmlFile = cleaner.clean()
        pdfPath = htmlFile.replace('.html', self.append + '.pdf')
        electron = self.settings['polygot']['electron path']
        cmd = '%(electron)s -i "%(htmlFile)s" -o "%(pdfPath)s" ' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        if len(stderr):
            print stderr
        self.log.debug('output: %(stdout)s' % locals())
        os.remove(htmlFile)
        exists = os.path.exists(pdfPath)
        if not exists:
            print '%(pdfPath)s was not generated for some reason - please investigate' % locals()
            sys.exit(0)
        self.log.info('completed the ``_print_parsed_webpage()`` method')
        return pdfPath


if __name__ == '__main__':
    main()