# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/resource.py
# Compiled at: 2018-12-16 14:01:49
# Size of source mod 2**32: 30290 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import os, sys, traceback, collections, hashlib, base64, uuid, yaml, copy, json, requests, inspect
from pprint import pprint
from .handlers import DirectoryHandler, pythonResourceHandler, pythonCallableHandler
from .request import Request, Response
from xio.core.lib import utils
from xio.core import env
from functools import wraps, update_wrapper
is_string = utils.is_string
ABOUT_APP_PUBLIC_FIELDS = [
 'description', 'links', 'provide', 'configuration', 'links', 'profiles', 'network', 'methods', 'options', 'resources', 'scope']
RESOURCES_DEFAULT_ALLOWED_OPTIONS = [
 'HEAD', 'ABOUT', 'CHECK', 'API']

def client(*args, **kwargs):
    res = resource(*args, **kwargs)
    res.__CLIENT__ = True
    return res


def resource(handler=None, context=None, about=None, **kwargs):
    basepath = ''
    is_client = False
    if isinstance(handler, Resource):
        is_client = True
        handler = pythonResourceHandler(handler)
    else:
        if isinstance(handler, collections.Callable):
            handler = pythonCallableHandler(handler)
        else:
            if handler and is_string(handler):
                is_client = True
                handler, basepath = env.resolv(handler)
                if isinstance(handler, Resource):
                    resource = client(handler, context, **kwargs)
                    return resource
            elif handler:
                handler = pythonObjectHandler(handler)
    res = Resource(handler=handler, handler_path=basepath, handler_context=context, about=about, **kwargs)
    res.__CLIENT__ = is_client
    return res


def bind(path):
    """
    method decorator for auto binding class method to path
    """

    def _(func):
        setattr(func, '__xio_path__', path)
        return func

    return _


def getResponse(res, req, func):
    return req.send(lambda req: func(res, req))


def fixAbout(about):
    options = about.pop('options', [])
    if not isinstance(options, list):
        options = [o.strip().upper() for o in options.split(',')]
    if '*' in options:
        about['proxy'] = True
        options = RESOURCES_DEFAULT_ALLOWED_OPTIONS
    scope = about.pop('scope', [])
    if not isinstance(scope, list):
        scope = [s.strip().lower() for s in scope.split(',')]
    about.setdefault('options', options)
    about.setdefault('scope', scope)
    about.setdefault('methods', {})
    about.setdefault('routes', {})
    oldtype = about.pop('type', None)
    oldmethod = about.pop('method', '')
    oldinput = about.pop('input', {})
    oldoutput = about.pop('output', {})
    if oldinput:
        if not oldmethod:
            oldmethod = 'get,post'
    if oldmethod:
        for m in oldmethod.split(','):
            method = m.strip().upper()
            about['methods'][method] = {}
            if oldinput:
                about['methods'][method]['input'] = oldinput
            if oldoutput:
                about['methods'][method]['output'] = oldoutput

    for key in about['methods']:
        if key not in about['options']:
            about['options'].append(key)

    about.pop('output', None)
    about.pop('input', None)
    about.pop('method', None)
    return about


def extractAbout(h):
    about = {}
    if isinstance(h, str) and h.startswith('/'):
        if os.path.isfile(h):
            with open(h) as (f):
                raw = f.read()
            about = yaml.load(raw)
    else:
        about = h if isinstance(h, dict) else {}
        about = about or {}
        docstring = h.__doc__ if (h and (is_string(h) or isinstance)(h, collections.Callable)) else h
        if docstring:
            if is_string(docstring):
                try:
                    about = yaml.load(docstring)
                    assert isinstance(about, dict)
                    version = about.get('version')
                    if not version:
                        if not 'type' in about:
                            if not 'implement' in about:
                                if not 'methods' in about:
                                    if not 'options' in about:
                                        if not 'resources' in about:
                                            if not 'description':
                                                assert 'cache' in about
                except Exception as err:
                    try:
                        about = {}
                    finally:
                        err = None
                        del err

        return fixAbout(about)


