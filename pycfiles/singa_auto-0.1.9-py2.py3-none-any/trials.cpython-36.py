# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/admin/view/trials.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 2955 bytes
import pickle
from singa_auto.constants import UserType, RequestsParameters
from flask import jsonify, Blueprint, make_response, g
from singa_auto.utils.auth import auth
from singa_auto.utils.requests_params import param_check
trial_bp = Blueprint('trial', __name__)

@trial_bp.route('/trials/<trial_id>/logs', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
def get_trial_logs(auth, trial_id):
    admin = g.admin
    with admin:
        return jsonify(admin.get_trial_logs(trial_id))


@trial_bp.route('/trials/<trial_id>/parameters', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
def get_trial_parameters(auth, trial_id):
    admin = g.admin
    with admin:
        trial_params = admin.get_trial_parameters(trial_id)
    trial_params = pickle.dumps(trial_params)
    res = make_response(trial_params)
    res.headers.set('Content-Type', 'application/octet-stream')
    return res


@trial_bp.route('/trials/<trial_id>', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
def get_trial(auth, trial_id):
    admin = g.admin
    with admin:
        return jsonify(admin.get_trial(trial_id))


@trial_bp.route('/train_jobs/<app>/<app_version>/trials', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check(required_parameters=(RequestsParameters.TRIAL_GET_BEST))
def get_trials_of_train_job(auth, app, app_version, params):
    admin = g.admin
    max_count = int(params['max_count']) if 'max_count' in params else 2
    with admin:
        if params.get('type') == 'best':
            return jsonify(admin.get_best_trials_of_train_job(user_id=(auth['user_id']), app=app, app_version=(int(app_version)), max_count=max_count))
        else:
            return jsonify(admin.get_trials_of_train_job(user_id=(auth['user_id']), app=app, app_version=(int(app_version)), max_count=max_count))