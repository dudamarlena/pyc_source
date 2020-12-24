# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/channels/group.py
# Compiled at: 2012-02-14 23:34:00
from django.db import transaction
from booki.editor import models
from booki.utils import security

def remote_get_status_messages(request, message, groupid):
    from booki.statusnet.models import searchMessages
    group = models.BookiGroup.objects.get(url_name=groupid)
    mess = searchMessages('%%23%s' % group.url_name)
    messages = [ '<a href="http://status.flossmanuals.net/notice/%s">%s: %s</a>' % (m['id'], m['from_user'], m['text']) for m in mess['results'] ]
    return {'list': messages}


def remote_init_group(request, message, groupid):
    import sputnik
    try:
        _onlineUsers = sputnik.smembers('sputnik:channel:%s:users' % message['channel'])
    except:
        _onlineUsers = []

    if request.user.username not in _onlineUsers:
        try:
            sputnik.sadd('sputnik:channel:%s:users' % message['channel'], request.user.username)
        except:
            pass

    return {}


def remote_leave_group(request, message, groupid):
    group = models.BookiGroup.objects.get(url_name=groupid)
    group.members.remove(request.user)
    transaction.commit()
    return {'result': True}


def remote_join_group(request, message, groupid):
    group = models.BookiGroup.objects.get(url_name=groupid)
    group.members.add(request.user)
    transaction.commit()
    return {'result': True}