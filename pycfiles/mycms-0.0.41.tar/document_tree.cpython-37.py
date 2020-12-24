# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/creole/shared/document_tree.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 2637 bytes
"""
    python-creole
    ~~~~~~~~~~~~~

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
from __future__ import division, absolute_import, print_function, unicode_literals
import warnings, inspect
from mycms.creole.py3compat import TEXT_TYPE
from mycms.creole.shared.utils import dict2string

class DocNode:
    __doc__ = '\n    A node in the document tree for html2creole and creole2html.\n    \n    The Document tree would be created in the parser and used in the emitter.\n    '

    def __init__(self, kind='', parent=None, content=None, attrs=[], level=None):
        self.kind = kind
        self.children = []
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)
        self.attrs = dict(attrs)
        if content:
            assert isinstance(content, TEXT_TYPE), "Given content %r is not unicode, it's type: %s" % (
             content, type(content))
        self.content = content
        self.level = level

    def get_attrs_as_string(self):
        """
        FIXME: Find a better was to do this.

        >>> node = DocNode(attrs={'foo':"bar", "no":123})
        >>> node.get_attrs_as_string()
        "foo='bar' no=123"

        >>> node = DocNode(attrs={"foo":'bar', "no":"ABC"})
        >>> node.get_attrs_as_string()
        "foo='bar' no='ABC'"
        """
        return dict2string(self.attrs)

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return '<DocNode %s: %r>' % (self.kind, self.content)

    def debug(self):
        print('________________________________________________________________________________')
        print('\tDocNode - debug:')
        print('str(): %s' % self)
        print('attributes:')
        for i in dir(self):
            if not i.startswith('_'):
                if i == 'debug':
                    continue
                print('%20s: %r' % (i, getattr(self, i, '---')))


class DebugList(list):

    def __init__(self, html2creole):
        self.html2creole = html2creole
        super(DebugList, self).__init__()

    def append(self, item):
        line, method = inspect.stack()[1][2:4]
        msg = '%-8s   append: %-35r (%-15s line:%s)' % (
         self.html2creole.getpos(), item,
         method, line)
        warnings.warn(msg)
        list.append(self, item)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())