def handleRequest(func):
    """
    handle
        -> automatic converion of input to req object
        -> automatic converion of result to res object
        -> prevent req.path modification by handlers
    """

    @wraps(func)
    def _(self, method, *args, **kwargs):
        if not isinstance(method, Request):
            if not args:
                path, data = (None, None)
            else:
                if len(args) == 1:
                    path, data = (args[0], None) if is_string(args[0]) else (None, args[0])
                else:
                    if len(args) == 2:
                        path, data = args
                    else:
                        path = args[0]
                        data = args[1]
        else:
            path = path or ''
            if path:
                if path[0] == '/':
                    path = path[1:]
                else:
                    kwquery = kwargs.pop('query', None)
                    kwdata = kwargs.pop('data', None)
                    if method == 'GET':
                        query = data or kwquery
                        data = None
                    else:
                        query = kwquery
                    data = data or kwdata
                client = self.context.get('client')
                req = Request(method, path, data=data, query=query, client_context=self._handler_context, client=client, server=self._root, **kwargs)
            else:
                req = method
                req._stack.append(self)
            if not (req and isinstance(req, Request)):
                raise AssertionError
            assert is_string(req.method)
            ori_path = req.path
            req.context['resource'] = self
            req.context['root'] = self._root
            req.context['debug'] = kwargs.get('debug')
            if kwargs.get('skiphandler'):
                req.context['skiphandler'] = kwargs.get('skiphandler')
            resp = getResponse(self, req, func)
            req.path = isinstance(resp, Resource) or ori_path
            resp = self._toResource(req, resp)
        assert isinstance(resp, Resource)
        assert not isinstance(resp.content, Resource)
        return resp

    return _


def handleAuth(func):

    @wraps(func)
    def _(self, req):
        if not self.__CLIENT__:
            if not req.OPTIONS:
                if req.fullpath.startswith('xio/admin'):
                    req.require('auth', 'xio/ethereum')
                    req.require('scope', 'admin')
            if not req.ABOUT:
                required_scope = self._about.get('scope')
                if required_scope:
                    pass
        result = getResponse(self, req, func)
        resp = req.response
        if self.__CLIENT__:
            if resp.status in (401, 402, 403):
                peer = self.context.get('client')
                if hasattr(peer, 'key') and hasattr(peer.key, 'private'):
                    if resp.status in (401, 403):
                        auhtenticate = resp.headers.get('WWW-Authenticate')
                        if auhtenticate:
                            if 'realm' in auhtenticate:
                                realm = auhtenticate.split('=').pop().strip().replace('"', '')
                                scheme = realm.split('/').pop()
                            else:
                                scheme = auhtenticate.split(' ').pop(0).split('/').pop()
                            token = peer.key.generateToken(scheme)
                            authorization = 'bearer %s' % token.decode()
                            self._handler_context['authorization'] = authorization
                            req.headers['Authorization'] = authorization
                            req.init()
                            result = getResponse(self, req, func)
                    if resp.status == 402:
                        peer = self.context.get('client')
                        signed = peer.key.account('ethereum').signTransaction(resp.content)
                        kwargs.setdefault('headers', {})
                        req.headers['XIO-Signature'] = signed
                        result = getResponse(self, req, func)
        return result

    return _


def handleHooks(func):

    @wraps(func)
    def _(self, req):
        if not self._hooks:
            return func(self, req)
        flow = copy.copy(self._hooks)
        flow.append(lambda req: func(self, req))

        def _():
            h = flow.pop(0)
            return h(req)

        setattr(req, 'execute', _)
        return req.execute()

    return _


def handleDelegate(func):

    @wraps(func)
    def _(self, req):
        skiphandler = req.context.get('skiphandler') and self._skip_handler_allowed
        must_delegate = self._handler and isinstance(self._handler, collections.Callable) and not skiphandler
        if must_delegate:
            if not self.__CLIENT__:
                if req.ABOUT or req.API:
                    if not req.path:
                        if self._about:
                            if 'ABOUT' not in self._about.get('options'):
                                must_delegate = False
        if req.OPTIONS:
            if not req.path:
                must_delegate = False
        req.response.status = 0
        if must_delegate:
            if req.path:
                c, p, u = self._getChild(req.path)
                must_delegate = not bool(c)
        if must_delegate:
            result = self._callhandler(req)
            req.response.status = req.response.status or 200
            req.response.content = result
            if req.response.content == req.PASS:
                req.response.status = 0
                req.response.content = None
        return func(self, req)

    return _


