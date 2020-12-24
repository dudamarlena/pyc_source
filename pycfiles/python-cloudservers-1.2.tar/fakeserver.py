# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/cloudservers/tests/fakeserver.py
# Compiled at: 2010-08-16 13:49:38
"""
A fake server that "responds" to API methods with pre-canned responses.

All of these responses come from the spec, so if for some reason the spec's
wrong the tests might fail. I've indicated in comments the places where actual
behavior differs from the spec.
"""
import httplib2, urlparse, urllib
from nose.tools import assert_equal
from cloudservers import CloudServers
from cloudservers.client import CloudServersClient
from utils import fail, assert_in, assert_not_in, assert_has_keys

class FakeServer(CloudServers):

    def __init__(self, username=None, password=None):
        super(FakeServer, self).__init__('username', 'apikey')
        self.client = FakeClient()

    def assert_called--- This code section failed: ---

 L.  26         0  LOAD_FAST             1  'method'
                3  LOAD_FAST             2  'url'
                6  BUILD_TUPLE_2         2 
                9  STORE_FAST            4  'expected'

 L.  27        12  LOAD_FAST             0  'self'
               15  LOAD_ATTR             0  'client'
               18  LOAD_ATTR             1  'callstack'
               21  LOAD_CONST               -1
               24  BINARY_SUBSCR    
               25  LOAD_CONST               0
               28  LOAD_CONST               2
               31  SLICE+3          
               32  STORE_FAST            5  'called'

 L.  29        35  LOAD_FAST             0  'self'
               38  LOAD_ATTR             0  'client'
               41  LOAD_ATTR             1  'callstack'
               44  POP_JUMP_IF_TRUE     60  'to 60'
               47  LOAD_ASSERT              AssertionError
               50  LOAD_CONST               'Expected %s %s but no calls were made.'
               53  LOAD_FAST             4  'expected'
               56  BINARY_MODULO    
               57  RAISE_VARARGS_2       2  None

 L.  31        60  LOAD_FAST             4  'expected'
               63  LOAD_FAST             5  'called'
               66  COMPARE_OP            2  ==
               69  POP_JUMP_IF_TRUE     89  'to 89'
               72  LOAD_ASSERT              AssertionError
               75  LOAD_CONST               'Expected %s %s; got %s %s'
               78  LOAD_FAST             4  'expected'
               81  LOAD_FAST             5  'called'
               84  BINARY_ADD       
               85  BINARY_MODULO    
               86  RAISE_VARARGS_2       2  None

 L.  33        89  LOAD_FAST             3  'body'
               92  LOAD_CONST               None
               95  COMPARE_OP            9  is-not
               98  POP_JUMP_IF_FALSE   131  'to 131'

 L.  34       101  LOAD_GLOBAL           4  'assert_equal'
              104  LOAD_FAST             0  'self'
              107  LOAD_ATTR             0  'client'
              110  LOAD_ATTR             1  'callstack'
              113  LOAD_CONST               -1
              116  BINARY_SUBSCR    
              117  LOAD_CONST               2
              120  BINARY_SUBSCR    
              121  LOAD_FAST             3  'body'
              124  CALL_FUNCTION_2       2  None
              127  POP_TOP          
              128  JUMP_FORWARD          0  'to 131'
            131_0  COME_FROM           128  '128'

 L.  36       131  BUILD_LIST_0          0 
              134  LOAD_FAST             0  'self'
              137  LOAD_ATTR             0  'client'
              140  STORE_ATTR            1  'callstack'
              143  LOAD_CONST               None
              146  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 143

    def authenticate(self):
        pass


