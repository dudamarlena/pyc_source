# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/simiki/cli.py
# Compiled at: 2017-06-02 11:17:28
"""
Simiki CLI

Usage:
  simiki init [-p <path>]
  simiki (new | n) -t <title> -c <category> [-f <file>]
  simiki (generate | g) [--draft]
  simiki (preview | p) [--host <host>] [--port <port>] [-w]
  simiki update
  simiki -h | --help
  simiki -V | --version

Subcommands:
  init                Initial site
  new                 Create a new wiki page
  generate            Generate site
  preview             Preview site locally (develop mode)
  update              Update builtin scripts and themes under local site

Options:
  -h, --help          Help information
  -V, --version       Show version
  -p <path>           Specify the target path
  -c <category>       Specify the category
  -t <title>          Specify the new post title
  -f <file>           Specify the new post filename
  --host <host>       Bind host to preview [default: 127.0.0.1]
  --port <port>       Bind port to preview [default: 8000]
  -w                  Auto regenerated when file changed
  --draft             Include draft pages to generate
"""
from __future__ import print_function, unicode_literals, absolute_import
import os, os.path, sys, io, datetime, shutil, logging, random, multiprocessing, time, warnings
from docopt import docopt
from yaml import YAMLError
from simiki.generators import PageGenerator, CatalogGenerator, FeedGenerator
from simiki.initiator import Initiator
from simiki.config import parse_config
from simiki.log import logging_init
from simiki.server import preview
from simiki.watcher import watch
from simiki.updater import update_builtin
from simiki.utils import copytree, emptytree, mkdir_p, write_file
from simiki.compat import unicode, basestring, xrange
from simiki import __version__
try:
    from os import getcwdu
except ImportError:
    from os import getcwd as getcwdu

warnings.simplefilter(b'default')
logger = logging.getLogger(__name__)
config = None

def init_site(target_path):
    default_config_file = os.path.join(os.path.dirname(__file__), b'conf_templates', b'_config.yml.in')
    try:
        initiator = Initiator(default_config_file, target_path)
        if os.environ.get(b'TEST_MODE'):
            initiator.init(ask=False)
        else:
            initiator.init(ask=True)
    except Exception:
        logging.exception(b'Initialize site with error:')
        sys.exit(1)


def create_new_wiki(category, title, filename):
    global config
    if not filename:
        _title = title.replace(os.sep, b' slash ').lower()
        filename = (b'{0}.{1}').format(_title.replace(b' ', b'-'), config[b'default_ext'])
    now = datetime.datetime.now().strftime(b'%Y-%m-%d %H:%M')
    meta = (b'\n').join([
     b'---',
     (b'title: "{0}"').format(title),
     (b'date: {0}').format(now),
     b'---']) + b'\n\n'
    category_path = os.path.join(config[b'source'], category)
    if not os.path.exists(category_path):
        mkdir_p(category_path)
        logger.info((b'Creating category: {0}.').format(category))
    fn = os.path.join(category_path, filename)
    if os.path.exists(fn):
        logger.warning((b'File exists: {0}').format(fn))
    else:
        logger.info((b'Creating wiki: {0}').format(fn))
        with io.open(fn, b'wt', encoding=b'utf-8') as (fd):
            fd.write(meta)


def preview_site(host, port, dest, root, do_watch):
    """Preview site with watch content"""
    p_server = multiprocessing.Process(target=preview, args=(
     dest, root, host, port), name=b'ServerProcess')
    p_server.start()
    if do_watch:
        base_path = getcwdu()
        p_watcher = multiprocessing.Process(target=watch, args=(
         config, base_path), name=b'WatcherProcess')
        p_watcher.start()
    try:
        while p_server.is_alive():
            time.sleep(1)

        if do_watch:
            p_watcher.terminate()
    except (KeyboardInterrupt, SystemExit):
        pass


def method_proxy(cls_instance, method_name, *args, **kwargs):
    return getattr(cls_instance, method_name)(*args, **kwargs)


