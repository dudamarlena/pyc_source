# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/restresource/__init__.py
# Compiled at: 2007-09-24 16:48:57
"""
restresource

cherrypy controller mixin to make it easy to build REST applications.

handles nested resources and method-based dispatching.

here's a rough sample of what a controller would look like using this:

cherrypy.root = MainController()
cherrypy.root.user = UserController()

class PostController(RESTResource):
    def read(self,post):
        return post.as_html()
    read.expose_resource = True

    def delete(self,post):
        post.destroySelf()
        return "ok"
    delete.expose_resource = True

    def update(self,post,title="",body=""):
        post.title = title
        post.body = body
        return "ok"
    update.expose_resource = True

    def create(self, post, title="", body="")
        post.title = title
        post.body = body
        return "ok"
    create.expose_resource = True

    def REST_instantiate(self, slug, **kwargs):
        try:
            user = self.parents[0]
            return Post.select(Post.q.slug == slug, Post.q.userID = user.id)[0]
        except:
            return None

    def REST_create(self, slug, **kwargs):
        user = self.parents[0]
        return Post(slug=slug,user=user)

class UserController(RESTResource):
    REST_children = {'posts' : PostController()}

    def read(self,user):
        return user.as_html()
    read.expose_resource = True

    def delete(self,user):
        user.destroySelf()
        return "ok"
    delete.expose_resource = True

    def update(self,user,fullname="",email=""):
        user.fullname = fullname
        user.email = email
        return "ok"
    update.expose_resource = True

    def create(self, user, fullname="", email=""):
        user.fullname = fullname
        user.email = email
        return "ok"
    create.expose_resource = True

    def get_extra_action(self,user):
        # do something else
    get_extra_action.expose_resource = True

    def REST_instantiate(self, username, **kwargs):
        try:
            return User.byUsername(username)
        except:
            return None

    def REST_create(self, username, **kwargs):
        return User(username=username)

then, the site would have urls like:

    /user/bob
    /user/bob/posts/my-first-post
    /user/bob/posts/my-second-post
    /user/bob/extra_action

which represent REST resources. calling 'GET /user/bob' would call the read() method on UserController
for the user bob. 'PUT /user/joe' would create a new user with username 'joe'. 'DELETE /user/joe'
would delete that user. 'GET /user/bob/posts/my-first-post' would call read() on the Post Controller
with the post with the slug 'my-first-post' that is owned by bob.

There are actually two URL scheme options.  Note that the first corresponds to the scheme above, as well.
Scheme One (default) --this follows 'WSGI Collection' semicolon rules
    REST_ids_are_root = True
    /user/bob;extra_action OR /user/bob/extra_action

Scheme Two:
    If you put the following in your RESTResource class:
    REST_ids_are_root = False
    /user;bob/extra_action OR /user/;bob/extra_action

    This has the advantage of making both the collection and the members 'context'
    resources, meantin at /user;bob/ you can send a relative-url for 'extra_action'
    and it will go to the expected location.
"""
import cherrypy

def strip_empty(path):
    return [ e for e in path if e != '' ]


