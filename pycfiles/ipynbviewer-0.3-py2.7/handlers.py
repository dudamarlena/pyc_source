# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/ipynbviewer/handlers.py
# Compiled at: 2015-01-26 23:20:59
import io, os, time
from urllib import quote
from datetime import datetime
from contextlib import contextmanager
from tornado.log import app_log
from tornado import web, gen
from tornado.ioloop import IOLoop
from IPython.nbformat.current import reads_json
from IPython.nbconvert.exporters import Exporter
from IPython.html.base.handlers import notebook_path_regex, path_regex
from IPython.html import DEFAULT_STATIC_FILES_PATH as ipython_static_path
component_path = os.path.join(ipython_static_path, 'components')
date_fmt = '%a, %d %b %Y %H:%M:%S UTC'

class NbFormatError(Exception):
    pass


exporters = {}

def render_notebook(exporter, nbfile, nb, url=None, config=None):
    if not isinstance(exporter, Exporter):
        exporter_cls = exporter
        if exporter_cls not in exporters:
            app_log.info('instantiating %s' % exporter_cls.__name__)
            exporters[exporter_cls] = exporter_cls(config=config, log=app_log)
        exporter = exporters[exporter_cls]
    css_theme = nb.get('metadata', {}).get('_nbviewer', {}).get('css', None)
    if not css_theme or not css_theme.strip():
        css_theme = None
    try:
        name = nb.metadata.name
    except AttributeError:
        name = ''

    if not name and url is not None:
        name = url.rsplit('/')[(-1)]
    if not name.endswith('.ipynb'):
        name = name + '.ipynb'
    html, resources = exporter.from_filename(nbfile)
    config = {'download_name': name, 
       'css_theme': css_theme}
    return (
     html, config)


def url_path_join(*pieces):
    initial = pieces[0].startswith('/')
    final = pieces[(-1)].endswith('/')
    stripped = [ s.strip('/') for s in pieces ]
    result = ('/').join(s for s in stripped if s)
    if initial:
        result = '/' + result
    if final:
        result = result + '/'
    if result == '//':
        result = '/'
    return result


def url_escape(path):
    """Escape special characters in a URL path
    Turns '/foo bar/' into '/foo%20bar/'
    """
    parts = path.split('/')
    return ('/').join([ quote(p) for p in parts ])


class IndexHandler(web.RequestHandler):
    """Render the tree view, listing notebooks"""

    @property
    def base_url(self):
        return self.settings.get('base_url', '/')

    @property
    def log(self):
        return self.settings['log']

    @property
    def notebook_manager(self):
        return self.settings['notebook_manager']

    def render_template(self, name, **ns):
        template = self.settings['jinja2_env'].get_template(name)
        return template.render(**ns)

    def generate_breadcrumbs(self, path):
        breadcrumbs = [
         (
          url_escape(url_path_join(self.base_url, 'tree')), '')]
        comps = path.split('/')
        for i, comp in enumerate(comps):
            if comp:
                link = url_escape(url_path_join(self.base_url, 'tree', *comps[0:i + 1]))
                breadcrumbs.append((link, comp))

        return breadcrumbs

    def generate_page_title(self, path):
        comps = path.split('/')
        if len(comps) > 3:
            for i in range(len(comps) - 2):
                comps.pop(0)

        page_title = url_path_join(*comps)
        if page_title:
            return page_title + '/'
        else:
            return 'Home'

    def get(self, path='', name=None):
        path = path.strip('/')
        nbm = self.notebook_manager
        errors = None
        if name is not None:
            url = url_escape(url_path_join(self.base_url, 'notebooks', path, name))
            self.log.debug('Redirecting %s to %s', self.request.path, url)
            self.redirect(url)
        else:
            if not nbm.path_exists(path=path):
                errors = 'Directory is hidden or does not exist.'
            elif nbm.is_hidden(path):
                self.log.info('Refusing to serve hidden directory, via 404 Error')
                errors = 'Refusing to serve hidden directory'
            breadcrumbs = self.generate_breadcrumbs(path)
            page_title = self.generate_page_title(path)
            notebook_list = nbm.list_dirs(path) + nbm.list_notebooks(path)
            if not notebook_list:
                errors = 'Notebook list empty'
                notebook_list = [errors]
            html = self.render_template('index.html', page_title=page_title, breadcrumbs=breadcrumbs, notebook_list=notebook_list, errors=errors)
            self.write(html)
        return


