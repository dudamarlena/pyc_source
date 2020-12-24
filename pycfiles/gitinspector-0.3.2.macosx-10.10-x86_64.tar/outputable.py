# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/outputable.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
import format

class Outputable(object):

    def output_html(self):
        print(_(b'HTML output not yet supported in') + b' "' + self.__class__.__name__ + b'".')

    def output_text(self):
        print(_(b'Text output not yet supported in') + b' "' + self.__class__.__name__ + b'".')

    def output_xml(self):
        print(_(b'XML output not yet supported in') + b' "' + self.__class__.__name__ + b'".')


def output(outputable):
    if format.get_selected() == b'html' or format.get_selected() == b'htmlembedded':
        outputable.output_html()
    elif format.get_selected() == b'text':
        outputable.output_text()
    else:
        outputable.output_xml()