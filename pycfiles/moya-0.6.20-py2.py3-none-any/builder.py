# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/docgen/builder.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from .. import pilot
from ..context import Context
from ..template.moyatemplates import MoyaTemplateEngine
from ..docgen.theme import Theme
from ..docgen.doc import Doc
from .. import bbcode
from .. import syntax
from ..filter import MoyaFilterBase
from fs import utils
from fs.opener import fsopendir
from fs.path import *
from os.path import join as pathjoin
from json import loads
from collections import defaultdict

class _LocationFilter(MoyaFilterBase):

    def __moyafilter__(self, context, app, value, params):
        tag_index = params[b'index']
        next_tag = None
        prev_tag = None
        for i, tag in enumerate(tag_index):
            if tag[b'tag_name'] == value:
                try:
                    next_tag = tag_index[(i + 1)]
                except IndexError:
                    pass

                if i > 0:
                    try:
                        prev_tag = tag_index[(i - 1)]
                    except IndexError:
                        pass

        return (
         prev_tag, next_tag)


class Builder(object):
    """Generate html documentation"""

    def __init__(self, source_fs, output_fs, theme_fs):
        self.source_fs = source_fs
        self.output_fs = output_fs
        self.theme_fs = theme_fs
        self.template_engine = MoyaTemplateEngine(None, self.theme_fs, None)
        self.docs = {}
        self.theme = Theme(self.theme_fs)
        self.settings = None
        self.pages = {}
        self.doc_paths = {}
        self.indices = {}
        return

    def build(self, build_data=None):
        source_fs = self.source_fs
        paths = list(source_fs.walkfiles(wildcard=b'*.json'))
        urls = defaultdict(dict)
        with pilot.console.progress(b'Reading', len(paths)) as (progress):
            for path in progress(paths):
                doc_data = loads(self.source_fs.getcontents(path, b'rt'))
                doc = Doc.from_dict(doc_data)
                for page in self.theme.get_pages(doc):
                    data = doc.data
                    context = Context({b'data': data})
                    with context.frame(b'data'):
                        path = page.get(context, b'path')
                        name = page.get(context, b'name')
                        full_path = self.output_fs.getsyspath(path)
                        if name:
                            urls[page.doc_class][name] = full_path
                        if b'namespace' in data:
                            urls[page.doc_class][(b'{{{}}}{}').format(data[b'namespace'], name)] = full_path

                self.docs[doc.id] = doc
                self.theme.get_pages(doc)

        self.process_indices(urls)
        assets_source_path = self.theme.get_relative_path(self.theme.get(b'assets', b'source', b'./assets'))
        assets_fs = fsopendir(assets_source_path)
        with pilot.console.progress(b'Copying theme assets', None) as (progress):

            def copy_progress(step, num_steps):
                progress.set_num_steps(num_steps)
                progress.update(step)

            utils.copydir_progress(copy_progress, assets_fs, (
             self.output_fs, b'assets'))
        with pilot.console.progress(b'Rendering', len(self.docs)) as (progress):
            for doc in progress(self.docs.values()):
                self.render_doc(doc, urls, build_data)

        if b'doc' in urls:
            return urls[b'doc'].get(b'index', None)
        else:
            return

    def process_indices(self, urls):
        for doc in self.docs.values():
            data = doc.data
            if b'indices' in data:
                doc_indices = data[b'indices']
                for index_name, (index_type, template, docs) in doc_indices.items():
                    if template:
                        index = docs
                    else:
                        index = []
                        for doc_name in docs:
                            doc_key = (b'doc.{}').format(doc_name)
                            indexed_doc = self.docs.get(doc_key, None)
                            if indexed_doc is None:
                                continue
                            index.append(indexed_doc)

                    self.indices[index_name] = (
                     index_type, template, index)

        return

    def render_index(self, context, index, template=b'docindex.html'):
        html = self.template_engine.render(template, {b'index': index}, base_context=context)
        return html

    _re_sub_index = re.compile(b'\\{\\{\\{INDEX (.*?)\\}\\}\\}')

    def sub_indices(self, context, html):

        def repl(match):
            index = self.indices.get(match.group(1), None)
            if index is not None:
                return self.render_index(context, index)
            else:
                return b''

        return self._re_sub_index.sub(repl, html)

    def get_doc(self, doc_id):
        return self.docs[doc_id]

    def get_navigation(self, doc_id):
        for index_type, template, index in self.indices.values():
            if template:
                continue
            for i, doc in enumerate(index):
                if doc.id == doc_id:
                    found = i
                    break

            continue
            nav = {}

            def seq(n):
                if index_type == b'A':
                    return chr(ord(b'A') + n - 1)
                else:
                    if index_type == b'a':
                        return chr(ord(b'a') + n - 1)
                    return n

            if found >= 1:
                nav[b'prev'] = {b'index': seq(found), b'doc': index[(found - 1)]}
            if found < len(index) - 1:
                nav[b'next'] = {b'index': seq(found + 2), b'doc': index[(found + 1)]}
            return nav

        return [
         None, None]

    def render_doc(self, doc, urls, render_data=None):
        for page in self.theme.get_pages(doc):
            data = doc.data
            context = Context({b'data': data})
            context[b'bbcode'] = bbcode.parser
            context[b'syntax'] = syntax.SyntaxFilter()
            context[b'section'] = page.get(context, b'section')
            context[b'getnav'] = _LocationFilter()
            with context.frame(b'data'):
                output_path = page.get(context, b'path')
                output_dir = normpath(dirname(output_path))
                template = page.get(context, b'template')
            context[b'.doc'] = doc
            context[b'.path'] = output_path
            context[b'.root_path'] = self.output_fs.getsyspath(b'/')
            context[b'.request'] = {b'path': self.output_fs.getsyspath(output_path)}
            context[b'.urls'] = urls
            context[b'.nav'] = self.get_navigation(doc.id)
            context[b'.docs'] = self.docs
            if render_data is not None:
                context.root.update(render_data)
            assets = relpath(normpath(self.theme.get(b'assets', b'location', b'assets')))
            dir_level = output_dir.count(b'/') + 1 if output_dir else 0
            assets_path = pathjoin(dir_level * b'../', assets) + b'/'
            context[b'assets_path'] = assets_path
            with context.frame(b'data'):
                for doc_id in doc.references:
                    ref_doc = self.get_doc(doc_id)
                    context[ref_doc.name] = ref_doc.data

            context[b'.id'] = doc.id
            html = self.template_engine.render(template, context[b'data'], base_context=context)
            html = self.sub_indices(context, html)
            self.output_fs.makedir(output_dir, allow_recreate=True, recursive=True)
            self.output_fs.setcontents(output_path, html)

        return