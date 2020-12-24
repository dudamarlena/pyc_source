# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\workspace\mine\python\haf-webmanager\hafweb\route\route_token.py
# Compiled at: 2019-04-16 02:50:19
# Size of source mod 2**32: 2725 bytes
import hafweb.app as app
from haf.config import BANNER_STRS
from hafweb.generator import GeneratorHtml, GeneratorApi
from hafweb.controller.controller import *
from flask import request
from hafweb.error import *
import json

@app.route('/api/v1/token', methods=['GET', 'POST'])
def get_token() -> str:
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        if user_name:
            request_data = password or json.loads(request.data)
            user_name = request_data.get('username') or user_name
            password = request_data.get('password') or password
        elif request.method == 'GET':
            user_name = request.args.get('username')
            password = request.args.get('password')
        else:
            return GeneratorApi.genrate_api_pure('tokens', status=200)
    else:
        print(f"{user_name} -- {password}")
        return user_name and password or GeneratorApi.generate_error(ErrorHandler('get_token', '123456', status=401))
    all_users = ControllerToken.get_user_name_all()
    for user in all_users:
        if user.username == user_name:
            if user.password == password:
                return GeneratorApi.genrate_api_pure((user.token), status=200)
            return GeneratorApi.generate_error(ErrorHandler('get_token', 'password is wrong!', status=401))


@app.route('/api/v1/users/me', methods=['GET', 'POST'])
def get_user_me() -> str:
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        if user_name:
            request_data = password or json.loads(request.data)
            user_name = request_data.get('username') or user_name
            password = request_data.get('password') or password
        elif request.method == 'GET':
            user_name = request.args.get('username')
            password = request.args.get('password')
        else:
            return GeneratorApi.genrate_api_pure('tokens', status=200)
    else:
        print(f"{user_name} -- {password}")
        return user_name and password or GeneratorApi.generate_error(ErrorHandler('get_token', '123456', status=401))
    all_users = ControllerToken.get_user_name_all()
    for user in all_users:
        if user.username == user_name:
            if user.password == password:
                return GeneratorApi.genrate_api_pure((user.token), status=200)
            return GeneratorApi.generate_error(ErrorHandler('get_token', 'password is wrong!', status=401))