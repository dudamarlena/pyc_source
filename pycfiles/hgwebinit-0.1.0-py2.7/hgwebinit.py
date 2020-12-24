# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hgwebinit\hgwebinit.py
# Compiled at: 2013-01-24 19:17:22
"""An extension for hgweb that allows for repository creation.  Since the hg
wire protocol does not currently have support for doing remote init via HTTP,
this extension instead watches for push requests to non-existent repositories
and prompts the (duely authorized) user to create it.  Following that the push
continues as expected."""
import shutil, tempfile, unittest
from mercurial import hg, extensions, encoding, templater
from mercurial.hgweb import hgwebdir_mod
from mercurial.hgweb.common import ErrorResponse, HTTP_UNAUTHORIZED
from mercurial.hgweb.common import HTTP_METHOD_NOT_ALLOWED, HTTP_FORBIDDEN

def getLocalPathForVirtual(ui, path):
    pass


def path_is_a_repo(ui, path):
    pass


def should_create_repo(obj, req):
    """Check if the requested repository exists and if this is a push request.
    """
    virtual = req.env.get('PATH_INFO', '').strip('/')
    if virtual.startswith('static/') or 'static' in req.form:
        return False
    if not virtual:
        return False
    repos = dict(obj.repos)
    virtualrepo = virtual
    while virtualrepo:
        real = repos.get(virtualrepo)
        if real:
            return False
        up = virtualrepo.rfind('/')
        if up < 0:
            break
        virtualrepo = virtualrepo[:up]

    subdir = virtual + '/'
    if [ r for r in repos if r.startswith(subdir) ]:
        return False
    paths = {}
    for name, value in obj.ui.configitems('paths'):
        paths[name] = value

    if not path_is_in_collection(virtual, paths):
        return False
    return True


def hgwebinit_run_wsgi_wrapper(orig, obj, req):
    """Handles hgwebdir_mod requests, looking for pushes to non-existent repos.
    If one is detected, the user is first authorized and then prompted to init.
    Following that we simply hand the request off ot the next handler in the
    chain - typically hgwebdir_mod itself."""
    try:
        tmpl = obj.templater(req)
        ctype = tmpl('mimetype', encoding=encoding.encoding)
        ctype = templater.stringify(ctype)
        obj.refresh()
        if should_create_repo(obj, req):
            if create_allowed(obj.ui, req):
                virtual = req.env.get('PATH_INFO', '').strip('/')
                paths = {}
                for name, value in obj.ui.configitems('paths'):
                    paths[name] = value

                local = local_path_for_repo(virtual, paths)
                if obj.ui.configbool('web', 'implicit_init', False):
                    hg.repository(obj.ui, path=local, create=True)
                obj.lastrefresh = 0
    except ErrorResponse as err:
        req.respond(err, ctype)
        return tmpl('error', error=err.message or '')

    return orig(obj, req)


def uisetup(ui):
    """Hooks into hgwebdir_mod's run_wsgi method so that we can listen for
    requests."""
    extensions.wrapfunction(hgwebdir_mod.hgwebdir, 'run_wsgi', hgwebinit_run_wsgi_wrapper)


def create_allowed(ui, req):
    """Check allow_create and deny_create config options of a repo's ui object
    to determine user permissions.  By default, with neither option set (or
    both empty), deny all users to create new repos.  There are two ways a
    user can be denied create access:  (1) deny_create is not empty, and the
    user is unauthenticated or deny_create contains user (or *), and (2)
    allow_create is not empty and the user is not in allow_create.  Return True
    if user is allowed to read the repo, else return False.
    
    This is modeled on (copied almost verbatim) hg's read_allowed function."""
    user = req.env.get('REMOTE_USER')
    scheme = req.env.get('wsgi.url_scheme')
    if ui.configbool('web', 'push_ssl', True) and scheme != 'https':
        raise ErrorResponse(HTTP_FORBIDDEN, 'ssl required')
    deny = ui.configlist('web', 'deny_push')
    if deny and (not user or deny == ['*'] or user in deny):
        raise ErrorResponse(HTTP_UNAUTHORIZED, 'push not authorized')
    allow = ui.configlist('web', 'allow_push')
    result = allow and (allow == ['*'] or user in allow)
    if not result:
        raise ErrorResponse(HTTP_UNAUTHORIZED, 'push not authorized')
    deny_create = ui.configlist('web', 'deny_create', untrusted=True)
    if deny_create and (not user or deny_create == ['*'] or user in deny_create):
        raise ErrorResponse(HTTP_UNAUTHORIZED, 'create not authorized')
    allow_create = ui.configlist('web', 'allow_create', untrusted=True)
    result = allow_create == ['*'] or user in allow_create
    if not result:
        raise ErrorResponse(HTTP_UNAUTHORIZED, 'create not authorized')
    return True


