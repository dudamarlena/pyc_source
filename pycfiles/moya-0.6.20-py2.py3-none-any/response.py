# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/response.py
# Compiled at: 2017-06-14 17:51:26
from __future__ import unicode_literals
from __future__ import absolute_import
from ..elements.elementbase import LogicElement, Attribute
from ..tags.context import DataSetter
from .. import logic
from .. import http
from .. import serve
from .. import errors
from .. import interface
from .. import urltools
from .. import moyajson
from ..compat import text_type, PY2, py2bytes, urlencode, urlparse, parse_qs, urlunparse, quote_plus
from ..request import ReplaceRequest
from ..response import MoyaResponse
from ..urlmapper import MissingURLParameter, RouteError
from webob.response import Response
from datetime import datetime
import base64, pytz, logging
from fs.path import dirname
GMT = pytz.timezone(b'GMT')
log = logging.getLogger(b'moya.runtime')

class ResponseTag(DataSetter):
    """Create a response object"""

    class Help:
        synopsis = b'create a response object'

    class Meta:
        tag_name = b'response'

    status = Attribute(b'Status code', type=b'httpstatus', required=False, default=200)
    contenttype = Attribute(b'Content Type', default=b'text/html; charset=UTF-8')
    body = Attribute(b'Response body', type=b'expression', default=None)
    charset = Attribute(b'Character set', default=b'utf-8')
    headers = Attribute(b'Headers', type=b'dict', default=None)

    def get_value(self, context):
        let_map = self.get_let_map(context)
        status, content_type, body, charset, headers = self.get_parameters(context, b'status', b'contenttype', b'body', b'charset', b'headers')
        text = None
        if body is None:
            text = context.sub(self.text)
        response = MoyaResponse(status=status, content_type=py2bytes(content_type), body=body, text=text, charset=py2bytes(charset))
        for k, v in let_map.items():
            try:
                setattr(response, k, v)
            except:
                self.throw(b'bad-value.response-value', (b"Can't set {} to {}").format(context.to_expr(k), context.to_expr(v)))

        if headers:
            response.headers.update(headers)
        return response


class Respond(ResponseTag):
    """
    Immediately return a response.

    Useful for more esoteric status codes.

    """

    class Help:
        synopsis = b'serve a response'
        example = b'\n        <respond status="im_a_teapot" />\n        '

    class Meta:
        tag_name = b'respond'

    def logic(self, context):
        response = self.get_value(context)
        raise logic.EndLogic(response)


class Serve(LogicElement):
    """
    This tag serves a response object, which may be created with the [tag]response[/tag].

    """

    class Help:
        synopsis = b'serve a response object'
        example = b'\n        <url route="/test/">\n            <response status="im_a_teapot" dst="teapot_response">\n                Short and Stout\n            </response>\n            <serve response="teapot_response" />\n        </url>\n        '

    response = Attribute(b'Response object to serve', type=b'expression', required=True)

    def logic(self, context):
        response = self.response(context)
        raise logic.EndLogic(response)


class ServeFile(LogicElement):
    """Serve a static file."""

    class Help:
        synopsis = b'serve a file'
        example = b'\n        <serve-file fs="static" path="/images/logo.jpg />\n        '

    path = Attribute(b'Path in filesystem', required=True)
    fsobj = Attribute(b'Filesystem object', type=b'Index')
    fs = Attribute(b'Filesystem name')
    ifexists = Attribute(b'Only serve a response if the file exists', type=b'boolean')
    filename = Attribute(b'Name of the file being serve', required=False, default=None)

    def logic(self, context):
        params = self.get_parameters(context)
        if params.fsobj is not None:
            fs = params.fsobj
        else:
            try:
                fs = self.archive.filesystems[params.fs]
            except KeyError:
                self.throw(b'serve.no-fs', (b"No filesystem called '{}'").format(params.fs))

        path = params.path
        if params.ifexists and not fs.isfile(path):
            return
        else:
            req = context.root[b'request']
            serve.serve_file(req, fs, path, filename=params.filename)
            return


class ServeText(LogicElement):
    """
    Serve text.

    """
    status = Attribute(b'Status code', type=b'httpstatus', required=False, default=200)

    class Help:
        synopsis = b'serve simple text'
        example = b'\n        <serve-text>Nobody here but us chickens</serve-text>\n        '

    def logic(self, context):
        response = MoyaResponse(status=self.status(context), content_type=py2bytes(b'text'), text=context.sub(self.text), charset=py2bytes(b'utf-8'))
        raise logic.EndLogic(response)


