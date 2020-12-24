# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/lp/inlinesyntaxhighlight.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 3274 bytes
from docutils import nodes
import re
from sphinx.writers.html import HTMLTranslator
DIV_PRE_RE = re.compile('^<div[^>]*><pre>')
PRE_DIV_RE = re.compile('\\s*</pre></div>\\s*$')

def html_visit_literal(self, node):
    env = self.builder.env
    shall_highlight = False
    if node.rawsource.startswith('``'):
        if not ('role' not in node.attributes and env.config.inline_highlight_literals):
            if 'code' in node['classes']:
                if env.config.inline_highlight_respect_highlight:
                    lang = self.highlightlang
                else:
                    lang = None
                highlight_args = node.get('highlight_args', {})
                if node.has_key('language'):
                    lang = node['language']
                    highlight_args['force'] = True

                def warner(msg, **kwargs):
                    (self.builder.warn)((self.builder.current_docname), msg, (node.line), **kwargs)

                highlighted = (self.highlighter.highlight_block)(
 node.astext(), lang, warn=warner, **highlight_args)
                highlighted = DIV_PRE_RE.sub('', highlighted)
                highlighted = PRE_DIV_RE.sub('', highlighted)
                starttag = self.starttag(node,
                  'code',
                  suffix='',
                  CLASS=('docutils literal highlight highlight-%s' % lang))
                self.body.append(starttag + highlighted + '</code>')
    else:
        return old_html_visit_literal(self, node)
    raise nodes.SkipNode


old_html_visit_literal = HTMLTranslator.visit_literal
HTMLTranslator.visit_literal = html_visit_literal

def setup(app):
    app.add_config_value('inline_highlight_literals', True, 'env')
    app.add_config_value('inline_highlight_respect_highlight', True, 'env')