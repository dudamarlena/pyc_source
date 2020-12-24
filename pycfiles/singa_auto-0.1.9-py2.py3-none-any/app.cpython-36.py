# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/admin/app.py
# Compiled at: 2020-04-15 15:14:24
# Size of source mod 2**32: 2134 bytes
import traceback
from flask import Flask, g
from flask_cors import CORS
from singa_auto.admin import Admin
from singa_auto.admin.view.events import events_bp
from singa_auto.admin.view.inference_job import inference_bp
from singa_auto.admin.view.user import user_bp
from singa_auto.admin.view.datasets import dataset_bp
from singa_auto.admin.view.model import model_bp
from singa_auto.admin.view.train_jobs import trainjob_bp
from singa_auto.admin.view.trials import trial_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(dataset_bp, url_prefix='/datasets')
    app.register_blueprint(model_bp, url_prefix='/models')
    app.register_blueprint(trainjob_bp, url_prefix='/train_jobs')
    app.register_blueprint(trial_bp)
    app.register_blueprint(inference_bp, url_prefix='/inference_jobs')
    app.register_blueprint(events_bp)
    CORS(app)
    print('finish creating app')

    @app.before_request
    def requests_context():
        print(hasattr(g, 'admin'))
        if not hasattr(g, 'admin'):
            g.admin = Admin()

    @app.route('/')
    def index():
        return 'Singa-Auto Admin is up.'

    @app.errorhandler(Exception)
    def handle_error(error):
        traceback.print_exc()
        return (traceback.format_exc(), 500)

    return app