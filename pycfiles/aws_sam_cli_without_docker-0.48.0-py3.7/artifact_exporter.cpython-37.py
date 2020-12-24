# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/package/artifact_exporter.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 23727 bytes
"""
Logic for uploading to S3 per Cloudformation Specific Resource
"""
import logging, os, tempfile, zipfile, contextlib
from contextlib import contextmanager
import uuid
from urllib.parse import urlparse, parse_qs
import shutil
from botocore.utils import set_value_from_jmespath
import jmespath
from samcli.commands._utils.resources import AWS_SERVERLESSREPO_APPLICATION, AWS_SERVERLESS_FUNCTION, AWS_SERVERLESS_API, AWS_APPSYNC_GRAPHQLSCHEMA, AWS_APPSYNC_RESOLVER, AWS_APPSYNC_FUNCTIONCONFIGURATION, AWS_LAMBDA_FUNCTION, AWS_APIGATEWAY_RESTAPI, AWS_ELASTICBEANSTALK_APPLICATIONVERSION, AWS_CLOUDFORMATION_STACK, AWS_SERVERLESS_APPLICATION, AWS_LAMBDA_LAYERVERSION, AWS_SERVERLESS_LAYERVERSION, AWS_GLUE_JOB
from samcli.commands._utils.template import METADATA_WITH_LOCAL_PATHS, RESOURCES_WITH_LOCAL_PATHS
from samcli.commands.package import exceptions
from samcli.lib.utils.hash import dir_checksum
from samcli.yamlhelper import yaml_dump, yaml_parse
LOG = logging.getLogger(__name__)

def is_path_value_valid(path):
    return isinstance(path, str)


def make_abs_path(directory, path):
    if is_path_value_valid(path):
        if not os.path.isabs(path):
            return os.path.normpath(os.path.join(directory, path))
    return path


def is_s3_url(url):
    try:
        parse_s3_url(url)
        return True
    except ValueError:
        return False


def is_local_folder(path):
    return is_path_value_valid(path) and os.path.isdir(path)


def is_local_file(path):
    return is_path_value_valid(path) and os.path.isfile(path)


def is_zip_file(path):
    return is_path_value_valid(path) and zipfile.is_zipfile(path)


def parse_s3_url(url, bucket_name_property='Bucket', object_key_property='Key', version_property=None):
    if isinstance(url, str):
        if url.startswith('s3://'):
            parsed = urlparse(url)
            query = parse_qs(parsed.query)
            if parsed.netloc:
                if parsed.path:
                    result = dict()
                    result[bucket_name_property] = parsed.netloc
                    result[object_key_property] = parsed.path.lstrip('/')
                    if version_property is not None:
                        if 'versionId' in query:
                            if len(query['versionId']) == 1:
                                result[version_property] = query['versionId'][0]
                    return result
    raise ValueError('URL given to the parse method is not a valid S3 url {0}'.format(url))


def upload_local_artifacts(resource_id, resource_dict, property_name, parent_dir, uploader):
    """
    Upload local artifacts referenced by the property at given resource and
    return S3 URL of the uploaded object. It is the responsibility of callers
    to ensure property value is a valid string

    If path refers to a file, this method will upload the file. If path refers
    to a folder, this method will zip the folder and upload the zip to S3.
    If path is omitted, this method will zip the current working folder and
    upload.

    If path is already a path to S3 object, this method does nothing.

    :param resource_id:     Id of the CloudFormation resource
    :param resource_dict:   Dictionary containing resource definition
    :param property_name:   Property name of CloudFormation resource where this
                            local path is present
    :param parent_dir:      Resolve all relative paths with respect to this
                            directory
    :param uploader:        Method to upload files to S3

    :return:                S3 URL of the uploaded object
    :raise:                 ValueError if path is not a S3 URL or a local path
    """
    local_path = jmespath.search(property_name, resource_dict)
    if local_path is None:
        local_path = parent_dir
    if is_s3_url(local_path):
        LOG.debug('Property %s of %s is already a S3 URL', property_name, resource_id)
        return local_path
    local_path = make_abs_path(parent_dir, local_path)
    if is_local_folder(local_path):
        return zip_and_upload(local_path, uploader)
    if is_local_file(local_path):
        return uploader.upload_with_dedup(local_path)
    raise exceptions.InvalidLocalPathError(resource_id=resource_id, property_name=property_name, local_path=local_path)