class FakeClient(CloudServersClient):

    def __init__(self):
        self.username = 'username'
        self.apikey = 'apikey'
        self.callstack = []

    def _cs_request(self, url, method, **kwargs):
        if method in ('GET', 'DELETE'):
            assert_not_in('body', kwargs)
        elif method in ('PUT', 'POST'):
            assert_in('body', kwargs)
        munged_url = url.strip('/').replace('/', '_').replace('.', '_')
        callback = '%s_%s' % (method.lower(), munged_url)
        if not hasattr(self, callback):
            fail('Called unknown API method: %s %s' % (method, url))
        self.callstack.append((method, url, kwargs.get('body', None)))
        status, body = getattr(self, callback)(**kwargs)
        return (httplib2.Response({'status': status}), body)

    def _munge_get_url(self, url):
        return url

    def get_limits(self, **kw):
        return (
         200,
         {'limits': {'rate': [
                              {'verb': 'POST', 
                                 'URI': '*', 
                                 'regex': '.*', 
                                 'value': 10, 
                                 'remaining': 2, 
                                 'unit': 'MINUTE', 
                                 'resetTime': 1244425439},
                              {'verb': 'POST', 
                                 'URI': '*/servers', 
                                 'regex': '^/servers', 
                                 'value': 50, 
                                 'remaining': 49, 
                                 'unit': 'DAY', 
                                 'resetTime': 1244511839},
                              {'verb': 'PUT', 
                                 'URI': '*', 
                                 'regex': '.*', 
                                 'value': 10, 
                                 'remaining': 2, 
                                 'unit': 'MINUTE', 
                                 'resetTime': 1244425439},
                              {'verb': 'GET', 
                                 'URI': '*changes-since*', 
                                 'regex': 'changes-since', 
                                 'value': 3, 
                                 'remaining': 3, 
                                 'unit': 'MINUTE', 
                                 'resetTime': 1244425439},
                              {'verb': 'DELETE', 
                                 'URI': '*', 
                                 'regex': '.*', 
                                 'value': 100, 
                                 'remaining': 100, 
                                 'unit': 'MINUTE', 
                                 'resetTime': 1244425439}], 
                       'absolute': {'maxTotalRAMSize': 51200, 
                                    'maxIPGroups': 50, 
                                    'maxIPGroupMembers': 25}}})

    def get_servers(self, **kw):
        return (
         200, {'servers': [{'id': 1234, 'name': 'sample-server'}, {'id': 5678, 'name': 'sample-server2'}]})

    def get_servers_detail(self, **kw):
        return (
         200,
         {'servers': [
                      {'id': 1234, 
                         'name': 'sample-server', 
                         'imageId': 2, 
                         'flavorId': 1, 
                         'hostId': 'e4d909c290d0fb1ca068ffaddf22cbd0', 
                         'status': 'BUILD', 
                         'progress': 60, 
                         'addresses': {'public': [
                                                '1.2.3.4', '5.6.7.8'], 
                                       'private': [
                                                 '10.11.12.13']}, 
                         'metadata': {'Server Label': 'Web Head 1', 
                                      'Image Version': '2.1'}},
                      {'id': 5678, 
                         'name': 'sample-server2', 
                         'imageId': 2, 
                         'flavorId': 1, 
                         'hostId': '9e107d9d372bb6826bd81d3542a419d6', 
                         'status': 'ACTIVE', 
                         'addresses': {'public': [
                                                '9.10.11.12'], 
                                       'private': [
                                                 '10.11.12.14']}, 
                         'metadata': {'Server Label': 'DB 1'}}]})

    def post_servers(self, body, **kw):
        assert_equal(body.keys(), ['server'])
        assert_has_keys(body['server'], required=[
         'name', 'imageId', 'flavorId'], optional=[
         'sharedIpGroupId', 'metadata', 'personality'])
        if 'personality' in body['server']:
            for pfile in body['server']['personality']:
                assert_has_keys(pfile, required=['path', 'contents'])

        return (
         202, self.get_servers_1234()[1])

    def get_servers_1234(self, **kw):
        r = {'server': self.get_servers_detail()[1]['servers'][0]}
        return (
         200, r)

    def get_servers_5678(self, **kw):
        r = {'server': self.get_servers_detail()[1]['servers'][1]}
        return (
         200, r)

    def put_servers_1234(self, body, **kw):
        assert_equal(body.keys(), ['server'])
        assert_has_keys(body['server'], optional=['name', 'adminPass'])
        return (204, None)

    def delete_servers_1234(self, **kw):
        return (202, None)

    def get_servers_1234_ips(self, **kw):
        return (
         200, {'addresses': self.get_servers_1234()[1]['server']['addresses']})

    def get_servers_1234_ips_public(self, **kw):
        return (
         200, {'public': self.get_servers_1234_ips()[1]['addresses']['public']})

    def get_servers_1234_ips_private(self, **kw):
        return (
         200, {'private': self.get_servers_1234_ips()[1]['addresses']['private']})

    def put_servers_1234_ips_public_1_2_3_4(self, body, **kw):
        assert_equal(body.keys(), ['shareIp'])
        assert_has_keys(body['shareIp'], required=['sharedIpGroupId', 'configureServer'])
        return (202, None)

    def delete_servers_1234_ips_public_1_2_3_4(self, **kw):
        return (202, None)

    def post_servers_1234_action(self, body, **kw):
        assert_equal(len(body.keys()), 1)
        action = body.keys()[0]
        if action == 'reboot':
            assert_equal(body[action].keys(), ['type'])
            assert_in(body[action]['type'], ['HARD', 'SOFT'])
        elif action == 'rebuild':
            assert_equal(body[action].keys(), ['imageId'])
        elif action == 'resize':
            assert_equal(body[action].keys(), ['flavorId'])
        else:
            if action == 'confirmResize':
                assert_equal(body[action], None)
                return (204, None)
            if action == 'revertResize':
                assert_equal(body[action], None)
            else:
                fail('Unexpected server action: %s' % action)
        return (202, None)

    def get_flavors(self, **kw):
        return (
         200, {'flavors': [{'id': 1, 'name': '256 MB Server'}, {'id': 2, 'name': '512 MB Server'}]})

    def get_flavors_detail(self, **kw):
        return (
         200, {'flavors': [{'id': 1, 'name': '256 MB Server', 'ram': 256, 'disk': 10}, {'id': 2, 'name': '512 MB Server', 'ram': 512, 'disk': 20}]})

    def get_flavors_1(self, **kw):
        return (
         200, {'flavor': self.get_flavors_detail()[1]['flavors'][0]})

    def get_flavors_2(self, **kw):
        return (
         200, {'flavor': self.get_flavors_detail()[1]['flavors'][1]})

    def get_images(self, **kw):
        return (
         200, {'images': [{'id': 1, 'name': 'CentOS 5.2'}, {'id': 2, 'name': 'My Server Backup'}]})

    def get_images_detail(self, **kw):
        return (
         200,
         {'images': [
                     {'id': 1, 
                        'name': 'CentOS 5.2', 
                        'updated': '2010-10-10T12:00:00Z', 
                        'created': '2010-08-10T12:00:00Z', 
                        'status': 'ACTIVE'},
                     {'id': 743, 
                        'name': 'My Server Backup', 
                        'serverId': 12, 
                        'updated': '2010-10-10T12:00:00Z', 
                        'created': '2010-08-10T12:00:00Z', 
                        'status': 'SAVING', 
                        'progress': 80}]})

    def get_images_1(self, **kw):
        return (
         200, {'image': self.get_images_detail()[1]['images'][0]})

    def get_images_2(self, **kw):
        return (
         200, {'image': self.get_images_detail()[1]['images'][1]})

    def post_images(self, body, **kw):
        assert_equal(body.keys(), ['image'])
        assert_has_keys(body['image'], required=['serverId', 'name'])
        return (202, self.get_images_1()[1])

    def delete_images_1(self, **kw):
        return (204, None)

    def get_servers_1234_backup_schedule(self, **kw):
        return (
         200,
         {'backupSchedule': {'enabled': True, 
                               'weekly': 'THURSDAY', 
                               'daily': 'H_0400_0600'}})

    def post_servers_1234_backup_schedule(self, body, **kw):
        assert_equal(body.keys(), ['backupSchedule'])
        assert_has_keys(body['backupSchedule'], required=['enabled'], optional=['weekly', 'daily'])
        return (204, None)

    def delete_servers_1234_backup_schedule(self, **kw):
        return (204, None)

    def get_shared_ip_groups(self, **kw):
        return (
         200, {'sharedIpGroups': [{'id': 1, 'name': 'group1'}, {'id': 2, 'name': 'group2'}]})

    def get_shared_ip_groups_detail(self, **kw):
        return (
         200, {'sharedIpGroups': [{'id': 1, 'name': 'group1', 'servers': [1234]}, {'id': 2, 'name': 'group2', 'servers': [5678]}]})

    def get_shared_ip_groups_1(self, **kw):
        return (
         200, {'sharedIpGroup': self.get_shared_ip_groups_detail()[1]['sharedIpGroups'][0]})

    def post_shared_ip_groups(self, body, **kw):
        assert_equal(body.keys(), ['sharedIpGroup'])
        assert_has_keys(body['sharedIpGroup'], required=['name'], optional=['server'])
        return (201,
         {'sharedIpGroup': {'id': 10101, 
                              'name': body['sharedIpGroup']['name'], 
                              'servers': 'server' in body['sharedIpGroup'] and [body['sharedIpGroup']['server']] or None}})

    def delete_shared_ip_groups_1(self, **kw):
        return (204, None)