class Resource(object):
    __CLIENT__ = False
    __XMETHODS__ = True
    _skip_handler_allowed = True
    _tests = None
    _about = None
    traceback = None

    def __init__(self, content=None, path='', status=0, headers=None, parent=None, root=None, handler=None, handler_path=None, handler_context=None, about=None, **context):
        if root:
            assert isinstance(root, Resource)
        self.path = path
        self.content = content
        self.status = status
        self.headers = headers or {}
        self.content_type = self.headers.get('Content-Type')
        self._handler = handler if handler else self.content if (self.content and isinstance(self.content, collections.Callable)) else None
        self._handler_path = handler_path
        self._handler_context = handler_context or {}
        self._parent = parent
        self._root = root or (parent._root if parent else self)
        self._children = collections.OrderedDict()
        self._hooks = []
        if not self._about:
            self._about = extractAbout(about or self._handler or self.content)
        self.context = context

    def options(self, *args, **kwargs):
        return (self.request)('OPTIONS', *args, **kwargs)

    def head(self, *args, **kwargs):
        return (self.request)('HEAD', *args, **kwargs)

    def connect(self, *args, **kwargs):
        return (self.request)('CONNECT', *args, **kwargs)

    def get(self, *args, **kwargs):
        return (self.request)('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return (self.request)('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return (self.request)('PUT', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return (self.request)('PATCH', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return (self.request)('DELETE', *args, **kwargs)

    def about(self, *args, **kwargs):
        return (self.request)('ABOUT', *args, **kwargs)

    def check(self, *args, **kwargs):
        return (self.request)('CHECK', *args, **kwargs)

    def api(self, *args, **kwargs):
        return (self.request)('API', *args, **kwargs)

    def test(self, *args, **kwargs):
        return (self.request)('TEST', *args, **kwargs)

    def debug(self, show=True):
        result = []
        for key in self._children:
            res = self.get(key)
            result.append(res)
            result += res.debug(show=False)

        if show:
            for res in result:
                cls = res.__class__.__name__
                content = res.content
                children = res.content
                path = res.path
                colurn = res.path

        return result

    def _hasabstract(self):
        if self._abstactchildname == None:
            self._abstactchildname == False
            for k, v in list(self._children.items()):
                if k[0] == ':':
                    self._abstactchildname = k

        return self._abstactchildname

    def _getChild(self, path):
        pathdata = {}
        p = path.split('/')
        childname = p.pop(0)
        postpath = '/'.join(p)
        child = self._children.get(childname)
        if not child:
            for k, v in list(self._children.items()):
                if k[0] == ':':
                    return (
                     v, postpath, {k: childname})

        return (
         child, postpath, pathdata)

    def _toResource(self, req, resp, handler_path=None):
        if not isinstance(resp, Response):
            result = resp
            resp = req.response
            if not resp.status:
                resp.status = 200
            resp.content = result
        elif self.path:
            path = self.path + '/' + req.path if req.path else self.path
        else:
            path = req.path
        content = resp.content if resp else None
        status = resp.status if resp else 404
        res = copy.copy(self)
        res.path = path
        res.content = content
        res.content_type = resp.headers.get('Content-Type')
        res.headers = resp.headers
        res.status = status
        res.traceback = resp.traceback if resp else None
        res._handler_path = handler_path
        return res

    def resource(self, relativepath, status=200, content=None, headers=None, handler_path=None):
        if self.path:
            path = self.path + '/' + relativepath if relativepath else self.path
        else:
            path = relativepath
        headers = headers or {}
        res = copy.copy(self)
        res.path = path
        res.content = content
        res.content_type = headers.get('Content-Type')
        res.headers = headers
        res.status = status
        res._handler_path = handler_path
        return res

    @handleRequest
    @handleAuth
    @handleHooks
    @handleDelegate
    def request(self, req):
        if not isinstance(req, Request):
            raise AssertionError
        else:
            assert is_string(req.method)
            if req.response.status != 0:
                if isinstance(req.response.content, Resource):
                    return req.response.content
                    handler_path = self._handler_path + '/' + req.path if self._handler_path else req.path
                    resp = req.response
                else:
                    pass
            resp = self._defaultHandler(req)
            handler_path = None
        if isinstance(resp, Resource):
            return resp
        return self._toResource(req, resp, handler_path)

    def render(self, req):
        """
        generic methode for server side public resource delivery
        for app this method add 'www' path prefix + add common feature
        """
        return self.request(req)

    def _callhandler(self, req):
        ori_path = req.path
        if req.method == 'GET':
            if not req.path:
                if req.query == None:
                    return self
        if self._handler_path:
            req.path = self._handler_path + '/' + req.path if req.path else self._handler_path
        options = self._about.get('options', [])
        method = req.xmethod or req.method
        if not req.path:
            if req.ABOUT:
                if options:
                    if 'ABOUT' not in options:
                        return req.PASS
        mod_proxy = self._about.get('proxy', False)
        if not mod_proxy:
            if not req.path:
                if not req.OPTIONS:
                    if options:
                        if not method in options:
                            assert method in RESOURCES_DEFAULT_ALLOWED_OPTIONS, Exception(405)
            params = self._about.get('methods', {}).get(method, {}).get('input', {}).get('params', [])
            mapping = {'integer':int, 
             'float':float, 
             'text':str}
            for param in params:
                name = param.get('name')
                paramtype = param.get('type')
                required = param.get('required')
                default = param.get('default')
                pattern = param.get('pattern')
                value = req.input.get(name)
                if not value:
                    if required:
                        raise AssertionError(Exception(400, 'Missing required parameter : %s' % name))
                if paramtype and not value == None:
                    assert isinstance(value, mapping.get(paramtype)), Exception(400, 'Wrong datatype parameter : %s' % name)
                    if pattern and value:
                        import re
                        rpattern = re.compile(pattern)
                        assert re.match(rpattern, value), Exception(400, 'Wrong format parameter : %s' % name)

        result = self._handler(req)
        req.path = ori_path
        return result

    def _defaultHandler(self, req):
        method = req.xmethod or req.method
        path = req.path
        data = req.data
        must_redirect = bool(path)
        put_context = req.PUT and path and '/' not in path
        if must_redirect:
            res, postpath, urldata = self._getChild(path)
            if res == None:
                if method == 'PUT':
                    if '/' in path:
                        p = path.split('/')
                        childname = p.pop(0)
                        postpath = '/'.join(p)
                        res = self.put(childname)
            if res != None:
                if isinstance(req.input, dict):
                    req.context.update(urldata)
                req.path = postpath
                return res.request(req)
            if not put_context:
                return self.resource(path, content=None, status=404)
        name = path
        assert '/' not in name
        if method == 'ABOUT':
            return self._handleAbout(req)
        if method == 'CHECK':
            return self._handleCheck(req)
        if method == 'TEST':
            return self._handleTest(req)
        if method == 'API':
            return self._handleApi(req)
        if method == 'GET':
            return self
        if method == 'PUT':
            if not name:
                self.content = data
                if isinstance(data, collections.Callable):
                    self._handler = data
                    self._about = extractAbout(self._handler)
            else:
                return self
                if not name:
                    raise AssertionError
                else:
                    path = self.path + '/' + name if self.path else name
                    import xio
                    from xio.core.app.app import App
                    if isinstance(data, App):
                        child = xio.client(data)
                    else:
                        if isinstance(data, Resource):
                            child = data
                        else:
                            child = Resource(path=path, content=data, status=201, parent=self)
            self._children[name] = child
            return self._children[name]

    def __getattr__(self, name):
        if name[0] != '_':
            if self.__CLIENT__ and self.__XMETHODS__:
                setattr(self, name, lambda *args, **kwargs: (self.request)(name.upper(), *args, **{'data': kwargs}))
            else:
                if self.content:
                    if hasattr(self.content, name):
                        return getattr(self.content, name)
                if self._handler:
                    setattr(self, name, lambda *args, **kwargs: (self.request)(name.upper(), *args, **{'data': kwargs}))
        return object.__getattribute__(self, name)

    def __repr__(self):
        return '%s %s #%s %s %s [%s] %s' % ('CLI' if self.__CLIENT__ else '', self.__class__.__name__.upper(), id(self), repr(self.path), self._handler or 'nohandler', self.status, str(self.content)[0:50] + '...')

    def __call__(self, *args, **kwargs):
        return (self.content)(*args, **kwargs)

    def __iter__(self):
        return iter(self.content)

    def bind(self, *args, **kwargs):
        if len(args) > 1:
            path = args[0]
            content = args[1]
            kwargs['skiphandler'] = True
            return (self.put)(path, content, **kwargs)

        def _wrapper(func):
            path = args[0]
            kwargs['skiphandler'] = True
            return (self.put)(path, func, *args, **kwargs)

        return _wrapper

    def hook(self, path, *args, **kwargs):

        def _(func):
            target = self.resource(path)
            target._hooks.insert(0, func)
            return target

        return _

    def oldhook(self, path, *args, **kwargs):

        class _hookwrapper:

            def __init__(self, h, ori):
                self.h = h
                self.ori = ori

            def __call__(self, req):
                setattr(req, 'hook', self.ori)
                return self.h(req)

        def _(func):
            target = self.get(path)
            target.content = _hookwrapper(func, target.content)
            return target

        return _

    def publish(self, message):
        self._root.publish(self.path, message)

    def _handleAbout(self, req):
        about = copy.copy(self._about)
        root = req.context.get('root')
        fullpath = req.fullpath.replace('/', '')
        from .peer import Peer
        peerserver = self._root or req.server or root
        add_peerinfo = peerserver and isinstance(self, Peer) or fullpath == 'www' or self.path == 'www'
        if add_peerinfo:
            if peerserver:
                about['id'] = peerserver.id
                about['name'] = peerserver.name
                for k in ABOUT_APP_PUBLIC_FIELDS:
                    if peerserver._about and k in peerserver._about:
                        about[k] = peerserver._about[k]

            about['type'] = self.__class__.__name__.lower() if not peerserver else peerserver.__class__.__name__.lower()
        about.setdefault('resources', {})
        for childname, child in list(self._children.items()):
            about['resources'][childname] = {}

        return about

    def _handleCheck(self, req):
        results = {}
        try:
            about = self.about().content
            assert isinstance(about, dict)
            result = (200, '')
        except Exception as err:
            try:
                result = (
                 500, err)
            finally:
                err = None
                del err

        results['about'] = result
        return results

    def _handleApi(self, req):
        api = collections.OrderedDict()
        about = self.about().content
        methods = about.get('methods', {})
        routes = about.get('resources', {})
        description = about.get('description')
        info = {}
        if description:
            info['description'] = description
        if methods:
            info['methods'] = collections.OrderedDict()
            for method, methodinfo in list(methods.items()):
                info['methods'][method] = methodinfo

        api['/'] = info
        for childpath, info in routes.items():
            childapi = self.api(childpath).content or {}
            for cpath, cinfo in list(childapi.items()):
                if cpath[(-1)] == '/':
                    cpath = cpath[:-1]
                cpath = '/' + childpath + cpath
                api[cpath] = cinfo

        return api

    def _handleTest(self, req):
        tests = self._about.get('tests', [])
        results = []
        for test in tests:
            try:
                method = test.get('method', 'GET')
                path = test.get('path', '')
                query = test.get('input', {})
                req = Request(method, path, query=query)
                resp = self.request(req)
                assertions = test.get('assert')
                if assertions.get('content'):
                    raise resp.content and str(assertions.get('content')) in str(resp.content) or AssertionError
                if assertions.get('status'):
                    assert int(assertions.get('status')) == resp.status
                result = {'status': 200}
            except Exception as err:
                try:
                    result = {'status':500, 
                     'error':err}
                finally:
                    err = None
                    del err

            results.append(result)

        return results

    def debug(self):
        res = self
        RESET_SEQ = '\x1b[0m'
        COLOR_SEQ = '\x1b[1;%dm'
        BOLD_SEQ = '\x1b[1m'
        CODE_BACKGROUND = 40
        CODE_FOREGROUND = 30
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = list(range(8))
        BOLD = -1

        def colorize(txt, code, background=False):
            if code == BOLD:
                return BOLD_SEQ + txt + RESET_SEQ
            if code:
                TYPE = CODE_BACKGROUND if background else CODE_FOREGROUND
                return COLOR_SEQ % (TYPE + code) + txt + RESET_SEQ
            return txt

        def _map(res, stack):
            try:
                cls = res.__class__.__name__
                content = res.content
                children = res.content
                import inspect
                if content and inspect.isclass(content):
                    content = colorize(str(content)[0:50], YELLOW)
                else:
                    if content and is_string(content):
                        content = colorize(str(content)[0:50], RED)
                    else:
                        if content and isinstance(content, collections.Callable):
                            content = colorize(str(content)[0:50], GREEN)
                        else:
                            content = str(content)[0:50] if content else ''
                path = []
                colouredpath = []
                for k, v in stack:
                    path.append(k)
                    if isinstance(v, Resource):
                        colouredpath.append(colorize(k, BLUE))
                    else:
                        colouredpath.append(colorize(k, CYAN))

                path = '/'.join([v[0] for v in stack])
                colurn = colorize(path, BLUE)
                print('\t', colurn, '.' * (60 - len(path)), cls.upper()[0:3] + ' ' + str(id(res)) + ' %s ' % res.status + ' ' * (10 - len(cls)), content or '')
                if isinstance(res, Resource):
                    children = res._children
                    keys = list(children.keys())
                    keys.sort()
                    for name in keys:
                        child = children.get(name)
                        _map(child, stack + [(name, child)])

            except Exception as err:
                try:
                    print(('\tERR', err, '...', res))
                finally:
                    err = None
                    del err

        print('\n______ DEBUG ______\n')
        print('\tresource     :', self)
        print('\tpath         :', self.path)
        print('\thandler      :', self._handler)
        print('\thandler_path :', self._handler_path)
        print('\tcontext      :', self.context)
        print('\tabout        :', self._about)
        print('\tchildren     :', list(self._children.keys()))
        _map(self, [])
        print('\n______ /DEBUG ______\n')