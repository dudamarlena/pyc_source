# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\api.py
# Compiled at: 2015-01-11 14:47:47
from chatpy.binder import bind_api
from chatpy.parsers import ModelParser

class API(object):
    """Chatwork API"""

    def __init__(self, auth_handler=None, host='api.chatwork.com', cache=None, secure=True, api_root='/v1', retry_count=0, retry_delay=0, retry_errors=None, timeout=60, parser=None, compression=False):
        self.auth = auth_handler
        self.host = host
        self.api_root = api_root
        self.cache = cache
        self.secure = secure
        self.compression = compression
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.timeout = timeout
        self.parser = parser or ModelParser()

    me = bind_api(path='/me', payload_type='my_account')
    status = bind_api(path='/my/status', payload_type='status')
    tasks = bind_api(path='/my/tasks', payload_type='task', payload_list=True)
    contacts = bind_api(path='/contacts', payload_type='account', payload_list=True)
    rooms = bind_api(path='/rooms', payload_type='room', payload_list=True)
    create_room = bind_api(path='/rooms', method='POST', allowed_param=[
     'description', 'icon_preset', 'members_admin_ids', 'members_member_ids', 'members_readonly_ids',
     'name'])
    get_room = bind_api(path='/rooms/{room_id}', payload_type='room', allowed_param=[
     'room_id'])
    change_room = bind_api(path='/rooms/{room_id}', method='PUT', allowed_param=[
     'description', 'icon_preset', 'name'])
    delete_room = bind_api(path='/rooms/{room_id}', method='DELETE', allowed_param=[
     'room_id', 'action_type'])
    get_members = bind_api(path='/rooms/{room_id}/members', payload_type='account', payload_list=True, allowed_param=[
     'room_id'])
    change_room_members = bind_api(path='/rooms/{room_id}/members', method='PUT', allowed_param=[
     'members_admin_ids', 'members_member_ids', 'members_readonly_ids'])
    messages = bind_api(path='/rooms/{room_id}/messages', method='GET', allowed_param=[
     'force'], payload_type='message', payload_list=True)
    post_message = bind_api(path='/rooms/{room_id}/messages', method='POST', allowed_param=[
     'room_id', 'body'])
    room_tasks = bind_api(path='/rooms/{room_id}/tasks', payload_type='task', payload_list=True, allowed_param=[
     'room_id'])
    post_tasks = bind_api(path='/rooms/{room_id}/tasks', method='POST', payload_type='task', allowed_param=[
     'room_id', 'body', 'to_ids', 'limit'])
    get_task = bind_api(path='/rooms/{room_id}/tasks/{task_id}', payload_type='task', allowed_param=[
     'room_id', 'task_id'])
    files = bind_api(path='/rooms/{room_id}/files', payload_type='attachment', payload_list=True, allowed_param=[
     'room_id'])
    get_file = bind_api(path='/rooms/{room_id}/files/{file_id}', payload_type='attachment', allowed_param=[
     'room_id', 'file_id'])