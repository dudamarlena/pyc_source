# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/base/views/NotificationController.py
# Compiled at: 2017-04-27 17:01:41
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
from onyxbabel import gettext
from flask.ext.login import login_required, current_user
from onyx.api.exceptions import *
from onyx.api.notification import *
notif = Notification()

@core.route('notifications')
@login_required
def notifications():
    notif.user = current_user.id
    notif.mark_read()
    return render_template('notifications/index.html')


@core.route('notifications/delete/<int:id>')
@login_required
def delete_notifications(id):
    try:
        notif.id = id
        notif.user = current_user.id
        notif.delete()
        return redirect(url_for('core.notifications'))
    except NotifException:
        flash(gettext('An error has occured'), 'error')
        return redirect(url_for('core.notifications'))