# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ui/views.py
# Compiled at: 2017-09-08 11:38:51
# Size of source mod 2**32: 1028 bytes
from django.http import HttpResponse
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket
from bamb import Bamb
from domain import user
from common import constants

@accept_websocket
def simple_websocket_client(request):
    if not request.is_websocket():
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'ui/websocket.html')

    else:
        acc = request.GET['account']
        um = Bamb.bean(constants.SERVICE_USER_MANAGER)
        if len(acc) > 0:
            u = user.User(acc, client=request.websocket)
            um.user_login(u)
        users = um.online_users
        for message in request.websocket:
            for k, u in users.items():
                ws = u.client_object
                if ws is not None:
                    if not ws.closed:
                        ws.send(message)