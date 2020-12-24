# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/server.py
# Compiled at: 2017-07-27 15:30:22
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from ..elements import Attribute
from ..elements.elementbase import LogicElement
from ..tags.context import ContextElementBase, DataSetter
from .. import logic
from ..urlmapper import URLMapper, MissingURLParameter, RouteError
from ..context.expressiontime import ExpressionDateTime
from ..render import render_object
from .. import http
from ..http import StatusCode, standard_response, RespondWith
from .. import errors
from ..template.errors import MissingTemplateError
from ..template.rendercontainer import RenderContainer
from .. import trace
from .. import __version__
from ..content import Content
from ..tags.content import ContentElementMixin
from ..tools import get_return
from .. import syntax
from ..timezone import Timezone
from ..context.tools import to_expression, set_dynamic
from ..sites import LocaleProxy
from ..compat import text_type, itervalues, py2bytes, iteritems
from .. import db
from ..response import MoyaResponse
from ..request import ReplaceRequest
from ..urltools import urlencode as moya_urlencode
from .. import tools
from .. import pilot
from .. import namespaces
from webob import Response
from fs.path import splitext
from fs.errors import NoSysPath
import pytz, sys, logging
log = logging.getLogger(b'moya.runtime')
startup_log = logging.getLogger(b'moya.startup')

class Mountpoint(LogicElement):
    """
    A [i]mountpoint[/i] defines a collection of URL *routes* which map incoming requests on to moya code.

    An app will typically have at least one mountpoint with [c]name="main"[/c] (the default) which is used when the app is mounted. Moya will check each enclosed <url> in turn until it finds a route which matches.

    An app may contain multiple mountpoints, which can be [i]mounted[/i] separately.

    """

    class Help:
        synopsis = b'define a collection of url routes'
        example = b'\n        <mountpoint name="main">\n            <!-- should contain <url> tags -->\n        </mountpoint>\n\n        '

    name = Attribute(b'Mountpoint name unique to the application', default=b'main', map_to=b'_name')
    preserve_attributes = [b'urlmapper', b'middleware', b'name']

    def post_build(self, context):
        self.urlmapper = URLMapper(self.libid)
        self.middleware = dict(request=URLMapper(), response=URLMapper())
        self.name = self._name(context)


class URL(LogicElement):
    """
    Add a URL route to a [tag]mountpoint[/tag].
    """

    class Help:
        synopsis = b'add a url to a mountpoint'

    mountpoint = Attribute(b'Name of the parent mount point', required=False)
    mount = Attribute(b'Mountpoint to mount on this url', required=False, default=None)
    route = Attribute(b'URL route', required=True)
    view = Attribute(b'View element', required=False, map_to=b'target', example=b'#post')
    methods = Attribute(b'A list of comma separated HTTP methods', type=b'commalist', evaldefault=True, required=False, default=b'GET,POST', example=b'GET,POST', map_to=b'_methods')
    handler = Attribute(b'A list of comma separated http status codes', type=b'commalist', evaldefault=False, required=False, default=[], example=b'404', map_to=b'_handlers')
    name = Attribute(b'An optional name', required=False, default=None)
    final = Attribute(b'Ignore further URLs if this route matches?', type=b'boolean', default=False)

    def lib_finalize(self, context):
        if not self.check(context):
            return
        else:
            defaults = self.get_let_map(context)
            params = self.get_parameters(context)
            methods = params._methods
            handlers = []
            for h in params._handlers:
                try:
                    handlers.append(StatusCode(h))
                except KeyError:
                    raise errors.ElementError((b'"{}" is not a valid http status code').format(h), element=self)

            target = params.target
            url_target = self.document.lib.qualify_libname(self.libname)
            try:
                if target is None:
                    target = (
                     url_target,)
                else:
                    target = (
                     url_target,
                     self.document.qualify_element_ref(target, lib=self.lib))
            except errors.ElementNotFoundError:
                raise errors.ElementError((b"No view called '{}' in the project").format(target), element=self)

            if params.mountpoint is None:
                mount_point = self.get_ancestor(b'mountpoint')
            else:
                _, mount_point = self.get_element(params.mountpoint)
            if params.mount:
                try:
                    _, element = self.archive.get_element(params.mount, lib=self.lib)
                    if not hasattr(element, b'urlmapper'):
                        raise ValueError((b'element {} is not mountable').format(element))
                    mount_point.urlmapper.map(params.route.rstrip(b'/') + b'/*', [
                     url_target], methods=methods, handlers=handlers or None, defaults=defaults)
                    mount_point.urlmapper.mount(params.route, element.urlmapper, name=params.name, defaults=defaults)
                except Exception as e:
                    raise errors.ElementError(text_type(e), element=self, diagnosis=getattr(e, b'diagnosis', None))

            else:
                try:
                    mount_point.urlmapper.map(params.route, target, methods=methods, handlers=handlers or None, name=params.name, defaults=defaults, final=params.final)
                except ValueError as e:
                    raise errors.ElementError(text_type(e), element=self)

            return


