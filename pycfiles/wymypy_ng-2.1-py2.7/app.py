# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/app.py
# Compiled at: 2013-12-03 16:52:19
import ConfigParser
from functools import wraps
import json
from flask import Flask, render_template, request, abort, Response
from wymypy.libs.mpdsafe import MpdSafe
app = Flask(__name__)
config = ConfigParser.SafeConfigParser()
mpd = MpdSafe()
plugins = []

def requires_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if config.has_option('auth', 'enabled') and config.getboolean('auth', 'enabled'):
            auth = request.authorization
            if not auth or not (auth.username == config.get('auth', 'username') and auth.password == config.get('auth', 'password')):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)

    return decorated


@app.route('/')
@requires_auth
def root():
    return render_template('main.html', player=plugins['player'].index(), player_playlist=plugins['player'].playlist(), player_stream=config.get('mpd', 'stream') if config.has_option('mpd', 'stream') else None, plugins=sorted(plugins.values(), key=lambda plugin: plugin.button_index))


@app.route('/player')
@requires_auth
def player():
    return render_template('player.html')


@app.route('/plugin/<plugin>', methods=['GET', 'POST'])
@app.route('/plugin/<plugin>/<method>', methods=['GET', 'POST'])
@requires_auth
def plugin_methods(plugin, method=None):
    inst = plugins[plugin.lower()]
    args = request.form.to_dict()
    if method is None:
        method = 'index'
    if hasattr(inst, method):
        return app.make_response(getattr(inst, method)(**args))
    else:
        abort(404)
        return


@app.route('/__ajax/<method>', methods=['GET', 'POST'])
@app.route('/__ajax/<plugin>/<method>', methods=['GET', 'POST'])
@requires_auth
def ajax_methods(method, plugin=None):
    if plugin is None:
        abort(404)
    inst = plugins[plugin.lower()]
    args = request.form.to_dict()
    if hasattr(inst, 'ajax_' + method):
        response = app.make_response(json.dumps(getattr(inst, 'ajax_' + method)(**args)))
        response.headers['Cache-Control'] = 'no-cache'
        return response
    else:
        abort(404)
        return