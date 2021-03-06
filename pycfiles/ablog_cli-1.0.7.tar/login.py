# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ablog_api/login.py
# Compiled at: 2016-08-24 12:22:33
__doc__ = '\n    Module ablog_api.login\n'
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
            """ class of User, for login"""

            def __init__(self, username):
                self.username = username

            def check_password(self, password):
                if self.username in [ i['username'] for i in app.config['USERS'] ]:
                    if [ i['password'] for i in app.config['USERS'] if i['username'] == self.username ][0] == password:
                        return True
                return False

            def is_authenticated(self):
                return True

            def is_active(self):
                return True

            def is_anonymous(self):
                return False

            def get_id(self):
                return [ i['id'] for i in app.config['USERS'] if i['username'] == self.username ][0]

            def __repr__(self):
                return '<User %r>' % self.username

        @self.login_manager.unauthorized_handler
        def unauthorized():
            return abort(401)

        @self.login_manager.user_loader
        def load_user(id):
            return User([ i['username'] for i in app.config['USERS'] if i['id'] == id ][0])

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