class ServeJSON(LogicElement):
    """

    Serve an object encoded as JSON.

    This tag with either serialize an object ([i]obj[/i]) if provided, or serve the tag text as JSON.

    Like other serve- tags, this will return a response and stop processing the view.

    """

    class Help:
        example = b'\n        <!-- serialize an object -->\n        <serve-json obj="{\'crew\': [\'john\', \'scorpius\']}"/>\n\n        <!-- just serve the contents -->\n        <serve-json>\n            {"crew": ["john", "scorpius"]}\n        </serve-json>\n\n        '
        synopsis = b'serve an object as JSON'

    obj = Attribute(b'Object to build JSON from', type=b'expression', required=False, default=None, missing=False)
    indent = Attribute(b'Indent to make JSON more readable', type=b'integer', required=False, default=4)
    status = Attribute(b'Status code', type=b'httpstatus', required=False, default=200)

    def logic(self, context):
        if self.has_parameter(b'obj'):
            obj = self.obj(context)
            try:
                json_obj = moyajson.dumps(obj, indent=self.indent(context))
            except Exception as e:
                self.throw(b'serve-json.fail', text_type(e))

        else:
            json_obj = context.sub(self.text)
        response = MoyaResponse(status=self.status(context), content_type=b'application/json' if PY2 else b'application/json', body=json_obj)
        raise logic.EndLogic(response)


class ServeJsonObject(LogicElement):
    """

    Serve a dict encoded as a JSON object.

    Like other serve- tags, this will return a response and stop processing the view.

    Keys in the json object can be given via the let extension. Here's an example:
    [code xml]
    <serve-json-object let:success="yes" let:message="'upload was successful'"/>
    [/code]

    This will serve the following JSON:
    [code]
    {
        "success": true,
        "message": "upload was successful"
    }
    [/code]

    You can also create the json object as you would a [tag]dict[/tag]. The following returns the same response as above:
    [code xml]
    <serve-json-object>
        <let success="yes"/>
        <let-str msg="upload was successful"/>
    </serve-json-object/>
    [/code]
    """

    class Help:
        synopsis = b'serve an dict as JSON'

    indent = Attribute(b'Indent to make JSON more readable', type=b'integer', required=False, default=4)
    status = Attribute(b'Status code', type=b'httpstatus', required=False, default=200)

    def logic(self, context):
        obj = self.get_let_map(context)
        with context.data_scope(obj):
            yield logic.DeferNodeContents(self)
        try:
            json_obj = moyajson.dumps(obj, indent=self.indent(context))
        except Exception as e:
            self.throw(b'serve-json-object.fail', text_type(e))

        response = MoyaResponse(status=self.status(context), content_type=b'application/json' if PY2 else b'application/json', body=json_obj)
        raise logic.EndLogic(response)


class ServeXML(LogicElement):
    """Serve XML"""

    class Help:
        synopsis = b'serve xml'

    obj = Attribute(b'A string of XML, or an object that may be converted to XML', type=b'expression', required=True, missing=False)
    content_type = Attribute(b'Mime type', default=b'application/xml')

    def logic(self, context):
        params = self.get_parameters(context)
        mime_type = params.content_type
        xml = params.obj
        if hasattr(xml, b'__xml__'):
            try:
                xml = xml.__xml__()
            except Exception as e:
                self.throw(b'serve-xml.fail', (b'failed to covert {} to XML ({})').format(context.to_expr(xml), e))

        if not isinstance(xml, bytes):
            xml = text_type(xml)
            xml_bytes = xml.encode(b'utf-8')
        else:
            xml_bytes = xml
        response = MoyaResponse(content_type=py2bytes(mime_type), body=xml_bytes)
        raise logic.EndLogic(response)


class NotFound(LogicElement):
    """Respond to the request with a '404 not found' response"""

    class Help:
        synopsis = b"serve a '404 not found' response"

    def logic(self, context):
        raise logic.EndLogic(http.RespondNotFound())


class Forbidden(LogicElement):
    """Respond to the request with a '403 forbidden' response"""

    class Help:
        synopsis = b'respond with a forbidden response'

    def logic(self, context):
        raise logic.EndLogic(http.RespondForbidden())


class Denied(LogicElement):
    """
    Reject basic auth. Generally used in conjunction with [tag]auth-check[/tag].

    """
    realm = Attribute(b'Basic auth realm', type=b'text', required=False)

    class Help:
        synopsis = b'reject basic authorization'

    def logic(self, context):
        if self.has_parameter(b'realm'):
            realm = self.realm(context) or b'restricted'
        else:
            realm = context[b'_realm'] or b'restricted'
        headers = {b'WWW-Authenticate': (b'Basic realm="{}:"').format(realm)}
        raise logic.EndLogic(http.RespondUnauthorized(headers=headers))


