# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/peers.py
# Compiled at: 2018-12-16 15:27:33
# Size of source mod 2**32: 10382 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from xio.core.resource import resource, Resource, handleRequest
from xio.core.request import Request, Response
from xio.core.lib.logs import log
from xio.core.lib.utils import is_string, urlparse, md5
from xio.core.peer import Peer
import xio, traceback
from pprint import pprint
import datetime, hashlib, base64, uuid, time, json, sys, collections
PEER_STATUS_NEW = 0
PEER_STATUS_READY = 1
PEER_STATUS_ERROR = 2
PEER_MOD_PUBLIC = 'public'
PEER_MOD_PROTECTED = 'protected'
PEER_MOD_PRIVATE = 'private'

class Peers:

    def __init__(self, peer=None, db=None):
        self.peer = peer
        self.id = peer.id if peer else None
        db = db or xio.db()
        self.db = db.container('peers')
        self.db.truncate()
        self.localresources = xio.db().container('resources')

    def register(self, endpoint=None, nodeid=None, type=None, uid=None, id=None, name=None, sub_register=False):
        if not endpoint:
            raise AssertionError
        else:
            nodeid = nodeid or self.id
            uid = uid if uid else None
            peertype = type if type else None
            peerid = id if id else None
            peername = name if name else None
            assert endpoint
            if not is_string(endpoint):
                if not isinstance(endpoint, Peer):
                    assert isinstance(endpoint, collections.Callable)
            log.info('register', endpoint, 'by', self.peer)
            client = xio.client(endpoint, client=(self.peer))
            resp = client.about()
            about = resp.content
            assert about
            peerid = about.get('id')
            peername = about.get('name', None)
            if sub_register:
                peername = sub_register
                assert peerid
            peertype = about.get('type', 'app').lower()
            assert peerid
            assert peerid != self.id
            provide = sub_register or resp.content.get('provide')
            if provide:
                for xrn in provide:
                    try:
                        if not xrn.startswith(peername + ':'):
                            raise AssertionError(Exception('invalid xrn'))
                        else:
                            postpath = xrn.split(':').pop()
                            if not is_string(endpoint):
                                childendpoint = client.get(postpath)
                            else:
                                childendpoint = endpoint + '/' + postpath
                        self.register(childendpoint, sub_register=xrn)
                    except Exception as err:
                        try:
                            log.error('subregister', xrn, err)
                        finally:
                            err = None
                            del err

            for peer in self.select(id=peerid):
                if peer.data.get('nodeid') == nodeid and peer.id == peerid:
                    log.warning('register ALREADY EXIST', peerid)
                    return

            if not uid:
                uid = md5(nodeid, peerid)
            is_string(endpoint) or self.localresources.put(uid, {'endpoint': endpoint})
            endpoint = '~'
        data = {'uid':uid, 
         'nodeid':nodeid, 
         'id':peerid, 
         'name':peername, 
         'endpoint':endpoint, 
         'type':peertype.lower(), 
         'status':200}
        self.put(uid, data)
        return self.get(uid)

    def unregister(self, peerid):
        for peer in self.select(id=peerid, nodeid=(self.id)):
            self.delete(peer.uid)

    def get(self, index, **kwargs):
        data = self.db.get(index)
        if data:
            peer = PeerClient(self, **data) if not isinstance(data, PeerClient) else data
            return peer
        if str(index).startswith('xrn:'):
            rows = self.select(name=index)
            if rows:
                return rows[0]
            return
        byids = self.select(id=index)
        if byids:
            return byids[0]

    def select(self, **filter):
        result = []
        for row in self.db.select(filter=filter):
            result.append(row)

        return [PeerClient(self, **row) for row in result]

    def put(self, index, peer):
        self.db.put(index, peer)

    def delete(self, index):
        self.db.delete(index)

    def export(self):
        result = []
        for peer in self.select():
            if not peer.endpoint:
                continue
            elif peer.status not in (200, 201):
                continue
            else:
                if peer.type == 'app':
                    if not peer.endpoint:
                        continue
                if peer.type == 'app':
                    mod = PEER_MOD_PROTECTED
                else:
                    if peer.type == 'node':
                        if not peer.conn_type == 'WS':
                            mod = is_string(peer.endpoint) or PEER_MOD_PROTECTED
                        else:
                            mod = PEER_MOD_PUBLIC
                    else:
                        mod = PEER_MOD_PUBLIC
            info = {'type':peer.type, 
             'uid':peer.uid, 
             'name':peer.name, 
             'id':peer.id, 
             'endpoint':peer.endpoint if mod == PEER_MOD_PUBLIC else '~/' + peer.uid}
            result.append(info)

        return result

    def sync(self):
        log.info('=========== PEERS SYNCHRONIZE ...')
        maxage = 60
        for peer in self.select():
            t1 = time.time()
            t0 = peer.checked
            if not t0 and maxage or int(t1) - int(t0) > maxage:
                result = peer.check()
                check_status = result.get('status')
                check_time = result.get('time')
                index = peer.data['_id']
                self.db.update(index, {'status':check_status, 
                 'time':check_time, 
                 'checked':int(time.time())})


class PeerClient(Resource):

    def __init__(self, peers, **data):
        self.peers = peers
        self.data = data
        self.id = data.get('id')
        self.name = data.get('name')
        self.endpoint = data.get('endpoint')
        self.status = data.get('status')
        self.type = data.get('type')
        self.uid = data.get('uid')
        self.checked = int(data.get('checked', 0))
        self.conn_type = data.get('conn_type')
        Resource.__init__(self)
        self.status = data.get('status')

    def check(self):
        headers = {}
        try:
            t0 = time.time()
            resp = self.request('HEAD', '', headers=headers)
            t1 = time.time()
            check_result = {'status':resp.status, 
             'time':int((t1 - t0) * 1000)}
        except Exception as err:
            try:
                traceback.print_exc()
                check_result = {'status':-1, 
                 'error':traceback.format_exc()}
            finally:
                err = None
                del err

        return check_result

    def getInfo(self):
        return self.data

    @handleRequest
    def request(self, req):
        import xio
        context = req.client.context or {}
        if self.endpoint == '~':
            from pprint import pprint
            print('...PEERS GET localresources', self.uid)
            pprint(list(self.peers.localresources.select()))
            endpoint = self.peers.localresources.get(self.uid).get('endpoint')
        else:
            endpoint = self.endpoint
        client = xio.client(endpoint, context)
        try:
            res = client.request((req.method), (req.path), data=(req.data), query=(req.query), headers=(req.headers))
            if res.status == 201:
                if 'Location' in res.headers:
                    self.client = xio.client(res.headers['Location'])
        except Exception as err:
            try:
                traceback.print_exc()
                response = Response(-1)
            finally:
                err = None
                del err

        return res