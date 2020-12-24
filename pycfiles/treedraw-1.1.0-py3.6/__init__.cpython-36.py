# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treedraw/__init__.py
# Compiled at: 2017-10-18 02:00:45
# Size of source mod 2**32: 208 bytes
"""
Treedraw
"""
from .render import Renderer
from .parser import Parser
if __name__ == '__main__':
    parser = Parser('test.tree')
    rend = Renderer('test.png')
    rend.render_tree(parser.make_tree())