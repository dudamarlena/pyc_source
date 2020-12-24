# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/url.py
# Compiled at: 2011-11-24 06:30:21
"""
All URL handling functions

"""
import re, sys, urlparse, pypoly, pypoly.session

class URL(object):
    """
    This is an URL.

    Example::

        url = pypoly.url(action = 'index')
        print str(url)

    :since: 0.2
    """

    def __init__(self, name, action=None, scheme='default', secure=False, values={}, **kwargs):
        """
        Initalize the URL-object.

        :since: 0.2

        :param name: the url name
        :type name: String
        :param secure: create a secure url
        :type secure: Boolean
        :param args: list containing all given arguments
        :param kwargs: dict containing all given arguments
        """
        self.name = name
        self.secure = secure
        self.scheme = scheme
        self.action = action
        self.values = values
        self.kwargs = kwargs

    def is_accessible(self):
        """
        Check if a user can access the created URL.

        Example::

            url = pypoly.url(action = 'index')
            if url.is_accessible():
                append url to table

        :since: 0.2

        :return: True = the resource with the given URL is accessible | False = the resource with the given URL is not accessible
        :rtype: Boolean
        """
        kwargs = self.kwargs
        if self.action == None:
            self.action = 'index'
        if '_scheme' in kwargs:
            pypoly.log.deprecated("Don't use _scheme!!! Use scheme instead")
            self.scheme = kwargs.pop('_scheme', self.scheme)
        func = pypoly._dispatcher.get_handler(self.name, action=self.action, scheme=self.scheme)
        if func == None:
            return False
        else:
            if not hasattr(func, '_pypoly_config'):
                return False
            conditions = func._pypoly_config.get('auth.require', None)
            if conditions == None:
                return True
            if pypoly.session.get('user.username', None) == None:
                return False
            for condition in conditions:
                if not condition():
                    return False

            return True

    def __str__(self):
        """
        Create the URL String.

        :since: 0.2
        """
        return pypoly.url._get_url(self.name, action=self.action, scheme=self.scheme, values=self.values, **self.kwargs)


class URLHandler(object):
    """
    Handles all the URL stuff.
    """

    def __call__(self, *args, **kwargs):
        """
        This function tries to detect from where you are calling and generates
        an url for it.

        Calling this function from a module named xyz will create an url like:
        http://example.com/xyz

        Example::

            url = pypoly.url(action = 'index')
            print str(url)

        It's also possible to use it to create text URLs.

        ::
            url = pypoly.url("/my-path")

        :since: 0.1

        :param plain: Create a plain text URL and add the static path.
        :type plain: Boolean
        :param raw: Create a raw text URL and use the given string as link
        :type plain: Boolean
        """
        caller = pypoly.get_caller()
        if len(args) > 0:
            path = args[0]
            if kwargs.get('raw', False):
                return path
            if len(path) > 0 and path[0] == '/':
                path = path[1:]
            static_url = pypoly.config.get('static.url')
            if static_url[(-1)] != '/':
                static_url = static_url + '/'
            if kwargs.get('plain', False):
                return urlparse.urljoin(static_url, path)
            if caller.name == None or len(caller.name) == 0:
                return ''
            return urlparse.urljoin(static_url, ('/').join([
             caller.type.lower(),
             caller.name.lower(),
             path]))
        else:
            if caller.type == 'module':
                name = ('.').join(['module', caller.pkg_root])
            elif caller.type == 'plugin':
                name = ('.').join(['plugin', caller.pkg_root])
            return URL(name, *args, **kwargs)

    def connect(self, route, *args, **kargs):
        """
        this function connects a new route

        see routes for python

        this handles only the namespaces for the system

        <namespace>.<name>.<rule name>

        e.g.: modules.demo.foo

        :since: 0.1

        """
        pypoly.log.debug('connecting  route:')
        scheme = kargs.pop('_scheme', None)
        if scheme != None:
            pypoly.log.deprecated("Don't use _scheme!!! Use scheme instead")
        else:
            scheme = kargs.pop('scheme', 'default')
        caller = pypoly.get_caller()
        if caller.type == 'module':
            path = pypoly.structure.get_module_path(caller.pkg_root)
            if len(path) == 0:
                path = [
                 caller.name.lower()]
            if len(route) > 0 and route[0] == '/':
                route = route[1:]
            route = ('/').join(path + [route])
            route = '/' + route
            name = ('.').join(['module', caller.pkg_root] + [scheme])
        elif caller.type == 'plugin':
            route = '/_plugin/' + caller.name.lower() + '/' + route
            name = ('.').join(['plugin', caller.pkg_root] + [scheme])
        elif caller.type == 'pypoly':
            name = ('.').join(['pypoly', scheme])
            route = '/' + route
        routes = []
        actions = []
        controller = kargs['controller']
        for func_name in dir(controller):
            func_object = getattr(controller, func_name)
            if hasattr(func_object, '_pypoly_config'):
                func_routes = func_object._pypoly_config.get('routes', None)
                if func_routes == None:
                    actions.append(func_name)
                    continue
                if type(func_routes) != list:
                    func_routes = [
                     func_routes]
                routes = routes + func_routes

        if len(actions) > 0:
            path = ''
            if not re.compile('{action(:[^}]*)?}').search(route):
                path = '{action}'
            routes.append({'path': path, 
               'requirements': {'action': ('|').join(actions)}})
        if route == None:
            return 'Error'
        else:
            pypoly._dispatcher.extend(name, kargs['controller'], routes, path_prefix=route)
            pypoly.log.debug('  route:' + str(route))
            pypoly.log.debug('  kargs:' + str(kargs))
            pypoly.log.debug('  name :' + str(name))
            return

    def _get_url(self, name, action=None, scheme='default', values={}, **kwargs):
        """
        this is an internal function for url handling

        creates the route name with the scheme and gets the route with that name

        :since: 0.1

        :param name: the route name without the scheme
        :return: the url
        """
        if '_scheme' in kwargs:
            pypoly.log.deprecated("Don't use _scheme!!! Use scheme insted")
        scheme = kwargs.pop('_scheme', scheme)
        if len(values) == 0 and len(kwargs) > 0:
            pypoly.log.deprecated('Use the values param to supply values')
            values = kwargs
        name = ('.').join([name, scheme])
        for route in pypoly._dispatcher._routes:
            if route.name == name:
                url = route.generate(action=action, values=values)
                if url != None:
                    return url

        return ''

    def get_module(self, name, *args, **kwargs):
        """
        Returns an URL for a module

        :since: 0.1

        :param name: the module name
        :type name: String
        """
        return URL(('.').join(['module', name]), **kwargs)

    def get_plugin(self, name, *args, **kwargs):
        """
        Returns an URL for a plugin

        :since: 0.1

        :param name: the plugin name
        :type name: String
        """
        return URL(('.').join(['plugins', name]), **kwargs)