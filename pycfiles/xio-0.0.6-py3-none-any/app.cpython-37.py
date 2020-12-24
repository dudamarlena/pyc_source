# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/app/app.py
# Compiled at: 2018-12-21 03:15:53
# Size of source mod 2**32: 22889 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from xio.core import resource
from xio.core.resource import handleRequest, getResponse
from xio.core import peer
from xio.core.request import Request, Response
from xio.core.lib.logs import log
from xio.core.lib.utils import is_string, urlparse
from xio import path
from xio.core.utils import spawn
import os, posixpath, sys, traceback, time, importlib, yaml, collections
from functools import wraps
import requests, json, base64, uuid, inspect, hashlib, copy
from pprint import pprint
_extdir = os.path.dirname(os.path.realpath(__file__)) + '/ext'
path.append(_extdir)

def getAppsFromDirectory(path):
    syspath = path
    p = path.split('/')
    apps = []
    sys.path.insert(0, syspath)
    if os.path.isdir(path):
        for name in os.listdir(path):
            try:
                directory = path + '/' + name
                if os.path.isdir(directory):
                    modpath = name + '.app'
                    mod = importlib.import_module(modpath, package='.')
                    apps.append((name, mod.app))
            except Exception as err:
                try:
                    import xio, traceback
                    xio.log.warning('unable to load', name, 'from', directory)
                finally:
                    err = None
                    del err

    sys.path.remove(syspath)
    return apps


def app(*args, **kwargs):
    return (App.factory)(*args, **kwargs)


def handleCache(func):

    @wraps(func)
    def _(res, req):
        method = req.xmethod or req.method
        xio_skip_cache = req.query.pop('xio_skip_cache', None)
        ttl = res._about.get('ttl') or res._about.get('methods', {}).get(method, {}).get('ttl')
        usecache = req.GET and ttl
        cached = None
        if usecache:
            xio_skip_cache or print('----handlecache', res._about)
            service = req.service('cache')
            if service:
                uid = req.uid()
                cached = service.get(uid)
                print('----handlecache', cached)
                if cached and cached.status in (200, 201):
                    if cached.content:
                        info = cached.content or {}
                        result = info.get('content')
                        print('found cache !!!', info)
                        req.response = Response(200)
                        req.response.content_type = info.get('content_type')
                        req.response.headers = info.get('headers', {})
                        req.response.ttl = 0
                        print('CACHED RESULT ....', str(req.response.content))
                        return result
        result = getResponse(res, req, func)
        try:
            response = req.response
            if (ttl or req.response).ttl:
                if isinstance(req.response.ttl, int):
                    ttl = req.response.ttl
            write_cache = usecache and ttl and bool(response) and response.status == 200 and not inspect.isgenerator(response.content)
            if write_cache:
                if service:
                    uid = req.uid()
                    print(res._about, res)
                    print('write cache !!!!!!', uid, ttl, response.content)
                    headers = dict(response.headers)
                    service.put(uid, {'content':response.content,  'ttl':int(ttl),  'headers':headers})
        except Exception as err:
            try:
                print('cache error', err)
                traceback.print_exc()
            finally:
                err = None
                del err

        return result

    return _


def handleStats(func):

    @wraps(func)
    def _(self, req):
        return getResponse(self, req, func)

    return _


