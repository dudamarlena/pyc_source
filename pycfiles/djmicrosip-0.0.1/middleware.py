# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Admin\Documents\GitHub\djmicrosip\djmicrosip\core\middleware.py
# Compiled at: 2015-01-28 22:11:26
from threading import local
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
my_local_global = local()

class Middleware(object):

    def process_request(self, request):
        my_local_global.database_name, my_local_global.conexion_activa = get_database_name(request)


def get_database_name(request):
    session_key = request.session.session_key
    try:
        session = Session.objects.get(session_key=session_key)
    except:
        return (None, None)

    uid = session.get_decoded().get('_auth_user_id')
    if uid:
        selected_database = None
        conexion_activa = None
        if 'selected_database' in request.session:
            selected_database = request.session['selected_database']
        if 'conexion_activa' in request.session:
            conexion_activa = request.session['conexion_activa']
        return (selected_database, conexion_activa)
    else:
        return (None, None)
        return