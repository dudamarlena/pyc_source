# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/app/controller/backend/IndexController.py
# Compiled at: 2016-07-15 00:10:26
import time
from flask import redirect, request, session, escape, render_template
from . import ADMIN_URL
from app import web, db
from app.CommonClass.ValidateClass import ValidateClass
from app.models import CobraAdminUser
__author__ = 'lightless'
__email__ = 'root@lightless.me'

@web.route(ADMIN_URL + '/', methods=['GET'])
@web.route(ADMIN_URL + '/index', methods=['GET', 'POST'])
def index():
    if ValidateClass.check_login():
        return redirect(ADMIN_URL + '/main')
    if request.method == 'POST':
        vc = ValidateClass(request, 'username', 'password')
        ret, msg = vc.check_args()
        if not ret:
            return msg
        au = CobraAdminUser.query.filter_by(username=vc.vars.username).first()
        if not au or not au.verify_password(vc.vars.password):
            return 'Wrong username or password.'
        session['role'] = au.role
        session['username'] = escape(au.username)
        session['is_login'] = True
        current_time = time.strftime('%Y-%m-%d %X', time.localtime())
        au.last_login_time = current_time
        au.last_login_ip = request.remote_addr
        db.session.add(au)
        db.session.commit()
        return 'Login success, jumping...<br /><script>window.setTimeout("location=\'main\'", 1000);</script>'
    else:
        return render_template('backend/index/index.html')


@web.route(ADMIN_URL + '/main', methods=['GET'])
def main():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    else:
        return render_template('backend/index/main.html')