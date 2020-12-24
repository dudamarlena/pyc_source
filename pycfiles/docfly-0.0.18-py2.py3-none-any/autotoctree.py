# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/docfly-project/docfly/directives/autotoctree.py
# Compiled at: 2020-03-21 11:28:22
"""

"""
from __future__ import unicode_literals
import sphinx.util
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx.directives.other import TocTree
from pathlib_mate import Path
from ..doctree import ArticleFolder

class AutoTocTree(Directive):
    """
    Automatically includes index.rst in toctree from::

        <current_dir>/<any-folder>/index.rst

    Any toctree directive arguments are supported.

    Example, the content of ``<current_dir>/index.rst``::

        .. autodoctree::

    Will be converted to::

        .. toctree::

            ./section1/index.rst
            ./section2/index.rst
            ...
    """
    has_content = True
    option_spec = TocTree.option_spec.copy()
    option_spec[b'append_ahead'] = directives.flag

    def run(self):
        node = nodes.Element()
        node.document = self.state.document
        current_file = self.state.document.current_source
        output_rst = self.derive_toctree_rst(current_file)
        view_list = StringList(output_rst.splitlines(), source=b'')
        sphinx.util.nested_parse_with_titles(self.state, view_list, node)
        return node.children

    def derive_toctree_rst(self, current_file):
        """
        Generate the rst content::

            .. toctree::
                args ...

                example.rst
                ...

        :param current_file:
        :return:
        """
        TAB = b'    '
        lines = list()
        lines.append(b'.. toctree::')
        for opt in TocTree.option_spec:
            value = self.options.get(opt)
            if value is not None:
                lines.append((b'{}:{}: {}').format(TAB, opt, value).rstrip())

        lines.append(b'')
        append_ahead = b'append_ahead' in self.options
        if append_ahead:
            for line in list(self.content):
                lines.append(TAB + line)

        article_folder = ArticleFolder(dir_path=Path(current_file).parent.abspath)
        for af in article_folder.sub_article_folders:
            line = (b'{}{} <{}>').format(TAB, af.title, af.rel_path)
            lines.append(line)

        append_behind = not append_ahead
        if append_behind:
            for line in list(self.content):
                lines.append(TAB + line)

        lines.append(b'')
        return (b'\n').join(lines)