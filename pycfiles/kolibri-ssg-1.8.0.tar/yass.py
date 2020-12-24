# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Yass/yass/yass.py
# Compiled at: 2019-04-07 20:09:57
"""
~ Yass ~
"""
import os, re, sys, copy, json, time, yaml, arrow, shutil, jinja2, logging, requests, frontmatter, pkg_resources, webassets.loaders
from slugify import slugify
from extras import md
from paginator import Paginator
from distutils.dir_util import copy_tree
from webassets import Environment as WAEnv
from webassets.ext.jinja2 import AssetsExtension
from webassets.script import CommandLineEnvironment
from .__about__ import *
from . import utils
NAME = 'Yass'
PAGE_FORMAT = ('.html', '.md')
DEFAULT_LAYOUT = 'layouts/default.html'

class Yass(object):
    RE_BLOCK_BODY = re.compile('{%\\s*block\\s+body\\s*%}')
    RE_BLOCK_BODY_PARSED = re.compile('{%\\s*block\\s+body\\s*%}(.*?){%\\s*endblock\\s*%}')
    RE_EXTENDS = re.compile('{%\\s*extends\\s+(.*?)\\s*%}')
    default_page_meta = {'title': '', 
       'markup': None, 
       'slug': None, 
       'url': '', 
       'description': '', 
       'pretty_url': True, 
       'meta': {}, 'layout': None, 
       'template': None, 
       'sfc': True}
    tpl_env = None
    _templates = {}
    _pages_meta = {}

    def __init__(self, root_dir, config=None):
        """

        :param root_dir: The application root dir
        :param config: (dict), Dict configuration, will override previously set data
        """
        self.root_dir = root_dir
        self.build_dir = os.path.join(self.root_dir, 'build')
        self.static_dir = os.path.join(self.root_dir, 'static')
        self.content_dir = os.path.join(self.root_dir, 'content')
        self.pages_dir = os.path.join(self.root_dir, 'pages')
        self.templates_dir = os.path.join(self.root_dir, 'templates')
        self.data_dir = os.path.join(self.root_dir, 'data')
        self.build_static_dir = os.path.join(self.build_dir, 'static')
        config_file = os.path.join(self.root_dir, 'yass.yml')
        self.config = utils.load_conf(config_file, config)
        self.default_layout = self.config.get('default_layout', DEFAULT_LAYOUT)
        self.site_config = utils.dictdot(self.config.get('site', {}))
        self.site_config.setdefault('base_url', '/')
        self.base_url = self.site_config.get('base_url')
        self.sitename = utils.extract_sitename(self.config.get('sitename'))
        self._data = self._load_data()
        self._init_jinja({'site': self.site_config, 
           'data': self._data, 
           '__YASS__': self._yass_vars()})
        self._init_webassets()

    def _yass_vars(self):
        """ Global variables """
        utc = arrow.utcnow()
        return {'NAME': __title__, 
           'VERSION': __version__, 
           'URL': __uri__, 
           'GENERATOR': '%s %s' % (__title__, __version__), 
           'YEAR': utc.year}

    def _init_jinja(self, global_context={}):
        loader = jinja2.ChoiceLoader([
         jinja2.DictLoader({'yass.macros': pkg_resources.resource_string(__name__, 'extras/macros.html')}),
         jinja2.FileSystemLoader(self.templates_dir)])
        env_extensions = [
         'yass.extras.md.MarkdownExtension',
         'yass.extras.md.MarkdownTagExtension',
         AssetsExtension]
        if self.config.get('compress_html') is True:
            env_extensions.append('yass.extras.htmlcompress.HTMLCompress')
        self.tpl_env = jinja2.Environment(loader=loader, extensions=env_extensions)
        self.tpl_env.globals.update(global_context)
        self.tpl_env.filters.update({'format_datetime': lambda dt, format: arrow.get(dt).format(format), 
           'yass_link_to': self._link_to, 
           'yass_url_to': self._url_to})

    def _get_page_meta(self, page):
        """
        Cache the page meta from the frontmatter and assign new keys
        The cache data will be used to build links or other properties
        """
        meta = self._pages_meta.get(page)
        if not meta:
            src_file = os.path.join(self.pages_dir, page)
            with open(src_file) as (f):
                _, _ext = os.path.splitext(src_file)
                markup = _ext.replace('.', '')
                _meta, _ = frontmatter.parse(f.read())
                meta = self.default_page_meta.copy()
                meta['meta'].update(self.config.get('site.meta', {}))
                meta.update(_meta)
                dest_file, url = self._get_dest_file_and_url(page, meta)
                meta['url'] = url
                meta['filepath'] = dest_file
                if meta.get('markup') is None:
                    meta['markup'] = markup
                self._pages_meta[page] = meta
        return meta

    def _get_page_content(self, page):
        """ Get the page content without the frontmatter """
        src_file = os.path.join(self.pages_dir, page)
        with open(src_file) as (f):
            _meta, content = frontmatter.parse(f.read())
            return content

    def _link_to(self, page, text=None, title=None, _class='', id='', alt='', **kwargs):
        """ Build the A HREF LINK To a page."""
        anchor = ''
        if '#' in page:
            page, anchor = page.split('#')
            anchor = '#' + anchor
        meta = self._get_page_meta(page)
        return ('<a href=\'{url}\' class=\'{_class}\' id=\'{id}\'  title="{title}">{text}</a>').format(url=meta.get('url', '/') + anchor, text=text or meta.get('title') or title, title=title or '', _class=_class, id=id)

    def _url_to(self, page):
        """ Get the url of a  page """
        anchor = ''
        if '#' in page:
            page, anchor = page.split('#')
            anchor = '#' + anchor
        meta = self._get_page_meta(page)
        return meta.get('url')

    def _get_dest_file_and_url(self, filepath, page_meta={}):
        """ Return tuple of the file destination and url """
        filename = filepath.split('/')[(-1)]
        filepath_base = filepath.replace(filename, '').rstrip('/')
        slug = page_meta.get('slug')
        fname = slugify(slug) if slug else filename.replace('.html', '').replace('.md', '')
        if page_meta.get('pretty_url') is False:
            dest_file = os.path.join(filepath_base, '%s.html' % fname)
        else:
            dest_dir = filepath_base
            if filename not in ('index.html', 'index.md'):
                dest_dir = os.path.join(filepath_base, fname)
            dest_file = os.path.join(dest_dir, 'index.html')
        url = '/' + dest_file.replace('index.html', '')
        return (dest_file, url)

    def _load_data(self):
        data = {}
        for root, _, files in os.walk(self.data_dir):
            for fname in files:
                if fname.endswith(('.json', )):
                    name = fname.replace('.json', '')
                    fname = os.path.join(root, fname)
                    if os.path.isfile(fname):
                        with open(fname) as (f):
                            _ = json.load(f)
                            if isinstance(_, dict):
                                _ = utils.dictdot(_)
                            data[name] = _

        data_api_urls = self.site_config.get('data_api_urls')
        if data_api_urls:
            for name, url in data_api_urls.items():
                try:
                    r = requests.get(url)
                    if r.status_code == 200:
                        _ = r.json()
                        if isinstance(_, dict):
                            _ = utils.dictdot(_)
                        data[name] = _
                    else:
                        raise Exception('`%s -> %s` returns status code %s' % (name, url, r.status_code))
                except Exception as e:
                    raise Exception('Data API URLS Error: %s' % e)

        return utils.dictdot(data)

    def _init_webassets(self):
        assets_env = WAEnv(directory='./static', url=self.config.get('static_url', '/static'))
        bundles = self.config.get('assets_bundles', {})
        assets_env.register(bundles)
        self.tpl_env.assets_environment = assets_env
        self.webassets_cmd = None
        if bundles:
            handler = logging.StreamHandler if self.config.get('debug', False) else logging.NullHandler
            log = logging.getLogger('webassets')
            log.addHandler(handler())
            log.setLevel(logging.DEBUG)
            self.webassets_cmd = CommandLineEnvironment(assets_env, log)
        return

    def clean_build_dir(self):
        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)

    def build_static(self):
        """ Build static files """
        if not os.path.isdir(self.build_static_dir):
            os.makedirs(self.build_static_dir)
        copy_tree(self.static_dir, self.build_static_dir)
        if self.webassets_cmd:
            self.webassets_cmd.build()

    def build_pages(self):
        """Iterate over the pages_dir and build the pages """
        for root, _, files in os.walk(self.pages_dir):
            base_dir = root.replace(self.pages_dir, '').lstrip('/')
            if not base_dir.startswith('_'):
                for f in files:
                    src_file = os.path.join(base_dir, f)
                    self._build_page(src_file)

    def _build_page(self, filepath):
        """ To build from filepath, relative to pages_dir """
        filename = filepath.split('/')[(-1)]
        if not filename.startswith(('_', '.')) and filename.endswith(PAGE_FORMAT):
            meta = self._get_page_meta(filepath)
            content = self._get_page_content(filepath)
            _default_page = {'build_dir': self.build_dir, 
               'filepath': meta['filepath'], 
               'context': {'page': meta}, 'content': content, 
               'markup': meta.get('markup'), 
               'template': meta.get('template'), 
               'layout': meta.get('layout') or self.default_layout}
            _generator = meta.get('_generator')
            if _generator:
                data = self._data.get(_generator.get('data_source'))
                special_meta = [
                 'title', 'slug', 'description']
                if _generator.get('type') == 'single':
                    for d in data:
                        dmeta = copy.deepcopy(meta)
                        page = copy.deepcopy(_default_page)
                        for _ in special_meta:
                            if _ in d:
                                dmeta[_] = d.get(_)

                        if 'slug' in _generator:
                            dmeta['slug'] = _generator.get('slug').format(**d)
                        if 'slug' not in dmeta:
                            print "WARNING: Skipping page because it's missing `slug`"
                            continue
                        slug = dmeta.get('slug')
                        dmeta['url'] = slug
                        dmeta['context'] = d
                        page.update({'filepath': slug, 
                           'context': {'page': dmeta}})
                        self.create_page(**page)

                if _generator.get('type') == 'pagination':
                    per_page = int(_generator.get('per_page', self.site_config.get('pagination.per_page', 10)))
                    left_edge = int(_generator.get('left_edge', self.site_config.get('pagination.left_edge', 2)))
                    left_current = int(_generator.get('left_edge', self.site_config.get('pagination.left_current', 3)))
                    right_current = int(_generator.get('right_current', self.site_config.get('pagination.right_current', 4)))
                    right_edge = int(_generator.get('right_edge', self.site_config.get('pagination.right_edge', 2)))
                    padding = _generator.get('padding')
                    slug = _generator.get('slug')
                    limit = _generator.get('limit')
                    if 'limit' in _generator:
                        data = data[:int(limit)]
                    data_chunks = utils.chunk_list(data, per_page)
                    len_data = len(data)
                    for i, d in enumerate(data_chunks):
                        dmeta = copy.deepcopy(meta)
                        page = copy.deepcopy(_default_page)
                        page_num = i + 1
                        _paginator = Paginator([], total=len_data, page=page_num, per_page=per_page, padding=padding, left_edge=left_edge, right_edge=right_edge, left_current=left_current, right_current=right_current)
                        _paginator.slug = slug
                        _paginator.index_slug = _generator.get('index_slug')
                        _slug = slug.format(**{'page_num': page_num})
                        dmeta['url'] = _slug
                        dmeta['context'] = d
                        dmeta['paginator'] = _paginator
                        page.update({'filepath': _slug, 
                           'context': {'page': dmeta}})
                        self.create_page(**page)
                        if i == 0 and _generator.get('index_slug'):
                            page['filepath'] = _generator.get('index_slug')
                            self.create_page(**page)

            else:
                self.create_page(**_default_page)

    def create_page(self, build_dir, filepath, context={}, content=None, template=None, markup=None, layout=None):
        """
        To dynamically create a page and save it in the build_dir
        :param build_dir: (path) The base directory that will hold the created page
        :param filepath: (string) the name of the file to create. May  contain slash to indicate directory
                        It will also create the url based on that name
                        If the filename doesn't end with .html, it will create a subdirectory
                        and create `index.html`
                        If file contains `.html` it will stays as is
                        ie:
                            post/waldo/where-is-waldo/ -> post/waldo/where-is-waldo/index.html
                            another/music/new-rap-song.html -> another/music/new-rap-song.html
                            post/page/5 -> post/page/5/index.html
        :param context: (dict) context data
        :param content: (text) The content of the file to be created. Will be overriden by template
        :param template: (path) if source is not provided, template can be used to create the page.
                         Along with context it allows to create dynamic pages.
                         The file is relative to `/templates/`
                         file can be in html|md
        :param markup: (string: html|md), when using content. To indicate which markup to use.
                        based on the markup it will parse the data
                        html: will render as is
                        md: convert to the appropriate format
        :param layout: (string) when using content. The layout to use.
                        The file location is relative to `/templates/`
                        file can be in html|md
        :return:
        """
        build_dir = build_dir.rstrip('/')
        filepath = filepath.lstrip('/').rstrip('/')
        if not filepath.endswith('.html'):
            filepath += '/index.html'
        dest_file = os.path.join(build_dir, filepath)
        dest_dir = os.path.dirname(dest_file)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        _context = context
        if 'page' not in _context:
            _context['page'] = self.default_page_meta.copy()
        if 'url' not in _context['page']:
            _context['page']['url'] = '/' + filepath.lstrip('/').replace('index.html', '')
        if template:
            if template not in self._templates:
                self._templates[template] = self.tpl_env.get_template(template)
            tpl = self._templates[template]
        else:
            sfc = utils.destruct_sfc(content)
            content = sfc[1].get('template')
            if markup == 'md':
                _context['page']['__toc__'] = md.get_toc(content)
                content = md.convert(content)
            if re.search(self.RE_EXTENDS, content) is None:
                layout = layout or self.default_layout
                content = ("\n{% extends '{}' %} \n\n").replace('{}', layout) + content
            if re.search(self.RE_BLOCK_BODY, content) is None:
                _layout_block = re.search(self.RE_EXTENDS, content).group(0)
                content = content.replace(_layout_block, '')
                content = '\n' + _layout_block + '\n' + '{% block body %} \n' + content.strip() + '\n{% endblock %}'
            tpl = self.tpl_env.from_string(content)
        if sfc[0] is True:
            pass
        with open(dest_file, 'w') as (fw):
            fw.write(tpl.render(**_context))
        return

    def build(self):
        self.clean_build_dir()
        if not os.path.isdir(self.build_dir):
            os.makedirs(self.build_dir)
        self.build_static()
        self.build_pages()