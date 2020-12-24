# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/node/node.py
# Compiled at: 2018-12-12 11:21:20
# Size of source mod 2**32: 5407 bytes
import xio
from xio.core import resource
from xio.core.resource import handleRequest
from xio.core.request import Request, Response
from xio.core.app.app import App
from xio.core.lib.logs import log
from xio.core.lib.utils import is_string, urlparse, generateuid
from .containers import Containers
import traceback
from pprint import pprint
import datetime, os.path, hashlib, base64, uuid, time, json, sys, collections

def node(*args, **kwargs):
    return (Node.factory)(*args, **kwargs)


class Node(App):

    def __init__(self, name=None, network=None, **kwargs):
        (App.__init__)(self, name, **kwargs)
        self.uid = generateuid()
        self.network = self.connect(network) if network else None
        if self.network:
            try:
                self._about['network'] = self.network.about()
            except Exception as err:
                try:
                    self.log.warning('self.network error', err)
                finally:
                    err = None
                    del err

        else:
            self.bind('www', self.renderWww)
            import xio
            if self.redis:
                memdb = xio.db(name='xio', type='redis')
            else:
                memdb = xio.db()
        self.put('services/db', memdb)
        from xio.core.peers import Peers
        self.peers = Peers(peer=self, db=memdb)
        node_heartbeat = xio.env.get('node_heartbeat', 300)
        self.schedule(node_heartbeat, self.sync)
        node_peers_heartbeat = xio.env.get('node_peers_heartbeat', 300)
        self.schedule(node_peers_heartbeat, self.peers.sync)
        try:
            from ext.docker.service import DockerService
            self.put('services/docker', DockerService(self))
            self.containers = Containers(self, db=memdb)
            node_containers_heartbeat = xio.env.get('node_containers_heartbeat', 300)
            self.schedule(node_containers_heartbeat, self.containers.sync)
        except Exception as err:
            try:
                self.log.warning('self.docker error', err)
            finally:
                err = None
                del err

    def register(self, endpoints):
        if not isinstance(endpoints, list):
            endpoints = [
             endpoints]
        for endpoint in endpoints:
            return self.peers.register(endpoint)

    def getContainersToProvide(self):
        try:
            res = self.network.get('containers')
            return res.content or []
        except Exception as err:
            try:
                xio.log.error('unable to fetch containers to provide', err)
            finally:
                err = None
                del err

    def sync(self):
        self.containers.sync()

    def renderWww(self, req):
        """
        options: ABOUT,GET
        """
        self.log.info('NODE.RENDER', req)
        self.log.info(req.headers)
        if not req.path:
            if req.OPTIONS:
                return ''
        if not req.path:
            if req.ABOUT:
                about = self._handleAbout(req)
                about['id'] = self.id
                if self.network:
                    about['network'] = self.network.about().content
                if req.client.peer:
                    about['user'] = {'id': req.client.peer.id}
                return about
        if not req.path:
            if req.GET:
                peers = [peer.about().content for peer in self.peers.select()]
                return peers
            if req.CHECK:
                req.require('scope', 'admin')
                return self._handleCheck(req)
            if req.REGISTER:
                endpoint = req.data.get('endpoint', req.context.get('REMOTE_ADDR').split(':').pop())
                if '://' not in endpoint:
                    endpoint = 'http://%s' % endpoint
                return self.peers.register(endpoint)
            if req.CHECKALL:
                return self.checkall()
            if req.SYNC:
                return self.peers.sync()
            if req.CLEAR:
                return self.peers.clear()
            if req.EXPORT:
                return self.peers.export()
            raise Exception(405, 'METHOD NOT ALLOWED')
        assert req.path
        p = req.path.split('/')
        peerid = p.pop(0)
        assert peerid
        if peerid == 'user':
            return self.network.request(req)
        log.info('==== DELIVERY REQUEST =====', req.method, req.xmethod)
        log.info('==== DELIVERY FROM =====', req.client.id, req.client.peer)
        log.info('==== DELIVERY TO   =====', peerid)
        peer = self.peers.get(peerid)
        assert peer, Exception(404)
        try:
            req.path = '/'.join(p)
            resp = peer.request(req)
            req.response.status = resp.status
            req.response.headers = resp.headers
            req.response.content_type = resp.content_type
            req.response.ttl = resp.ttl
            return resp.content
        except Exception as err:
            try:
                traceback.print_exc()
                req.response.status = 500
                return
            finally:
                err = None
                del err