class Middleware(LogicElement):
    """Add middleware to a mountpoint"""

    class Help:
        synopsis = b'add middleware to a mountpoint'

    route = Attribute(b'Route', required=True)
    methods = Attribute(b'A list of comma separated HTTP methods', required=False, type=b'commalist', evaldefault=True, default=b'*', example=b'GET,POST', map_to=b'_methods')
    mountpoint = Attribute(b'Mount point', required=False)
    stage = Attribute(b'Stage in request handling', required=False, default=b'request', metavar=b'STAGE', choices=[
     b'request', b'response'])
    macro = Attribute(b'Macro to call', required=False, default=None)
    name = Attribute(b'An optional name', required=False, default=None)

    def lib_finalize(self, context):
        if not self.check(context):
            return
        else:
            params = self.get_parameters(context)
            methods = params._methods
            target = params.macro
            url_target = self.document.lib.qualify_libname(self.libname)
            if target is None:
                target = (
                 url_target,)
            else:
                target = (
                 url_target,
                 self.document.qualify_element_ref(target))
            if params.mountpoint is None:
                mount_point = self.get_ancestor(b'mountpoint')
            else:
                _, mount_point = self.get_element(params.mountpoint)
            mapper = mount_point.middleware[params.stage]
            _route = mapper.map(params.route, target, methods=methods, name=params.name)
            return


class Mount(LogicElement):
    """Mount a library."""

    class Help:
        synopsis = b'mount a library on a given URL'

    app = Attribute(b'Application', required=True)
    url = Attribute(b'Url', required=True)
    mountpoint = Attribute(b'Mount point', required=False, default=b'main')
    priority = Attribute(b'Priority (highest priority is checked first)', type=b'integer', required=False, default=0)

    def logic(self, context):
        if self.archive.test_build:
            return
        self.archive.build_libs()
        params = self.get_parameters(context)
        app = self.archive.find_app(params.app)
        server = self.get_ancestor(b'server')
        url_params = self.get_let_map(context, check_missing=False)
        url_params[b'app'] = app.name
        mountpoint = app.lib.get_element_by_type_and_attribute(b'mountpoint', b'name', params.mountpoint)
        app.mounts.append((params.mountpoint, params.url))
        server.urlmapper.mount(params.url, mountpoint.urlmapper, defaults=url_params, name=app.name, priority=params.priority)
        for stage, urlmapper in server.middleware.items():
            urlmapper.mount(params.url, mountpoint.middleware[stage], defaults=url_params, name=app.name, priority=params.priority)

        startup_log.debug(b'%s (%s) mounted on %s', app, params.mountpoint, tools.normalize_url_path(params.url))


class GetURL(DataSetter):
    """Get a named URL."""

    class Help:
        synopsis = b'get a named URL'

    name = Attribute(b'URL name', required=True)
    _from = Attribute(b'Application', type=b'application', default=None, evaldefault=True)
    query = Attribute(b'Mapping expression to use as a query string', metavar=b'EXPRESSION', required=False, default=None, type=b'expression', missing=False)
    _with = Attribute(b'Extract URL values from this object', type=b'expression', required=False, default=None)
    base = Attribute(b'Base (protocol and domain) of the URL', default=None)

    def get_value(self, context):
        params = self.get_parameters(context)
        query = params.query
        app = self.get_app(context)
        try:
            if self.has_parameter(b'with'):
                url_params = self.get_let_map(context)
                url_params.update(params[b'with'])
            else:
                url_params = {k:text_type(v) for k, v in iteritems(self.get_let_map(context))}
            for k, v in iteritems(url_params):
                if not v:
                    self.throw(b'bad-value.parameter', (b"URL parameter '{}' must not be blank or missing (it is {})").format(k, to_expression(context, v)))

            url = context[b'.server'].get_url(app.name, params.name, url_params)
        except MissingURLParameter as e:
            self.throw(b'get-url.missing-parameter', text_type(e))
        except RouteError as e:
            self.throw(b'get-url.no-route', text_type(e))

        if query and hasattr(query, b'items'):
            qs = moya_urlencode(query)
            if qs:
                url += b'?' + qs
        url = self.qualify(context, url)
        return url

    def qualify(self, context, url):
        base = self.base(context)
        if base is not None:
            url = base.rstrip(b'/') + b'/' + url.lstrip(b'/')
        return url


