# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/model/rest.py
# Compiled at: 2010-06-08 22:36:02
from docutils import core
from docutils.writers.html4css1 import Writer, HTMLTranslator

class NoHeaderHTMLTranslator(HTMLTranslator):

    def __init__(self, document):
        HTMLTranslator.__init__(self, document)
        self.head_prefix = ['', '', '', '', '']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []

    def astext(self):
        return ('').join(self.body)


_w = Writer()
_w.translator_class = NoHeaderHTMLTranslator

def reSTify(string):
    result = core.publish_string(string, writer=_w)
    if isinstance(result, basestring):
        result = unicode(result, 'utf-8')
    return result