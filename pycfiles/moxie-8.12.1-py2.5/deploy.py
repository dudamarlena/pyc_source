# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/moxie/deploy.py
# Compiled at: 2008-12-19 18:06:00
from __future__ import with_statement
import contextlib, logging, optparse, os, shutil, urlparse, webbrowser
from wsgiref.simple_server import make_server
import pkg_resources, webob, moxie.web
log = logging.getLogger(__name__)

def _setup_logging():
    _log_handler = logging.StreamHandler()
    _log_handler.setFormatter(logging.Formatter('%(message)s'))
    _log_handler.setLevel(logging.INFO)
    log.addHandler(_log_handler)


def local(bindaddr='localhost', port=8080):
    """Deploy a test web server."""
    server = make_server(bindaddr, port, moxie.web.app())
    url = 'http://%s:%u/' % (bindaddr, port)
    print url
    webbrowser.open(url)
    server.serve_forever()


def static():
    """Deploy a set of static files to a directory."""
    parser = optparse.OptionParser(usage='Usage: %prog [options] [directories ...]', description='moxie makes mixtapes!')
    parser.add_option('-f', '--force', help='overwrite existing files', action='store_true')
    parser.add_option('-v', '--verbose', help='explain what is being done', action='store_true')
    parser.add_option('-u', '--url', help="the directory's base URL", action='store')
    (options, args) = parser.parse_args()
    _setup_logging()
    if options.verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARN)
    if not args:
        args = [
         '.']
        log.info('Using current directory...')
    for d in args:
        app = moxie.web.app(d)
        if not app.music:
            log.error('Skipping %s (no music)' % d)
            continue
        if options.url:
            options.url = options.url.strip('/')
        else:
            log.warn('No base URL specified (--url). Expect weirdness!')
        for (uri, func) in moxie.web.uri.uris(app):
            req = webob.Request.blank('/' + uri, base_url=options.url)
            res = req.get_response(app)
            fn = os.path.join(d, uri if uri else 'index.html')
            if os.path.exists(fn) and not options.force:
                log.warn('Skipping %s (file exists)' % fn)
            else:
                with file(fn, 'w') as (f):
                    f.write(res.body)
                    log.info('Wrote %s' % fn)

        for bfn in pkg_resources.resource_listdir(__name__, 'static'):
            stream = pkg_resources.resource_stream(__name__, os.path.join('static', bfn))
            with contextlib.closing(stream) as (f_in):
                fn = os.path.join(d, bfn)
                if os.path.exists(fn) and not options.force:
                    log.warn('Skipping %s (file exists)' % fn)
                else:
                    with file(fn, 'w') as (f_out):
                        shutil.copyfileobj(f_in, f_out)
                        log.info('Wrote %s' % fn)