def path_is_subrepo(path, conf_paths):
    for virt in conf_paths:
        local = conf_paths[virt]
        if path == virt:
            continue
        if local.endswith('**') or local.endswith('*'):
            continue
        if path.startswith(virt):
            return True

    return False


def path_is_in_collection(path, conf_paths):
    """Checks if path is contained within a set of given collection paths.  A 
    path is considered to be contained only if it is in a collection and only if
    the configured collection depth is appropriate for the path given.
    
    >>>path_is_in_collection('/', [('/howdy'], '/home/repos/howdy'))
    False
    >>>path_is_in_collection('/howdy', [('/howdy', '/home/repos/howdy')])
    False
    >>>path_is_in_collection('/howdy/hithere', [('/howdy', '/home/repos/*')])
    True
    >>>path_is_in_collection('/howdy/hithere/hello', [('/howdy', '/home/repos/*')])
    False
    >>>path_is_in_collection('/howdy/hithere/hello', [('/howdy', '/home/repos/**)'])
    True
    
    @param conf_paths: A dictionary of virtual-paths to local filesystem paths.
    """
    if path[0] != '/':
        path = '/' + path
    for virt in conf_paths:
        local = conf_paths[virt]
        if not (local.endswith('**') or local.endswith('*')):
            continue
        if path.startswith(virt):
            return True

    return False


def local_path_for_repo(path, conf_paths):
    import os.path
    if path[0] != '/':
        path = '/' + path
    for virt in conf_paths:
        local = conf_paths[virt]
        if local.endswith('*') and path == virt:
            continue
        if local.endswith('**'):
            local = local[:-3]
        else:
            if local.endswith('*'):
                local = local[:-2]
            if path.startswith(virt):
                p = os.path.normpath(path)
                v = os.path.normpath(virt)
                local = os.path.normpath(local)
                l = p.replace(v, local, 1)
                return l

    return


class TempDirTestCase(unittest.TestCase):
    """Base class for TestCases that allows for easily creating temporary
    directories and automatically deletes them on tearDown."""

    def setUp(self):
        self._on_teardown = []

    def make_temp_dir(self):
        temp_dir = tempfile.mkdtemp(prefix='tmp-%s-' % self.__class__.__name__)

        def tear_down():
            shutil.rmtree(temp_dir)

        self._on_teardown.append(tear_down)
        return temp_dir

    def tearDown(self):
        for func in reversed(self._on_teardown):
            func()


class Env(object):

    def __init__(self, env):
        self.env = env

    def get(self, key, default=None):
        if self.env.has_key(key):
            return self.env[key]
        else:
            return default


class UiMock(object):
    """A simple Mock for hg's ui object that allows access to configuration
    information."""

    def __init__(self, src=None, config=None):
        if config is None:
            config = {}
        self.config = config
        return

    def configlist(self, section, name, default=[], untrusted=False):
        val = self.config[section].get(name, default)
        if type(val) != list:
            val = [
             val]
        return val

    def configbool(self, section, name, default=False, untrusted=False):
        return self.config.get(section, {}).get(name, default)

    def copy(self):
        return self.__class__(self)

    def readconfig(self, filename, root=None, trust=False, sections=None, remap=None):
        pass

    def configitems(self, section, untrusted=False):
        s_dict = self.config.get(section, {})
        if s_dict is None:
            s_dict = {}
        return s_dict.items()


class RequestMock(object):
    """A simple Mock for hg's Request object.  It allows access to environment
    variables."""

    def __init__(self, env=None, form=None):
        self.env = env
        if env is None:
            self.env = {}
        self.form = form
        if form is None:
            self.form = {}
        return


class ModuleMock(object):

    def __init__(self, ui):
        self.ui = ui
        self.repos = []

    def refresh(self):
        pass