def resource_not_packageable(resource_dict):
    inline_code = jmespath.search('InlineCode', resource_dict)
    if inline_code is not None:
        return True
    return False


def zip_and_upload(local_path, uploader):
    with zip_folder(local_path) as (zip_file, md5_hash):
        return uploader.upload_with_dedup(zip_file, precomputed_md5=md5_hash)


@contextmanager
def zip_folder(folder_path):
    """
    Zip the entire folder and return a file to the zip. Use this inside
    a "with" statement to cleanup the zipfile after it is used.

    :param folder_path:
    :return: Name of the zipfile
    """
    md5hash = dir_checksum(folder_path, followlinks=True)
    filename = os.path.join(tempfile.gettempdir(), 'data-' + md5hash)
    zipfile_name = make_zip(filename, folder_path)
    try:
        yield (
         zipfile_name, md5hash)
    finally:
        if os.path.exists(zipfile_name):
            os.remove(zipfile_name)


def make_zip(file_name, source_root):
    zipfile_name = '{0}.zip'.format(file_name)
    source_root = os.path.abspath(source_root)
    with open(zipfile_name, 'wb') as (f):
        zip_file = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
        with contextlib.closing(zip_file) as (zf):
            for root, _, files in os.walk(source_root, followlinks=True):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, source_root)
                    zf.write(full_path, relative_path)

    return zipfile_name


@contextmanager
def mktempfile():
    directory = tempfile.gettempdir()
    filename = os.path.join(directory, uuid.uuid4().hex)
    try:
        with open(filename, 'w+') as (handle):
            yield handle
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def copy_to_temp_dir(filepath):
    tmp_dir = tempfile.mkdtemp()
    dst = os.path.join(tmp_dir, os.path.basename(filepath))
    shutil.copyfile(filepath, dst)
    return tmp_dir


class Resource:
    __doc__ = '\n    Base class representing a CloudFormation resource that can be exported\n    '
    RESOURCE_TYPE = None
    PROPERTY_NAME = None
    PACKAGE_NULL_PROPERTY = True
    FORCE_ZIP = False

    def __init__(self, uploader):
        self.uploader = uploader

    def export(self, resource_id, resource_dict, parent_dir):
        if resource_dict is None:
            return
            if resource_not_packageable(resource_dict):
                return
            property_value = jmespath.search(self.PROPERTY_NAME, resource_dict)
            if not property_value:
                if not self.PACKAGE_NULL_PROPERTY:
                    return
            if isinstance(property_value, dict):
                LOG.debug('Property %s of %s resource is not a URL', self.PROPERTY_NAME, resource_id)
                return
        else:
            temp_dir = None
            if is_local_file(property_value):
                if not is_zip_file(property_value):
                    if self.FORCE_ZIP:
                        temp_dir = copy_to_temp_dir(property_value)
                        set_value_from_jmespath(resource_dict, self.PROPERTY_NAME, temp_dir)
        try:
            try:
                self.do_export(resource_id, resource_dict, parent_dir)
            except Exception as ex:
                try:
                    LOG.debug('Unable to export', exc_info=ex)
                    raise exceptions.ExportFailedError(resource_id=resource_id,
                      property_name=(self.PROPERTY_NAME),
                      property_value=property_value,
                      ex=ex)
                finally:
                    ex = None
                    del ex

        finally:
            if temp_dir:
                shutil.rmtree(temp_dir)

    def do_export(self, resource_id, resource_dict, parent_dir):
        """
        Default export action is to upload artifacts and set the property to
        S3 URL of the uploaded object
        """
        uploaded_url = upload_local_artifacts(resource_id, resource_dict, self.PROPERTY_NAME, parent_dir, self.uploader)
        set_value_from_jmespath(resource_dict, self.PROPERTY_NAME, uploaded_url)


