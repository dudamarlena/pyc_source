# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rst/sphinx.py
# Compiled at: 2020-03-27 18:36:32
# Size of source mod 2**32: 706 bytes
from docutils.nodes import raw, title

def rst_document_parsed(self, context, document):

    def callback(text):
        return '{} <a href="#"></a>'.format(text)

    def gen_toc(children, toc, level=1):
        for child in children[:]:
            if isinstance(child, title):
                toc.append((child.astext(), level))
                new_text = callback(child.astext())
                child.children = [
                 raw('', new_text, format='html')]

    context.content['toc'] = []
    gen_toc(document.children, context.content['toc'])


class rstSphinx:
    pass