class AuthCheck(LogicElement):
    """
    Perform a basic auth check.

    This tag returns a 401 response if basic auth isn't supplied.

    If basic auth credentials are included in the request, they are decoded and the enclosed block is executed with the variables [c]username[/c] and [c]password[/c]. The enclosed block can then use the [tag]denied[/tag] tag to reject bad credentials. Here is an example:

    [code xml]
    <auth-check>
        <denied if="[username, password] != ['john', 'iloveaeryn']" />
    </auth-check>
    [/code]

    """
    realm = Attribute(b'Basic auth realm', type=b'text', default=b'restricted')

    class Help:
        synopsis = b'perform basic auth check'

    def logic(self, context):
        realm = self.realm(context)
        authorization = context[b'.request.authorization']
        if not authorization:
            self.denied(realm)
        auth_method, auth = authorization
        if auth_method.lower() != b'basic':
            self.denied(realm)
        try:
            username, _, password = base64.b64decode(auth).partition(b':')
        except:
            self.denied(realm)

        if not username or not password:
            self.denied(realm)
        scope = {b'username': username, 
           b'password': password, 
           b'_realm': realm}
        with context.data_scope(scope):
            yield logic.DeferNodeContents(self)

    def denied(self, realm):
        headers = {b'WWW-Authenticate': (b'Basic realm="{}:"').format(realm)}
        raise logic.EndLogic(http.RespondUnauthorized(headers=headers))


class AdminOnly(LogicElement):
    """
    Respond with a forbidden response if the user is not admin.

    This tag is a shortcut for the following:

    [code xml]
    <forbidden if="not .permissions.admin"/>
    [/code]

    """

    class Help:
        synopsis = b'return a forbidden response if the user is not admin'

    def logic(self, context):
        if not context[b'.permissions.admin']:
            raise logic.EndLogic(http.RespondForbidden())


class RedirectToBase(object):

    def logic(self, context):
        url, path, query, fragment = self.get_parameters(context, b'url', b'path', b'query', b'fragment')
        if url is not None:
            parsed_url = urlparse(url)
            url = urlunparse(parsed_url[0:3] + ('', '', ''))
            url_query = parsed_url.query
            query_components = parse_qs(url_query)
        else:
            query_components = {}
        request = context[b'.request']
        query_components.update(self.get_let_map(context))
        if query:
            query_components.update(query)
        if query_components:
            qs = urlencode(query_components, True)
            url += b'?' + qs
        if url is not None:
            location = url
        elif path is not None:
            location = request.relative_url(path)
        if fragment:
            location = (b'{}#{}').format(location, fragment)
        self.new_location(context, location)
        return


class RedirectTo(RedirectToBase, LogicElement):
    """Redirect to new location."""

    class Help:
        synopsis = b'redirect to a new location'
        example = b'\n    <redirect-to url="http://www.moyaproject.com" />\n    <redirect-to path="../newuser?result=success" />\n    '

    url = Attribute(b'Destination URL', metavar=b'URL', required=False, default=None)
    path = Attribute(b'New path portion of the url, may be relative', metavar=b'PATH', required=False)
    code = Attribute(b'HTTP response code (use 301 for permanent redirect)', metavar=b'HTTPCODE', required=False, default=303, type=b'httpstatus')
    query = Attribute(b'Mapping expression to use as a query string', metavar=b'EXPRESSION', required=False, default=None, type=b'expression')
    fragment = Attribute(b'Fragment component in url')

    def new_location(self, context, location):
        code = self.code(context)
        response = MoyaResponse(status=code)
        response.location = location
        raise logic.EndLogic(response)


class RedirectBase(object):

    def logic(self, context):
        urlname, query, fragment = self.get_parameters(context, b'name', b'query', b'fragment')
        app = self.get_app(context)
        if not app:
            raise errors.AppMissingError()
        app_name = app.name
        url_params = self.get_let_map(context)
        try:
            url = context[b'.server'].get_url(app_name, urlname, url_params)
        except MissingURLParameter as e:
            self.throw(b'redirect.missing-parameter', text_type(e))
        except RouteError as e:
            self.throw(b'redirect.no-route', text_type(e))

        if query:
            qs = urltools.urlencode(query)
            url += b'?' + qs
        location = url
        if fragment:
            location = (b'{}#{}').format(location, fragment)
        self.new_location(context, location)


class Redirect(RedirectBase, LogicElement):
    """Redirect to a mounted URL"""

    class Help:
        synopsis = b'redirect to a named URL'

    name = Attribute(b'URL name', required=True, metavar=b'URL NAME')
    _from = Attribute(b'Application', type=b'application', default=None)
    code = Attribute(b'HTTP response code (use 301 for permanent redirect)', metavar=b'HTTPCODE', required=False, default=b'303', type=b'httpstatus')
    query = Attribute(b'Mapping expression to use as a query string', metavar=b'EXPRESSION', required=False, default=None, type=b'expression')
    fragment = Attribute(b'Fragment component in url')

    def new_location(self, context, location):
        code = self.code(context)
        response = MoyaResponse(status=code)
        response.location = location
        raise logic.EndLogic(response)


