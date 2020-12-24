# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/transforms/writer_aux.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2609 bytes
"""
Auxiliary transforms mainly to be used by Writer components.

This module is called "writer_aux" because otherwise there would be
conflicting imports like this one::

    from docutils import writers
    from docutils.transforms import writers
"""
__docformat__ = 'reStructuredText'
from docutils import nodes, utils, languages
from docutils.transforms import Transform

class Compound(Transform):
    __doc__ = '\n    Flatten all compound paragraphs.  For example, transform ::\n\n        <compound>\n            <paragraph>\n            <literal_block>\n            <paragraph>\n\n    into ::\n\n        <paragraph>\n        <literal_block classes="continued">\n        <paragraph classes="continued">\n    '
    default_priority = 910

    def apply(self):
        for compound in self.document.traverse(nodes.compound):
            first_child = True
            for child in compound:
                if first_child:
                    if not isinstance(child, nodes.Invisible):
                        first_child = False
                else:
                    child['classes'].append('continued')

            compound.replace_self(compound[:])


class Admonitions(Transform):
    __doc__ = '\n    Transform specific admonitions, like this:\n\n        <note>\n            <paragraph>\n                 Note contents ...\n\n    into generic admonitions, like this::\n\n        <admonition classes="note">\n            <title>\n                Note\n            <paragraph>\n                Note contents ...\n\n    The admonition title is localized.\n    '
    default_priority = 920

    def apply(self):
        language = languages.get_language(self.document.settings.language_code, self.document.reporter)
        for node in self.document.traverse(nodes.Admonition):
            node_name = node.__class__.__name__
            node['classes'].append(node_name)
            if not isinstance(node, nodes.admonition):
                admonition = (nodes.admonition)(node.rawsource, *(node.children), **node.attributes)
                title = nodes.title('', language.labels[node_name])
                admonition.insert(0, title)
                node.replace_self(admonition)