class RESTResource:
    REST_defaults = {'DELETE': 'delete', 'GET': 'read', 
       'POST': 'update', 
       'PUT': 'create'}
    REST_map = {}
    REST_children = {}
    parents = []
    REST_content_types = {}
    REST_default_content_type = ''
    REST_ids_are_root = True

    def CT_dispatch(self, d):
        method = cherrypy.request.method
        if method != 'GET':
            return d
        if cherrypy.request.headerMap.has_key('Accept'):
            accept = cherrypy.request.headerMap['Accept']
            if self.REST_content_types.has_key(accept):
                m = self.REST_content_types[accept]
                if hasattr(self, m):
                    cherrypy.response.headerMap['Content-Type'] = accept
                    return getattr(self, m)(d)
        if self.REST_default_content_type != '':
            if self.REST_content_types.has_key(self.REST_default_content_type):
                m = self.REST_content_types[self.REST_default_content_type]
                if hasattr(self, m):
                    cherrypy.response.headerMap['Content-Type'] = self.REST_default_content_type
                    return getattr(self, m)(d)
        return d

    def REST_childOverride(self, child_obj, *resources):
        """If this is overridden in a subclass, you can:
           1. return a non-false value which will override child responses
           2. decorate the child further (e.g. a la obj.parents)
           This should be useful if, for example, you want security
           restrictions to be inherited
        """
        return False

    def REST_collection_dispatch(self, func_params, **params):
        collection_method = cherrypy.request.method.lower()
        if func_params:
            param_method = ('_').join((collection_method,
             func_params[0]))
            if hasattr(self, param_method):
                collection_method = param_method
                func_params.pop(0)
        m = getattr(self, collection_method, self.list)
        if getattr(m, 'exposed', False):
            return self.CT_dispatch(m(**params))
        else:
            raise cherrypy.NotFound

    def REST_dispatch(self, resource, func_params, **params):
        method = cherrypy.request.method
        param_method = None
        if func_params:
            param_method = method.lower() + '_' + func_params[0]
        if param_method and hasattr(self, param_method):
            m = getattr(self, param_method)
            func_params.pop(0)
        elif self.REST_map.has_key(method):
            m = getattr(self, self.REST_map[method])
        elif self.REST_defaults.has_key(method):
            m = getattr(self, self.REST_defaults[method], getattr(self, 'index', None))
        if m and getattr(m, 'expose_resource', False):
            return m(resource, **params)
        raise cherrypy.NotFound
        return

    def parse_resource_token(self, token):
        resource_params = token.split(';')
        resource_name = resource_params.pop(0)
        return (resource_name, resource_params)

    @cherrypy.expose
    def default(self, *vpath, **params):
        """This method will get called by default by CherryPy when it can't
        map an object path directly (a.b.c for request /a/b/c) which if we have
        RESTful urls (interspersed with id's) will be most of the time.

        Before this would only be inherited by sub-Root controllers, but to handle
        situations like /a;1/ or /a;add_form it needs to be sub-classed by the
        Root Controller now.

        So default() now simply handles one token between /'s and other
        methods dispatch handling

        * pass resource to sub-object (update obj.parents first)
        * call local method
        * getresource(id)
        * continue down vpath
        """
        if vpath:
            vpath = list(vpath)
            vpath = strip_empty(vpath)
            if self in cherrypy.tree.mount_points.values():
                (rname, rparams) = self.parse_resource_token(vpath.pop(0))
                return self.map_vpath([], rname, rparams, vpath, params)
        return self.collection_dispatcher(None, [], vpath, params)

    def collection_dispatcher(self, myname, resource_params, vpath, params):
        resources = []
        if resource_params:
            if not self.REST_ids_are_root:
                resources.append(self.getresource(resource_params, params))
        if vpath:
            (rname, rparams) = self.parse_resource_token(vpath.pop(0))
            if self.REST_ids_are_root:
                if rname:
                    resources.append(self.getresource((rname,), params))
                    rname = None
                if vpath:
                    (rname, rparams) = self.parse_resource_token(vpath.pop(0))
            elif not self.REST_ids_are_root and not rname and rparams:
                resources.append(self.getresource(rparams, params))
                if vpath:
                    (rname, rparams) = self.parse_resource_token(vpath.pop(0))
            if rname:
                return self.map_vpath(resources, rname, rparams, vpath, params)
            elif self.REST_ids_are_root:
                resource_params.extend(rparams)
        if not self.REST_ids_are_root:
            resource_params = []
        if not resource_params and cherrypy.request.method == 'GET' and not cherrypy.request.path.endswith('/'):
            atoms = cherrypy.request.browser_url.split('?', 1)
            newUrl = atoms.pop(0) + '/'
            if atoms:
                newUrl += '?' + atoms[0]
            raise cherrypy.HTTPRedirect(newUrl)
        if resources:
            return self.REST_dispatch(resources[0], resource_params, **params)
        else:
            return self.REST_collection_dispatch(resource_params, **params)
        return

    def getresource(self, resource_params, params):
        """not doing anything with resource_params
        this could in theory be sent along to REST_* functions
        it is named without an '_' to avoid clobber from a '/col/;resource' hook
        """
        resource = self.REST_instantiate(resource_params[0], **params)
        if resource is None:
            if cherrypy.request.method in ('PUT', 'POST'):
                resource = self.REST_create(resource_params[0], **params)
            else:
                raise cherrypy.NotFound
        return resource

    def map_vpath(self, resources, a, rparams, vpath, params):
        obj = None
        if self.REST_children.has_key(a):
            obj = self.REST_children[a]
        elif isinstance(getattr(self, a, None), RESTResource):
            obj = getattr(self, a)
        if obj and hasattr(obj, 'collection_dispatcher'):
            obj.parents = [ p for p in self.parents ]
            obj.parents.extend(resources)
            return self.REST_childOverride(obj, *resources) or obj.collection_dispatcher(a, rparams, vpath, params)
        rparams.insert(0, a)
        if resources:
            return self.REST_dispatch(resources[0], rparams, **params)
        else:
            return self.REST_collection_dispatch(rparams, **params)
        return

    def REST_instantiate(self, id, *params, **kwargs):
        """ instantiate a REST resource based on the id

        this method MUST be overridden in your class. it will be passed
        the id (from the url fragment) and should return a model object
        corresponding to the resource.

        if the object doesn't exist, it should return None rather than throwing
        an error. if this method returns None and it is a PUT request,
        REST_create() will be called so you can actually create the resource.
        """
        raise cherrypy.NotFound

    def REST_create(self, id, *params, **kwargs):
        """ create a REST resource with the specified id

        this method should be overridden in your class.
        this method will be called when a PUT request is made for a resource
        that doesn't already exist. you should create the resource in this method
        and return it.
        """
        raise cherrypy.NotFound