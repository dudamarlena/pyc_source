# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/node/containers.py
# Compiled at: 2018-12-10 12:16:30
# Size of source mod 2**32: 9422 bytes
import sys, os
from pprint import pprint
import datetime, yaml, time, traceback, xio
from xio.core.utils import md5, mktime
import xio.core.lib.db as db

class Containers:

    def __init__(self, node, db=None):
        self.node = node
        self.docker = node.service('docker').content
        assert self.docker
        self.ipfs = node.service('ipfs')
        db = db or xio.db()
        self.db = db.container('containers')

    def get(self, index):
        container = Container(self, index, container=(self.db))
        return container

    def register(self, uri):
        index = md5(uri)
        container = self.get(index)
        if not container._created:
            container.uri = uri
            container.state = 'pending'
            container.autodeliver = False
            container.save()

    def deliver(self, uri):
        index = md5(uri)
        container = self.get(index)
        if not container._created:
            xio.log.info('delivering container from', uri)
            container.uri = uri
            container.state = 'fetch'
            container.autodeliver = True
            container.save()

    def resync(self):
        """ update containers states from current dockers running containers"""
        containers_to_provide = self.node.getContainersToProvide()
        for row in containers_to_provide:
            self.deliver(row)

        for row in self.db.select():
            if row['uri'] not in containers_to_provide:
                self.db.delete(row['_id'])

        running_endpoints = {}
        for container in self.docker.containers():
            name = container.name
            for k, v in container.ports.items():
                if v == 80:
                    http_endpoint = 'http://127.0.0.1:%s' % k
                    running_endpoints[name] = {'endpoint': http_endpoint}
                    try:
                        self.node.register(http_endpoint)
                    except Exception as err:
                        try:
                            print('dockersync error', err)
                        finally:
                            err = None
                            del err

        return running_endpoints

    def sync(self):
        self.resync()
        for row in self.db.select():
            container = self.get(row['_id'])
            if container.autodeliver:
                try:
                    container.sync()
                except Exception as err:
                    try:
                        self.node.log.error('container.sync error', err)
                    finally:
                        err = None
                        del err

    def select(self):
        return self.db.select()

    def images(self):
        return self.docker.images('xio')


from functools import wraps

def workflowOperation(func):

    @wraps(func)
    def _(self, *args, **kwargs):
        res = None
        opname = func.__name__
        state = self.state
        if state != opname:
            xio.log.warning('wrong state', opname, state)
            return
        workflow = self.workflow
        if not workflow:
            self.workflow = {}
        self.workflow.setdefault(opname, {})
        opstate = self.workflow.get(opname)
        if not opstate:
            opstate['started'] = int(time.time())
            opstate['status'] = 'RUNNING'
            self.save()
            try:
                xio.log.info('workflowOperation', opname, 'start')
                res = func(self, *args, **kwargs)
                opstate['status'] = 'SUCCEED'
            except Exception as err:
                try:
                    xio.log.error('workflowOperation', opname, 'FAILED', err)
                    opstate['status'] = 'FAILED'
                    opstate['error'] = err
                finally:
                    err = None
                    del err

            self.save()
            return res
        xio.log.warning('workflowOperation', opname, 'already running')

    return _


class Container(db.Item):

    def __init__(self, containers, *args, **kwargs):
        self._containers = containers
        self._docker = containers.docker
        self._log = self._containers.node.log
        (db.Item.__init__)(self, *args, **kwargs)

    def about(self):
        about = self.data
        about.update({'image':self.image.about() if self.image else {'name': self.iname}, 
         'container':self.container.about() if self.container else {'name': self.cname}})
        return about

    def sync(self):
        self._log.info('sync', self.uri)
        if self.state != 'running':
            self.fetch()
            self.build()
            self.run()
        else:
            dockercontainer = self._docker.container(name=(self.cname))
            running = dockercontainer.running if dockercontainer else False
            if running:
                try:
                    self._containers.node.register(self.endpoint)
                except Exception as err:
                    try:
                        xio.log.error('unable to register containers endpoint ', self.endpoint, err)
                    finally:
                        err = None
                        del err

            else:
                xio.log.warning('container not running, try to restart it ', self.iname)
                try:
                    self._containers.node.unregister(self.endpoint)
                except Exception as err:
                    try:
                        xio.log.error('unable to unregister containers endpoint', self.endpoint, err)
                    finally:
                        err = None
                        del err

                self.state = 'run'
                if self.workflow:
                    if 'run' in self.workflow:
                        del self.workflow['run']
                self.save()

    @workflowOperation
    def fetch(self):
        if self.uri.startswith('/'):
            self.directory = self.uri
        else:
            about_filepath = self.directory + '/about.yml'
            with open(about_filepath) as (f):
                about = yaml.load(f)
            self.name = about.get('name')
            nfo = self.name.split(':')
            nfo.pop(0)
            self.cname = '-'.join(nfo)
            dockerinfo = about.get('docker', {})
            dockerfile = self.directory + '/Dockerfile'
            if not os.path.isfile(dockerfile):
                self.iname = dockerinfo.get('image', 'inxio/app')
                self.dockerfile = None
            else:
                self.iname = self.cname.replace('-', '/')
            self.dockerfile = dockerfile
        self.state = 'build'

    @workflowOperation
    def build(self):
        dockercontainer = self._docker.container(name=(self.cname))
        if dockercontainer:
            dockercontainer.stop()
            dockercontainer.remove()
        if self.dockerfile:
            dockerimage = self._docker.image(name=(self.iname))
            if not dockerimage:
                if self.dockerfile:
                    self._docker.build(name=(self.iname), directory=(self.directory))
                    self._dockerimage = self._docker.image(name=(self.iname))
                    assert self._dockerimage
        self.state = 'run'

    @workflowOperation
    def run(self):
        dockercontainer = self._docker.container(name=(self.cname))
        cport = 80
        if not dockercontainer:
            assert self.cname
            assert self.iname
            assert self.directory
            container_volume = '/data/%s' % self.cname
            info = {'name':self.cname, 
             'image':self.iname, 
             'ports':{cport: ('127.0.0.1', 0)}, 
             'volumes':{'/apps/xio': '/apps/xio', 
              self.directory: '/apps/app', 
              container_volume: '/data'}}
            dockercontainer = (self._docker.run)(**info)
            assert dockercontainer
        else:
            if not dockercontainer.running:
                dockercontainer.start()
        portmapping = dockercontainer.about().get('port')
        for k, v in portmapping.items():
            if v == cport:
                self.endpoint = 'http://127.0.0.1:%s' % k
                self.port = k

        assert self.endpoint
        self.state = 'running'

    def test(self):
        dockercontainer = self._docker.container(self.cname)
        return dockercontainer.execute('python -m unittest app/tests.py')

    def logs(self):
        dockercontainer = self._docker.container(self.cname)
        return dockercontainer.logs()

    def request(self, method, path, query):
        """ test for ihm admin only ?"""
        if self.endpoint:
            import xio
            cli = xio.client(self.endpoint)
            resp = cli.request(method, path, {})
            return resp.content