class GetFqURL(GetURL):
    """Get a [i]fully qualified[/i] (including domain name and scheme) named URL."""
    base = Attribute(b'Base (protocol and domain) of the URL', default=None)

    class Help:
        synopsis = b'get a fully qualified URL'

    def qualify(self, context, url):
        base = self.base(context)
        if base is None:
            base = context[b'.sys.site.host'] or context[b'.request.host_url']
        url = base + url
        return url


class Trace(DataSetter):
    """
    Extract route information from a URL path.

    Returns route matches in a list of dictionaries. Route matches have three keys;
    [c]data[/c] is the url data (as returned in [c].url[/c]), [c]targets[/c] is a list of element references,
    [c]name[/c] is the name of the matching URL.

    If [c]app[/c] or [c]name[/c] is provided, this tag will return the first url route matching the given app / named url.

    """

    class Help:
        synopsis = b'extract routing information from mounted URL paths'
        example = b'\n        <trace path=".request.path" dst="matches"/>\n        '

    server = Attribute(b'Server containing URL routes', type=b'expression', default=b'.server', evaldefault=True)
    path = Attribute(b'URL path to parse', type=b'expression', required=True, missing=False)
    method = Attribute(b'HTTP method', type=b'text', default=b'GET')
    app = Attribute(b'Application name', required=False, default=None, type=b'text')
    name = Attribute(b'Route name to find', required=False, type=b'commalist', default=None)

    def get_value(self, context):
        server, path, method, app, name = self.get_parameters(context, b'server', b'path', b'method', b'app', b'name')
        if b'://' in path:
            _, _, path = path.partition(b'://')
        if not path.startswith(b'/'):
            path = b'/' + path
        if app is None and name is None:
            routes = []
            for route_match in server.urlmapper.iter_routes(path, method):
                if route_match is not None:
                    data, targets, name = route_match
                    routes.append({b'data': data, b'targets': targets, b'name': name})

            return routes
        for route_match in server.urlmapper.iter_routes(path, method):
            data, targets, _name = route_match
            if app is not None:
                if data.get(b'app', None) != app:
                    continue
            if name is not None:
                if _name not in name:
                    continue
            return {b'data': data, b'targets': targets, b'name': _name}
        else:
            return

        return


def wrap_element_error(f):

    def deco(self, context):
        try:
            for node in f(self, context):
                yield node

        except (errors.ElementError, logic.LogicFlowException):
            raise
        except Exception as e:
            raise errors.ElementError(text_type(e), self, diagnosis=getattr(e, b'diagnosis', None))

        return

    return deco


class View(ContextElementBase, ContentElementMixin):
    """Define a view to handle a URL"""

    class Help:
        synopsis = b'define a view to handle a URL'

    content = Attribute(b'Content', type=b'elementref', required=False, default=None)
    template = Attribute(b'Template', type=b'templates', required=False, default=None)
    requires = Attribute(b'Permission expression', type=b'expression', required=False, default=None)
    withscope = Attribute(b'Use scope as template / content data?', type=b'boolean', required=False, default=True)

    def extend_context(self, context):
        """Hook to extend the context."""
        pass

    @wrap_element_error
    def run(self, context):
        content, templates, requires, withscope = self.get_parameters(context, b'content', b'template', b'requires', b'withscope')
        if self.has_parameter(b'requires'):
            if not requires:
                raise logic.EndLogic(http.RespondForbidden())
        self.extend_context(context)
        yield logic.DeferNodeContents(self)
        if b'_return' in context:
            scope = get_return(context.get(b'_return'))
        elif withscope:
            scope = context[b'.call']
        else:
            scope = {}
        if scope is not None and not isinstance(scope, Content):
            app = self.get_app(context)
            template = self.resolve_templates(app, templates)
            if content is not None:
                if not hasattr(scope, b'items'):
                    self.throw(b'view.bad-return', (b'View should return a dict or other mapping object (not {})').format(to_expression(scope)))
                for defer in self.generate_content(context, content, app, td=scope):
                    yield defer

                context.copy(b'_content', b'_return')
            elif template is not None:
                render_container = RenderContainer.create(app, template=template)
                render_container.update(scope)
                context[b'_return'] = render_container
        return


