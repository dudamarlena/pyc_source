# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\administrator\pycharmprojects\airtest_for_h9\airtest\webgui\routers\home.py
# Compiled at: 2014-12-03 20:37:50
import flask
from . import utils
bp = flask.Blueprint('home', __name__)

@bp.route('/tmp/<path:path>')
def static_proxy(path):
    return flask.send_from_directory(utils.TMPDIR, path)


@bp.route('/')
def home():
    return flask.render_template('index.html')