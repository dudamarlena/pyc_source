# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/widgets/views/Calendar.py
# Compiled at: 2017-04-02 16:32:59
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
from onyx.api.assets import Json
from flask.ext.login import current_user
from .. import widgets
from flask import render_template
from onyx.api.calendar import *
events = Calendar()
json = Json()

@widgets.route('calendar')
def calendar():
    events.user = current_user.id
    json.json = events.get()
    events_list = json.decode()
    return render_template('widgets/calendar.html', events=events_list)


@widgets.context_processor
def utility_processor():

    def split(str):
        return str.split(' ')

    return dict(split=split)