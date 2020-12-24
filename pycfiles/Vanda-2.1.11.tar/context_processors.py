# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/apps/dashboard/context_processors.py
# Compiled at: 2013-01-07 03:52:15
from base import dashboard as DASHBOARD

def dashboard(request):
    if request.user.is_authenticated():
        DASHBOARD.load_user_data(request.user)
    return {'dashboard': DASHBOARD}