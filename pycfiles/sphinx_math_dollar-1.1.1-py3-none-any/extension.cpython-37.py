# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aaronmeurer/Documents/sphinx-math-dollar/build/lib/sphinx_math_dollar/extension.py
# Compiled at: 2019-09-17 19:56:44
# Size of source mod 2**32: 2221 bytes
from __future__ import print_function
import os, sys
from .math_dollar import split_dollars
from docutils.nodes import GenericNodeVisitor, Text, math, FixedTextElement, literal
from docutils.transforms import Transform
NODE_BLACKLIST = node_blacklist = (
 FixedTextElement, literal, math)
DEBUG = bool(os.environ.get('MATH_DOLLAR_DEBUG', False))

class MathDollarReplacer(GenericNodeVisitor):

    def default_visit(self, node):
        return node

    def visit_Text(self, node):
        global DEBUG
        global node_blacklist
        parent = node.parent
        while parent:
            if isinstance(parent, node_blacklist):
                if DEBUG:
                    if any((i == 'math' for i, _ in split_dollars(node.rawsource))):
                        print('sphinx-math-dollar: Skipping', node, ('(node_blacklist = %s)' % (node_blacklist,)), file=(sys.stderr))
                return
            parent = parent.parent

        data = split_dollars(node.rawsource)
        nodes = []
        has_math = False
        for typ, text in data:
            if typ == 'math':
                has_math = True
                nodes.append(math(text, Text(text)))
            elif typ == 'text':
                nodes.append(Text(text))
            else:
                raise ValueError('Unrecognized type from split_dollars %r' % typ)

        if has_math:
            node.parent.replace(node, nodes)


class TransformMath(Transform):
    default_priority = 500

    def apply(self, **kwargs):
        self.document.walk(MathDollarReplacer(self.document))


def config_inited(app, config):
    global DEBUG
    global node_blacklist
    node_blacklist = config.math_dollar_node_blacklist
    DEBUG = config.math_dollar_debug


def setup(app):
    app.add_transform(TransformMath)
    app.add_config_value('math_dollar_node_blacklist', NODE_BLACKLIST, 'env')
    app.add_config_value('math_dollar_debug', DEBUG, '')
    app.connect('config-inited', config_inited)