class ResourceWithS3UrlDict(Resource):
    __doc__ = '\n    Represents CloudFormation resources that need the S3 URL to be specified as\n    an dict like {Bucket: "", Key: "", Version: ""}\n    '
    BUCKET_NAME_PROPERTY = None
    OBJECT_KEY_PROPERTY = None
    VERSION_PROPERTY = None

    def do_export(self, resource_id, resource_dict, parent_dir):
        """
        Upload to S3 and set property to an dict representing the S3 url
        of the uploaded object
        """
        artifact_s3_url = upload_local_artifacts(resource_id, resource_dict, self.PROPERTY_NAME, parent_dir, self.uploader)
        parsed_url = parse_s3_url(artifact_s3_url,
          bucket_name_property=(self.BUCKET_NAME_PROPERTY),
          object_key_property=(self.OBJECT_KEY_PROPERTY),
          version_property=(self.VERSION_PROPERTY))
        set_value_from_jmespath(resource_dict, self.PROPERTY_NAME, parsed_url)


class ServerlessFunctionResource(Resource):
    RESOURCE_TYPE = AWS_SERVERLESS_FUNCTION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    FORCE_ZIP = True


class ServerlessApiResource(Resource):
    RESOURCE_TYPE = AWS_SERVERLESS_API
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    PACKAGE_NULL_PROPERTY = False


class GraphQLSchemaResource(Resource):
    RESOURCE_TYPE = AWS_APPSYNC_GRAPHQLSCHEMA
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    PACKAGE_NULL_PROPERTY = False


class AppSyncResolverRequestTemplateResource(Resource):
    RESOURCE_TYPE = AWS_APPSYNC_RESOLVER
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    PACKAGE_NULL_PROPERTY = False


class AppSyncResolverResponseTemplateResource(Resource):
    RESOURCE_TYPE = AWS_APPSYNC_RESOLVER
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][1]
    PACKAGE_NULL_PROPERTY = False


class AppSyncFunctionConfigurationRequestTemplateResource(Resource):
    RESOURCE_TYPE = AWS_APPSYNC_FUNCTIONCONFIGURATION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    PACKAGE_NULL_PROPERTY = False


class AppSyncFunctionConfigurationResponseTemplateResource(Resource):
    RESOURCE_TYPE = AWS_APPSYNC_FUNCTIONCONFIGURATION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][1]
    PACKAGE_NULL_PROPERTY = False


class LambdaFunctionResource(ResourceWithS3UrlDict):
    RESOURCE_TYPE = AWS_LAMBDA_FUNCTION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    BUCKET_NAME_PROPERTY = 'S3Bucket'
    OBJECT_KEY_PROPERTY = 'S3Key'
    VERSION_PROPERTY = 'S3ObjectVersion'
    FORCE_ZIP = True


class ApiGatewayRestApiResource(ResourceWithS3UrlDict):
    RESOURCE_TYPE = AWS_APIGATEWAY_RESTAPI
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    PACKAGE_NULL_PROPERTY = False
    BUCKET_NAME_PROPERTY = 'Bucket'
    OBJECT_KEY_PROPERTY = 'Key'
    VERSION_PROPERTY = 'Version'


class ElasticBeanstalkApplicationVersion(ResourceWithS3UrlDict):
    RESOURCE_TYPE = AWS_ELASTICBEANSTALK_APPLICATIONVERSION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    BUCKET_NAME_PROPERTY = 'S3Bucket'
    OBJECT_KEY_PROPERTY = 'S3Key'
    VERSION_PROPERTY = None


class LambdaLayerVersionResource(ResourceWithS3UrlDict):
    RESOURCE_TYPE = AWS_LAMBDA_LAYERVERSION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    BUCKET_NAME_PROPERTY = 'S3Bucket'
    OBJECT_KEY_PROPERTY = 'S3Key'
    VERSION_PROPERTY = 'S3ObjectVersion'
    FORCE_ZIP = True


class ServerlessLayerVersionResource(Resource):
    RESOURCE_TYPE = AWS_SERVERLESS_LAYERVERSION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    FORCE_ZIP = True


