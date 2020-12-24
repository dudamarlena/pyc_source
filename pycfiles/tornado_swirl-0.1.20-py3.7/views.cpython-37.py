# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tornado_swirl/views.py
# Compiled at: 2019-12-17 20:05:41
# Size of source mod 2**32: 14675 bytes
"""Swirl Handlers/Views"""
import inspect, json, re
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import tornado.template, tornado.web
from tornado.util import re_unescape
from tornado_swirl import settings, swagger
__author__ = 'rduldulao'

def json_dumps(obj, pretty=False):
    """Returns JSON string"""
    if pretty:
        return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    return json.dumps(obj)


class SwaggerUIHandler(tornado.web.RequestHandler):
    __doc__ = 'Serves the Swagger UI'

    def initialize(self, static_path, **kwds):
        self.static_path = static_path

    def set_default_headers(self):
        headers = settings.default_settings.get('swagger_ui_handlers_headers', [])
        for key, value in headers:
            self.add_header(key, value)

    def get_template_path(self):
        return self.static_path

    def get(self):
        discovery_url = urljoin(self.request.full_url(), self.reverse_url(settings.URL_SWAGGER_API_SPEC))
        self.render('index.html', discovery_url=discovery_url)


class SwaggerApiHandler(tornado.web.RequestHandler):
    __doc__ = 'Openapi 3.0 spec generator class handler'

    def set_default_headers(self):
        headers = settings.default_settings.get('swagger_spec_headers', [])
        for key, value in headers:
            self.add_header(key, value)

    def get(self):
        """Get handler"""
        self.set_header('content-type', 'application/json')
        apis = self.find_api()
        servers = []
        server_settings = settings.default_settings.get('servers')
        for server in server_settings:
            for key in list(server.keys()):
                if key not in ('url', 'description'):
                    server.pop(key, None)

            if server:
                servers.append(server)

        if not servers:
            server_host = self.request.host.split(',')[0]
            forwarded = self.request.headers.get('Forwarded', None)
            proto = None
            if forwarded:
                protopart = [part.strip() for part in forwarded.split(';') if part.strip().startswith('proto')]
                if protopart:
                    proto = protopart[0].split('=')[(-1)]
            proto = proto or self.request.headers.get('X-Forwarded-Proto', None) or self.request.protocol
            servers = [
             {'url':proto + '://' + server_host, 
              'description':'Default server'}]
        specs = {'openapi':settings.SWAGGER_VERSION, 
         'info':{'title':settings.default_settings.get('title'), 
          'description':settings.default_settings.get('description'), 
          'version':settings.default_settings.get('api_version')}, 
         'servers':servers, 
         'paths':{path:self._SwaggerApiHandler__get_api_spec(spec, operations) for path, spec, operations in apis}}
        if settings.SwirlVars.GLOBAL_TAGS:
            specs['tags'] = settings.SwirlVars.GLOBAL_TAGS
        schemas = settings.get_schemas()
        if schemas:
            specs.update({'components': {'schemas': {name:self._SwaggerApiHandler__get_schema_spec(schemaCls) for name, schemaCls in schemas.items()}}})
        security_schemes = settings.SwirlVars.SECURITY_SCHEMES
        if security_schemes:
            components = specs.get('components') or {}
            components['securitySchemes'] = {}
            for name, scheme in security_schemes.items():
                components['securitySchemes'][name] = scheme.spec()

        self.finish(json_dumps(specs, self.get_arguments('pretty')))

    def __get_schema_spec(self, cls):
        specs = list(cls.schema_spec)
        val = {}
        if len(specs) > 1:
            val = {'allOf': []}
            while len(specs) > 1:
                spec, specs = specs[0], specs[1:]
                if isinstance(spec, swagger.Ref):
                    val['allOf'].append({'$ref': spec.link})

        elif len(specs) == 1:
            props = [(prop.name, self._prop_to_dict(prop), prop.required) for _, prop in specs[0].properties.items()]
            required = [name for name, _, req in props if req]
            obj = {'type': 'object'}
            obj['description'] = specs[0].description or specs[0].summary
            if required:
                obj.update({'required': required})
            obj.update({'properties': {name:d for name, d, r in props}})
            val = val.get('allOf') or obj
        else:
            val['allOf'].append(obj)
        if specs[0].example:
            val['example'] = specs[0].example
        else:
            if specs[0].examples:
                val['examples'] = specs[0].examples
            return val

    def _prop_to_dict(self, prop):
        schema = self._SwaggerApiHandler__get_type(prop)['schema']
        if schema is not None:
            schema.update(prop.kwargs)
        if prop.description:
            schema.update({'description': prop.description})
        return schema

    def __get_api_spec(self, spec, operations):
        paths = {}
        for api in operations:
            paths[api[0]] = {'operationId':str(spec.__name__) + '.' + api[0], 
             'summary':api[1].summary.strip(), 
             'description':api[1].description.strip(), 
             'parameters':self._SwaggerApiHandler__get_params(api[1])}
            if api[1].deprecated:
                paths[api[0]]['deprecated'] = True
            if api[1].body_params:
                paths[api[0]]['requestBody'] = self._SwaggerApiHandler__get_request_body(api[1])
            paths[api[0]]['responses'] = self._SwaggerApiHandler__get_responses(api[1])
            if api[1].tags:
                paths[api[0]]['tags'] = self._SwaggerApiHandler__get_tags(api[1])
            if api[1].security:
                spec2 = self._SwaggerApiHandler__get_security_spec(api[1])
                if spec2:
                    paths[api[0]]['security'] = spec2

        return paths

    def __detect_content_from_type(self, val):
        if val.type.name == 'file':
            return (
             'file', False, val.type.contents)
        if val.type.name in settings.get_schemas().keys():
            return (
             val.type.name, True, None)
        if val.type.name == 'object':
            return ('object', True, None)
        return (val.type.name, False, None)

    def __get_params(self, path_spec):
        params = []
        allps = sorted((path_spec.path_params.values()), key=(lambda x: x.order)) + sorted((path_spec.header_params.values()), key=(lambda x: x.order)) + sorted((path_spec.query_params.values()), key=(lambda x: x.order)) + sorted((path_spec.cookie_params.values()), key=(lambda x: x.order))
        for param in allps:
            if param:
                param_data = {'in':param.ptype,  'name':param.name, 
                 'required':param.required, 
                 'description':str(param.description).strip()}
                param_data.update(self._SwaggerApiHandler__get_type(param))
                params.append(param_data)

        return params

    def __get_tags(self, path_spec):
        all_tags = sorted((path_spec.tags.values()), key=(lambda x: x.order))
        tag_list = []
        for tag in all_tags:
            if tag:
                tag_list.append(tag.name)

        return tag_list

    def __get_security_spec(self, path_spec):
        specs = []
        for name, schemes in path_spec.security.items():
            spec = {}
            scheme = settings.SwirlVars.SECURITY_SCHEMES.get(name)
            if not scheme:
                continue
            if scheme.type not in ('oauth2', 'openIdConnect'):
                spec[name] = []
            else:
                specs.append(spec)

        return specs

    def __get_request_body(self, path_spec):
        contents = {}
        if path_spec.body_params:
            files_detected = 0
            form_data_detected = 0
            models_detected = 0
            for _, val in path_spec.body_params.items():
                _, ismodel, ftype = self._SwaggerApiHandler__detect_content_from_type(val)
                if ftype is not None:
                    files_detected += 1
                elif ismodel:
                    models_detected += 1
                else:
                    form_data_detected += 1

            ctype = ''
            if form_data_detected > 0:
                if not files_detected:
                    if not models_detected:
                        ctype = 'application/x-www-form-urlencoded'
                        contents[ctype] = {'schema': {'properties': {spec.name:spec.type.schema for spec in path_spec.body_params.values()}}}
            if files_detected == 1 and not form_data_detected:
                if not models_detected:
                    entry = list(path_spec.body_params.values())[0]
                    contents[entry.type.contents] = {'schema': {'type':'string', 
                                'format':'binary'}}
                else:
                    if not files_detected > 0 or form_data_detected > 0 or models_detected > 0 or models_detected > 1:
                        contents['multipart/form-data'] = {'schema': {'properties': {spec.name:spec.type.schema for spec in path_spec.body_params.values()}}}
                if models_detected == 1 and not files_detected:
                    if not form_data_detected:
                        params_entry = list(path_spec.body_params.values())[0]
                        file_type = settings.default_settings.get('json_mime_type')
                        contents[file_type] = {'schema': params_entry.type.schema}
                    else:
                        ctype = 'Unknown'
        return {'content': contents}

    def __get_responses(self, path_spec):
        params = {}
        allresps = sorted((path_spec.responses.values()), key=(lambda x: x.name))
        for param in allresps:
            if param:
                params[param.name] = {'description':param.description,  'content':self._detect_content(param)}

        return params

    def _detect_content(self, param):
        if param.type.name == 'None':
            return
        if param.type.name in ('integer', 'number', 'string', 'boolean'):
            return {'text/plain': {'schema': param.type.schema}}
        return {settings.default_settings.get('json_mime_type'): {'schema': param.type.schema}}

    def __get_type(self, param):
        return {'schema': param.type.schema}

    @staticmethod
    def find_api():
        """Gets the API specs

        Returns:
            path, route_spec, opertiations:  Tuple
                path -- the API endpoint URL
                route_spec -- the Tornado Request Handler class
                operations -- list of tuples containing (method name, PathSpec object)
        """
        for route_spec in settings.api_routes():
            url, _ = _find_groups(route_spec[0])
            path = url
            spec = route_spec[1]
            operations = [(name, member.path_spec) for name, member in inspect.getmembers(spec) if hasattr(member, 'path_spec')]
            if operations:
                path_param_spec = operations[0][1].path_params
                for _, path_spec in operations[1:]:
                    if len(path_spec.path_params) > len(path_param_spec):
                        path_param_spec = path_spec.path_params

                for _, path_sp in operations:
                    path_sp.path_params = path_param_spec

                vals = path_param_spec.values()
                sorted(vals, key=(lambda x: x.order))
                path = url % tuple(['{%s}' % arg for arg in [param.name for param in vals]])
            else:
                continue
            yield (path, spec, operations)


def _find_groups(url):
    """Returns a tuple (reverse string, group count) for a url.

    For example: Given the url pattern /([0-9]{4})/([a-z-]+)/, this method
    would return ('/%s/%s/', 2).
    """
    regex = re.compile(url)
    pattern = url
    if pattern.startswith('^'):
        pattern = pattern[1:]
    if pattern.endswith('$'):
        pattern = pattern[:-1]
    if regex.groups != pattern.count('('):
        return (None, None)
    pieces = []
    for fragment in pattern.split('('):
        if ')' in fragment:
            paren_loc = fragment.index(')')
            if paren_loc >= 0:
                pieces.append('%s' + fragment[paren_loc + 1:])
        else:
            try:
                unescaped_fragment = re_unescape(fragment)
            except ValueError:
                return (None, None)
            else:
                pieces.append(unescaped_fragment)

    return (
     ''.join(pieces), regex.groups)