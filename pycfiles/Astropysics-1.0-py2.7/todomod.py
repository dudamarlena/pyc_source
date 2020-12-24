# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astropysics/sphinxext/todomod.py
# Compiled at: 2013-11-27 17:30:36
"""
The todomod sphinx extension adds the `todomodule` directive which will show all
the ``todo`` directives in a given module all in one place in the sphinx
documentation.  Like the :mod:`sphinx.ext.todo` extension, it will not be shown 
for non-release versions.
"""
from sphinx.ext.todo import Todo, todo_node, nodes
from sphinx.pycode import ModuleAnalyzer, PycodeError

class TodoModule(Todo):
    required_arguments = 1
    has_content = True

    def run(self):
        try:
            modfn = ModuleAnalyzer.for_module(self.arguments[0]).srcname
        except PycodeError as e:
            warnstr = "can't find module %s for todomodule: %s" % (self.arguments[0], e)
            return [self.state.document.reporter.warning(warnstr, lineno=self.lineno)]

        todolines = []
        with open(modfn) as (f):
            for l in f:
                if l.startswith('#TODO'):
                    todolines.append(l)

        todoreses = []
        for tl in todolines:
            text = tl.replace('#TODO:', '').replace('#TODO', '').strip()
            env = self.state.document.settings.env
            targetid = 'todo-%s' % env.index_num
            env.index_num += 1
            targetnode = nodes.target('', '', ids=[targetid])
            td_node = todo_node(text)
            title_text = _('Module Todo')
            textnodes, messages = self.state.inline_text(title_text, self.lineno)
            td_node += nodes.title(title_text, '', *textnodes)
            td_node += messages
            if 'class' in self.options:
                classes = self.options['class']
            else:
                classes = [
                 'admonition-' + nodes.make_id(title_text)]
            td_node['classes'] += classes
            td_node.append(nodes.paragraph(text, text))
            td_node.line = self.lineno
            todoreses.append(targetnode)
            todoreses.append(td_node)

        return todoreses


def setup(app):
    app.add_directive('todomodule', TodoModule)