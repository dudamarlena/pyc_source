# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-bluelogin/flask_bluelogin/controllers/login_controller.py
# Compiled at: 2017-04-30 09:41:53
# Size of source mod 2**32: 1545 bytes
import json
from flask import request, current_app
from flask_login import login_user
from ..models.error_model import ErrorModel
from ..models.user import User, Users
from ..util import NotFoundUserError, EchecAuthentification, Unauthorized, Error, to_json

@to_json
def login():
    """
    autentification
    Returns user authentified

    :rtype: User
    """
    try:
        data = json.loads(request.data.decode())
        current_app.logger.error(data)
        user = Users().get_user(id=(data['id']))
        if user.check_password(data['password']):
            login_user(user, remember=True)
            current_app.logger.error('check')
            return user
    except Error as e:
        pass

    return Unauthorized()


@to_json
def logout():
    """
    logout autentification
    Returns user authentified

    :rtype: User
    """
    pass


@to_json
def get_user(userId):
    """
    Find user by ID
    Returns a user
    :param userId: ID of userr that needs to be fetched
    :type userId: str

    :rtype: User
    """
    pass


@to_json
def set_user(userId):
    """
    Updates a user with form data
    update user by Id
    :param userId: ID of user that needs to be updated
    :type userId: str
    :param body: User object that needs to be updated
    :type body: dict | bytes

    :rtype: None
    """
    data = json.loads(request.data.decode())


@to_json
def add_user():
    """
    add user
    Returns user created

    :rtype: User
    """
    data = json.loads(request.data.decode())