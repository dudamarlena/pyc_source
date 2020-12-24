# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/routes.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 710 bytes
from flask import request, redirect
from .message import create_message_for_user
from .tasks import send_message_to_bot

def _hook(chat_id, hash):
    if not request.is_json:
        return ('Data must be in json format', 400)
    else:
        json_obj = request.get_json(cache=False)
        msg = create_message_for_user(request.headers, json_obj)
        send_message_to_bot.delay(chat_id, msg)
        return ('OK', 200)


def _root():
    return redirect('http://t.me/catch_web_hook_bot', code=302)


def register_routes(app):

    @app.route('/hooks/<chat_id>/<hash>', methods=['POST'])
    def hook(chat_id, hash):
        return _hook(chat_id, hash)

    @app.route('/', methods=['GET'])
    def root():
        return _root()