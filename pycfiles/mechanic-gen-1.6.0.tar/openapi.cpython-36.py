# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zackschrag/fctn/mechanic/mechanic/openapi.py
# Compiled at: 2018-03-26 10:46:42
# Size of source mod 2**32: 825 bytes
import os, yaml, flask
openapi_blueprint = flask.Blueprint('mechanic', __name__, template_folder='templates',
  static_folder='static',
  static_url_path='/static/mechanic')

@openapi_blueprint.route('/openapi')
def openapi():
    with open(os.path.abspath(os.path.curdir) + '/openapi.yaml') as (f):
        contents = f.read()
        yaml_contents = yaml.load(contents)
    return flask.render_template('swagger-ui-index.html', title=(yaml_contents.get('info', {}).get('title', 'Swagger UI')))


@openapi_blueprint.route('/openapi.yaml')
def openapi_docs():
    with open(os.path.abspath(os.path.curdir) + '/openapi.yaml') as (f):
        contents = f.read()
    return flask.render_template_string(contents)