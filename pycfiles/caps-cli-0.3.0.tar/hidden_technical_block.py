# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ag239446/git/nsap/doc/source/sphinxext/hidden_technical_block.py
# Compiled at: 2014-05-12 03:27:30
import logging
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.statemachine import ViewList
HTB_COUNTER = 0
js_showhide = '\n<script type="text/javascript">\n    function showhide(element){\n        if (!document.getElementById)\n            return\n\n        if (element.style.display == "block")\n            element.style.display = "none"\n        else\n            element.style.display = "block"\n    };\n</script>\n'

def nice_bool(arg):
    tvalues = ('true', 't', 'yes', 'y')
    fvalues = ('false', 'f', 'no', 'n')
    arg = directives.choice(arg, tvalues + fvalues)
    return arg in tvalues


class hidden_technical_block(nodes.Admonition, nodes.Element):
    """Node for inserting hidden technical block."""


class MyError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HiddenTechnicalBlock(BaseAdmonition):
    """Hidden technical block"""
    node_class = hidden_technical_block
    has_content = True
    required_arguments = 0
    optional_arguments = 2
    final_argument_whitespace = False
    option_spec = {'starthidden': nice_bool, 
       'label': str}

    def run(self):
        new_content = ViewList()
        for item in self.content:
            if item.startswith('.. include:: '):
                resource_path = item.replace('.. include:: ', '')
                try:
                    fo = open(resource_path, 'r')
                    item_content = [ x.replace('\n', '') for x in fo.readlines()
                                   ]
                    for string_content in item_content:
                        new_content.append(unicode(string_content), source=self.content)

                    fo.close()
                except MyError as e:
                    item_content = ("Can't open the resource file '{0}'").format(resource_path)
                    logging.error(item_content + e.value)
                    new_content.append(item_content, source=self.content)

            else:
                new_content.append(item, source=self.content)

        self.content = new_content
        return super(HiddenTechnicalBlock, self).run()


def visit_htb_html(self, node):
    """Visit hidden code block"""
    global HTB_COUNTER
    HTB_COUNTER += 1
    self.visit_admonition(node)
    technical_block = self.body[(-1)]
    fill_header = {'divname': ('hiddencodeblock{0}').format(HTB_COUNTER), 
       'startdisplay': 'none' if node['starthidden'] else 'block', 
       'label': node.get('label', '[+ show/hide technical details]')}
    divheader = ('<a href="javascript:showhide(document.getElementById(\'{divname}\'))">\n{label}</a><br />\n<div id="{divname}" style="display: {startdisplay}">').format(**fill_header)
    technical_block = js_showhide + divheader + technical_block
    self.body[-1] = technical_block


def depart_htb_html(self, node):
    """Depart hidden technical block"""
    self.depart_admonition(node)
    self.depart_admonition(node)


def setup(app):
    app.add_directive('hidden-technical-block', HiddenTechnicalBlock)
    app.add_node(hidden_technical_block, html=(
     visit_htb_html, depart_htb_html))