class ServerlessRepoApplicationLicense(Resource):
    RESOURCE_TYPE = AWS_SERVERLESSREPO_APPLICATION
    PROPERTY_NAME = METADATA_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]
    PACKAGE_NULL_PROPERTY = False


class ServerlessRepoApplicationReadme(Resource):
    RESOURCE_TYPE = AWS_SERVERLESSREPO_APPLICATION
    PROPERTY_NAME = METADATA_WITH_LOCAL_PATHS[RESOURCE_TYPE][1]
    PACKAGE_NULL_PROPERTY = False


class CloudFormationStackResource(Resource):
    __doc__ = '\n    Represents CloudFormation::Stack resource that can refer to a nested\n    stack template via TemplateURL property.\n    '
    RESOURCE_TYPE = AWS_CLOUDFORMATION_STACK
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[RESOURCE_TYPE][0]

    def do_export--- This code section failed: ---

 L. 439         0  LOAD_FAST                'resource_dict'
                2  LOAD_METHOD              get
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                PROPERTY_NAME
                8  LOAD_CONST               None
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  STORE_FAST               'template_path'

 L. 442        14  LOAD_FAST                'template_path'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_TRUE     58  'to 58'

 L. 443        22  LOAD_GLOBAL              is_s3_url
               24  LOAD_FAST                'template_path'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  POP_JUMP_IF_TRUE     58  'to 58'

 L. 444        30  LOAD_FAST                'template_path'
               32  LOAD_METHOD              startswith
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                uploader
               38  LOAD_ATTR                s3
               40  LOAD_ATTR                meta
               42  LOAD_ATTR                endpoint_url
               44  CALL_METHOD_1         1  '1 positional argument'
               46  POP_JUMP_IF_TRUE     58  'to 58'

 L. 445        48  LOAD_FAST                'template_path'
               50  LOAD_METHOD              startswith
               52  LOAD_STR                 'https://s3.amazonaws.com/'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  POP_JUMP_IF_FALSE    62  'to 62'
             58_0  COME_FROM            46  '46'
             58_1  COME_FROM            28  '28'
             58_2  COME_FROM            20  '20'

 L. 448        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L. 450        62  LOAD_GLOBAL              make_abs_path
               64  LOAD_FAST                'parent_dir'
               66  LOAD_FAST                'template_path'
               68  CALL_FUNCTION_2       2  '2 positional arguments'
               70  STORE_FAST               'abs_template_path'

 L. 451        72  LOAD_GLOBAL              is_local_file
               74  LOAD_FAST                'abs_template_path'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  POP_JUMP_IF_TRUE     98  'to 98'

 L. 452        80  LOAD_GLOBAL              exceptions
               82  LOAD_ATTR                InvalidTemplateUrlParameterError

 L. 453        84  LOAD_FAST                'self'
               86  LOAD_ATTR                PROPERTY_NAME
               88  LOAD_FAST                'resource_id'
               90  LOAD_FAST                'abs_template_path'
               92  LOAD_CONST               ('property_name', 'resource_id', 'template_path')
               94  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            78  '78'

 L. 456        98  LOAD_GLOBAL              Template
              100  LOAD_FAST                'template_path'
              102  LOAD_FAST                'parent_dir'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                uploader
              108  CALL_FUNCTION_3       3  '3 positional arguments'
              110  LOAD_METHOD              export
              112  CALL_METHOD_0         0  '0 positional arguments'
              114  STORE_FAST               'exported_template_dict'

 L. 458       116  LOAD_GLOBAL              yaml_dump
              118  LOAD_FAST                'exported_template_dict'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  STORE_FAST               'exported_template_str'

 L. 460       124  LOAD_GLOBAL              mktempfile
              126  CALL_FUNCTION_0       0  '0 positional arguments'
              128  SETUP_WITH          222  'to 222'
              130  STORE_FAST               'temporary_file'

 L. 461       132  LOAD_FAST                'temporary_file'
              134  LOAD_METHOD              write
              136  LOAD_FAST                'exported_template_str'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          

 L. 462       142  LOAD_FAST                'temporary_file'
              144  LOAD_METHOD              flush
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  POP_TOP          

 L. 464       150  LOAD_FAST                'self'
              152  LOAD_ATTR                uploader
              154  LOAD_METHOD              upload_with_dedup
              156  LOAD_FAST                'temporary_file'
              158  LOAD_ATTR                name
              160  LOAD_STR                 'template'
              162  CALL_METHOD_2         2  '2 positional arguments'
              164  STORE_FAST               'url'

 L. 467       166  LOAD_GLOBAL              parse_s3_url
              168  LOAD_FAST                'url'
              170  LOAD_STR                 'Version'
              172  LOAD_CONST               ('version_property',)
              174  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              176  STORE_FAST               'parts'

 L. 468       178  LOAD_FAST                'self'
              180  LOAD_ATTR                uploader
              182  LOAD_METHOD              to_path_style_s3_url
              184  LOAD_FAST                'parts'
              186  LOAD_STR                 'Key'
              188  BINARY_SUBSCR    
              190  LOAD_FAST                'parts'
              192  LOAD_METHOD              get
              194  LOAD_STR                 'Version'
              196  LOAD_CONST               None
              198  CALL_METHOD_2         2  '2 positional arguments'
              200  CALL_METHOD_2         2  '2 positional arguments'
              202  STORE_FAST               's3_path_url'

 L. 469       204  LOAD_GLOBAL              set_value_from_jmespath
              206  LOAD_FAST                'resource_dict'
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                PROPERTY_NAME
              212  LOAD_FAST                's3_path_url'
              214  CALL_FUNCTION_3       3  '3 positional arguments'
              216  POP_TOP          
              218  POP_BLOCK        
              220  LOAD_CONST               None
            222_0  COME_FROM_WITH      128  '128'
              222  WITH_CLEANUP_START
              224  WITH_CLEANUP_FINISH
              226  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 224


