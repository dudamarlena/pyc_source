# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/actions/views/Scenario.py
# Compiled at: 2017-04-03 03:04:28
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.exceptions import *
from onyxbabel import gettext
from flask_login import current_user
from onyx.api.notification import *
from onyx.api.assets import Json
from onyx.api.events import *
from .. import action
events = Event()
json = Json()
notif = Notification()

@action.route('notification')
def notification(param):
    json.json = param
    params = json.decode()
    notif.user = current_user.id
    notif.title = params[0]
    notif.text = params[1]
    notif.priority = params[2]
    notif.icon = params[3]
    notif.icon_color = params[4]
    notif.user = params[5]
    notif.notify()
    return 'Done'


@action.route('event')
def event(param):
    json.json = param
    params = json.decode()
    events.code = params[0]
    events.new()
    return json.encode({'status': 'success'})