# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/base/views/NavbarController.py
# Compiled at: 2017-03-29 12:18:51
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import core
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from onyx.decorators import admin_required
from onyxbabel import gettext
from onyx.api.navbar import Navbar
from onyx.api.exceptions import *
navbar = Navbar()

@core.route('navbar/update', methods=['POST'])
@login_required
def update_navbar():
    try:
        navbar.last = request.form['last']
        navbar.new = request.form['new']
        navbar.set_navbar()
        flash(gettext('Modified'), 'success')
        return redirect(url_for('core.options'))
    except NavbarException:
        flash(gettext('An error has occured'), 'error')
        return redirect(url_for('core.options'))