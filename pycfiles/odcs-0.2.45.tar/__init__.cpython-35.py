# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/__init__.py
# Compiled at: 2017-09-21 02:38:08
# Size of source mod 2**32: 3119 bytes
from logging import getLogger
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import BadRequest
from odcs.server.logger import init_logging
from odcs.server.config import init_config
from odcs.server.proxy import ReverseProxy
from odcs.server.errors import NotFound, Unauthorized, Forbidden
app = Flask(__name__)
app.wsgi_app = ReverseProxy(app.wsgi_app)
db = SQLAlchemy(app)
conf = init_config(app)
init_logging(conf)
log = getLogger(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
from odcs.server import views
from odcs.server.auth import init_auth
init_auth(login_manager, conf.auth_backend)

def json_error(status, error, message):
    response = jsonify({'status': status, 
     'error': error, 
     'message': message})
    response.status_code = status
    return response


@app.errorhandler(NotFound)
def notfound_error(e):
    """Flask error handler for NotFound exceptions"""
    return json_error(404, 'Not Found', e.args[0])


@app.errorhandler(Unauthorized)
def unauthorized_error(e):
    """Flask error handler for Unauthorized exceptions"""
    return json_error(401, 'Unauthorized', e.args[0])


@app.errorhandler(Forbidden)
def forbidden_error(e):
    """Flask error handler for Forbidden exceptions"""
    return json_error(403, 'Forbidden', e.args[0])


@app.errorhandler(ValueError)
def validationerror_error(e):
    """Flask error handler for ValueError exceptions"""
    return json_error(400, 'Bad Request', e.args[0])


@app.errorhandler(RuntimeError)
def runtimeerror_error(e):
    """Flask error handler for RuntimeError exceptions"""
    return json_error(500, 'Internal Server Error', e.args[0])


@app.errorhandler(BadRequest)
def badrequest_error(e):
    """Flask error handler for RuntimeError exceptions"""
    return json_error(e.code, 'Bad Request', e.get_description())