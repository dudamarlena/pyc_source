# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/simiki/generators.py
# Compiled at: 2019-04-21 07:38:45
"""Convert Markdown file to html, which is embeded in html template.
"""
from __future__ import print_function, with_statement, unicode_literals, absolute_import
import os, os.path, io, copy, re, traceback, warnings
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import markdown, yaml
from jinja2 import Environment, FileSystemLoader, TemplateError
from simiki import jinja_exts
from simiki.utils import import_string
from simiki.compat import is_py2, is_py3, basestring
if is_py3:
    from functools import cmp_to_key
PLAT_LINE_SEP = b'\n'

class BaseGenerator(object):
    """Base generator class"""

    def __init__(self, site_config, base_path):
        """
        :site_config: site global configuration parsed from _config.yml
        :base_path: root path of wiki directory
        """
        self.site_config = copy.deepcopy(site_config)
        self.base_path = base_path
        self._templates = {}
        self._template_vars = self._get_template_vars()
        _template_path = os.path.join(self.base_path, site_config[b'themes_dir'], site_config[b'theme'])
        if not os.path.exists(_template_path):
            raise Exception((b"Theme `{0}' not exists").format(_template_path))
        self.env = Environment(loader=FileSystemLoader(_template_path))
        self._jinja_load_exts()

    def _jinja_load_exts(self):
        """Load jinja custom filters and extensions"""
        for _filter in jinja_exts.filters:
            self.env.filters[_filter] = getattr(jinja_exts, _filter)

    def get_template(self, name):
        """Return the template by layout name"""
        if name not in self._templates:
            try:
                self._templates[name] = self.env.get_template(name + b'.html')
            except TemplateError:
                exc_msg = (b"unable to load template '{0}.html'\n{1}").format(name, traceback.format_exc())
                raise Exception(exc_msg)

        return self._templates[name]

    def _get_template_vars(self):
        """Return the common template variables"""
        template_vars = {b'site': self.site_config}
        site_root = template_vars[b'site'][b'root']
        if site_root.endswith(b'/'):
            template_vars[b'site'][b'root'] = site_root[:-1]
        return template_vars


