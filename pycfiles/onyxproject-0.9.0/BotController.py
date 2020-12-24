# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/base/views/BotController.py
# Compiled at: 2017-04-27 09:14:54
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import core
from flask import render_template, request
from flask.ext.login import login_required
from onyx.api.bot import *
from onyx.api.assets import Json
json = Json()
kernel = Bot()

@core.route('bot', methods=['GET', 'POST'])
@login_required
def bot():
    if request.method == 'POST':
        try:
            kernel.text = request.form['text']
            result = kernel.get()
            json.json = result
            data = json.decode()
            if data['status'] == 'success':
                return data['text']
            if data['status'] == 'unknown command':
                return gettext('Unknown Command !')
            return gettext('An error has occured !')
        except:
            return gettext('An error has occured !')