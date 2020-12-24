# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/ablog_api/ablog_api/login.py
# Compiled at: 2016-08-24 12:22:33
# Size of source mod 2**32: 2560 bytes
"""
    Module ablog_api.login
"""
import os, json
from flask import request, abort
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required

class Login:

    def __init__(self, app, base_url='/'):
        if base_url[(-1)] != '/':
            base_url = base_url + '/'
        self.login_manager = LoginManager()
        self.login_manager.init_app(app)

        class User:
            __doc__ = ' class of User, for login'

            def __init__(self, username):
                self.username = username

            def check_password(self, password):
                if self.username in [i['username'] for i in app.config['USERS']]:
                    if [i['password'] for i in app.config['USERS'] if i['username'] == self.username][0] == password:
                        return True
                return False

            def is_authenticated(self):
                return True

            def is_active(self):
                return True

            def is_anonymous(self):
                return False

            def get_id(self):
                return [i['id'] for i in app.config['USERS'] if i['username'] == self.username][0]

            def __repr__(self):
                return '<User %r>' % self.username

        @self.login_manager.unauthorized_handler
        def unauthorized():
            return abort(401)

        @self.login_manager.user_loader
        def load_user(id):
            return User([i['username'] for i in app.config['USERS'] if i['id'] == id][0])

        @app.route('%slogin' % base_url, methods=['POST'])
        @app.doc.doc()
        @app.trace
        def login():
            """
            Logs a user in
            
            **param:**

            - username
            - password
            """
            data = json.loads(request.data.decode())
            username = data['username']
            password = data['password']
            registered_user = User(username)
            if registered_user.check_password(password):
                login_user(registered_user, remember=True)
                data['status'] = 'login'
                return json.dumps(data)
            return abort(401)

        @app.route('%slogout' % base_url)
        def logout():
            logout_user()
            return 'logout'