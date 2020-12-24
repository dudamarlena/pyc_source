# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/admin/view/inference_job.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 4225 bytes
from singa_auto.constants import UserType, RequestsParameters, InferenceBudgetOption
from flask import jsonify, Blueprint, g
from singa_auto.utils.auth import UnauthorizedError, auth
from singa_auto.utils.requests_params import param_check
inference_bp = Blueprint('inference', __name__)

@inference_bp.route('', methods=['POST'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check(required_parameters=(RequestsParameters.INFERENCE_CREATE))
def create_inference_job(auth, params):
    admin = g.admin
    budget = params['budget'] if 'budget' in params else {}
    budget = {**{InferenceBudgetOption.GPU_COUNT: 0}, **budget}
    if 'app_version' in params:
        app_version = int(params['app_version'])
    else:
        app_version = -1
    with admin:
        return jsonify(admin.create_inference_job(user_id=(auth['user_id']), app=(params['app']),
          app_version=app_version,
          budget=budget))


@inference_bp.route('/checkpoint', methods=['POST'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check(required_parameters=(RequestsParameters.INFERENCE_CREATEBY_CHECKOUTPOINT))
def create_inference_job_by_checkpoint(auth, params):
    admin = g.admin
    budget = params['budget'] if 'budget' in params else {}
    budget = {**{InferenceBudgetOption.GPU_COUNT: 0}, **budget}
    with admin:
        return jsonify(admin.create_inference_job_by_checkpoint(user_id=(auth['user_id']), budget=budget,
          model_name=(params['model_name'])))


@inference_bp.route('', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check(required_parameters=(RequestsParameters.INFERENCE_GETBY_USER))
def get_inference_jobs_by_user(auth, params):
    admin = g.admin
    assert 'user_id' in params
    if auth['user_type'] in [UserType.APP_DEVELOPER, UserType.MODEL_DEVELOPER]:
        if auth['user_id'] != params['user_id']:
            raise UnauthorizedError()
    with admin:
        return jsonify((admin.get_inference_jobs_by_user)(**params))


@inference_bp.route('/<app>', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
def get_inference_jobs_of_app(auth, app):
    admin = g.admin
    with admin:
        return jsonify(admin.get_inference_jobs_of_app(user_id=(auth['user_id']), app=app))


@inference_bp.route('/<app>/<app_version>', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
def get_running_inference_job(auth, app, app_version):
    admin = g.admin
    with admin:
        return jsonify(admin.get_running_inference_job((auth['user_id']), app, app_version=(int(app_version))))


@inference_bp.route('/<app>/<app_version>/stop', methods=['POST'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
def stop_inference_job(auth, app, app_version=-1):
    admin = g.admin
    with admin:
        return jsonify(admin.stop_inference_job((auth['user_id']), app, app_version=(int(app_version))))