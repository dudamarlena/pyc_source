# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thierry/vmWareLinux/proj/simulatortofmu/SimulatorToFMU/simulatortofmu/doc/userGuide/source/mathjax.py
# Compiled at: 2017-07-07 15:44:04
"""
    sphinx.ext.mathjax
    ~~~~~~~~~~~~~~~~~~

    Allow `MathJax <http://mathjax.org/>`_ to be used to display math 
    in Sphinx's HTML writer - requires the MathJax JavaScript library
    on your webserver/computer.

    Kevin Dunn, kgdunn@gmail.com, 3-clause BSD license.
    

    For background, installation details and support: 
    
        https://bitbucket.org/kevindunn/sphinx-extension-mathjax

"""
from docutils import nodes
from sphinx.application import ExtensionError
from sphinx.ext.mathbase import setup_math as mathbase_setup

def html_visit_math(self, node):
    self.body.append(self.starttag(node, 'span', '', CLASS='math'))
    self.body.append(self.builder.config.mathjax_inline[0] + self.encode(node['latex']) + self.builder.config.mathjax_inline[1] + '</span>')
    raise nodes.SkipNode


def html_visit_displaymath(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='math'))
    if node['nowrap']:
        self.body.append(self.builder.config.mathjax_display[0] + node['latex'] + self.builder.config.mathjax_display[1])
        self.body.append('</div>')
        raise nodes.SkipNode
    parts = [ prt for prt in node['latex'].split('\n\n') if prt.strip() != '' ]
    for i, part in enumerate(parts):
        part = self.encode(part)
        if i == 0:
            if node['number']:
                self.body.append('<span class="eqno">(%s)</span>' % node['number'])
        if '&' in part or '\\\\' in part:
            self.body.append(self.builder.config.mathjax_display[0] + '\\begin{split}' + part + '\\end{split}' + self.builder.config.mathjax_display[1])
        else:
            self.body.append(self.builder.config.mathjax_display[0] + part + self.builder.config.mathjax_display[1])

    self.body.append('</div>\n')
    raise nodes.SkipNode


def builder_inited(app):
    if not app.config.mathjax_path:
        raise ExtensionError('mathjax_path config value must be set for the mathjax extension to work')
    app.add_javascript(app.config.mathjax_path)


def setup(app):
    mathbase_setup(app, (html_visit_math, None), (html_visit_displaymath, None))
    app.add_config_value('mathjax_path', '', False)
    app.add_config_value('mathjax_inline', ['\\(', '\\)'], 'html')
    app.add_config_value('mathjax_display', ['\\[', '\\]'], 'html')
    app.connect('builder-inited', builder_inited)
    return