# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/demo.py
# Compiled at: 2019-05-24 23:07:05
"""

"""
from __future__ import unicode_literals
import sphinx.util
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from pathlib_mate import Path
from rstobj.directives import ListTable, Image
try:
    from itertools import izip_longest as zip_longest
except:
    from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    u"""
    Collect data into fixed-length chunks or blocks.

    Example::

        >>> list(grouper(range(10), n=3, fillvalue=None))
        [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, None, None)]

    **中文文档**

    将一个序列按照尺寸n, 依次打包输出, 如果元素不够n的包, 则用 ``fillvalue`` 中的值填充。
    """
    args = [
     iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def derive_rst(current_dir, image_dir, n_columns):
    """
    scan ``image_dir`` find all image path, find the relative path to ``current_dir``,
    and put them in a table, ``n_columns`` width. return the list table rst
    directive text.
    """
    current_dir, image_dir = Path(current_dir), Path(image_dir)
    image_list = [ Image(uri=str(p.relative_to(current_dir)), height=64, width=64) for p in image_dir.select_image()
                 ]
    data = list(grouper(image_list, n_columns))
    ltable = ListTable(data=data, header=False, index=False)
    return ltable.render()


class IconTable(Directive):
    """
    ``.. icontable:: <dirpath>`` markup implementation.
    """
    required_arguments = 1
    option_spec = {b'n_columns': int}

    def run(self):
        node = nodes.Element()
        node.document = self.state.document
        current_file = self.state.document.current_source
        current_dir = Path(current_file).parent
        image_dir = Path(Path(current_file).parent, self.arguments[0])
        n_columns = self.options.get(b'n_columns', 3)
        if image_dir.exists():
            output_rst = derive_rst(current_dir=current_dir, image_dir=image_dir, n_columns=n_columns)
        else:
            output_rst = b''
        view_list = StringList(output_rst.splitlines(), source=b'')
        sphinx.util.nested_parse_with_titles(self.state, view_list, node)
        return node.children


def setup(app):
    app.add_directive(b'icontable', IconTable)


if __name__ == b'__main__':
    rst = derive_rst(current_dir=b'/Users/sanhehu/Documents/GitHub/rstobj-project/docs/source', image_dir=b'/Users/sanhehu/Documents/GitHub/rstobj-project/docs/source/demo-images', n_columns=3)
    print rst