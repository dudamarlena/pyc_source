# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Thoughtworker/Envs/wadl2swagger/lib/python2.7/site-packages/wadltools/swaggerconverter.py
# Compiled at: 2014-11-10 13:07:41
import os, re, json, yaml, textwrap, logging
from collections import OrderedDict
from wadltools.wadl import WADL, DocHelper, BadWADLError
from wadllib.application import WADLError

class WADLParseError(Exception):

    def __init__(self, message, wadl_file, location, cause):
        super(WADLParseError, self).__init__(message + ' in ' + wadl_file + ' ("' + location + '"), caused by ' + repr(cause))
        self.wadl_file = wadl_file
        self.location = location
        self.cause = cause


def merge_dicts(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                raise Exception('Conflict at %s' % ('.').join(path + [str(key)]))
        else:
            a[key] = b[key]

    return a


class SwaggerConverter:

    def __init__(self, options):
        self.options = options
        self.autofix = options.autofix
        self.strict = options.strict
        self.merge_dir = options.merge_dir

    def convert(self, title, wadl_file, swagger_file):
        try:
            self.logger = logging.getLogger(wadl_file)
            self.logger.info('Converting: %s to %s', wadl_file, swagger_file)
            defaults = self.default_swagger_dict(swagger_file)
            wadl = WADL.application_for(wadl_file)
            if self.autofix and wadl.resource_base is None:
                self.logger.warn('Autofix: No base path, setting to http://localhost')
                wadl.resource_base = 'http://localhost'
            self.logger.debug('Reading WADL from %s', wadl_file)
            swagger = OrderedDict()
            swagger['swagger'] = 2
            swagger['info'] = OrderedDict()
            try:
                swagger['info'] = defaults['info']
            except KeyError:
                swagger['info']['title'] = title
                swagger['info']['version'] = 'Unknown'

            try:
                swagger['consumes'] = defaults['consumes']
                swagger['produces'] = defaults['produces']
            except KeyError:
                swagger['consumes'] = [
                 'application/json']
                swagger['produces'] = ['application/json']

            swagger['paths'] = OrderedDict()
            for resource_element in wadl.resources:
                path = resource_element.attrib['path']
                resource = wadl.get_resource_by_path(path)
                if self.autofix and not path.startswith('/'):
                    self.logger.warn('Autofix: Adding leading / to path')
                    path = '/' + path
                swagger_resource = swagger['paths'][path] = OrderedDict()
                self.logger.debug('  Processing resource for %s', path)
                try:
                    for param in resource.params('application/json'):
                        if 'parameters' not in swagger_resource:
                            swagger_resource['parameters'] = []
                        swagger_resource['parameters'].append(self.build_param(param))

                except AttributeError:
                    self.logger.debug("   WARN: wadllib can't get parameters, possibly a wadllib bug")
                    self.logger.debug('     (It seems like it only works if the resource has a GET method')

                for method in resource.method_iter:
                    self.logger.debug('    Processing method %s %s', method.name, path)
                    verb = method.name
                    if self.autofix and verb == 'copy':
                        self.logger.warn('Autofix: Using PUT instead of COPY verb (OpenStack services accept either, Swagger does not allow COPY)')
                        verb = 'put'
                    swagger_method = swagger_resource[verb] = OrderedDict()
                    if '{http://docs.rackspace.com/api}id' in method.tag.attrib:
                        swagger_method['operationId'] = method.tag.attrib['{http://docs.rackspace.com/api}id']
                    swagger_method['summary'] = self.build_summary(method)
                    description = DocHelper.short_desc(method)
                    if description is not None:
                        swagger_method['description'] = description.text
                    swagger_method['produces'] = []
                    swagger_method['responses'] = OrderedDict()
                    if method.request.tag is not None:
                        request = method.request
                        for representation in request.representations:
                            for param in representation.params(resource):
                                if 'parameters' not in swagger_method:
                                    swagger_method['parameters'] = []
                                swagger_method['parameters'].append(self.build_param(param))

                    if method.response.tag is not None:
                        response = method.response
                        representation = response.get_representation_definition('application/json')
                        if representation is not None:
                            swagger_method['produces'].append(representation.media_type)
                        try:
                            statuses = response.tag.attrib['status'].split()
                        except KeyError as e:
                            raise BadWADLError('Response has no status', e, wadl_file)

                        for status in statuses:
                            swagger_method['responses'][int(status)] = self.build_response(response)
                            code_sample = None
                            code_samples = response.tag.findall('.//' + WADL.qname('docbook', 'programlisting') + '[@language="javascript"]')
                            if code_samples:
                                try:
                                    code_sample = code_samples[(-1)].text
                                    try:
                                        json.loads(code_sample)
                                    except ValueError:
                                        if self.autofix:
                                            match = re.match('.*^([\\{\\[].*)\\Z', code_sample, re.MULTILINE | re.DOTALL)
                                            if match:
                                                code_sample = match.group(1)
                                                json.loads(code_sample)
                                        else:
                                            raise

                                except ValueError as e:
                                    error = WADLParseError('Unparsable code sample', wadl_file, swagger_method['summary'], e)
                                    if self.strict:
                                        raise error
                                    else:
                                        self.logger.error(str(error))

                            if code_sample:
                                swagger_method['responses'][int(status)]['examples'] = self.build_code_sample(code_sample)

            swagger = merge_dicts(swagger, defaults)
            return swagger
        except Exception as e:
            raise BadWADLError('Could not convert WADL', e, wadl_file)

        return

    def default_swagger_dict(self, swagger_file):
        filename, _ = os.path.splitext(os.path.split(swagger_file)[1])
        merge_file = os.path.join(self.merge_dir, filename + '.yaml')
        if os.path.isfile(merge_file):
            self.logger.info('Using defaults from %s' % merge_file)
            with open(merge_file, 'r') as (stream):
                swagger = OrderedDict(yaml.load(stream))
        else:
            swagger = OrderedDict()
        return swagger

    def xsd_to_json_type(self, xsd_type):
        if xsd_type is None:
            return 'string'
        else:
            try:
                return {'xsd:boolean': 'boolean', 'xsd:integer': 'integer', 
                   'xsd:decimal': 'number', 
                   'xsd:string': 'string', 
                   'xsd:date': 'string', 
                   'xsd:time': 'string'}[xsd_type]
            except KeyError:
                self.logger.warn('Using unknown type: %s', xsd_type)
                return

            return

    def style_to_in(self, style):
        return {'matrix': 'unknown', 'query': 'query', 
           'header': 'header', 
           'template': 'path', 
           'plain': 'body'}[style]

    def build_summary(self, documented_wadl_object):
        return DocHelper.doc_tag(documented_wadl_object).attrib['title']

    def build_param(self, wadl_param):
        self.logger.debug('Found param: %s' % wadl_param.name)
        type = self.xsd_to_json_type(wadl_param.tag.get('type', 'string'))
        param = OrderedDict()
        param['name'] = wadl_param.name
        param['required'] = wadl_param.is_required
        param['in'] = self.style_to_in(wadl_param.style)
        if self.autofix and param['in'] == 'body':
            self.logger.warn('Autofix: Ignoring type on body parameter')
            type = None
        if type is not None:
            param['type'] = type
        if DocHelper.doc_tag(wadl_param) is not None and DocHelper.doc_tag(wadl_param).text is not None:
            description = DocHelper.description_text(DocHelper.doc_tag(wadl_param))
            description = textwrap.dedent(description)
            param['description'] = folded(description)
        return param

    def build_response(self, wadl_response):
        status = wadl_response.tag.attrib['status']
        try:
            description = (' ').join(DocHelper.doc_tag(wadl_response).text.split())
        except:
            description = '%s response' % status

        return {'description': literal(description)}

    def build_code_sample(self, wadl_code_sample):
        examples = OrderedDict()
        examples['application/json'] = literal(wadl_code_sample)
        return examples


class quoted(str):
    pass


def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


yaml.add_representer(quoted, quoted_presenter)

class folded(unicode):
    pass


def folded_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')


yaml.add_representer(folded, folded_presenter)

class literal(unicode):
    pass


def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')


yaml.add_representer(literal, literal_presenter)

def ordered_dict_presenter(dumper, data):
    return dumper.represent_dict(data.items())


yaml.add_representer(OrderedDict, ordered_dict_presenter)