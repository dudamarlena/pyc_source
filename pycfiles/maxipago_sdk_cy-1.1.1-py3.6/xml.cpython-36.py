# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/maxipago/utils/xml.py
# Compiled at: 2018-07-09 08:49:05
# Size of source mod 2**32: 868 bytes
from lxml import etree

def create_element_recursively(parent, path):
    nodes = path.split('/')
    node = parent
    for n_str in nodes:
        n = node.find(n_str)
        if n is None:
            node = etree.SubElement(node, n_str)
        else:
            node = n

    return node