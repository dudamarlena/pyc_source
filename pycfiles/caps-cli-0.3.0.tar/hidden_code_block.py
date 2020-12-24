# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ag239446/git/nsap/doc/source/sphinxext/hidden_code_block.py
# Compiled at: 2014-04-10 06:24:05
__doc__ = "Simple, inelegant Sphinx extension which adds a directive for a\nhighlighted code-block that may be toggled hidden and shown in HTML.  \nThis is possibly useful for teaching courses.\n\nThe directive, like the standard code-block directive, takes\na language argument and an optional linenos parameter.  The\nhidden-code-block adds starthidden and label as optional \nparameters.\n\nExamples:\n\n.. hidden-code-block:: python\n    :starthidden: False\n\n    a = 10\n    b = a + 5\n\n.. hidden-code-block:: python\n    :label: --- SHOW/HIDE ---\n\n    x = 10\n    y = x + 5\n\nThanks to http://www.javascriptkit.com/javatutors/dom3.shtml for \ninspiration on the javascript.  \n\nThanks to Milad 'animal' Fatenejad for suggesting this extension \nin the first place.\n\nWritten by Anthony 'el Scopz' Scopatz, January 2012.\n\nReleased under the WTFPL (http://sam.zoy.org/wtfpl/).\n"
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.code import CodeBlock
from sphinx.util.compat import make_admonition
HCB_COUNTER = 0
js_showhide = '<script type="text/javascript">\n    function showhide(element){\n        if (!document.getElementById)\n            return\n\n        if (element.style.display == "block")\n            element.style.display = "none"\n        else\n            element.style.display = "block"\n    };\n</script>\n'

def nice_bool(arg):
    tvalues = ('true', 't', 'yes', 'y')
    fvalues = ('false', 'f', 'no', 'n')
    arg = directives.choice(arg, tvalues + fvalues)
    return arg in tvalues


class hidden_code_block(nodes.General, nodes.FixedTextElement):
    pass


class HiddenCodeBlock(CodeBlock):
    """Hidden code block is Hidden"""
    option_spec = dict(starthidden=nice_bool, label=str, **CodeBlock.option_spec)

    def run(self):
        code = ('\n').join(self.content)
        hcb = hidden_code_block(code, code)
        hcb['language'] = self.arguments[0]
        hcb['linenos'] = 'linenos' in self.options
        hcb['starthidden'] = self.options.get('starthidden', True)
        hcb['label'] = self.options.get('label', '[+ show/hide code]')
        hcb.line = self.lineno
        return [
         hcb]


def visit_hcb_html(self, node):
    """Visit hidden code block"""
    global HCB_COUNTER
    HCB_COUNTER += 1
    try:
        self.visit_literal_block(node)
    except nodes.SkipNode:
        pass

    code_block = self.body[(-1)]
    fill_header = {'divname': ('hiddencodeblock{0}').format(HCB_COUNTER), 'startdisplay': 'none' if node['starthidden'] else 'block', 
       'label': node.get('label')}
    divheader = ('<a href="javascript:showhide(document.getElementById(\'{divname}\'))">{label}</a><br /><div id="{divname}" style="display: {startdisplay}">').format(**fill_header)
    code_block = js_showhide + divheader + code_block + '</div>'
    self.body[-1] = code_block
    raise nodes.SkipNode


def depart_hcb_html(self, node):
    """Depart hidden code block"""
    pass


def setup(app):
    app.add_directive('hidden-code-block', HiddenCodeBlock)
    app.add_node(hidden_code_block, html=(visit_hcb_html, depart_hcb_html))