class LocalFileHandler(web.RequestHandler):
    """Renderer for /localfile
    Serving notebooks from the local filesystem
    """

    @property
    def pool(self):
        return self.settings['pool']

    @property
    def exporter(self):
        return self.settings['exporter']

    @property
    def config(self):
        return self.settings['config']

    def render_template(self, name, **ns):
        template = self.settings['jinja2_env'].get_template(name)
        return template.render(**ns)

    @contextmanager
    def time_block(self, message):
        """context manager for timing a block
        logs millisecond timings of the block
        """
        tic = time.time()
        yield
        dt = time.time() - tic
        log = app_log.info if dt > 1 else app_log.debug
        log('%s in %.2f ms', message, 1000.0 * dt)

    @property
    def render_timeout(self):
        """0 render_timeout means never finish early"""
        return self.settings.setdefault('render_timeout', 0)

    @gen.coroutine
    def get(self, path, name=None):
        if not path:
            raise web.HTTPError(404)
        abspath = os.path.join(self.settings.get('document_path'), path)
        app_log.info("looking for file: '%s'" % abspath)
        if not os.path.exists(abspath):
            raise web.HTTPError(404)
        yield self.finish_notebook(abspath, url=path, msg='file from localfile: %s' % path)

    def initialize(self):
        loop = IOLoop.current()
        if self.render_timeout:
            self.slow_timeout = loop.add_timeout(loop.time() + self.render_timeout, self.finish_early)

    def finish_early(self):
        """When the render is slow, draw a 'waiting' page instead

        rely on the cache to deliver the page to a future request.
        """
        if self._finished:
            return
        else:
            app_log.info('finishing early %s', self.request.uri)
            html = self.render_template('slow_notebook.html')
            self.set_status(202)
            self.finish(html)
            self.write = self.finish = self.redirect = lambda chunk=None: None
            return

    @gen.coroutine
    def finish_notebook(self, nbfile, url, msg=None):
        """render a notebook from its JSON body.

        msg is extra information for the log message when rendering fails.
        """
        if msg is None:
            msg = url
        with io.open(nbfile, encoding='utf-8') as (f):
            json_notebook = f.read()
        nb = reads_json(json_notebook)
        try:
            app_log.debug('Requesting render of %s', url)
            with self.time_block('Rendered %s' % url):
                app_log.info('rendering %d B notebook from %s', len(json_notebook), url)
                nbhtml, config = yield self.pool.submit(render_notebook, self.exporter, nbfile, nb, url, config=self.config)
        except NbFormatError as e:
            app_log.error('Invalid notebook %s: %s', msg, e)
            raise web.HTTPError(400, str(e))
        except Exception as e:
            app_log.error('Failed to render %s', msg, exc_info=True)
            raise web.HTTPError(400, str(e))
        else:
            app_log.debug('Finished render of %s', url)

        html = self.render_template('notebook.html', body=nbhtml, url=url, date=datetime.utcnow().strftime(date_fmt), **config)
        yield self._finish(html)
        return

    @gen.coroutine
    def _finish(self, content=''):
        """Has not yet cached"""
        content = content.replace('https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js', '/static/js/require.min.js').replace('https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js', '/static/js/jquery.min.js')
        self.write(content)
        self.finish()


class Custom404(web.RequestHandler):
    """Render our 404 template"""

    def prepare(self):
        raise web.HTTPError(404)


handlers = [
 (
  '/components/(.*)', web.StaticFileHandler,
  dict(path=component_path)),
 (
  '/ipython-static/(.*)', web.StaticFileHandler,
  dict(path=ipython_static_path)),
 (
  '/tree%s' % notebook_path_regex, IndexHandler),
 (
  '/tree%s' % path_regex, IndexHandler),
 (
  '/tree', IndexHandler),
 (
  '/notebooks/(.*)', LocalFileHandler),
 (
  '/', web.RedirectHandler, {'url': '/tree'}),
 (
  '.*', Custom404)]