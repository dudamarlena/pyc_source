# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo89/mogo/mqueue/hooks/redis/serializer.py
# Compiled at: 2017-09-27 04:58:51
# Size of source mod 2**32: 832 bytes


def Pack(event):
    sep = '#!#'
    data = ['name:;' + event.name]
    if event.event_class:
        data.append('event_class:;' + event.event_class)
    if event.content_type:
        data.append('content_type:;' + str(event.content_type))
    if event.obj_pk:
        data.append('obj_pk:;' + str(event.obj_pk))
    if event.user:
        data.append('user:;' + str(event.user))
    if event.url:
        data.append('url:;' + event.url)
    if event.admin_url:
        data.append('admin_url:;' + event.admin_url)
    if event.notes:
        data.append('notes:;' + str(event.notes))
    if event.request:
        data.append('request:;' + event.request)
    if event.bucket:
        data.append('bucket:;' + event.bucket)
    if event.data or event.data != {}:
        data.append('data:;' + str(event.data))
    d = str.join(sep, data)
    return d