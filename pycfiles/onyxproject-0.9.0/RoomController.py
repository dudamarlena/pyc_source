# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/base/views/RoomController.py
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
from onyx.api.exceptions import *
from onyx.decorators import admin_required
from onyx.api.room import *
from onyxbabel import gettext
room = Room()

@core.route('room/add', methods=['POST'])
@admin_required
@login_required
def add_room():
    try:
        room.name = request.form['name']
        room.house = request.form.get('house')
        room.add()
        flash(gettext('Room Add'), 'success')
        return redirect(url_for('core.options'))
    except RoomException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.options'))


@core.route('room/delete/<int:id>')
@admin_required
@login_required
def delete_room(id):
    try:
        room.id = id
        room.delete()
        flash(gettext('Room Deleted'), 'success')
        return redirect(url_for('core.options'))
    except RoomException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.options'))