class Generator(object):

    def __init__(self, target_path):
        self.config = config
        self.config.update({b'version': __version__})
        self.target_path = target_path
        self.tags = {}
        self.pages = {}
        self.page_count = 0
        self.draft_count = 0
        self.include_draft = False

    def generate(self, include_draft=False):
        """
        :include_draft: True/False, include draft pages or not to generate.
        """
        self.include_draft = include_draft
        logger.debug(b'Empty the destination directory')
        dest_dir = os.path.join(self.target_path, self.config[b'destination'])
        if os.path.exists(dest_dir):
            exclude_list = [b'.git', b'CNAME', b'favicon.ico']
            emptytree(dest_dir, exclude_list)
        self.generate_tags()
        self.generate_pages()
        if not os.path.exists(os.path.join(self.config[b'source'], b'index.md')):
            self.generate_catalog(self.pages)
        feed_fn = b'atom.xml'
        if os.path.exists(os.path.join(getcwdu(), feed_fn)):
            self.generate_feed(self.pages, feed_fn)
        self.install_theme()
        self.copy_attach()
        for _fn in ('CNAME', 'favicon.ico'):
            _file = os.path.join(getcwdu(), _fn)
            if os.path.exists(_file):
                shutil.copy2(_file, os.path.join(self.config[b'destination'], _fn))

    def generate_tags(self):
        g = PageGenerator(self.config, self.target_path)
        for root, dirs, files in os.walk(self.config[b'source']):
            files = [ f for f in files if not f.startswith(b'.') ]
            dirs[:] = [ d for d in dirs if not d.startswith(b'.') ]
            for filename in files:
                if not filename.endswith(self.config[b'default_ext']):
                    continue
                md_file = os.path.join(root, filename)
                g.src_file = md_file
                meta, _ = g.get_meta_and_content(do_render=False)
                _tags = meta.get(b'tag') or []
                for t in _tags:
                    self.tags.setdefault(t, []).append(meta)

    def generate_feed(self, pages, feed_fn):
        logger.info(b'Generate feed.')
        feed_generator = FeedGenerator(self.config, self.target_path, pages, feed_fn)
        feed = feed_generator.generate_feed()
        ofile = os.path.join(self.target_path, self.config[b'destination'], feed_fn)
        write_file(ofile, feed)

    def generate_catalog(self, pages):
        logger.info(b'Generate catalog page.')
        catalog_generator = CatalogGenerator(self.config, self.target_path, pages)
        html = catalog_generator.generate_catalog_html()
        ofile = os.path.join(self.target_path, self.config[b'destination'], b'index.html')
        write_file(ofile, html)

    def generate_pages(self):
        logger.info(b'Start generating markdown files.')
        content_path = self.config[b'source']
        _pages_l = []
        for root, dirs, files in os.walk(content_path):
            files = [ f for f in files if not f.startswith(b'.') ]
            dirs[:] = [ d for d in dirs if not d.startswith(b'.') ]
            for filename in files:
                if not filename.endswith(self.config[b'default_ext']):
                    continue
                md_file = os.path.join(root, filename)
                _pages_l.append(md_file)

        npage = len(_pages_l)
        if npage:
            nproc = min(multiprocessing.cpu_count(), npage)
            split_pages = [ [] for n in xrange(0, nproc) ]
            random.shuffle(_pages_l)
            for i in xrange(npage):
                split_pages[(i % nproc)].append(_pages_l[i])

            pool = multiprocessing.Pool(processes=nproc)
            results = []
            for n in xrange(nproc):
                r = pool.apply_async(method_proxy, (
                 self, b'generate_multiple_pages', split_pages[n]), callback=self._generate_callback)
                results.append(r)

            pool.close()
            for r in results:
                r.get()

        generate_result = [
         (b'Generate {0} pages').format(self.page_count)]
        _err_npage = npage - self.page_count
        if self.include_draft:
            generate_result.append((b'include {0} drafts').format(self.draft_count))
        else:
            _err_npage -= self.draft_count
            generate_result.append((b'ignore {0} drafts').format(self.draft_count))
        if _err_npage:
            generate_result.append((b' {0} pages failed').format(_err_npage))
        logger.info((b', ').join(generate_result) + b'.')

    def generate_multiple_pages(self, md_files):
        _pages = {}
        _page_count = 0
        _draft_count = 0
        page_generator = PageGenerator(self.config, self.target_path, self.tags)
        for _f in md_files:
            try:
                page_meta = self.generate_single_page(page_generator, _f)
                if page_meta:
                    _pages[_f] = page_meta
                    _page_count += 1
                    if page_meta.get(b'draft'):
                        _draft_count += 1
                else:
                    _draft_count += 1
            except Exception:
                page_meta = None
                logger.exception((b'{0} failed to generate:').format(_f))

        return (
         _pages, _page_count, _draft_count)

    def generate_single_page(self, generator, md_file):
        logger.debug((b'Generate: {0}').format(md_file))
        html = generator.to_html(os.path.realpath(md_file), self.include_draft)
        if not html:
            return None
        else:
            category, filename = os.path.split(md_file)
            category = os.path.relpath(category, self.config[b'source'])
            output_file = os.path.join(self.target_path, self.config[b'destination'], category, (b'{0}.html').format(os.path.splitext(filename)[0]))
            write_file(output_file, html)
            meta = generator.meta
            meta[b'content'] = generator.content
            return meta

    def _generate_callback(self, result):
        _pages, _page_count, _draft_count = result
        self.pages.update(_pages)
        self.page_count += _page_count
        self.draft_count += _draft_count

    def install_theme(self):
        """Copy static directory under theme to destination directory"""
        src_theme = os.path.join(self.target_path, self.config[b'themes_dir'], self.config[b'theme'], b'static')
        dest_theme = os.path.join(self.target_path, self.config[b'destination'], b'static')
        if os.path.exists(dest_theme):
            shutil.rmtree(dest_theme)
        copytree(src_theme, dest_theme)
        logging.debug((b'Installing theme: {0}').format(self.config[b'theme']))

    def copy_attach(self):
        """Copy attach directory under root path to destination directory"""
        src_p = os.path.join(self.target_path, self.config[b'attach'])
        dest_p = os.path.join(self.target_path, self.config[b'destination'], b'attach')
        if os.path.exists(src_p):
            copytree(src_p, dest_p)


