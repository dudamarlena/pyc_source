# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/install/views.py
# Compiled at: 2017-05-05 09:03:28
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask import Blueprint, render_template, redirect, request, current_app as app, g, flash, url_for
from flask.ext.login import login_required
from onyxbabel import gettext
from onyx.extensions import db, login_manager
from onyx.core.models import *
from onyx.api.exceptions import *
from onyx.api.options import *
from onyx.config import get_config, get_path
from onyx.api.install import Install
import onyx, os
options = Options()
installation = Install()
install = Blueprint('install', __name__, url_prefix='/', template_folder='templates')

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))


@install.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('install/index.html')
    if request.method == 'POST':
        try:
            installation.username = request.form['username']
            installation.password = request.form['password']
            installation.email = request.form['email']
            installation.set()
            flash(gettext('Onyx is installed !'), 'success')
            return redirect(url_for('install.finish'))
        except Exception as e:
            flash(gettext('An error has occured !'), 'error')
            return redirect(url_for('install.index'))


@install.route('get_data')
def data():
    try:
        installation.get_data()
        return 'Done'
    except Exception as e:
        return 'Error'


@install.route('reboot')
def reboot():
    try:
        os.system('sudo pm2 restart onyx-client')
        return redirect(url_for('core.index'))
    except:
        return redirect(url_for('install.finish'))


@install.route('change_lang', methods=['POST'])
def change_lang():
    try:
        options.lang = request.form.get('lang')
        options.change_lang()
        os.system('sudo pm2 restart onyx-client')
        flash(gettext('The lang was changed ! If not please reboot Onyx'), 'success')
        return redirect(url_for('install.index'))
    except:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('install.index'))


@install.route('finish')
@login_required
def finish():
    print app.config('INSTALL')
    return render_template('install/finish.html')