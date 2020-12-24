# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/doomsday/git/cellarpy/venv/lib/python3.6/site-packages/cellar/web.py
# Compiled at: 2017-10-28 11:27:21
# Size of source mod 2**32: 2726 bytes
from bottle import response
from bottle import template
from bottle import MakoTemplate
from bottle import CheetahTemplate
from bottle import Jinja2Template
import functools, logging

def guess_type(filename, headers):
    """
    Try to guess Content-Encoding/Content-Type, and set it to current response
    """
    import mimetypes
    charset = 'UTF-8'
    mimetype, encoding = mimetypes.guess_type(filename)
    if not mimetype:
        if filename.find('.woff2'):
            mimetype, encoding = mimetypes.guess_type(filename + '.woff')
    if encoding:
        headers['Content-Encoding'] = encoding
    if mimetype:
        if mimetype[:5] == 'text/':
            if charset:
                if 'charset' not in mimetype:
                    mimetype += '; charset=%s' % charset
        headers['Content-Type'] = mimetype


def static_file(filename, root, *args, **kwargs):
    """
    Revised version of bottle static_file
    changelog: add support for woff2 extension
    """
    from bottle import static_file as bottle_static_file
    resp = bottle_static_file(filename, root, *args, **kwargs)
    if 'Content-Type' not in response.headers:
        guess_type(filename, resp.headers)
    return resp


def generate_less_from_css(filename, root, cache=None):
    from subprocess import call
    from cellar import fs
    from os import path
    css_cache = path.join(cache, filename)
    less_file = path.join(root, filename.replace('.css', '.less'))
    if not fs.static_file_exists(cache, filename) or path.getmtime(less_file) > path.getmtime(css_cache):
        logging.debug("Cache version of {0} doesn't exist or is outdated.".format(css_cache))
        with open(css_cache, 'w') as (fd):
            logging.debug('Write lessc output for {0} to {1}'.format(less_file, css_cache))
            call(['lessc', less_file], stdout=fd)
    return static_file(filename, root=cache)


def generate_static_file(filename, root, *args, **kwargs):
    """
    Merged static_file and template bottle functions.
    Can generate dynamic content in css or js file.
    e.g. very useful to generate path or size dynamically.
    
    If you want jinja2 instead of SimpleTemplate, you can use:
    from web import jinja2_static_file as generate_static_file
    """
    from cellar import fs
    if fs.static_file_exists(root, filename):
        return static_file(filename, root=root)
    else:
        guess_type(filename, response.headers)
        return template(filename, *args, **kwargs)


mako_static_file = functools.partial(generate_static_file, template_adapter=MakoTemplate)
cheetah_static_file = functools.partial(generate_static_file, template_adapter=CheetahTemplate)
jinja2_static_file = functools.partial(generate_static_file, template_adapter=Jinja2Template)