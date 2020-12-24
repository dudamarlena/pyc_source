# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/anand/github/anandology/mockdown/mockdown/__init__.py
# Compiled at: 2016-08-19 06:38:54
"""
   Mocker
   ~~~~~~

   Tool to simplify creating HTML mockups.
"""
import os, sys, glob, hashlib
from StringIO import StringIO
from flask import Flask, Blueprint, render_template, make_response, abort, redirect, url_for, send_from_directory
import yaml, pathlib
from .mockdown import Mockdown
mockdown_app = Blueprint('mockdown', __name__, template_folder='templates')
_mockdown = Mockdown(root='.')

def mockdown_url_for(endpoint, **kwargs):
    if endpoint == 'static':
        return url_for('static', **kwargs)
    else:
        return url_for('.mock', path=endpoint + '.html')


_mockdown.template_globals['url_for'] = mockdown_url_for

@mockdown_app.route('/')
@mockdown_app.route('/<path:path>')
def mock(path=''):
    if not _mockdown.exists(path):
        abort(404)
    else:
        if _mockdown.is_dir(path):
            return mock_index(path)
        if path.endswith('.html'):
            return _mockdown.render_template(path)
        if path.endswith('.yml'):
            data = _mockdown.read_yaml_file(path)
            return yaml.dump(data)
        print 'aborting...'
        abort(404)


def mock_index(path):
    if path and not path.endswith('/'):
        return redirect('/' + path + '/')
    root = pathlib.Path(_mockdown.root).name
    pathobj = pathlib.Path(_mockdown.root, path)
    subdirs = [ p.name for p in pathobj.iterdir() if p.is_dir() ]
    filenames = [ f.name for f in pathobj.glob('*.html') ] + [ f.name for f in pathobj.glob('*.yml') ]
    return render_template('index.html', root=root, path=path, subdirs=subdirs, filenames=filenames)


@mockdown_app.route('/static2/<path:filename>')
def base_static(filename):
    path = os.getcwd() + '/static/'
    return send_from_directory(path, filename)


def main():
    if len(sys.argv) > 1:
        _mockdown.root = sys.argv[1]
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.register_blueprint(mockdown_app)
    app.run()