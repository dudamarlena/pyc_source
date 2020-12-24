# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pdfkit/configuration.py
# Compiled at: 2016-12-19 08:41:12
import subprocess, sys

class Configuration(object):

    def __init__(self, wkhtmltopdf='', meta_tag_prefix='pdfkit-'):
        self.meta_tag_prefix = meta_tag_prefix
        self.wkhtmltopdf = wkhtmltopdf
        if not self.wkhtmltopdf:
            if sys.platform == 'win32':
                self.wkhtmltopdf = subprocess.Popen([
                 'where', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
            else:
                self.wkhtmltopdf = subprocess.Popen([
                 'which', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
        try:
            with open(self.wkhtmltopdf) as (f):
                pass
        except IOError:
            raise IOError('No wkhtmltopdf executable found: "%s"\nIf this file exists please check that this process can read it. Otherwise please install wkhtmltopdf - https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf' % self.wkhtmltopdf)