class AppUrlsProxy(object):

    def __moyacontext__(self, context):
        urls = context.get(b'.urls')
        app = context[b'.app']
        return urls[app.name]


class Trace(object):

    def __init__(self, target, app=None, route_data=None, response=None):
        self.target = target
        self.app = app
        self.route_data = route_data
        if isinstance(response, http.RespondWith):
            self.response = text_type(response)
        else:
            self.response = None
        return

    def __moyarepr__(self, context):
        return b'<trace>'

    @property
    def target_html(self):
        return syntax.highlight(b'target', self.target, line_numbers=False)


class GetLocale(DataSetter):
    """Get an object containing locale information"""

    class Help:
        synopsis = b'get locale information'

    locale = Attribute(b'Locale name')

    def logic(self, context):
        _locale = self.locale(context)
        try:
            locale = LocaleProxy(_locale)
        except:
            self.throw(b'get-locale.unknown-locale', (b'Couldn\'t get locale information for "{}"').format(_locale))

        self.set_context(context, self.dst(context), locale)


class SetLocale(LogicElement):
    """Switches the current locale"""

    class Help:
        synopsis = b'switch the current locale'

    locale = Attribute(b'Locale name')

    def logic(self, context):
        _locale = self.locale(context)
        try:
            locale = LocaleProxy(_locale)
        except:
            self.throw(b'change-locale.unknown-locale', (b'Couldn\'t get locale information for "{}"').format(_locale))

        context[b'.locale'] = locale


class SetLanguage(LogicElement):
    """Set the current language"""

    class Help:
        synopsis = b'set the current language'

    language = Attribute(b'Language code')

    def logic(self, context):
        language = self.language(context)
        if not isinstance(language, list):
            language = [
             language]
        context[b'.languages'] = language


