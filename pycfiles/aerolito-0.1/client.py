# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/api/client.py
# Compiled at: 2016-03-28 13:15:32
import io, requests
from future.utils import iteritems
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

VERSION_PREFIX = '/api/v1.3'
MAX_CHUNK_SIZE = 1048576

class APIClient(object):

    def __init__(self, instance_configuration, access_token):
        self.instance_configuration = instance_configuration
        self.access_token = access_token
        self.auth_headers = {'Authorization': ('Bearer {}').format(access_token), 
           'Content-Type': 'application/json', 
           'Endpoint-Consistency': 'strict'}
        self.url_prefix = ('https://{}{}').format(instance_configuration.hostname, VERSION_PREFIX)
        self.session = requests.Session()
        self.response_headers = None
        return

    def _handle_response(self, response):
        response.raise_for_status()
        self.response_headers = response.headers
        try:
            return response.json()
        except ValueError:
            return response.text or 'ok'

    def _do_delete(self, route, headers=None):
        if not headers:
            headers = self.auth_headers
        res = self.session.delete(('{}{}').format(self.url_prefix, route), headers=headers)
        return self._handle_response(res)

    def _do_get(self, route, headers=None):
        if not headers:
            headers = self.auth_headers
        res = self.session.get(('{}{}').format(self.url_prefix, route), headers=headers)
        return self._handle_response(res)

    def _do_post(self, route, data, headers=None):
        if not headers:
            headers = self.auth_headers
        res = self.session.post(('{}{}').format(self.url_prefix, route), json=data, headers=headers)
        return self._handle_response(res)

    def _do_put(self, route, data, serialize=True, headers=None):
        if not headers:
            headers = self.auth_headers
        url = ('{}{}').format(self.url_prefix, route)
        if serialize and data:
            res = self.session.put(url, json=data, headers=headers)
        else:
            headers = {k:v for k, v in iteritems(headers) if k != 'Content-Type' if k != 'Content-Type'}
            res = self.session.put(url, data=data, headers=headers)
        return self._handle_response(res)

    def get_users(self, limit=20, after=None, before=None):
        route = ('/users?limit={}').format(limit)
        if after:
            route += ('&after={}').format(after)
        if before:
            route += ('&before={}').format(before)
        return self._do_get(route)

    def get_user(self, email):
        route = ('/users/{}').format(email)
        return self._do_get(route)

    def create_user(self, email, first_name, last_name):
        route = '/users'
        data = {'email': email, 'first_name': first_name, 'last_name': last_name}
        return self._do_post(route, data)

    def update_user(self, email, first_name, last_name):
        route = ('/users/{}').format(email)
        data = {'email': email, 'first_name': first_name, 'last_name': last_name}
        return self._do_put(route, data)

    def delete_user(self, email):
        route = ('/users/{}').format(email)
        return self._do_delete(route)

    def update_user_password(self, email, password):
        route = ('/users/{}/password').format(email)
        data = ('"{}"').format(password)
        return self._do_put(route, data)

    def delete_user_password(self, email):
        route = ('/users/{}/password').format(email)
        return self._do_delete(route)

    def get_user_twofactor(self, email):
        route = ('/users/{}/two_factor').format(email)
        return self._do_get(route)

    def disable_user_twofactor(self, email):
        route = ('/users/{}/two_factor').format(email)
        return self._do_delete(route)

    def get_invitee(self, email):
        route = ('/invitees/{}').format(quote_plus(email))
        return self._do_get(route)

    def create_invitee(self, email_from, email_to):
        route = '/invitees'
        data = {'email_from': email_from, 'email_to': email_to}
        return self._do_post(route, data)

    def delete_invitee(self, email):
        route = ('/invitees/{}').format(quote_plus(email))
        return self._do_delete(route)

    def get_folder(self, folder_id, fields=None):
        route = ('/folders/{}').format(folder_id)
        if fields:
            route += ('?fields={}').format((',').join(fields))
        return self._do_get(route)

    def get_folder_path(self, folder_id):
        route = ('/folders/{}/path').format(folder_id)
        return self._do_get(route)

    def get_folder_children(self, folder_id):
        route = ('/folders/{}/children').format(folder_id)
        return self._do_get(route)

    def create_folder(self, parent_folder, foldername):
        route = '/folders'
        data = {'parent': parent_folder, 'name': foldername}
        return self._do_post(route, data)

    def move_folder(self, folder_id, parent_folder, foldername, ifmatch=None):
        headers = self.auth_headers
        if ifmatch:
            headers['If-Match'] = ifmatch
        route = ('/folders/{}').format(folder_id)
        data = {'parent': parent_folder, 'name': foldername}
        return self._do_put(route, data, headers=headers)

    def delete_folder(self, folder_id, ifmatch=None):
        headers = self.auth_headers
        if ifmatch:
            headers['If-Match'] = ifmatch
        route = ('/folders/{}').format(folder_id)
        return self._do_delete(route, headers=headers)

    def get_file(self, file_id, fields=None):
        route = ('/files/{}').format(file_id)
        if fields:
            route += ('?fields={}').format((',').join(fields))
        return self._do_get(route)

    def get_file_path(self, file_id):
        route = ('/files/{}/path').format(file_id)
        return self._do_get(route)

    def get_file_content(self, file_id, ranges=None, ifrange=None, ifnonematch=None):
        headers = self.auth_headers
        if ranges:
            headers['Range'] = (',').join(ranges)
        if ifrange:
            headers['If-Range'] = ifrange
        if ifnonematch:
            headers['If-None-Match'] = (',').join(ifnonematch)
        route = ('/files/{}/content').format(file_id)
        return self._do_get(route, headers=headers)

    def create_file(self, parent_folder, filename):
        route = '/files'
        data = {'parent': parent_folder, 'name': filename}
        return self._do_post(route, data)

    def upload_file_content(self, file_id, stream, ifmatch=None):
        route = ('/files/{}/content').format(file_id)
        chunks = [
         stream.read(MAX_CHUNK_SIZE)]
        while len(chunks[(-1)]) != 0:
            chunks.append(stream.read(MAX_CHUNK_SIZE))

        chunks.pop()
        if len(chunks) == 1:
            return self._do_put(route, io.BytesIO(chunks[0]), serialize=False)
        else:
            headers = dict(self.auth_headers, **{'Content-Range': 'bytes */*', 
               'Content-Length': '0'})
            if ifmatch:
                headers['If-Match'] = (',').join(ifmatch)
            self._do_put(route, None, headers=headers)
            upload_id = self.response_headers['Upload-ID']
            etag = self.response_headers.get('ETag')
            total_bytes_sent = 0
            for chunk in chunks:
                headers = dict(self.auth_headers, **{'Upload-ID': upload_id, 
                   'Content-Range': ('bytes {}-{}/*').format(total_bytes_sent, total_bytes_sent + len(chunk) - 1)})
                if etag:
                    headers['If-Match'] = etag
                self._do_put(route, io.BytesIO(chunk), serialize=False, headers=headers)
                total_bytes_sent += len(chunk)

            headers = dict(self.auth_headers, **{'Upload-ID': upload_id, 
               'Content-Range': ('bytes */{}').format(total_bytes_sent), 
               'Content-Length': '0'})
            if etag:
                headers['If-Match'] = etag
            return self._do_put(route, None, headers=headers)

    def move_file(self, file_id, parent_folder, filename, ifmatch=None):
        headers = self.auth_headers
        if ifmatch:
            headers['If-Match'] = (',').join(ifmatch)
        route = ('/files/{}').format(file_id)
        data = {'parent': parent_folder, 'name': filename}
        return self._do_put(route, data, headers=headers)

    def delete_file(self, file_id, ifmatch=None):
        headers = self.auth_headers
        if ifmatch:
            headers['If-Match'] = (',').join(ifmatch)
        route = ('/files/{}').format(file_id)
        return self._do_delete(route, headers=headers)

    def get_shared_folders(self, email, ifnonematch=None):
        headers = self.auth_headers
        if ifnonematch:
            headers['If-None-Match'] = (',').join(ifnonematch)
        route = ('/users/{}/shares').format(email)
        return self._do_get(route, headers=headers)

    def get_shared_folder(self, share_id, ifnonematch=None):
        headers = self.auth_headers
        if ifnonematch:
            headers['If-None-Match'] = (',').join(ifnonematch)
        route = ('/shares/{}').format(share_id)
        return self._do_get(route, headers=headers)

    def create_shared_folder(self, foldername):
        route = '/shares'
        data = {'name': foldername}
        return self._do_post(route, data)

    def get_sf_members(self, share_id, ifnonematch=None):
        headers = self.auth_headers
        if ifnonematch:
            headers['If-None-Match'] = (',').join(ifnonematch)
        route = ('/shares/{}/members').format(share_id)
        return self._do_get(route, headers=headers)

    def get_sf_member(self, share_id, email, ifnonematch=None):
        headers = self.auth_headers
        if ifnonematch:
            headers['If-None-Match'] = (',').join(ifnonematch)
        route = ('/shares/{}/members/{}').format(share_id, email)
        return self._do_get(route, headers=headers)

    def add_sf_member(self, share_id, email, permissions):
        route = ('/shares/{}/members').format(share_id)
        data = {'email': email, 'permissions': permissions}
        return self._do_post(route, data)

    def update_sf_member(self, share_id, email, permissions, ifmatch=None):
        headers = self.auth_headers
        if ifmatch:
            headers['If-Match'] = (',').join(ifmatch)
        route = ('/shares/{}/members/{}').format(share_id, email)
        data = {'permissions': permissions}
        return self._do_put(route, data, headers=headers)

    def remove_sf_member(self, share_id, email, ifmatch=None):
        headers = self.auth_headers
        if ifmatch:
            headers['If-Match'] = (',').join(ifmatch)
        route = ('/shares/{}/members/{}').format(share_id, email)
        return self._do_delete(route, headers=headers)

    def get_sf_group_members(self, share_id):
        route = ('/shares/{}/groups').format(share_id)
        return self._do_get(route)

    def get_sf_group_member(self, share_id, group_id):
        route = ('/shares/{}/groups/{}').format(share_id, group_id)
        return self._do_get(route)

    def add_sf_group_member(self, share_id, group_id, permissions):
        route = ('/shares/{}/groups').format(share_id)
        data = {'id': group_id, 'permissions': permissions}
        return self._do_post(route, data)

    def update_sf_group_member(self, share_id, group_id, permissions):
        route = ('/shares/{}/groups/{}').format(share_id, group_id)
        data = {'permissions': permissions}
        return self._do_put(route, data)

    def remove_sf_group_member(self, share_id, group_id):
        route = ('/shares/{}/groups/{}').format(share_id, group_id)
        return self._do_delete(route)

    def get_sf_pending_members(self, share_id, ifnonematch=None):
        headers = self.auth_headers
        if ifnonematch:
            headers['If-None-Match'] = (',').join(ifnonematch)
        route = ('/shares/{}/pending').format(share_id)
        return self._do_get(route, headers=headers)

    def get_sf_pending_member(self, share_id, email):
        route = ('/shares/{}/pending/{}').format(share_id, email)
        return self._do_get(route)

    def add_sf_pending_member(self, share_id, email, permissions, note):
        route = ('/shares/{}/pending').format(share_id)
        data = {'email': email, 'permissions': permissions, 'note': note}
        return self._do_post(route, data)

    def remove_sf_pending_member(self, share_id, email):
        route = ('/shares/{}/pending/{}').format(share_id, email)
        return self._do_delete(route)

    def get_invitations(self, email):
        route = ('/users/{}/invitations').format(quote_plus(email))
        return self._do_get(route)

    def get_invitation(self, email, uuid):
        route = ('/users/{}/invitations/{}').format(quote_plus(email), uuid)
        return self._do_get(route)

    def accept_invitation(self, email, uuid, external=False):
        route = ('/users/{}/invitations/{}').format(quote_plus(email), uuid)
        route += '?external=' + ('1' if external else '0')
        return self._do_post(route, dict())

    def ignore_invitation(self, email, uuid):
        route = ('/users/{}/invitations/{}').format(quote_plus(email), uuid)
        return self._do_delete(route)

    def get_groups(self, offset=0, results=10):
        route = ('/groups?offset={}&results={}').format(offset, results)
        return self._do_get(route)

    def get_group(self, group_id):
        route = ('/groups/{}').format(group_id)
        return self._do_get(route)

    def create_group(self, name):
        route = '/groups'
        data = {'name': name}
        return self._do_post(route, data)

    def delete_group(self, group_id):
        route = ('/groups/{}').format(group_id)
        return self._do_delete(route)

    def get_group_members(self, group_id):
        route = ('/groups/{}/members').format(group_id)
        return self._do_get(route)

    def get_group_member(self, group_id, email):
        route = ('/groups/{}/members/{}').format(group_id, email)
        return self._do_get(route)

    def add_group_member(self, group_id, email):
        route = ('/groups/{}/members').format(group_id)
        data = {'email': email}
        return self._do_post(route, data)

    def remove_group_member(self, group_id, email):
        route = ('/groups/{}/members/{}').format(group_id, email)
        return self._do_delete(route)

    def get_devices(self, email):
        route = ('/users/{}/devices').format(email)
        return self._do_get(route)

    def get_device(self, device_id):
        route = ('/devices/{}').format(device_id)
        return self._do_get(route)

    def get_device_status(self, device_id):
        route = ('/devices/{}/status').format(device_id)
        return self._do_get(route)

    def update_device(self, device_id, name):
        route = ('/devices/{}').format(device_id)
        data = {'name': name}
        return self._do_put(route, data)