class PageGenerator(BaseGenerator):

    def __init__(self, site_config, base_path, tags=None):
        super(PageGenerator, self).__init__(site_config, base_path)
        self._tags = tags
        self._reset()

    def _reset(self):
        """Reset the global self variables"""
        self._src_file = None
        self.meta = None
        self.content = None
        return

    def to_html(self, src_file, include_draft=False):
        """Load template, and generate html

        :src_file: the filename of the source file. This can either be an
                   absolute filename or a filename relative to the base path.
        :include_draft: True/False, include draft pages or not to generate
        """
        self._reset()
        self._src_file = os.path.relpath(src_file, self.base_path)
        self.meta, self.content = self.get_meta_and_content()
        if not include_draft and self.meta.get(b'draft', False):
            return None
        else:
            layout = self.get_layout(self.meta)
            template_vars = self.get_template_vars(self.meta, self.content)
            template = self.get_template(layout)
            html = template.render(template_vars)
            return html

    @property
    def src_file(self):
        return self._src_file

    @src_file.setter
    def src_file(self, filename):
        self._src_file = os.path.relpath(filename, self.base_path)

    def get_meta_and_content(self, do_render=True):
        meta_str, content_str = self.extract_page(self._src_file)
        meta = self.parse_meta(meta_str)
        if do_render and meta.get(b'render', True):
            content = self._parse_markup(content_str)
        else:
            content = content_str
        return (meta, content)

    def get_layout(self, meta):
        """Get layout config in meta, default is `page'"""
        if b'layout' in meta:
            if meta[b'layout'] == b'post':
                warn_msg = (b"{0}: layout `post' is deprecated, use `page'").format(self._src_file)
                if is_py2:
                    warn_msg = warn_msg.encode(b'utf-8')
                warnings.warn(warn_msg, DeprecationWarning)
                layout = b'page'
            else:
                layout = meta[b'layout']
        else:
            layout = b'page'
        return layout

    def get_template_vars(self, meta, content):
        """Get template variables, include site config and page config"""
        template_vars = copy.deepcopy(self._template_vars)
        page = {b'content': content}
        page.update(meta)
        page.update({b'relation': self.get_relation()})
        template_vars.update({b'page': page})
        return template_vars

    def get_category_and_file(self):
        """Get the name of category and file(with extension)"""
        src_file_relpath_to_source = os.path.relpath(self._src_file, self.site_config[b'source'])
        category, filename = os.path.split(src_file_relpath_to_source)
        return (category, filename)

    @staticmethod
    def extract_page(filename):
        """Split the page file texts by triple-dashed lines, return the mata
        and content.

        :param filename: the filename of markup page

        returns:
          meta_str (str): page's meta string
          content_str (str): html parsed from markdown or other markup text.
        """
        regex = re.compile(b'(?sm)^---(?P<meta>.*?)^---(?P<body>.*)')
        with io.open(filename, b'rt', encoding=b'utf-8') as (fd):
            match_obj = re.match(regex, fd.read())
            if match_obj:
                meta_str = match_obj.group(b'meta')
                content_str = match_obj.group(b'body')
            else:
                raise Exception(b'extracting page with format error, see <http://simiki.org/docs/metadata.html>')
        return (meta_str, content_str)

    def parse_meta(self, yaml_str):
        """Parse meta from yaml string, and validate yaml filed, return dict"""
        try:
            meta = yaml.load(yaml_str, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            e.extra_msg = b'yaml format error'
            raise

        category, src_fname = self.get_category_and_file()
        dst_fname = src_fname.replace((b'.{0}').format(self.site_config[b'default_ext']), b'.html')
        meta.update({b'category': category, b'filename': dst_fname})
        if b'tag' in meta:
            if isinstance(meta[b'tag'], basestring):
                _tags = [ t.strip() for t in meta[b'tag'].split(b',') ]
                meta.update({b'tag': _tags})
        if b'title' not in meta:
            raise Exception(b"no 'title' in meta")
        return meta

    def _parse_markup(self, markup_text):
        """Parse markup text to html

        Only support Markdown for now.
        """
        markdown_extensions = self._set_markdown_extensions()
        html_content = markdown.markdown(markup_text, extensions=markdown_extensions)
        return html_content

    def _set_markdown_extensions(self):
        """Set the extensions for markdown parser"""
        markdown_extensions_config = {b'fenced_code': {}, b'nl2br': {}, b'toc': {b'title': b'Table of Contents'}, b'extra': {}}
        if self.site_config[b'pygments']:
            markdown_extensions_config.update({b'codehilite': {b'css_class': b'hlcode'}})
        if b'markdown_ext' in self.site_config:
            markdown_extensions_config.update(self.site_config[b'markdown_ext'])
        markdown_extensions = []
        for k, v in markdown_extensions_config.items():
            ext = import_string(b'markdown.extensions.' + k).makeExtension()
            if v:
                for i, j in v.items():
                    ext.setConfig(i, j)

            markdown_extensions.append(ext)

        return markdown_extensions

    def get_relation(self):
        rn = []
        if self._tags and b'tag' in self.meta:
            for t in self.meta[b'tag']:
                rn.extend(self._tags[t])

        rn = [ r for r in rn if self.meta[b'title'] != r[b'title'] ]
        rn = [ r for n, r in enumerate(rn) if r not in rn[n + 1:] ]
        return rn


class CatalogGenerator(BaseGenerator):

    def __init__(self, site_config, base_path, pages):
        """
        :pages: all pages' meta variables, dict type
        """
        super(CatalogGenerator, self).__init__(site_config, base_path)
        self._pages = pages
        self.pages = None
        self.structure = None
        return

    def get_structure(self):
        """Ref: http://stackoverflow.com/a/9619101/1276501"""
        dct = {}
        ext = self.site_config[b'default_ext']
        for path, meta in self._pages.items():
            if not path.endswith(ext):
                continue
            p = dct
            for x in path.split(os.sep):
                if ext in x:
                    meta[b'name'] = os.path.splitext(x)[0]
                    p = p.setdefault(x, meta)
                else:
                    p = p.setdefault(x, {})

        self.structure = dct.get(self.site_config[b'source'], {})
        self.sort_structure()

    def sort_structure(self):
        """Sort index structure in lower-case, alphabetical order

        Compare argument is a key/value structure, if the compare argument is a
        leaf node, which has `title` key in its value, use the title value,
        else use the key to compare.
        """

        def _cmp(arg1, arg2):
            arg1 = arg1[1][b'title'] if b'title' in arg1[1] else arg1[0]
            arg2 = arg2[1][b'title'] if b'title' in arg2[1] else arg2[0]
            cmp = lambda x, y: (x > y) - (x < y)
            return cmp(arg1.lower(), arg2.lower())

        if is_py2:
            sorted_opts = {b'cmp': _cmp}
        elif is_py3:
            sorted_opts = {b'key': cmp_to_key(_cmp)}

        def _sort(structure):
            sorted_structure = copy.deepcopy(structure)
            for k, _ in sorted_structure.items():
                sorted_structure = OrderedDict(sorted(sorted_structure.items(), **sorted_opts))
                if k.endswith((b'.{0}').format(self.site_config[b'default_ext'])):
                    continue
                sorted_structure[k] = _sort(sorted_structure[k])

            return sorted_structure

        self.structure = _sort(self.structure)

    def get_pages(self):
        _category = {}
        for c in self.site_config.get(b'category', []):
            c_name = c.pop(b'name')
            _category[c_name] = c

        def convert(d, prefix=b''):
            pages = []
            for k, v in d.items():
                if b'name' in v:
                    v.update({b'fname': k})
                    pages.append(v)
                else:
                    k_with_prefix = os.path.join(prefix, k)
                    _pages = convert(v, prefix=k_with_prefix)
                    _s_category = {b'name': k, b'pages': _pages}
                    if k_with_prefix in _category:
                        _s_category.update(_category[k_with_prefix])
                    pages.append(_s_category)

            return pages

        self.pages = convert(self.structure)
        self.update_pages_collection()

    def update_pages_collection(self):
        pages = copy.deepcopy(self.pages)
        self.pages = []
        for category in pages:
            if b'fname' in category:
                continue
            _c_pages = []
            _colls = {}
            for page in category.pop(b'pages'):
                if b'collection' in page:
                    coll_name = page[b'collection']
                    _colls.setdefault(coll_name, []).append(page)
                else:
                    _c_pages.append(page)

            colls = []
            for _coll_n, _coll_p in _colls.items():
                colls.append({b'name': _coll_n, b'pages': _coll_p})

            _c_pages.extend(colls)
            category.update({b'pages': _c_pages})
            self.pages.append(category)

    def get_template_vars(self):
        template_vars = copy.deepcopy(self._template_vars)
        self.get_structure()
        template_vars[b'site'].update({b'structure': self.structure})
        self.get_pages()
        template_vars.update({b'pages': self.pages})
        return template_vars

    def generate_catalog_html(self):
        tpl_vars = self.get_template_vars()
        html = self.env.get_template(b'index.html').render(tpl_vars)
        return html


class FeedGenerator(BaseGenerator):

    def __init__(self, site_config, base_path, pages, feed_fn=b'atom.xml'):
        """
        :pages: all pages' meta variables, dict type
        """
        super(FeedGenerator, self).__init__(site_config, base_path)
        self.pages = pages
        self.feed_fn = feed_fn

    def get_template_vars(self):
        tpl_vars = {b'site': self.site_config, 
           b'pages': self.pages}
        site_root = tpl_vars[b'site'][b'root']
        if site_root.endswith(b'/'):
            tpl_vars[b'site'][b'root'] = site_root[:-1]
        return tpl_vars

    def generate_feed(self):
        tpl_vars = self.get_template_vars()
        with open(os.path.join(self.base_path, self.feed_fn), b'r') as (fd):
            template = self.env.from_string(fd.read())
            feed_content = template.render(tpl_vars)
        return feed_content