# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/base/views/OptionsController.py
# Compiled at: 2017-04-26 15:38:59
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import core
import os, sys
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from onyx.decorators import admin_required
from onyx.api.navbar import *
from onyx.api.options import *
from onyx.api.server import *
from onyx.api.exceptions import *
from onyx.api.install import Install
from werkzeug._reloader import *
reloader = ReloaderLoop()
install = Install()
option = Options()
server = Server()

@core.route('options', methods=['GET', 'POST'])
@login_required
def options():
    if request.method == 'GET':
        return render_template('options/index.html')
    else:
        if request.method == 'POST':
            try:
                option.user = current_user.id
                if request.form.get('color') == None:
                    option.color = current_user.buttonColor
                else:
                    option.color = request.form.get('color')
                option.set_account()
                flash(gettext('Account changed successfully'), 'success')
                return redirect(url_for('core.options'))
            except OptionsException:
                flash(gettext('An error has occured'), 'error')
                return redirect(url_for('core.options'))

        return


@core.route('change_lang', methods=['POST'])
@admin_required
@login_required
def change_lang():
    try:
        option.lang = request.form.get('lang')
        option.change_lang()
        flash(gettext('Please reboot Onyx to change language'), 'success')
        return redirect(url_for('core.options'))
    except OptionsException:
        flash(gettext('An error has occured'), 'error')
        return redirect(url_for('core.options'))


@core.route('shutdown')
@admin_required
@login_required
def shutdown():
    try:
        server.shutdown()
        return render_template('options/close.html')
    except ServerException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.index'))


@core.route('reboot')
@login_required
def reboot():
    try:
        os.system('sudo pm2 restart 0')
        return redirect(url_for('core.index'))
    except:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.index'))


@core.route('maj')
@admin_required
@login_required
def maj():
    try:
        server.update()
        flash(gettext('Onyx is now upgrade !'), 'success')
        return redirect(url_for('core.options'))
    except ServerException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.options'))


@core.route('data/update')
@admin_required
@login_required
def update_data_git():
    try:
        install.update_data()
        flash(gettext('Data Modified'), 'success')
        return redirect(url_for('core.options'))
    except DataException:
        flash(gettext('An errorhas occured'), 'error')
        return redirect(url_for('core.options'))