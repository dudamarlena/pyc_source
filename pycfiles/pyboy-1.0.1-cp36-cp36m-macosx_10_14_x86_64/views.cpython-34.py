# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\app\core\views.py
# Compiled at: 2015-08-20 10:37:20
# Size of source mod 2**32: 547 bytes
__doc__ = 'core\x0biews.py: This file contains the main views.'
__author__ = 'dan'
from flask import send_from_directory, render_template
from os.path import join
from . import core

@core.route('/')
def index():
    post = render_template('widgets/post.html')
    return render_template('index.html', author='Dan Wolf', post=post)


@core.route('/favicon.ico')
def favicon():
    return send_from_directory(join(core.root_path, 'static', 'images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')