class App(peer.Peer):
    name = 'lambda'
    module = None
    directory = None
    _about = None
    _skip_handler_allowed = True

    def __init__(self, name=None, module=None, **kwargs):
        (peer.Peer.__init__)(self, **kwargs)
        if module:
            self.module = module
            self.directory = os.path.realpath(os.path.dirname(self.module.__file__)) if self.module else None
            self.load()
        self.endpoint = None
        self._started = None
        self.log = log
        self._events = {}
        self._started = 0
        self.init()

    @classmethod
    def factory(cls, id=None, *args, **kwargs):
        if is_string(id):
            module = sys.modules.get(id)
            if module:
                return cls(module=module, **kwargs)
        if callable(id):
            if inspect.isfunction(id):
                app = cls(*args, **kwargs)
                app.bind('www', id)
                return app
        kwargs.setdefault('_cls', cls)
        return (peer.Peer.factory)(id, *args, **kwargs)

    def load(self):
        module = self.module
        import xio
        if os.path.isfile(self.directory + '/.env'):
            xio.env.load(self.directory + '/.env')
        if os.path.isdir(self.directory + '/ext'):
            xio.path.append(self.directory + '/ext')
            for childname, child in getAppsFromDirectory(self.directory + '/ext'):
                child = xio.app(child)
                self.put('ext/%s' % childname, child)

        if os.path.isfile(self.directory + '/about.yml'):
            with open(self.directory + '/about.yml') as (f):
                self._about = yaml.load(f)
        else:
            self.name = self._about.get('name')
            if self.name:
                if self.name.startswith('xrn:'):
                    xio.register(self.name, self)
            if 'id' in self._about:
                self.id = self._about.get('id')
            else:
                import xio.core.lib.crypto as crypto
            self.key = crypto.key(seed=(self.name))
            self.id = self.key.account('ethereum').address
            self.token = self.key.generateToken('ethereum')
        if os.path.isfile(self.directory + '/tests.py') or os.path.isdir(self.directory + '/tests'):
            sys.path.insert(0, self.directory)
            try:
                print('.....', self.directory)
                import tests
                self._tests = tests
            except Exception as err:
                try:
                    log.warning('TEST LOADING FAILED', err)
                    self._tests = None
                finally:
                    err = None
                    del err

            sys.path.remove(self.directory)

    def init(self):
        for m in dir(self):
            h = getattr(self, m)
            if callable(h) and hasattr(h, '__xio_path__'):
                self.bind(h.__xio_path__, h)

        self.redis = False
        try:
            import xio, redis
            endpoint = xio.env.get('redis')
            if endpoint:
                self.redis = redis.Redis(endpoint)
        except Exception as err:
            try:
                self.log.debug('redis error : %s' % err)
            finally:
                err = None
                del err

        from lib.cron import SchedulerService
        self.put('services/cron', SchedulerService(self))
        from lib.pubsub import PubSubService
        self.put('services/pubsub', PubSubService(self))
        from lib.stats import StatsService
        self.put('services/stats', StatsService(self))
        from lib.cache import CacheService
        self.put('services/cache', CacheService(self))
        services = copy.deepcopy(self._about.get('services'))
        if services:
            log.info('=== LOADING SERVICES ===')
            for service in services:
                log.info('=== LOADING SERVICE ', service)
                name = service.pop('name')
                handler_class = service.get('handler', None)
                handler_params = service.get('params', {})
                if is_string(handler_class):
                    remotehandler = ':' in handler_class or '/' in handler_class
                    pythonhandler = not remotehandler and '.' in handler_class
                    if remotehandler:
                        servicehandler = xio.client(handler_class, handler_params, client=self)
                    else:
                        import importlib
                        p = handler_class.split('.')
                        classname = p.pop()
                        modulepath = '.'.join(p)
                        module = importlib.import_module(modulepath)
                        handler_class = getattr(module, classname)
                        servicehandler = handler_class(app=self, **handler_params)
                    if servicehandler:
                        self.put('services/%s' % name, servicehandler)
                    else:
                        log.warning('unable to load service', service)

        from .admin import enhance
        enhance(self)
        if 'www' not in self._children:
            self.put('www', None)
        if self.directory:
            wwwdir = self.directory + '/www'
            if os.path.isdir(wwwdir):
                self.bind('www', resource.DirectoryHandler(wwwdir))
            wwwstaticdir = self.directory + '/www/static'
            if os.path.isdir(wwwstaticdir):
                self.bind('www/static', resource.DirectoryHandler(wwwstaticdir))

    @handleRequest
    @handleCache
    @handleStats
    def render(self, req):
        """
        pb with code in this method not called if we use request ...
        """
        if not req.path:
            if req.TEST:
                return self._handleTest(req)
        req.path = 'www/' + req.path if req.path else 'www'
        return self.request(req)

    def _handleCheck(self, req):
        results = peer.Peer._handleCheck(self, req)
        print(self._tests)
        if self._tests:
            try:
                testresult = self._handleTest(req)
                result = (200, testresult)
            except Exception as err:
                try:
                    import traceback
                    traceback.print_exc()
                    result = (500, err)
                finally:
                    err = None
                    del err

            results['test'] = result
        for name, service in self.get('services')._children.items():
            try:
                res = service.check()
                result = (res.status, res.content)
            except Exception as err:
                try:
                    result = (
                     500, err)
                finally:
                    err = None
                    del err

            results['service/%s' % name] = result

        return results

    def _handleTest(self, req):
        if self._tests:
            import unittest
            modules = [
             self._tests]
            suite = unittest.TestSuite()
            loader = unittest.TestLoader()
            for mod in modules:
                suitemod = loader.loadTestsFromModule(mod)
                suite.addTests(suitemod)

            results = unittest.TestResult()
            results.buffer = True
            suite.run(results)
        print(results)
        print(dir(results))
        return {'run': results.run}

    def run(self, loop=True, **options):
        (self.start)(**options)
        if loop:
            import time
            while True:
                time.sleep(0.1)

    def uwsgi(self):
        """
        run app in uwsgi thread
        return app as wsgi application
        usage :  uwsgi --python --module app:uwsgi()
        """
        import uwsgidecorators

        @uwsgidecorators.postfork
        @uwsgidecorators.thread
        def _run():
            self.run()

        return self

    def start(self, use_wsgi=False, **options):
        import xio
        if not use_wsgi:
            self.emit('start')
        http = options.get('http', xio.env.get('http', 8080))
        ws = options.get('ws', xio.env.get('ws'))
        debug = options.get('debug', xio.env.get('debug'))
        if http:
            self.put('etc/services/http', {'port': int(http)})
        if ws:
            self.put('etc/services/ws', {'port': int(ws)})
        if debug:
            log.setLevel('DEBUG')
        self._started = int(time.time())
        for name, res in list(self.get('etc/services')._children.items()):
            try:
                servicehandler = None
                if use_wsgi:
                    if name not in ('http', 'https', 'ws', 'wss'):
                        continue
                conf = copy.copy(res.content)
                self.log.info('STARTING SERVICE %s (%s)' % (name, conf))
                if not isinstance(conf, dict):
                    servicehandler = conf
                else:
                    from .lib import websocket
                    from .lib import http
                    port = conf.get('port')
                    scheme = conf.get('scheme', name)
                    options = {}
                    path = conf.get('path')
                    if scheme == 'ws':
                        servicehandler = (websocket.WebsocketService)(app=self, port=port, **options)
                    else:
                        if scheme == 'http':
                            servicehandler = (http.HttpService)(app=self, path=path, port=port, **options)
                        else:
                            if scheme == 'https':
                                servicehandler = (http.HttpsService)(app=self, path=path, port=port, **options)
                            if servicehandler:
                                if hasattr(servicehandler, 'start'):
                                    servicehandler.start()
                                    self.put('run/services/%s' % name, servicehandler)
            except Exception as err:
                try:
                    self.log.error('STARTING SERVICE %s FAIL : %s' % (name, err))
                finally:
                    err = None
                    del err

        if not use_wsgi:
            self.emit('started')
            self.debug()

    def __call__(self, environ, start_response=None):
        """
        this method can be used as WSGI callable as well as xio.app handler

        for wsgi in uwsgi context we have to start the app if not already do
        """
        if isinstance(environ, Request):
            req = environ
            return self.request(req)
            if not self._started:
                import xio
                print('...wsgi init')
                self.start(use_wsgi=True)
            if environ.get('HTTP_CONNECTION') == 'Upgrade' and environ.get('HTTP_UPGRADE') == 'websocket' and environ.get('HTTP_SEC_WEBSOCKET_KEY'):
                handler = self.get('run/services/ws')._handler
            else:
                handler = self.get('run/services/http')._handler
            print('...wsgi call handling', handler)
            if not environ:
                self.log.warning('BAD WSGI CTX')
                return
            if not handler:
                self.log.warning('NO WSGI HANDLER')
                return
        else:
            try:
                result = handler(environ, start_response)
            except Exception as err:
                try:
                    import traceback
                    traceback.print_exc()
                    start_response('500 ERROR', [('Content-Type', 'text')])
                    result = [str(traceback.format_exc())]
                finally:
                    err = None
                    del err

        print('...wsgi call stop')
        return result

    def service(self, name):
        service = self.get('services').get(name)
        return service

    def schedule(self, *args, **kwargs):
        scheduler = self.get('services/cron')
        if len(args) > 1:
            (scheduler.schedule)(*args, **kwargs)
        else:

            def _wrapper(func):
                c = args[0]
                return (scheduler.schedule)(c, func, *(args[1:]), **kwargs)

            return _wrapper

    def on(self, *args):
        if len(args) > 1:
            event, handler = args
            self._events.setdefault(event, [])
            self._events[event].append(handler)
        else:

            def _(handler):
                event = args[0]
                self._events.setdefault(event, [])
                self._events[event].append(handler)

            return _

    def emit(self, event, *args, **kwargs):
        for handler in self._events.get(event, []):
            try:
                (spawn(handler))(*args, **kwargs)
            except Exception as err:
                try:
                    log.warning('event handler error', err)
                    import traceback
                    traceback.print_exc()
                finally:
                    err = None
                    del err

    def publish(self, topic, *args, **kwargs):
        pubsubservice = self.get('services/pubsub').content
        if pubsubservice:
            print('...app.publish', topic)
            return (pubsubservice.publish)(topic, *args, **kwargs)

    def subscribe(self, *args):
        if len(args) > 1:
            topic, callback = args
            return self.get('services/pubsub').subscribe(topic, callback)

        def _wrapper(callback):
            topic = args[0]
            return self.get('services/pubsub').subscribe(topic, callback)

        return _wrapper

    def main--- This code section failed: ---

 L. 597         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              sys
                6  STORE_FAST               'sys'

 L. 598         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              os
               14  STORE_FAST               'os'

 L. 599        16  LOAD_CONST               0
               18  LOAD_CONST               ('pprint',)
               20  IMPORT_NAME              pprint
               22  IMPORT_FROM              pprint
               24  STORE_FAST               'pprint'
               26  POP_TOP          

 L. 600        28  LOAD_CONST               0
               30  LOAD_CONST               None
               32  IMPORT_NAME_ATTR         os.path
               34  STORE_FAST               'os'

 L. 601        36  LOAD_CONST               0
               38  LOAD_CONST               None
               40  IMPORT_NAME              xio
               42  STORE_FAST               'xio'

 L. 603        44  LOAD_CONST               0
               46  LOAD_CONST               None
               48  IMPORT_NAME              argparse
               50  STORE_FAST               'argparse'

 L. 605        52  LOAD_FAST                'argparse'
               54  LOAD_ATTR                ArgumentParser
               56  LOAD_CONST               False
               58  LOAD_CONST               ('add_help',)
               60  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               62  STORE_FAST               'parser'

 L. 606        64  LOAD_FAST                'parser'
               66  LOAD_ATTR                add_argument
               68  LOAD_STR                 'cmd'
               70  LOAD_STR                 '?'
               72  LOAD_CONST               None
               74  LOAD_CONST               None
               76  LOAD_CONST               ('nargs', 'const', 'default')
               78  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               80  POP_TOP          

 L. 607        82  LOAD_FAST                'parser'
               84  LOAD_ATTR                add_argument
               86  LOAD_STR                 'param'
               88  LOAD_STR                 '?'
               90  LOAD_CONST               None
               92  LOAD_CONST               None
               94  LOAD_CONST               ('nargs', 'const', 'default')
               96  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               98  POP_TOP          

 L. 608       100  LOAD_FAST                'parser'
              102  LOAD_ATTR                add_argument
              104  LOAD_STR                 '--http'
              106  LOAD_GLOBAL              int
              108  LOAD_STR                 '?'
              110  LOAD_CONST               8080
              112  LOAD_CONST               8080
              114  LOAD_CONST               ('type', 'nargs', 'const', 'default')
              116  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              118  POP_TOP          

 L. 609       120  LOAD_FAST                'parser'
              122  LOAD_ATTR                add_argument
              124  LOAD_STR                 '--ws'
              126  LOAD_GLOBAL              int
              128  LOAD_STR                 '?'
              130  LOAD_CONST               8484
              132  LOAD_CONST               None
              134  LOAD_CONST               ('type', 'nargs', 'const', 'default')
              136  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              138  POP_TOP          

 L. 610       140  LOAD_FAST                'parser'
              142  LOAD_ATTR                add_argument
              144  LOAD_STR                 '--debug'
              146  LOAD_STR                 'store_true'
              148  LOAD_CONST               ('action',)
              150  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              152  POP_TOP          

 L. 611       154  LOAD_FAST                'parser'
              156  LOAD_ATTR                add_argument
              158  LOAD_STR                 '--network'
              160  LOAD_STR                 'store_true'
              162  LOAD_CONST               ('action',)
              164  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              166  POP_TOP          

 L. 612       168  LOAD_FAST                'parser'
              170  LOAD_ATTR                add_argument
              172  LOAD_STR                 '--env'
              174  LOAD_GLOBAL              str
              176  LOAD_CONST               None
              178  LOAD_CONST               ('type', 'default')
              180  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              182  POP_TOP          

 L. 615       184  SETUP_LOOP          244  'to 244'
              186  LOAD_FAST                'xio'
              188  LOAD_ATTR                env
              190  LOAD_METHOD              items
              192  CALL_METHOD_0         0  '0 positional arguments'
              194  GET_ITER         
              196  FOR_ITER            242  'to 242'
              198  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST               'k'
              202  STORE_FAST               'v'

 L. 616       204  SETUP_EXCEPT        228  'to 228'

 L. 617       206  LOAD_FAST                'parser'
              208  LOAD_ATTR                add_argument
              210  LOAD_STR                 '--'
              212  LOAD_FAST                'k'
              214  BINARY_ADD       
              216  LOAD_FAST                'v'
              218  LOAD_CONST               ('default',)
              220  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              222  POP_TOP          
              224  POP_BLOCK        
              226  JUMP_BACK           196  'to 196'
            228_0  COME_FROM_EXCEPT    204  '204'

 L. 618       228  POP_TOP          
              230  POP_TOP          
              232  POP_TOP          

 L. 619       234  POP_EXCEPT       
              236  JUMP_BACK           196  'to 196'
              238  END_FINALLY      
              240  JUMP_BACK           196  'to 196'
              242  POP_BLOCK        
            244_0  COME_FROM_LOOP      184  '184'

 L. 621       244  LOAD_FAST                'parser'
              246  LOAD_METHOD              parse_args
              248  CALL_METHOD_0         0  '0 positional arguments'
              250  STORE_FAST               'args'

 L. 622       252  LOAD_GLOBAL              vars
              254  LOAD_FAST                'parser'
              256  LOAD_METHOD              parse_args
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  STORE_FAST               'options'

 L. 623       264  SETUP_LOOP          302  'to 302'
              266  LOAD_FAST                'options'
              268  LOAD_METHOD              items
              270  CALL_METHOD_0         0  '0 positional arguments'
              272  GET_ITER         
              274  FOR_ITER            300  'to 300'
              276  UNPACK_SEQUENCE_2     2 
              278  STORE_FAST               'key'
              280  STORE_FAST               'val'

 L. 624       282  LOAD_FAST                'xio'
              284  LOAD_ATTR                env
              286  LOAD_METHOD              set
              288  LOAD_FAST                'key'
              290  LOAD_FAST                'val'
              292  CALL_METHOD_2         2  '2 positional arguments'
              294  POP_TOP          
          296_298  JUMP_BACK           274  'to 274'
              300  POP_BLOCK        
            302_0  COME_FROM_LOOP      264  '264'

 L. 627       302  LOAD_FAST                'xio'
              304  LOAD_ATTR                env
              306  LOAD_METHOD              get
              308  LOAD_STR                 'env'
              310  CALL_METHOD_1         1  '1 positional argument'
              312  STORE_FAST               'envfilepath'

 L. 628       314  LOAD_FAST                'envfilepath'
          316_318  POP_JUMP_IF_FALSE   346  'to 346'
              320  LOAD_FAST                'os'
              322  LOAD_ATTR                path
              324  LOAD_METHOD              isfile
              326  LOAD_FAST                'envfilepath'
              328  CALL_METHOD_1         1  '1 positional argument'
          330_332  POP_JUMP_IF_FALSE   346  'to 346'

 L. 629       334  LOAD_FAST                'xio'
              336  LOAD_ATTR                env
              338  LOAD_METHOD              load
              340  LOAD_FAST                'envfilepath'
              342  CALL_METHOD_1         1  '1 positional argument'
              344  POP_TOP          
            346_0  COME_FROM           330  '330'
            346_1  COME_FROM           316  '316'

 L. 630       346  LOAD_GLOBAL              print
              348  CALL_FUNCTION_0       0  '0 positional arguments'
              350  POP_TOP          

 L. 631       352  LOAD_GLOBAL              print
              354  LOAD_STR                 '\tapp='
              356  LOAD_FAST                'self'
              358  CALL_FUNCTION_2       2  '2 positional arguments'
              360  POP_TOP          

 L. 632       362  LOAD_GLOBAL              print
              364  LOAD_STR                 '\tapp='
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                id
              370  CALL_FUNCTION_2       2  '2 positional arguments'
              372  POP_TOP          

 L. 633       374  LOAD_GLOBAL              print
              376  LOAD_STR                 '\tapp='
              378  LOAD_FAST                'self'
              380  LOAD_ATTR                name
              382  CALL_FUNCTION_2       2  '2 positional arguments'
              384  POP_TOP          

 L. 634       386  LOAD_GLOBAL              print
              388  LOAD_STR                 '\tapp='
              390  LOAD_FAST                'self'
              392  LOAD_ATTR                _about
              394  CALL_FUNCTION_2       2  '2 positional arguments'
              396  POP_TOP          

 L. 635       398  LOAD_GLOBAL              print
              400  LOAD_STR                 '\tnode='
              402  LOAD_FAST                'xio'
              404  LOAD_ATTR                env
              406  LOAD_METHOD              get
              408  LOAD_STR                 'node'
              410  CALL_METHOD_1         1  '1 positional argument'
              412  CALL_FUNCTION_2       2  '2 positional arguments'
              414  POP_TOP          

 L. 636       416  SETUP_LOOP          468  'to 468'
              418  LOAD_FAST                'xio'
              420  LOAD_ATTR                env
              422  LOAD_METHOD              items
              424  CALL_METHOD_0         0  '0 positional arguments'
              426  GET_ITER         
              428  FOR_ITER            466  'to 466'
              430  UNPACK_SEQUENCE_2     2 
              432  STORE_FAST               'k'
              434  STORE_FAST               'v'

 L. 637       436  LOAD_GLOBAL              print
              438  LOAD_STR                 '\tenv'
              440  LOAD_FAST                'k'
              442  LOAD_STR                 '.'
              444  LOAD_CONST               40
              446  LOAD_GLOBAL              len
              448  LOAD_FAST                'k'
              450  CALL_FUNCTION_1       1  '1 positional argument'
              452  BINARY_SUBTRACT  
              454  BINARY_MULTIPLY  
              456  LOAD_FAST                'v'
              458  CALL_FUNCTION_4       4  '4 positional arguments'
              460  POP_TOP          
          462_464  JUMP_BACK           428  'to 428'
              466  POP_BLOCK        
            468_0  COME_FROM_LOOP      416  '416'

 L. 638       468  LOAD_GLOBAL              print
              470  CALL_FUNCTION_0       0  '0 positional arguments'
              472  POP_TOP          

 L. 640       474  LOAD_FAST                'args'
              476  LOAD_ATTR                cmd
              478  LOAD_STR                 'run'
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   528  'to 528'

 L. 642       486  LOAD_FAST                'self'
              488  LOAD_ATTR                run
              490  BUILD_TUPLE_0         0 
              492  LOAD_FAST                'options'
              494  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              496  POP_TOP          

 L. 644       498  LOAD_CONST               0
              500  LOAD_CONST               None
              502  IMPORT_NAME              time
              504  STORE_FAST               'time'

 L. 645       506  SETUP_LOOP          524  'to 524'

 L. 646       508  LOAD_FAST                'time'
              510  LOAD_METHOD              sleep
              512  LOAD_CONST               0.1
              514  CALL_METHOD_1         1  '1 positional argument'
              516  POP_TOP          
          518_520  JUMP_BACK           508  'to 508'
              522  POP_BLOCK        
            524_0  COME_FROM_LOOP      506  '506'
          524_526  JUMP_FORWARD       1058  'to 1058'
            528_0  COME_FROM           482  '482'

 L. 648       528  LOAD_FAST                'args'
              530  LOAD_ATTR                cmd
              532  LOAD_STR                 'about'
              534  COMPARE_OP               ==
          536_538  POP_JUMP_IF_FALSE   620  'to 620'

 L. 650       540  LOAD_FAST                'args'
              542  LOAD_ATTR                param
          544_546  POP_JUMP_IF_TRUE    596  'to 596'

 L. 651       548  LOAD_GLOBAL              print
              550  LOAD_STR                 '\n======= about /'
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  POP_TOP          

 L. 652       556  LOAD_FAST                'pprint'
              558  LOAD_FAST                'self'
              560  LOAD_METHOD              about
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  LOAD_ATTR                content
              566  CALL_FUNCTION_1       1  '1 positional argument'
              568  POP_TOP          

 L. 653       570  LOAD_GLOBAL              print
              572  LOAD_STR                 '\n======= about www'
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  POP_TOP          

 L. 655       578  LOAD_FAST                'pprint'
              580  LOAD_FAST                'self'
              582  LOAD_METHOD              render
              584  LOAD_STR                 'ABOUT'
              586  CALL_METHOD_1         1  '1 positional argument'
              588  LOAD_ATTR                content
              590  CALL_FUNCTION_1       1  '1 positional argument'
              592  POP_TOP          
              594  JUMP_FORWARD       1058  'to 1058'
            596_0  COME_FROM           544  '544'

 L. 657       596  LOAD_FAST                'pprint'
              598  LOAD_FAST                'self'
              600  LOAD_METHOD              render
              602  LOAD_STR                 'ABOUT'
              604  LOAD_FAST                'args'
              606  LOAD_ATTR                param
              608  CALL_METHOD_2         2  '2 positional arguments'
              610  LOAD_ATTR                content
              612  CALL_FUNCTION_1       1  '1 positional argument'
              614  POP_TOP          
          616_618  JUMP_FORWARD       1058  'to 1058'
            620_0  COME_FROM           536  '536'

 L. 659       620  LOAD_FAST                'args'
              622  LOAD_ATTR                cmd
              624  LOAD_STR                 'api'
              626  COMPARE_OP               ==
          628_630  POP_JUMP_IF_FALSE   744  'to 744'

 L. 661       632  LOAD_FAST                'args'
              634  LOAD_ATTR                param
          636_638  JUMP_IF_TRUE_OR_POP   642  'to 642'
              640  LOAD_STR                 ''
            642_0  COME_FROM           636  '636'
              642  STORE_FAST               'path'

 L. 662       644  LOAD_FAST                'self'
              646  LOAD_METHOD              render
              648  LOAD_STR                 'API'
              650  LOAD_FAST                'path'
              652  CALL_METHOD_2         2  '2 positional arguments'
              654  STORE_FAST               'res'

 L. 663       656  LOAD_GLOBAL              print
              658  LOAD_FAST                'res'
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  POP_TOP          

 L. 664       664  LOAD_FAST                'self'
              666  LOAD_METHOD              render
              668  LOAD_STR                 'API'
              670  LOAD_FAST                'path'
              672  CALL_METHOD_2         2  '2 positional arguments'
              674  LOAD_ATTR                content
              676  STORE_FAST               'api'

 L. 665       678  LOAD_FAST                'api'
          680_682  POP_JUMP_IF_TRUE    688  'to 688'
              684  LOAD_ASSERT              AssertionError
              686  RAISE_VARARGS_1       1  'exception instance'
            688_0  COME_FROM           680  '680'

 L. 666       688  LOAD_FAST                'pprint'
              690  LOAD_GLOBAL              dict
              692  LOAD_FAST                'api'
              694  CALL_FUNCTION_1       1  '1 positional argument'
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  POP_TOP          

 L. 667       700  SETUP_LOOP          740  'to 740'
              702  LOAD_FAST                'api'
              704  LOAD_METHOD              items
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  GET_ITER         
              710  FOR_ITER            738  'to 738'
              712  UNPACK_SEQUENCE_2     2 
              714  STORE_FAST               'key'
              716  STORE_FAST               'val'

 L. 668       718  LOAD_GLOBAL              print
              720  LOAD_FAST                'key'
              722  LOAD_FAST                'val'
              724  LOAD_METHOD              get
              726  LOAD_STR                 'description'
              728  CALL_METHOD_1         1  '1 positional argument'
              730  CALL_FUNCTION_2       2  '2 positional arguments'
              732  POP_TOP          
          734_736  JUMP_BACK           710  'to 710'
              738  POP_BLOCK        
            740_0  COME_FROM_LOOP      700  '700'
          740_742  JUMP_FORWARD       1058  'to 1058'
            744_0  COME_FROM           628  '628'

 L. 670       744  LOAD_FAST                'args'
              746  LOAD_ATTR                cmd
              748  LOAD_STR                 'get'
              750  COMPARE_OP               ==
          752_754  POP_JUMP_IF_FALSE  1014  'to 1014'

 L. 672       756  LOAD_GLOBAL              param1
          758_760  JUMP_IF_TRUE_OR_POP   764  'to 764'
              762  LOAD_STR                 ''
            764_0  COME_FROM           758  '758'
              764  STORE_FAST               'path'

 L. 674       766  LOAD_GLOBAL              getattr
              768  LOAD_FAST                'self'
              770  LOAD_GLOBAL              method
              772  CALL_FUNCTION_2       2  '2 positional arguments'
              774  STORE_FAST               'h'

 L. 675       776  LOAD_FAST                'h'
              778  LOAD_FAST                'path'
              780  CALL_FUNCTION_1       1  '1 positional argument'
              782  STORE_FAST               'res'

 L. 676       784  LOAD_GLOBAL              print
              786  LOAD_GLOBAL              type
              788  LOAD_FAST                'res'
              790  LOAD_ATTR                content
              792  CALL_FUNCTION_1       1  '1 positional argument'
              794  CALL_FUNCTION_1       1  '1 positional argument'
              796  POP_TOP          

 L. 677       798  LOAD_GLOBAL              print
              800  CALL_FUNCTION_0       0  '0 positional arguments'
              802  POP_TOP          

 L. 678       804  LOAD_GLOBAL              print
              806  LOAD_STR                 '______________________________'
              808  CALL_FUNCTION_1       1  '1 positional argument'
              810  POP_TOP          

 L. 679       812  LOAD_GLOBAL              print
              814  CALL_FUNCTION_0       0  '0 positional arguments'
              816  POP_TOP          

 L. 680       818  LOAD_GLOBAL              print
              820  LOAD_STR                 '\trequest:\t'
              822  LOAD_GLOBAL              method
              824  LOAD_GLOBAL              repr
              826  LOAD_FAST                'path'
          828_830  JUMP_IF_TRUE_OR_POP   834  'to 834'
              832  LOAD_STR                 '/'
            834_0  COME_FROM           828  '828'
              834  CALL_FUNCTION_1       1  '1 positional argument'
              836  CALL_FUNCTION_3       3  '3 positional arguments'
              838  POP_TOP          

 L. 681       840  LOAD_GLOBAL              print
              842  LOAD_STR                 '\tresponse:\t'
              844  LOAD_FAST                'res'
              846  CALL_FUNCTION_2       2  '2 positional arguments'
              848  POP_TOP          

 L. 682       850  LOAD_GLOBAL              print
              852  LOAD_STR                 '\tresponse code:\t'
              854  LOAD_FAST                'res'
              856  LOAD_ATTR                status
              858  CALL_FUNCTION_2       2  '2 positional arguments'
              860  POP_TOP          

 L. 683       862  LOAD_GLOBAL              print
              864  LOAD_STR                 '\tresponse headers:\t'
              866  CALL_FUNCTION_1       1  '1 positional argument'
              868  POP_TOP          

 L. 684       870  SETUP_LOOP          914  'to 914'
              872  LOAD_GLOBAL              list
              874  LOAD_FAST                'res'
              876  LOAD_ATTR                headers
              878  LOAD_METHOD              items
              880  CALL_METHOD_0         0  '0 positional arguments'
              882  CALL_FUNCTION_1       1  '1 positional argument'
              884  GET_ITER         
              886  FOR_ITER            912  'to 912'
              888  UNPACK_SEQUENCE_2     2 
              890  STORE_FAST               'k'
              892  STORE_FAST               'v'

 L. 685       894  LOAD_GLOBAL              print
              896  LOAD_STR                 '\t\t'
              898  LOAD_FAST                'k'
              900  LOAD_STR                 ':'
              902  LOAD_FAST                'v'
              904  CALL_FUNCTION_4       4  '4 positional arguments'
              906  POP_TOP          
          908_910  JUMP_BACK           886  'to 886'
              912  POP_BLOCK        
            914_0  COME_FROM_LOOP      870  '870'

 L. 686       914  LOAD_GLOBAL              print
              916  LOAD_STR                 '\tresponse type:\t'
              918  LOAD_FAST                'res'
              920  LOAD_ATTR                content_type
              922  CALL_FUNCTION_2       2  '2 positional arguments'
              924  POP_TOP          

 L. 687       926  LOAD_GLOBAL              print
              928  LOAD_STR                 '\tcontent:\t'
              930  LOAD_FAST                'res'
              932  LOAD_ATTR                content
              934  CALL_FUNCTION_2       2  '2 positional arguments'
              936  POP_TOP          

 L. 688       938  LOAD_GLOBAL              print
              940  CALL_FUNCTION_0       0  '0 positional arguments'
              942  POP_TOP          

 L. 690       944  LOAD_GLOBAL              isinstance
              946  LOAD_FAST                'res'
              948  LOAD_ATTR                content
              950  LOAD_GLOBAL              list
              952  CALL_FUNCTION_2       2  '2 positional arguments'
          954_956  POP_JUMP_IF_TRUE    972  'to 972'
              958  LOAD_GLOBAL              isinstance
              960  LOAD_FAST                'res'
              962  LOAD_ATTR                content
              964  LOAD_GLOBAL              dict
              966  CALL_FUNCTION_2       2  '2 positional arguments'
          968_970  POP_JUMP_IF_FALSE   984  'to 984'
            972_0  COME_FROM           954  '954'

 L. 691       972  LOAD_FAST                'pprint'
              974  LOAD_FAST                'res'
              976  LOAD_ATTR                content
              978  CALL_FUNCTION_1       1  '1 positional argument'
              980  POP_TOP          
              982  JUMP_FORWARD       1006  'to 1006'
            984_0  COME_FROM           968  '968'

 L. 693       984  LOAD_GLOBAL              print
              986  LOAD_GLOBAL              str
              988  LOAD_FAST                'res'
              990  LOAD_ATTR                content
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  LOAD_CONST               0
              996  LOAD_CONST               500
              998  BUILD_SLICE_2         2 
             1000  BINARY_SUBSCR    
             1002  CALL_FUNCTION_1       1  '1 positional argument'
             1004  POP_TOP          
           1006_0  COME_FROM           982  '982'

 L. 695      1006  LOAD_GLOBAL              print
             1008  CALL_FUNCTION_0       0  '0 positional arguments'
             1010  POP_TOP          
             1012  JUMP_FORWARD       1058  'to 1058'
           1014_0  COME_FROM           752  '752'

 L. 697      1014  LOAD_FAST                'args'
             1016  LOAD_ATTR                cmd
         1018_1020  POP_JUMP_IF_FALSE  1050  'to 1050'

 L. 699      1022  LOAD_FAST                'self'
             1024  LOAD_METHOD              get
             1026  LOAD_STR                 'bin/%s'
             1028  LOAD_FAST                'args'
             1030  LOAD_ATTR                cmd
             1032  BINARY_MODULO    
           1034_0  COME_FROM           594  '594'
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  STORE_FAST               'h'

 L. 700      1038  LOAD_FAST                'pprint'
             1040  LOAD_FAST                'h'
             1042  LOAD_ATTR                content
             1044  CALL_FUNCTION_1       1  '1 positional argument'
             1046  POP_TOP          

 L. 706      1048  JUMP_FORWARD       1058  'to 1058'
           1050_0  COME_FROM          1018  '1018'

 L. 709      1050  LOAD_FAST                'self'
             1052  LOAD_METHOD              debug
             1054  CALL_METHOD_0         0  '0 positional arguments'
             1056  POP_TOP          
           1058_0  COME_FROM          1048  '1048'
           1058_1  COME_FROM          1012  '1012'
           1058_2  COME_FROM           740  '740'
           1058_3  COME_FROM           616  '616'
           1058_4  COME_FROM           524  '524'

Parse error at or near `COME_FROM' instruction at offset 1034_0