class Rewrite(RedirectBase, LogicElement):
    """
    This tag tells Moya to serve the content from a different named URL.

    Note, that unlike [tag]redirect[/tag], this does not involve an extra request.

    """

    class Help:
        synopsis = b'serve response from a different named URL'

    name = Attribute(b'URL name', required=True, metavar=b'URL NAME')
    _from = Attribute(b'Application', type=b'application', default=None)
    query = Attribute(b'Mapping expression to use as a query string', metavar=b'EXPRESSION', required=False, default=None, type=b'expression')
    fragment = Attribute(b'Fragment component in url')

    def new_location(self, context, location):
        url = urlparse(location)
        request = context[b'.request']
        new_request = request.copy()
        new_request.environ[b'QUERY_STRING'] = url.query
        new_request.environ[b'PATH_INFO'] = url.path
        log.debug(b'rewriting url to %s', location)
        raise logic.EndLogic(ReplaceRequest(new_request))


class RewriteTo(RedirectToBase, LogicElement):
    """
    This tag tells Moya to serve the content from a different URL.

    Note, that unlike [tag]redirect-to[/tag], this does not involve an extra request.

    """
    url = Attribute(b'Destination URL', metavar=b'URL', required=False, default=None)
    path = Attribute(b'New path portion of the url, may be relative', metavar=b'PATH', required=False)
    query = Attribute(b'Mapping expression to use as a query string', metavar=b'EXPRESSION', required=False, default=None, type=b'expression')
    fragment = Attribute(b'Fragment component in url')

    class Help:
        synopsis = b'serve response from a different location'

    def new_location(self, context, location):
        url = urlparse(location)
        request = context[b'.request']
        new_request = request.copy()
        new_request.environ[b'QUERY_STRING'] = url.query
        new_request.environ[b'PATH_INFO'] = url.path
        log.debug(b'rewriting url to %s', location)
        raise logic.EndLogic(ReplaceRequest(new_request))


class SetHeader(LogicElement):
    """
    Add additional headers to the outgoing response.

    """
    header = Attribute(b'Header name', required=True)
    value = Attribute(b'Header Value', required=False, default=b'')

    class Help:
        synopsis = b'add additional headers'
        example = b'\n        <set-header header="moya-example">In your headerz</set-header>\n        '

    def logic(self, context):
        header, value = self.get_parameters(context, b'header', b'value')
        if not self.has_parameter(b'value'):
            value = context.sub(self.text).strip()
        headers = context.set_new_call(b'.headers', dict)
        headers[header] = value


class CheckModified(LogicElement):
    """
    Return a not_modifed (304) response if a resource hasn't changed.

    This tag allows a view to skip generating a page if it hasn't changed since the last time a browser requested it.
    To use this tag, set either the [url https://en.wikipedia.org/wiki/HTTP_ETag]etag[/url] parameter, or the [c]time[/c] parameter, which should be the time the page was last modified. Moya will compare these attributes to the request headers, and generate a not modified (304) response if the page hasn't changed. Otherwise the view will continue processing as normal.

    """
    time = Attribute(b'Time resource was updated', type=b'expression', required=False)
    etag = Attribute(b'ETag for resource', type=b'text', required=False)

    class Help:
        synopsis = b'conditionally return a not modified response'
        example = b'\n        <view libname="view.show_post" template="post.html">\n            <db:get model="#Post" let:slug=".url.slug"/>\n            <check-modified time="post.updated_date" />\n        </view>\n        '

    def logic(self, context):
        request = context[b'.request']
        if request.method not in ('GET', 'HEAD'):
            return
        headers = context.set_new_call(b'.headers', dict)
        if self.has_parameter(b'time'):
            _dt = self.time(context)
            dt = interface.unproxy(_dt)
            if not isinstance(dt, datetime):
                self.throw(b'bad-value.time', (b"attribute 'time' should be a datetime object, not {}").format(context.to_expr(dt)))
            gmt_time = GMT.localize(dt)
            modified_date = gmt_time.strftime(b'%a, %d %b %Y %H:%M:%S GMT')
            headers[b'Last-Modified'] = modified_date
            if request.if_modified_since and gmt_time >= request.if_modified_since:
                response = Response(status=http.StatusCode.not_modified, headers=headers)
                raise logic.EndLogic(response)
        if self.has_parameter(b'etag'):
            etag = self.etag(context)
            headers[b'ETag'] = etag
            if etag in request.if_none_match:
                response = Response(status=http.StatusCode.not_modified, headers=headers)
                raise logic.EndLogic(response)