# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/lib/swagger/reader.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 9489 bytes
"""
Read Swagger documents from variety of sources
"""
import os, tempfile, logging
from six.moves.urllib.parse import urlparse, parse_qs
from six import string_types
import boto3, botocore
from samcli.yamlhelper import yaml_parse
LOG = logging.getLogger(__name__)
_FN_TRANSFORM = 'Fn::Transform'

def parse_aws_include_transform(data):
    """
    If the input data is an AWS::Include data, then parse and return the location of the included file.

    AWS::Include transform data usually has the following format:
    {
        "Fn::Transform": {
            "Name": "AWS::Include",
            "Parameters": {
                "Location": "s3://MyAmazonS3BucketName/swagger.yaml"
            }
        }
    }

    Parameters
    ----------
    data : dict
        Dictionary data to parse

    Returns
    -------
    str
        Location of the included file, if available. None, otherwise
    """
    if not data:
        return
    if _FN_TRANSFORM not in data:
        return
    transform_data = data[_FN_TRANSFORM]
    name = transform_data.get('Name')
    location = transform_data.get('Parameters', {}).get('Location')
    if name == 'AWS::Include':
        LOG.debug('Successfully parsed location from AWS::Include transform: %s', location)
        return location


class SwaggerReader:
    __doc__ = '\n    Class to read and parse Swagger document from a variety of sources. This class accepts the same data formats as\n    available in Serverless::Api SAM resource\n    '

    def __init__(self, definition_body=None, definition_uri=None, working_dir=None):
        """
        Initialize the class with swagger location

        Parameters
        ----------
        definition_body : dict
            Swagger document as a dictionary directly or inlined using AWS::Include transform.

        definition_uri : str or dict
            Location of the Swagger file. Supports three formats:
                - S3 URI Ex: ``s3://mybucket/swagger.yaml``
                - S3 URI as a dictionary Ex: ``{"Bucket": "mybucket", "Key": "swagger.yaml", "Version": "123"}``
                - Local file path either as absolute or relative path Ex: ``./swagger.yaml``. Relative paths are
                  resolved to with respect to the given working directory.

        working_dir : str
            Path to the working directory with respect which we will resolve local relative paths
        """
        self.definition_body = definition_body
        self.definition_uri = definition_uri
        self.working_dir = working_dir
        if not self.definition_body:
            if not self.definition_uri:
                raise ValueError('Require value for either DefinitionBody or DefinitionUri')

    def read(self):
        """
        Gets the Swagger document from either of the given locations. If we fail to retrieve or parse the Swagger
        file, this method will return None.

        Returns
        -------
        dict:
            Swagger document. None, if we cannot retrieve the document
        """
        swagger = None
        if self.definition_body:
            swagger = self._read_from_definition_body()
        if not swagger:
            if self.definition_uri:
                swagger = self._download_swagger(self.definition_uri)
        return swagger

    def _read_from_definition_body(self):
        """
        Read the Swagger document from DefinitionBody. It could either be an inline Swagger dictionary or an
        AWS::Include macro that contains location of the included Swagger. In the later case, we will download and
        parse the Swagger document.

        Returns
        -------
        dict
            Swagger document, if we were able to parse. None, otherwise
        """
        location = parse_aws_include_transform(self.definition_body)
        if location:
            LOG.debug('Trying to download Swagger from %s', location)
            return self._download_swagger(location)
        LOG.debug('Detected Inline Swagger definition')
        return self.definition_body

    def _download_swagger(self, location):
        """
        Download the file from given local or remote location and return it

        Parameters
        ----------
        location : str or dict
            Local path or S3 path to Swagger file to download. Consult the ``__init__.py`` documentation for specifics
            on structure of this property.

        Returns
        -------
        dict or None
            Downloaded and parsed Swagger document. None, if unable to download
        """
        if not location:
            return
        else:
            bucket, key, version = self._parse_s3_location(location)
            if bucket:
                if key:
                    LOG.debug('Downloading Swagger document from Bucket=%s, Key=%s, Version=%s', bucket, key, version)
                    swagger_str = self._download_from_s3(bucket, key, version)
                    return yaml_parse(swagger_str)
            if not isinstance(location, string_types):
                LOG.debug('Unable to download Swagger file. Invalid location: %s', location)
                return
            filepath = location
            if self.working_dir:
                filepath = os.path.join(self.working_dir, location)
            os.path.exists(filepath) or LOG.debug('Unable to download Swagger file. File not found at location %s', filepath)
            return
        LOG.debug('Reading Swagger document from local file at %s', filepath)
        with open(filepath, 'r') as (fp):
            return yaml_parse(fp.read())

    @staticmethod
    def _download_from_s3(bucket, key, version=None):
        """
        Download a file from given S3 location, if available.

        Parameters
        ----------
        bucket : str
            S3 Bucket name

        key : str
            S3 Bucket Key aka file path

        version : str
            Optional Version ID of the file

        Returns
        -------
        str
            Contents of the file that was downloaded

        Raises
        ------
        botocore.exceptions.ClientError if we were unable to download the file from S3
        """
        s3 = boto3.client('s3')
        extra_args = {}
        if version:
            extra_args['VersionId'] = version
        with tempfile.TemporaryFile() as (fp):
            try:
                s3.download_fileobj(bucket, key, fp, ExtraArgs=extra_args)
                fp.seek(0)
                return fp.read()
            except botocore.exceptions.ClientError:
                LOG.error('Unable to download Swagger document from S3 Bucket=%s Key=%s Version=%s', bucket, key, version)
                raise

    @staticmethod
    def _parse_s3_location(location):
        """
        Parses the given location input as a S3 Location and returns the file's bucket, key and version as separate
        values. Input can be in two different formats:

        1. Dictionary with ``Bucket``, ``Key``, ``Version`` keys
        2. String of S3 URI in format ``s3://<bucket>/<key>?versionId=<version>``

        If the input is not in either of the above formats, this method will return (None, None, None) tuple for all
        the values.

        Parameters
        ----------
        location : str or dict
            Location of the S3 file

        Returns
        -------
        str
            Name of the S3 Bucket. None, if bucket value was not found
        str
            Key of the file from S3. None, if key was not provided
        str
            Optional Version ID of the file. None, if version ID is not provided
        """
        bucket, key, version = (None, None, None)
        if isinstance(location, dict):
            bucket, key, version = location.get('Bucket'), location.get('Key'), location.get('Version')
        else:
            if isinstance(location, string_types):
                if location.startswith('s3://'):
                    parsed = urlparse(location)
                    query = parse_qs(parsed.query)
                    bucket = parsed.netloc
                    key = parsed.path.lstrip('/')
                    if query:
                        if 'versionId' in query:
                            if len(query['versionId']) == 1:
                                version = query['versionId'][0]
        return (
         bucket, key, version)