class PermissionCheckTests(TempDirTestCase):
    """Tests for user/client/connection permission to create repositories."""

    def setUp(self):
        """Set up some baseline configuration for hgwebinit."""
        TempDirTestCase.setUp(self)
        self.default_config = {'web': {'deny_create': [
                                 'deny_user'], 
                   'allow_create': [
                                  'allow_user'], 
                   'allow_push': '*'}}
        self.ui = UiMock(config=self.default_config)

    def tearDown(self):
        """Teardown."""
        TempDirTestCase.tearDown(self)

    def testDenyNoSsl(self):
        self.assertRaises(ErrorResponse, create_allowed, self.ui, RequestMock(env={'REMOTE_USER': 'allow2_user', 
           'REQUEST_METHOD': 'POST', 
           'wsgi.url_scheme': 'http'}))

    def testDenyHttpGet(self):
        self.assertRaises(ErrorResponse, create_allowed, self.ui, RequestMock(env={'REMOTE_USER': 'allow2_user', 
           'REQUEST_METHOD': 'GET', 
           'wsgi.url_scheme': 'https'}))

    def testDenyCreate(self):
        self.assertRaises(ErrorResponse, create_allowed, self.ui, RequestMock(env={'REMOTE_USER': 'deny_user', 
           'REQUEST_METHOD': 'POST', 
           'wsgi.url_scheme': 'https'}))

    def testAllowCreate(self):
        self.assertTrue(create_allowed(self.ui, RequestMock(env={'REMOTE_USER': 'allow_user', 
           'REQUEST_METHOD': 'POST', 
           'wsgi.url_scheme': 'https'})))

    def testDefaultCreate(self):
        """Test the case where the authenticated user isn't the list for either 
        of allow_create or deny_create but everything else passes.  The user
        should be denied, by default, from create a new repository.  Only 
        explicit permission will get the job done."""
        self.assertRaises(ErrorResponse, create_allowed, self.ui, RequestMock(env={'REMOTE_USER': 'allow2_user', 
           'REQUEST_METHOD': 'POST', 
           'wsgi.url_scheme': 'https'}))
        self.assertRaises(ErrorResponse, create_allowed, self.ui, RequestMock(env={'REMOTE_USER': 'deny2_user', 
           'REQUEST_METHOD': 'POST', 
           'wsgi.url_scheme': 'https'}))


class RepoDetectionTests(TempDirTestCase):
    """Tests for whether a repo should be created.  Assumes that request
    parameters are normal (POST with SSL)."""

    def setUp(self):
        """Set up some baseline configuration for hgwebinit."""
        TempDirTestCase.setUp(self)
        import os.path
        collectiondir = self.make_temp_dir()
        manycollectiondir = self.make_temp_dir()
        tmprepo = self.make_temp_dir()
        self.default_config = {'web': {'deny_create': [
                                 'deny_user'], 
                   'allow_create': [
                                  'allow_user'], 
                   'allow_push': '*'}, 
           'paths': {'/trunk2/short': os.path.join(collectiondir, '*'), 
                     '/trunk2/many': os.path.join(manycollectiondir, '**'), 
                     '/trunk1': tmprepo}}
        self.req = RequestMock(env={'REMOTE_USER': 'allow_user', 
           'REQUEST_METHOD': 'POST', 
           'wsgi.url_scheme': 'https'})
        self.ui = UiMock(config=self.default_config)
        self.mod = ModuleMock(self.ui)
        self.mod.repos = ['/trunk1']

    def tearDown(self):
        """Teardown."""
        TempDirTestCase.tearDown(self)

    def checkPath(self, path, mod=None, req=None):
        if mod is None:
            mod = self.mod
        if req is None:
            req = self.req
        req.env['PATH_INFO'] = path
        return should_create_repo(mod, req)

    def checkInCollection(self, path, ui=None):
        if ui is None:
            ui = self.ui
        return path_is_in_collection(path, ui.config['paths'])

    def testNonRepoPathRequests(self):
        """Given a URL for static resources, ensure the extension returns
        without creating a repo."""
        self.assertFalse(self.checkPath('/static/mystylesheet.css'))
        req = RequestMock(env={'REMOTE_USER': 'allow_user', 
           'REQUEST_METHOD': 'POST', 
           'wsgi.url_scheme': 'https'}, form={'static': True})
        self.assertFalse(self.checkPath('/', req=req))
        self.assertFalse(self.checkPath('/'))
        m = ModuleMock(self.ui)
        repos = [('trunk/test1', '')]
        m.repos += repos
        self.assertFalse(self.checkPath('/trunk/test1/', mod=m))
        m = ModuleMock(self.ui)
        repos = [('trunk/test1', '')]
        m.repos += repos
        self.assertFalse(self.checkPath('/trunk/test1/howdy.txt', mod=m))

    def testRepoPathRequest(self):
        """Given a request for an existing Repo, ensure the extension returns 
        without creating a repo."""
        req = RequestMock(env={'REMOTE_USER': 'allow_user', 
           'REQUEST_METHOD': 'GET', 
           'wsgi.url_scheme': 'http', 
           'PATH_INFO': '/trunk1'})
        m = ModuleMock(self.ui)
        self.assertFalse(should_create_repo(m, req))

    def testNonPushRequest(self):
        """For an otherwise acceptable, but non-push request, ensure the
        extension returns without creating a repo."""
        self.assertTrue(False)

    def testCreateOnCollection(self):
        """Allow for creation of repos within collections.
        Note: This is relying on repo detection to prevent a new repo from being
        created at the location of an existing one."""
        pass

    def testPathConflict(self):
        self.assertFalse(self.checkInCollection('/trunk2'))

    def testShallowChildOnShortCollection(self):
        self.assertTrue(self.checkInCollection('/trunk2/short/test1'))

    def testDeepChildOnShortCollection(self):
        self.assertTrue(self.checkInCollection('/trunk2/short/test2/test2'))

    def testShallowChildOnDeepCollection(self):
        self.assertTrue(self.checkInCollection('/trunk2/many/test3'))

    def testDeepChildOnDeepCollection(self):
        self.assertTrue(self.checkInCollection('/trunk2/many/test4/test4'))

    def testNonCollectionConflict(self):
        self.assertFalse(self.checkInCollection('/trunk1'))

    def testChildAtRoot(self):
        self.assertFalse(self.checkInCollection('/test1'))

    def testSubRepo(self):
        """Sub-repos must still be in a collection."""
        self.assertFalse(self.checkInCollection('/trunk1/newrepo'))

    def testSubRepoInCollection(self):
        self.assertTrue(self.checkInCollection('/trunk2/many/test1/newrepo'))


