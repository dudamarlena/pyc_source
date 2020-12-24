# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/admin/view/user.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 3182 bytes
from datetime import datetime
from singa_auto.constants import UserType, RequestsParameters
from flask import Blueprint, jsonify, g
from singa_auto.utils.auth import UnauthorizedError, generate_token, auth
from singa_auto.utils.requests_params import param_check
user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
@auth([UserType.ADMIN])
@param_check(required_parameters=(RequestsParameters.USER_CREATE))
def create_user(auth, params):
    admin = g.admin
    if auth['user_type'] != UserType.SUPERADMIN:
        if params['user_type'] in [UserType.ADMIN, UserType.SUPERADMIN]:
            raise UnauthorizedError()
    with admin:
        return jsonify(admin.create_user(email=(params['email']), password=(params['password']),
          user_type=(params['user_type'])))


@user_bp.route('/users', methods=['GET'])
@auth([UserType.ADMIN])
def get_users(auth):
    admin = g.admin
    with admin:
        return jsonify(admin.get_users())


@user_bp.route('/users', methods=['DELETE'])
@auth([UserType.ADMIN])
@param_check(required_parameters=(RequestsParameters.USER_BAN))
def ban_user(auth, params):
    admin = g.admin
    with admin:
        user = admin.get_user_by_email(params['email'])
        if user is not None:
            if auth['user_type'] != UserType.SUPERADMIN:
                if user['user_type'] in [UserType.ADMIN, UserType.SUPERADMIN]:
                    raise UnauthorizedError()
            if auth['user_id'] == user['id']:
                raise UnauthorizedError()
        return jsonify(admin.ban_user(email=(params['email'])))


@user_bp.route('/tokens', methods=['POST'])
@param_check(required_parameters=(RequestsParameters.TOKEN))
def generate_user_token(params):
    admin = g.admin
    with admin:
        user = (admin.authenticate_user)(**params)
    if user.get('banned_date') is not None:
        if datetime.now() > user.get('banned_date'):
            raise UnauthorizedError('User is banned')
    token = generate_token(user)
    return jsonify({'user_id':user['id'], 
     'user_type':user['user_type'], 
     'token':token})