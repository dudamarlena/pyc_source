# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/s3filesystem.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 7721 bytes
"""
This module contains the S3Storage plugin for fastr
"""
import urllib.parse, os, fastr, fastr.data
from fastr import exceptions
from fastr.core.ioplugin import IOPlugin
boto_loaded = False
try:
    import boto3, botocore
    boto_loaded = True
except ImportError:
    pass

class S3Filesystem(IOPlugin):
    __doc__ = '\n    .. warning::\n\n        As this IOPlugin is under development, it has not been thoroughly\n        tested.\n\n        example url: s3://bucket.server/path/to/resource\n    '
    scheme = ('s3', 's3list')

    def __init__(self):
        super(S3Filesystem, self).__init__()
        self._s3clients = {}

    def cleanup(self):
        pass

    @classmethod
    def test(cls):
        if not boto_loaded:
            raise exceptions.FastrImportError('Could not import the required boto3/botocore modules for this plugin')

    def expand_url(self, url):
        """
                Expand an S3 URL. This allows a source to collect multiple
                samples from a single url.

                :param str url: url to expand
                :return: the resulting url(s), a tuple if multiple, otherwise a str
                :rtype: str or tuple of str
        """
        if fastr.data.url.get_url_scheme(url) != 's3list':
            raise exceptions.FastrValueError('URL not of {} type!'.format('s3list'))
        try:
            data = self._get_file_as_var(url)
            return tuple(((None, x.strip()) for x in data.strip().split('\n')))
        except botocore.exceptions.ClientError as e:
            try:
                raise self._translate_boto_to_fastr_exception(e)
            finally:
                e = None
                del e

    def fetch_url(self, inurl, outpath):
        """
        Get the file(s) or values from s3.

        :param inurl: url to the item in the data store
        :param outpath: path where to store the fetch data locally
        """
        if fastr.data.url.get_url_scheme(inurl) != 's3':
            raise exceptions.FastrValueError('URL not of {} type!'.format('s3'))
        parsed_url = self._parse_url(inurl)
        s3 = self._create_client(profile=(parsed_url['profile']), server=(parsed_url['server']), bucket=(parsed_url['bucket']))
        try:
            s3.download_file(parsed_url['key'], outpath)
        except botocore.exceptions.ClientError as e:
            try:
                raise self._translate_boto_to_fastr_exception(e)
            finally:
                e = None
                del e

    def put_url(self, inpath, outurl):
        """
        Upload the files to the S3 storage

        :param inpath: path to the local data
        :param outurl: url to where to store the data in the external data store.
        """
        if fastr.data.url.get_url_scheme(outurl) != 's3':
            raise exceptions.FastrValueError('URL not of {} type!'.format('s3'))
        if os.path.isdir(inpath):
            try:
                listdir = os.listdir(inpath)
            except:
                raise exceptions.FastrIOError('Could not listdir {}'.format(inpath))
            else:
                for path in listdir:
                    if not outurl[-1:] == '/':
                        outurl = outurl + '/'
                    self.put_url(os.path.join(inpath, path), outurl + path)

        else:
            parsed_url = self._parse_url(outurl)
            s3 = self._create_client(profile=(parsed_url['profile']), server=(parsed_url['server']), bucket=(parsed_url['bucket']))
        try:
            s3.upload_file(inpath, parsed_url['key'])
            return True
        except botocore.exceptions.ClientError as e:
            try:
                raise self._translate_boto_to_fastr_exception(e)
            finally:
                e = None
                del e

    def put_value(self, value, outurl):
        """
        Put the value in S3

        :param value: value to store
        :param outurl: url to where to store the data, starts with ``file://``
        """
        if fastr.data.url.get_url_scheme(outurl) != 's3':
            raise exceptions.FastrValueError('URL not of {} type!'.format('s3'))
        parsed_url = self._parse_url(outurl)
        s3 = self._create_client(profile=(parsed_url['profile']), server=(parsed_url['server']), bucket=(parsed_url['bucket']))
        try:
            s3.put_object(Body=value, Key=(parsed_url['key']))
            return True
        except botocore.exceptions.ClientError as e:
            try:
                raise self._translate_boto_to_fastr_exception(e)
            finally:
                e = None
                del e

    def fetch_value(self, inurl):
        """
        Fetch a value from S3

        :param inurl: url of the value to read
        :return: the fetched value
        """
        if fastr.data.url.get_url_scheme(inurl) != 's3':
            raise exceptions.FastrValueError('URL not of {} type!'.format('s3'))
        try:
            return self._get_file_as_var(inurl)
        except botocore.exceptions.ClientError as e:
            try:
                raise self._translate_boto_to_fastr_exception(e)
            finally:
                e = None
                del e

    def _translate_boto_to_fastr_exception(self, exception):
        res = exception.response
        if res['Error']['Code'] == '404':
            return exceptions.FastrDataTypeValueError('The file was not found: ')
        return exceptions.FastrIOError('{} {} {}'.format(res['Error']['Code'], res['ResponseMetadata']['RequestId'], res['Error']['Message']))

    def _get_file_as_var(self, url):
        parsed_url = self._parse_url(url)
        s3 = self._create_client(profile=(parsed_url['profile']), server=(parsed_url['server']), bucket=(parsed_url['bucket']))
        try:
            return s3.Object(parsed_url['key']).get()['Body'].read().decode('utf-8')
        except botocore.exceptions.ClientError as e:
            try:
                raise
            finally:
                e = None
                del e

    def _parse_url(self, url):
        url = urllib.parse.urlparse(url)
        parts = url.netloc.split('@', 1)
        if len(parts) == 2:
            profile = parts[0]
            parts = parts[1].split('.', 1)
        else:
            profile = 'default'
            parts = parts[0].split('.', 1)
        if url.path[0] == '/':
            key = url.path[1:]
        else:
            key = url.path
        return {'bucket':parts[0],  'server':parts[1],  'profile':profile,  'key':key}

    def _create_client(self, profile, server, bucket):
        client_key = '{}.{}'.format(profile, server)
        if client_key in self._s3clients:
            s3 = self._s3clients[client_key]
        else:
            session = boto3.Session(profile_name=profile)
            s3 = session.resource('s3', endpoint_url=('http://{}'.format(server))).Bucket(bucket)
            self._s3clients[client_key] = s3
        return s3