class RepoPathCreationTests(TempDirTestCase):

    def setUp(self):
        TempDirTestCase.setUp(self)
        import os.path
        self.collectiondir = self.make_temp_dir()
        self.manycollectiondir = self.make_temp_dir()
        self.tmprepo = self.make_temp_dir()
        self.paths = {'/trunk2/short': os.path.join(self.collectiondir, '*'), 
           '/trunk2/many': os.path.join(self.manycollectiondir, '**'), 
           '/trunk1': self.tmprepo}

    def checkPath(self, path, conf_paths=None):
        if conf_paths is None:
            conf_paths = self.paths
        return local_path_for_repo(path, conf_paths)

    def testRootPath(self):
        """Local path for a non-configured repo returns None."""
        self.assertEqual(None, self.checkPath('/test1'))
        return

    def testShallowContainedPath(self):
        import os.path
        self.assertEqual(os.path.join(self.collectiondir, 'test1'), self.checkPath('/trunk2/short/test1'))

    def testDeepContainedPath(self):
        import os.path
        self.assertEqual(os.path.join(self.collectiondir, 'test1', 'test2'), self.checkPath('/trunk2/short/test1/test2'))

    def testSubRepoPath(self):
        import os.path
        self.assertEqual(os.path.join(self.tmprepo, 'test1', 'test2'), self.checkPath('/trunk1/test1/test2'))


class SubRepoTests(TempDirTestCase):

    def setUp(self):
        TempDirTestCase.setUp(self)
        import os.path
        self.collectiondir = self.make_temp_dir()
        self.manycollectiondir = self.make_temp_dir()
        self.tmprepo = self.make_temp_dir()
        self.paths = {'/trunk2/short': os.path.join(self.collectiondir, '*'), 
           '/trunk2/many': os.path.join(self.manycollectiondir, '**'), 
           '/trunk1': self.tmprepo}

    def testPathIsSubRepo(self):
        self.assertTrue(path_is_subrepo('/trunk1/test1', self.paths))
        self.assertTrue(path_is_subrepo('/trunk1/test1/test2', self.paths))

    def testPathIsRepo(self):
        self.assertFalse(path_is_subrepo('/trunk1', self.paths))

    def testPathIsInCollection(self):
        self.assertFalse(path_is_subrepo('/trunk2/short/howdy1', self.paths))
        self.assertFalse(path_is_subrepo('/trunk2/many/howdy1', self.paths))
        self.assertFalse(path_is_subrepo('/trunk2/many/howdy1/howdy2', self.paths))

    def testPathAtRoot(self):
        self.assertFalse(path_is_subrepo('/', self.paths))
        self.assertFalse(path_is_subrepo('/test1', self.paths))