# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /django/.envs/simpletickets/local/lib/python2.7/site-packages/simpletickets/helpers.py
# Compiled at: 2016-10-01 08:49:43
import os
from .settings import ST_ATTACHMENTS, ST_ATTACH_URL, MONITOR_FILES_DIR

def monitorfile_url(ticket):
    return ST_ATTACH_URL + ('{id}-{user}.mon').format(id=ticket.id, user=ticket.user)


def monitorfile(ticket):
    return os.path.join(ST_ATTACHMENTS, MONITOR_FILES_DIR, ('{id}-{user}.mon').format(id=ticket.id, user=ticket.user))


def monitor(myfilename, msg):
    with open(myfilename, 'a') as (monitor):
        monitor.write(msg)