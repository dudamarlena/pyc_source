# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/docgen/doc.py
# Compiled at: 2015-09-01 07:17:44
"""A container that contains information to generate documentation files"""
from __future__ import unicode_literals
from __future__ import print_function
from ..html import slugify
from ..compat import PY2
from json import dump

class Doc(object):

    def __init__(self, namespace, name, doc_class=b'document'):
        self.doc_namespace = namespace
        self.id = self.make_id(name)
        self.name = name
        self.doc_class = doc_class
        self.data = {}
        self.references = []

    def __repr__(self):
        return (b"<doc '{}'>").format(self.id)

    @classmethod
    def from_dict(cls, d):
        doc = cls(d[b'doc_namespace'], d[b'name'], d[b'doc_class'])
        doc.id = d[b'id']
        doc.data = d[b'data']
        doc.references = d[b'references']
        return doc

    def make_id(self, name):
        return (b'{}.{}').format(self.doc_namespace, name)

    def add_reference(self, name):
        doc_id = self.make_id(name) if b'.' not in name else name
        self.references.append(doc_id)

    @property
    def package(self):
        data = {k:v for k, v in self.data.iteritems() if not k.startswith(b'_') if not k.startswith(b'_')}
        doc_package = {b'id': self.id, 
           b'name': self.name, 
           b'doc_class': self.doc_class, 
           b'references': self.references, 
           b'data': data, 
           b'doc_namespace': self.doc_namespace}
        return doc_package

    def _process_docmap(self, docmap):
        doctree = [
         {b'title': b'Document', b'level': 0, 
            b'children': []}]
        stack = [
         doctree[0]]
        for level, text in docmap:
            current_level = stack[(-1)][b'level']
            node = {b'title': text.strip(), b'slug': slugify(text), 
               b'level': level, 
               b'children': []}
            if level > current_level:
                stack[(-1)][b'children'].append(node)
                stack.append(node)
            elif level == current_level:
                stack[(-2)][b'children'].append(node)
                stack[-1] = node
            else:
                while level < stack[(-1)][b'level']:
                    stack.pop()

                stack[(-2)][b'children'].append(node)
                stack[-1] = node

        doctree = doctree[0][b'children']
        return doctree

    @property
    def doctree(self):
        if b'docmap' in self.data:
            doctree = self._process_docmap(self.data[b'docmap'])
        else:
            doctree = None
        return doctree

    def write(self, fs):
        """Write a pickle file containing the doc info"""
        doc_package = self.package
        filename = (b'{}.json').format(self.name).replace(b'/', b'_')
        with fs.open(filename, b'wb' if PY2 else b'wt') as (f):
            dump(doc_package, f, indent=4, separators=(',', ': '))