class Server(LogicElement):
    """Defines a server"""

    class Help:
        synopsis = b'define a server'

    def post_build(self, context):
        self.urlmapper = URLMapper()
        self.middleware = {b'request': URLMapper(), 
           b'response': URLMapper()}
        self.fs = None
        super(Server, self).post_build(context)
        return

    def startup(self, archive, context, fs, breakpoint=False):
        self.fs = fs
        archive.build_libs()
        try:
            if breakpoint:
                logic.debug(archive, context, logic.DeferNodeContents(self))
            else:
                logic.run_logic(archive, context, logic.DeferNodeContents(self))
        except Exception as e:
            raise

        archive.build_libs()

    def get_url(self, app_name, url_name, params=None):
        app_routes = self.urlmapper.get_routes(app_name)
        url = None
        for route in app_routes[:-1]:
            try:
                url = route.target.get_url(url_name, params, base_route=route)
            except RouteError:
                continue
            else:
                break

        else:
            route = app_routes[(-1)]
            url = route.target.get_url(url_name, params, base_route=route)

        return url

    def trace(self, archive, url, method=b'GET'):
        for route_match in self.urlmapper.iter_routes(url, method):
            route_data = route_match.data
            target = route_match.target
            if target:
                for element_ref in target:
                    app = archive.get_app(route_data.get(b'app', None))
                    yield (route_data, archive.get_element(element_ref, app))

        return

    def process_response(self, context, response):
        cookies = context.root.get(b'cookiejar', {})
        for cookie in itervalues(cookies):
            cookie.set(response)

        for cookie_name in cookies.deleted_cookies:
            response.delete_cookie(cookie_name)

        try:
            if not response.date and b'now' in context.root:
                response.date = context.root[b'now']._dt
        except:
            log.exception(b'error setting response date')

        return response

    def render_response(self, archive, context, obj, status=StatusCode.ok):
        response = Response(charset=py2bytes(b'utf8'), status=int(getattr(obj, b'http_status', status)))
        result = render_object(obj, archive, context, b'html')
        response.text = text_type(result)
        return self.process_response(context, response)

    def _dispatch_result(self, archive, context, request, result, status=StatusCode.ok):
        if result is None:
            return
        else:
            if isinstance(result, ReplaceRequest):
                return result
            if isinstance(result, RespondWith):
                return self.dispatch_handler(archive, context, request, status=result.status, headers=result.headers)
            if not isinstance(result, Response):
                status = int(getattr(result, b'http_status', None) or status)
                response = MoyaResponse(charset=py2bytes(b'utf8'), status=status)
                html = render_object(result, archive, context, b'html')
                response.text = html
            else:
                response = result
            return self.process_response(context, response)

    def handle_error(self, archive, context, request, error, exc_info):
        context.safe_delete(b'._callstack')
        context.safe_delete(b'.call')
        return self.dispatch_handler(archive, context, request, status=StatusCode.internal_error, error=error, exc_info=exc_info)

    def _dispatch_mapper(self, archive, context, mapper, url, method=b'GET', status=None, breakpoint=False):
        """Loop to call targets for a url/method/status combination"""
        dispatch_trace = context.root.get(b'_urltrace', [])
        if breakpoint:
            call = archive.debug_call
        else:
            call = archive.call
        root = context.root
        for route_data, target, name in mapper.iter_routes(url, method, status):
            root.update(urlname=name, headers={})
            if target:
                for element_ref in target:
                    app, element = archive.get_element(element_ref)
                    if element:
                        app = app or archive.get_app(route_data.get(b'app', None))
                        context.root.update(url=route_data)
                        result = call(element_ref, context, app, url=route_data)
                        dispatch_trace.append(Trace(element_ref, app, route_data, result))
                        if result is not None:
                            yield result
                    else:
                        dispatch_trace.append(Trace(element_ref))

            else:
                dispatch_trace.append(Trace(element_ref))

        return

    @classmethod
    def set_site(cls, archive, context, request):
        """Set site data for a request"""
        domain = request.host
        if b':' in domain:
            domain = domain.split(b':', 1)[0]
        site_instance = archive.sites.match(domain, context=context)
        if site_instance is None:
            log.error((b'no site matching domain "{domain}", consider adding [site:{domain}] to settings').format(domain=domain))
            return
        else:
            context.root[b'sys'][b'site'] = site_instance
            try:
                context.root[b'sys'][b'base'] = archive.project_fs.getsyspath(b'/')
            except NoSysPath:
                context.root[b'sys'][b'base'] = None

            context.root[b'site'] = site_instance._data
            return site_instance

    @classmethod
    def _get_tz(self, context, default_timezone=b'UTC', user_timezone=False):
        """lazy insertion of .tz"""
        if context is None:
            context = pilot.context
        tz = None
        if user_timezone:
            tz = context.get(b'.user.timezone', None)
        if not tz:
            tz = context.get(b'.sys.site.timezone', None)
        if not tz:
            tz = default_timezone
        if not tz:
            return
        else:
            try:
                return Timezone(tz)
            except pytz.UnknownTimeZoneError:
                log.error(b"invalid value for timezone '%s', defaulting to UTC", tz)
                return Timezone(b'UTC')

            return

    def run_middleware(self, stage, archive, context, request, url, method):
        middleware = self.middleware[stage]
        try:
            for result in self._dispatch_mapper(archive, context, middleware, url, method):
                response = self._dispatch_result(archive, context, request, result)
                if response:
                    return response

        except Exception as e:
            return self.handle_error(archive, context, request, e, sys.exc_info())

    def _populate_context(self, archive, context, request):
        """Add standard values to context."""
        populate_context = {b'permissions': {}, b'libs': archive.libs, 
           b'apps': archive.apps, 
           b'debug': archive.debug, 
           b'develop': archive.develop, 
           b'sys': {}, b'server': self, 
           b'urls': self.urlmapper, 
           b'now': ExpressionDateTime.moya_utcnow(), 
           b'appurls': AppUrlsProxy(), 
           b'moya': {b'version': __version__}, b'enum': archive.enum, 
           b'accept_language': list(request.accept_language), 
           b'media_url': archive.media_url, 
           b'filters': archive.filters, 
           b'secret': archive.secret}
        context.root.update(populate_context)
        set_dynamic(context)

    def dispatch(self, archive, context, request, breakpoint=False):
        """Dispatch a request to the server and return a response object."""
        url = request.path_info
        method = request.method
        self._populate_context(archive, context, request)
        site = self.set_site(archive, context, request)
        if site is None:
            return self.dispatch_handler(archive, context, request, StatusCode.not_found)
        else:
            root = context.root
            if site.head_as_get and method == b'HEAD':
                request = request.copy()
                request.method = b'GET'
                root[b'request'] = request
                method = b'GET'
            root[b'locale'] = site.locale
            context.set_lazy(b'.tz', self._get_tz, None, user_timezone=site.user_timezone, default_timezone=site.timezone)
            response = self.run_middleware(b'request', archive, context, request, url, method)
            if response is not None:
                return response

            def response_middleware(response):
                context.safe_delete(b'._callstack', b'.call')
                context.root[b'response'] = response
                new_response = self.run_middleware(b'response', archive, context, request, url, method)
                return new_response or response

            root[b'urltrace'] = root[b'_urltrace'] = []
            context.safe_delete(b'._callstack', b'.call')
            response = None
            try:
                try:
                    for result in self._dispatch_mapper(archive, context, self.urlmapper, url, method, breakpoint=breakpoint):
                        response = self._dispatch_result(archive, context, request, result)
                        if response:
                            response = response_middleware(response)
                            db.commit_sessions(context)
                            return response
                        db.commit_sessions(context)

                except Exception as e:
                    db.rollback_sessions(context, close=False)
                    return self.handle_error(archive, context, request, e, sys.exc_info())

            finally:
                for thread in context.get(b'._threads', []):
                    thread.wait()

                context.safe_delete(b'._threads')
                db.close_sessions(context)

            root[b'_urltrace'] = []
            if not url.endswith(b'/') and site.append_slash:
                if method in ('HEAD', 'GET') and self.urlmapper.has_route(url + b'/', method, None):
                    _, ext = splitext(url)
                    if not ext:
                        response = MoyaResponse(status=StatusCode.temporary_redirect, location=url + b'/')
                        return response
            if request.method in ('GET', 'POST', 'HEAD'):
                status_code = StatusCode.not_found
            else:
                status_code = StatusCode.method_not_allowed
            return self.dispatch_handler(archive, context, request, status=status_code)

    def dispatch_handler(self, archive, context, request, status=404, headers=None, error=None, exc_info=None):
        """Respond to a status code"""
        context.safe_delete(b'._callstack', b'.call', b'.td', b'._td', b'.contentstack', b'.content', b'.headers')
        if headers is not None:
            context.root[b'headers'] = headers
        moya_trace = None
        error2 = None
        moya_trace2 = None
        if error is not None:
            moya_trace = getattr(error, b'moya_trace', None)
            if moya_trace is None:
                try:
                    moya_trace = trace.build(context, None, None, error, exc_info, request)
                except Exception as e:
                    raise

        try:
            url = request.path_info
            method = request.method
            for result in self._dispatch_mapper(archive, context, self.urlmapper, url, method, status):
                if not isinstance(result, RespondWith):
                    return self._dispatch_result(archive, context, request, result, status=status)

        except Exception as e:
            log.exception(b'error in dispatch_handler')
            if status != StatusCode.internal_error:
                return self.handle_error(archive, context, request, e, sys.exc_info())
            error2 = e
            moya_trace2 = getattr(error2, b'moya_trace', None)
            if moya_trace2 is None:
                moya_trace2 = trace.build(context, None, None, error2, sys.exc_info(), request)

        if error is not None:
            log.error((b'unhandled exception ({})').format(text_type(error).lstrip()))
            try:
                context[b'.console'].obj(context, moya_trace)
            except:
                pass

        context.reset()
        context.safe_delete(b'._callstack', b'.call', b'.td', b'._td', b'.contentstack', b'.content', b'_funccalls', b'._for', b'_for_stack')
        template_filename = (b'{}.html').format(int(status))
        try:
            response = MoyaResponse(charset=py2bytes(b'utf8'), status=status)
            rc = RenderContainer.create(None, template=template_filename)
            rc[b'request'] = request
            rc[b'status'] = status
            rc[b'error'] = error
            rc[b'trace'] = moya_trace
            rc[b'error2'] = error
            rc[b'trace2'] = moya_trace2
            rc[b'moya_error'] = getattr(moya_trace.exception, b'type', None) if moya_trace else None
            if status == 500:
                archive.fire(context, b'sys.unhandled-exception', data=rc)
            response.text = render_object(rc, archive, context, b'html')
            return response
        except MissingTemplateError:
            pass
        except Exception as e:
            log.error(b'unable to render %s (%s)', template_filename, text_type(e))

        response = Response(charset=py2bytes(b'utf8'), status=status)
        url = request.path_info
        try:
            response.text = standard_response(status, url, error, moya_trace, debug=archive.debug)
        except Exception as e:
            log.exception(b'error generating standard response')

        return response