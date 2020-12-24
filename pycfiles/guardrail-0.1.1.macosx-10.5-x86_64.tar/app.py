# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jmcarp/miniconda/envs/guardian/lib/python2.7/site-packages/examples/flask_sqla/app.py
# Compiled at: 2015-04-05 12:07:54
import flask
from flask.ext.login import LoginManager
import models, fixtures, permissions
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager(app)
models.db.init_app(app)
with app.app_context():
    models.db.create_all()
fixtures.ensure(app)

@login_manager.user_loader
@login_manager.request_loader
def load_user_from_request(*args, **kwargs):
    return models.db.session.query(models.User).get(1)


@app.route('/posts/<id>/', methods=['GET'])
@permissions.has_post_permission('read')
def view_post(agent, target, **kwargs):
    return flask.jsonify(title=target.title, content=target.content)


@app.route('/posts/<id>/', methods=['PUT'])
@permissions.has_post_permission('write')
def edit_post(agent, target, **kwargs):
    data = flask.request.get_json()
    target.content = data['content']
    models.db.session.add(target)
    models.db.session.commit()
    return flask.jsonify(status='success')