class ServerlessApplicationResource(CloudFormationStackResource):
    __doc__ = '\n    Represents Serverless::Application resource that can refer to a nested\n    app template via Location property.\n    '
    RESOURCE_TYPE = AWS_SERVERLESS_APPLICATION
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[AWS_SERVERLESS_APPLICATION][0]


class GlueJobCommandScriptLocationResource(Resource):
    __doc__ = '\n    Represents Glue::Job resource.\n    '
    RESOURCE_TYPE = AWS_GLUE_JOB
    PROPERTY_NAME = RESOURCES_WITH_LOCAL_PATHS[AWS_GLUE_JOB][0]


RESOURCES_EXPORT_LIST = [
 ServerlessFunctionResource,
 ServerlessApiResource,
 GraphQLSchemaResource,
 AppSyncResolverRequestTemplateResource,
 AppSyncResolverResponseTemplateResource,
 AppSyncFunctionConfigurationRequestTemplateResource,
 AppSyncFunctionConfigurationResponseTemplateResource,
 ApiGatewayRestApiResource,
 LambdaFunctionResource,
 ElasticBeanstalkApplicationVersion,
 CloudFormationStackResource,
 ServerlessApplicationResource,
 ServerlessLayerVersionResource,
 LambdaLayerVersionResource,
 GlueJobCommandScriptLocationResource]
METADATA_EXPORT_LIST = [
 ServerlessRepoApplicationReadme, ServerlessRepoApplicationLicense]

def include_transform_export_handler(template_dict, uploader, parent_dir):
    if template_dict.get('Name', None) != 'AWS::Include':
        return template_dict
        include_location = template_dict.get('Parameters', {}).get('Location', None)
        if not include_location and is_path_value_valid(include_location) or is_s3_url(include_location):
            return template_dict
        abs_include_location = os.path.join(parent_dir, include_location)
        if is_local_file(abs_include_location):
            template_dict['Parameters']['Location'] = uploader.upload_with_dedup(abs_include_location)
    else:
        raise exceptions.InvalidLocalPathError(resource_id='AWS::Include',
          property_name='Location',
          local_path=abs_include_location)
    return template_dict


