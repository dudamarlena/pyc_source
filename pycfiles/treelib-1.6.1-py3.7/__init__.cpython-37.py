# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treelib/__init__.py
# Compiled at: 2020-02-27 08:49:21
# Size of source mod 2**32: 1594 bytes
"""
treelib - Python 2/3 Tree Implementation

`treelib` is a Python module with two primary classes: Node and Tree.
Tree is a self-contained structure with some nodes and connected by branches.
A tree owns merely a root, while a node (except root) has some children and one parent.

Note: To solve string compatibility between Python 2.x and 3.x, treelib follows
the way of porting Python 3.x to 2/3. That means, all strings are manipulated as
unicode and you do not need u'' prefix anymore. The impacted functions include `str()`,
`show()` and `save2file()` routines.
But if your data contains non-ascii characters and Python 2.x is used,
you have to trigger the compatibility by declaring `unicode_literals` in the code:

.. code-block:: python

   >>> from __future__ import unicode_literals
"""
__version__ = '1.6.1'
from .tree import Tree
from .node import Node