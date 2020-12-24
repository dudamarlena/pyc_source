# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/admin/view/datasets.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 3237 bytes
import tempfile
from singa_auto.constants import UserType, RequestsParameters
from flask import request, jsonify, Blueprint, g
from singa_auto.utils.auth import auth
from singa_auto.utils.requests_params import param_check
dataset_bp = Blueprint('datasets', __name__)

@dataset_bp.route('', methods=['POST'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check(required_parameters=(RequestsParameters.DATASET_POST))
def create_dataset(auth, params):
    admin = g.admin
    print('params', params)
    with tempfile.NamedTemporaryFile() as (f):
        if 'dataset' in request.files:
            file_storage = request.files['dataset']
            file_storage.save(f.name)
            file_storage.close()
        else:
            assert 'dataset_url' in params
            r = request.get((params['dataset_url']), allow_redirects=True)
            f.write(r.content)
            del params['dataset_url']
        params['data_file_path'] = f.name
        with admin:
            return jsonify(admin.create_dataset(user_id=(auth['user_id']), name=(params['name']), task=(params['task']),
              data_file_path=(params['data_file_path'])))


@dataset_bp.route('', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check()
def get_datasets(auth, params):
    admin = g.admin
    if 'task' in params:
        task = params['task']
    else:
        task = None
    with admin:
        return jsonify(admin.get_datasets((auth['user_id']), task=task))


@dataset_bp.route('/datasets/<id>', methods=['DELETE'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check()
def del_dataset(auth, id, params):
    admin = g.admin
    with admin:
        return jsonify((admin.del_datasets)((auth['user_id']), id, **params))


@dataset_bp.route('/datasets/<id>', methods=['GET'])
@auth([UserType.ADMIN, UserType.MODEL_DEVELOPER, UserType.APP_DEVELOPER])
@param_check()
def get_dataset(auth, id, params):
    admin = g.admin
    with admin:
        return jsonify((admin.get_dataset_by_id)((auth['user_id']), id, **params))