GLOBAL_EXPORT_DICT = {'Fn::Transform': include_transform_export_handler}

class Template:
    __doc__ = '\n    Class to export a CloudFormation template\n    '

    def __init__(self, template_path, parent_dir, uploader, resources_to_export=frozenset(RESOURCES_EXPORT_LIST), metadata_to_export=frozenset(METADATA_EXPORT_LIST)):
        """
        Reads the template and makes it ready for export
        """
        if not (is_local_folder(parent_dir) and os.path.isabs(parent_dir)):
            raise ValueError('parent_dir parameter must be an absolute path to a folder {0}'.format(parent_dir))
        abs_template_path = make_abs_path(parent_dir, template_path)
        template_dir = os.path.dirname(abs_template_path)
        with open(abs_template_path, 'r') as (handle):
            template_str = handle.read()
        self.template_dict = yaml_parse(template_str)
        self.template_dir = template_dir
        self.resources_to_export = resources_to_export
        self.metadata_to_export = metadata_to_export
        self.uploader = uploader

    def export_global_artifacts(self, template_dict):
        """
        Template params such as AWS::Include transforms are not specific to
        any resource type but contain artifacts that should be exported,
        here we iterate through the template dict and export params with a
        handler defined in GLOBAL_EXPORT_DICT
        """
        for key, val in template_dict.items():
            if key in GLOBAL_EXPORT_DICT:
                template_dict[key] = GLOBAL_EXPORT_DICT[key](val, self.uploader, self.template_dir)
            else:
                if isinstance(val, dict):
                    self.export_global_artifacts(val)

        return template_dict

    def export_metadata(self, template_dict):
        """
        Exports the local artifacts referenced by the metadata section in
        the given template to an s3 bucket.

        :return: The template with references to artifacts that have been
        exported to s3.
        """
        if 'Metadata' not in template_dict:
            return template_dict
        for metadata_type, metadata_dict in template_dict['Metadata'].items():
            for exporter_class in self.metadata_to_export:
                if exporter_class.RESOURCE_TYPE != metadata_type:
                    continue
                exporter = exporter_class(self.uploader)
                exporter.export(metadata_type, metadata_dict, self.template_dir)

        return template_dict

    def apply_global_values(self, template_dict):
        """
        Takes values from the "Global" parameters and applies them to resources where needed for packaging.

        This transform method addresses issue 1706, where CodeUri is expected to be allowed as a global param for
        packaging, even when there may not be a build step (such as the source being an S3 file). This is the only
        known use case for using any global values in the package step, so any other such global value applications
        should be scoped to this method if possible.

        Intentionally not dealing with Api:DefinitionUri at this point.
        """
        for _, resource in self.template_dict['Resources'].items():
            resource_type = resource.get('Type', None)
            resource_dict = resource.get('Properties', None)
            if resource_dict is not None and 'CodeUri' not in resource_dict and resource_type == AWS_SERVERLESS_FUNCTION:
                code_uri_global = self.template_dict.get('Globals', {}).get('Function', {}).get('CodeUri', None)
                if code_uri_global is not None and resource_dict is not None:
                    resource_dict['CodeUri'] = code_uri_global

        return template_dict

    def export(self):
        """
        Exports the local artifacts referenced by the given template to an
        s3 bucket.

        :return: The template with references to artifacts that have been
        exported to s3.
        """
        self.template_dict = self.export_metadata(self.template_dict)
        if 'Resources' not in self.template_dict:
            return self.template_dict
        self.template_dict = self.apply_global_values(self.template_dict)
        self.template_dict = self.export_global_artifacts(self.template_dict)
        for resource_id, resource in self.template_dict['Resources'].items():
            resource_type = resource.get('Type', None)
            resource_dict = resource.get('Properties', None)
            for exporter_class in self.resources_to_export:
                if exporter_class.RESOURCE_TYPE != resource_type:
                    continue
                exporter = exporter_class(self.uploader)
                exporter.export(resource_id, resource_dict, self.template_dir)

        return self.template_dict