def unicode_docopt(args):
    for k in args:
        if isinstance(args[k], basestring) and not isinstance(args[k], unicode):
            args[k] = args[k].decode(b'utf-8')


def main(args=None):
    global config
    if not args:
        args = docopt(__doc__, version=(b'Simiki {0}').format(__version__))
    unicode_docopt(args)
    logging_init(logging.DEBUG)
    target_path = args[b'-p'] if args[b'-p'] else getcwdu()
    if args[b'init']:
        init_site(target_path)
    else:
        config_file = os.path.join(target_path, b'_config.yml')
        try:
            config = parse_config(config_file)
        except (Exception, YAMLError):
            logging.exception(b'Parse config with error:')
            sys.exit(1)

        level = logging.DEBUG if config[b'debug'] else logging.INFO
        logging_init(level)
        if args[b'generate'] or args[b'g']:
            generator = Generator(target_path)
            generator.generate(include_draft=args[b'--draft'])
        elif args[b'new'] or args[b'n']:
            create_new_wiki(args[b'-c'], args[b'-t'], args[b'-f'])
        elif args[b'preview'] or args[b'p']:
            args[b'--port'] = int(args[b'--port'])
            preview_site(args[b'--host'], args[b'--port'], config[b'destination'], config[b'root'], args[b'-w'])
        elif args[b'update']:
            update_builtin(themes_dir=config[b'themes_dir'])
    logger.info(b'Done.')


if __name__ == b'__main__':
    main()