# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ag239446/git/nsap/doc/source/sphinxext/link_to_block.py
# Compiled at: 2014-05-12 07:53:08
import os
from docutils import nodes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.statemachine import ViewList

class link_to_block(nodes.Admonition, nodes.Element):
    """ Node for inserting a link to button."""


class LinkToBlock(BaseAdmonition):
    """ Hidden technical block"""
    node_class = link_to_block
    has_content = False
    required_arguments = 1
    optional_arguments = 2
    final_argument_whitespace = True
    option_spec = {'right-side': bool, 
       'label': str}

    def run(self):
        new_content = ViewList()
        ref = (':ref:`{0} <{1}>`').format(self.options.get('label', 'Link To'), ('').join(self.arguments))
        new_content.append(ref, source=self.content)
        self.content = new_content
        return super(LinkToBlock, self).run()


def visit_ltb_html(self, node):
    """ Visit link to block"""
    position = node.get('right-side', True)
    self.body.append(("<div class='{0}'>").format('buttonNext' if position else 'buttonPrevious'))


def depart_ltb_html(self, node):
    """ Depart link to block"""
    self.depart_admonition(node)


def setup(app):
    app.add_directive('link-to-block', LinkToBlock)
    app.add_node(link_to_block, html=(visit_ltb_html, depart_ltb_html))