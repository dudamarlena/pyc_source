# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/python_storagelib/src/kiwixstorage/__init__.py
# Compiled at: 2020-04-13 13:58:15
# Size of source mod 2**32: 25252 bytes
""" Kiwix/OpenZIM S3 interface

    helpers for S3 storage, autoconf from URL + Wasabi (wasabisys.com) extras

    Goal is mainly to provide a configured s3.client and s3.resource from an URL
    Users could limit usage to this and use boto3 directly from there.

    A few additional wrappers are in place to simplify common actions.
    Also, non-S3, wasabi-specific features are exposed directly. """
import sys, uuid, json, urllib, pathlib, hashlib, logging, datetime, threading, boto3, botocore, requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
logger = logging.getLogger(__name__)

class TransferHook(object):
    __doc__ = ' Generic transfer hook based on size '

    def __init__(self, size=-1, output=sys.stdout, flush=None, name='', fmt='\r{progress} / {total} ({percentage:.2f}%)'):
        self.size = size
        self.output = output
        if flush is None:
            if getattr(output, 'name') in ('<stdout>', '<stderr>'):
                flush = True
        self.flush = bool(flush)
        self.name = name
        self.fmt = fmt
        self.seen_so_far = 0

    def __call__(self, bytes_amount):
        self.seen_so_far += bytes_amount
        if self.size > 0:
            total = self.size
            percentage = self.seen_so_far / self.size * 100
        else:
            total = '?'
            percentage = 0
        self.output.write(self.fmt.format(name=(self.name),
          progress=(self.seen_so_far),
          total=total,
          percentage=percentage))
        if self.flush:
            self.output.flush()


class FileTransferHook(TransferHook):
    __doc__ = ' Sample progress report hook printing to STDOUT '

    def __init__(self, filename, output=sys.stdout, flush=None, fmt='\r{name} {progress} / {total} ({percentage:.2f}%)'):
        super().__init__(size=(float(pathlib.Path(filename).stat().st_size)),
          output=output,
          flush=flush,
          fmt=fmt)
        self.name = filename
        self.lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self.lock:
            super().__call__(bytes_amount)


class HeadStat(object):
    __doc__ = ' easy access to useful object properties '

    def __init__(self, data={}):
        self.data = data

    def __dict__(self):
        return ', '.join([f"{k}={getattr(self, k)}" for k in ('mtime', 'size', 'etag',
                                                              'type', 'meta')])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__()})"

    def __str__(self):
        return str(self.__repr__())

    @property
    def mtime(self):
        return self.data.get('LastModified')

    @property
    def size(self):
        return self.data.get('ContentLength')

    @property
    def etag(self):
        return self.data.get('ETag')

    @property
    def type(self):
        return self.data.get('ContentType')

    @property
    def meta(self):
        return self.data.get('Metadata')


class AuthenticationError(Exception):
    pass


class NotFoundError(Exception):
    pass


class KiwixStorage(object):
    BUCKET_NAME = 'bucketname'
    KEY_ID = 'keyid'
    SECRET_KEY = 'secretaccesskey'
    ENDPOINT_URL = 'endpoint_url'
    EXTRA_ARGS_KEY = 'ExtraArgs'
    META_KEY = 'Metadata'
    CALLBACK_KEY = 'Callback'
    PUBLIC_ACCESS_POLICY = '{\n  "Version": "2012-10-17",\n  "Statement": [\n    {\n      "Sid": "AllowPublicDownloads",\n      "Effect": "Allow",\n      "Principal": "*",\n      "Action": ["s3:GetObject"],\n      "Resource": "arn:aws:s3:::{bucket_name}/*"\n    }\n  ]\n}\n'

    def __init__(self, url, **kwargs):
        self._resource = self._bucket = None
        self._params = {}
        (self._parse_url)(url, **kwargs)

    def _parse_url(self, url, **kwargs):
        try:
            self.url = urllib.parse.urlparse(url)
            env = {v:k.lower() for k, v in urllib.parse.parse_qs(self.url.query).items()}
            env['endpoint_url'] = f"{self.url.scheme}://{self.url.netloc}"
            for key in (self.KEY_ID, self.SECRET_KEY, self.BUCKET_NAME):
                env[key] = env.get(key, [None])[(-1)]

        except Exception as exc:
            try:
                raise ValueError(f"Incorrect URL: {exc}")
            finally:
                exc = None
                del exc

        else:
            self._params.update(env)
            self._params.update(kwargs)

    @property
    def params(self):
        """ dict of query parameters from URL """
        return self._params

    @property
    def bucket_name(self):
        """ bucket name set in URL """
        return self.params.get(self.BUCKET_NAME)

    @property
    def is_wasabi(self):
        return self.url.hostname.endswith('wasabisys.com')

    @property
    def wasabi_url(self):
        return f"https://{self.url.netloc}"

    @property
    def region(self):
        """ region from URL endpoint """
        parts = self.url.hostname.split('.', 2)
        if len(parts) < 3:
            return
        return parts[1]

    @property
    def client(self):
        """ Configured boto3 client """
        return self.resource.meta.client

    @property
    def aws_auth(self):
        """ requests-compatible AWS authentication plugin """
        return self.get_aws_auth_for(access_key_id=(self.params.get(self.KEY_ID)),
          secret_access_key=(self.params.get(self.SECRET_KEY)),
          host=(self.url.netloc))

    @property
    def resource(self):
        if self._resource is None:
            self._resource = self.get_resource()
        return self._resource

    def get_resource(self):
        """ Configured boto3.resource('s3') """
        try:
            return boto3.resource('s3',
              aws_access_key_id=(self.params.get(self.KEY_ID)),
              aws_secret_access_key=(self.params.get(self.SECRET_KEY)),
              endpoint_url=(self.params.get(self.ENDPOINT_URL)))
            except Exception as exc:
            try:
                raise AuthenticationError(str(exc))
            finally:
                exc = None
                del exc

    def get_service_endpoint(self, service_name):
        """ non-s3 service endpoint based on provided URL """
        domain = self.url.netloc.split('.', 1)[1]
        return f"https://{service_name}.{domain}"

    def get_service(self, service_name, use_default_region=True):
        """ configured generic boto3 service """
        try:
            return boto3.client(service_name,
              aws_access_key_id=(self.params.get(self.KEY_ID)),
              aws_secret_access_key=(self.params.get(self.SECRET_KEY)),
              endpoint_url=(self.get_service_endpoint('iam')),
              region_name='us-east-1' if (self.is_wasabi and use_default_region) else (self.region))
            except Exception as exc:
            try:
                raise AuthenticationError(str(exc))
            finally:
                exc = None
                del exc

    def test_access_list_buckets(self):
        self.client.list_buckets()

    def test_access_bucket(self, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        if not bucket_name:
            raise ValueError("Can't test for bucket without a bucket name")
        if self.get_bucket(bucket_name).creation_date is None:
            raise AuthenticationError("Bucket doesn't exist of not reachable")

    def test_access_write(self, key=None, bucket_name=None, check_read=False):
        bucket_name = self._bucket_name_param(bucket_name)
        if not bucket_name:
            raise ValueError("Can't test for write without a bucket name")
        if key is None:
            key = f"{uuid.uuid4().hex}/{uuid.uuid4().hex}"
        self.put_text_object(key, key, bucket_name=bucket_name)
        try:
            try:
                if check_read:
                    self.test_access_read(key, bucket_name)
            except Exception as exc:
                try:
                    raise exc
                finally:
                    exc = None
                    del exc

        finally:
            self.client.delete_object(Bucket=(self.bucket_name), Key=key)

    def test_access_read(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        if not bucket_name:
            raise ValueError("Can't test for read without a bucket name")
        elif self.has_object(key):
            self.get_object_head(key)
        else:
            raise ValueError(f"Can't test read with missing key: {key}")

    def check_credentials--- This code section failed: ---

 L. 317         0  LOAD_FAST                'list_buckets'
                2  POP_JUMP_IF_TRUE     24  'to 24'
                4  LOAD_FAST                'bucket'
                6  POP_JUMP_IF_TRUE     24  'to 24'
                8  LOAD_FAST                'write'
               10  POP_JUMP_IF_TRUE     24  'to 24'
               12  LOAD_FAST                'read'
               14  POP_JUMP_IF_TRUE     24  'to 24'

 L. 318        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'Nothing to test your credentials over.'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM            10  '10'
             24_2  COME_FROM             6  '6'
             24_3  COME_FROM             2  '2'

 L. 319        24  SETUP_FINALLY       208  'to 208'

 L. 320        26  SETUP_FINALLY        50  'to 50'

 L. 321        28  LOAD_FAST                'self'
               30  LOAD_ATTR                client
               32  POP_TOP          

 L. 323        34  LOAD_FAST                'list_buckets'
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 324        38  LOAD_FAST                'self'
               40  LOAD_METHOD              test_access_list_buckets
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
             46_0  COME_FROM            36  '36'
               46  POP_BLOCK        
               48  JUMP_FORWARD         98  'to 98'
             50_0  COME_FROM_FINALLY    26  '26'

 L. 325        50  DUP_TOP          
               52  LOAD_GLOBAL              botocore
               54  LOAD_ATTR                exceptions
               56  LOAD_ATTR                ClientError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    96  'to 96'
               62  POP_TOP          
               64  STORE_FAST               'exc'
               66  POP_TOP          
               68  SETUP_FINALLY        84  'to 84'

 L. 326        70  LOAD_GLOBAL              AuthenticationError
               72  LOAD_FAST                'exc'
               74  FORMAT_VALUE          0  ''
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_FINALLY    68  '68'
               84  LOAD_CONST               None
               86  STORE_FAST               'exc'
               88  DELETE_FAST              'exc'
               90  END_FINALLY      
               92  POP_EXCEPT       
               94  JUMP_FORWARD         98  'to 98'
             96_0  COME_FROM            60  '60'
               96  END_FINALLY      
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            48  '48'

 L. 328        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'bucket'
              102  LOAD_GLOBAL              str
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_FALSE   112  'to 112'
              108  LOAD_FAST                'bucket'
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM           106  '106'
              112  LOAD_CONST               None
            114_0  COME_FROM           110  '110'
              114  STORE_FAST               'bucket_name'

 L. 330       116  LOAD_FAST                'bucket'
              118  POP_JUMP_IF_FALSE   132  'to 132'

 L. 331       120  LOAD_FAST                'self'
              122  LOAD_ATTR                test_access_bucket
              124  LOAD_FAST                'bucket_name'
              126  LOAD_CONST               ('bucket_name',)
              128  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              130  POP_TOP          
            132_0  COME_FROM           118  '118'

 L. 333       132  LOAD_FAST                'write'
              134  POP_JUMP_IF_FALSE   170  'to 170'

 L. 334       136  LOAD_FAST                'self'
              138  LOAD_ATTR                test_access_write

 L. 335       140  LOAD_GLOBAL              isinstance
              142  LOAD_FAST                'write'
              144  LOAD_GLOBAL              str
              146  CALL_FUNCTION_2       2  ''
              148  POP_JUMP_IF_FALSE   154  'to 154'
              150  LOAD_FAST                'write'
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           148  '148'
              154  LOAD_CONST               None
            156_0  COME_FROM           152  '152'

 L. 336       156  LOAD_FAST                'bucket_name'

 L. 337       158  LOAD_FAST                'read'
              160  LOAD_CONST               True
              162  COMPARE_OP               is

 L. 334       164  LOAD_CONST               ('key', 'bucket_name', 'check_read')
              166  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              168  POP_TOP          
            170_0  COME_FROM           134  '134'

 L. 340       170  LOAD_FAST                'read'
              172  POP_JUMP_IF_FALSE   204  'to 204'
              174  LOAD_FAST                'read'
              176  LOAD_CONST               True
              178  COMPARE_OP               is-not
              180  POP_JUMP_IF_TRUE    186  'to 186'
              182  LOAD_FAST                'write'
              184  POP_JUMP_IF_TRUE    204  'to 204'
            186_0  COME_FROM           180  '180'

 L. 341       186  LOAD_FAST                'self'
              188  LOAD_ATTR                test_access_read

 L. 342       190  LOAD_GLOBAL              str
              192  LOAD_FAST                'read'
              194  CALL_FUNCTION_1       1  ''

 L. 342       196  LOAD_FAST                'bucket_name'

 L. 341       198  LOAD_CONST               ('read', 'bucket_name')
              200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              202  POP_TOP          
            204_0  COME_FROM           184  '184'
            204_1  COME_FROM           172  '172'
              204  POP_BLOCK        
              206  JUMP_FORWARD        262  'to 262'
            208_0  COME_FROM_FINALLY    24  '24'

 L. 344       208  DUP_TOP          
              210  LOAD_GLOBAL              AuthenticationError
              212  COMPARE_OP               exception-match
          214_216  POP_JUMP_IF_FALSE   260  'to 260'
              218  POP_TOP          
              220  STORE_FAST               'exc'
              222  POP_TOP          
              224  SETUP_FINALLY       248  'to 248'

 L. 345       226  LOAD_FAST                'failsafe'
              228  POP_JUMP_IF_FALSE   240  'to 240'

 L. 346       230  POP_BLOCK        
              232  POP_EXCEPT       
              234  CALL_FINALLY        248  'to 248'
              236  LOAD_CONST               False
              238  RETURN_VALUE     
            240_0  COME_FROM           228  '228'

 L. 347       240  LOAD_FAST                'exc'
              242  RAISE_VARARGS_1       1  'exception instance'
              244  POP_BLOCK        
              246  BEGIN_FINALLY    
            248_0  COME_FROM           234  '234'
            248_1  COME_FROM_FINALLY   224  '224'
              248  LOAD_CONST               None
              250  STORE_FAST               'exc'
              252  DELETE_FAST              'exc'
              254  END_FINALLY      
              256  POP_EXCEPT       
              258  JUMP_FORWARD        262  'to 262'
            260_0  COME_FROM           214  '214'
              260  END_FINALLY      
            262_0  COME_FROM           258  '258'
            262_1  COME_FROM           206  '206'

 L. 348       262  LOAD_CONST               True
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 232

    def _bucket_name_param(self, bucket_name=None):
        """ passed bucket_name if defined else self.bucket_name

            Used to easily use provided param if present & default to configured one"""
        if bucket_name is None:
            if not self.bucket_name:
                raise ValueError('No bucket_name supplied (not in params nor url)')
        if bucket_name is None:
            return self.bucket_name
        return bucket_name

    @property
    def bucket(self):
        if not self.bucket_name:
            return NotFoundError('No bucket specified')
        if self._bucket is None:
            self._bucket = self.get_bucket()
        return self._bucket

    @property
    def bucket_names(self):
        return [b['Name'] for b in self.client.list_buckets()['Buckets']]

    def bucket_exists(self, bucket_name=None):
        """ whether bucket exists on server """
        bucket_name = self._bucket_name_param(bucket_name)
        return bucket_name in self.bucket_names

    def get_bucket(self, bucket_name=None, must_exists=False):
        """ s3.Bucket()a from URL or param """
        bucket_name = self._bucket_name_param(bucket_name)
        if must_exists:
            if not self.bucket_exists(bucket_name):
                raise ValueError(f"Bucket `{bucket_name} does not exists or not reachable")
        return self.resource.Bucket(bucket_name)

    def create_bucket(self, bucket_name, **kwargs):
        bucket_name = self._bucket_name_param(bucket_name)
        if self.bucket_exists(bucket_name):
            raise ValueError(f"Bucket {bucket_name} already exists.")
        return (self.client.create_bucket)(Bucket=bucket_name, **kwargs)

    def has_object--- This code section failed: ---

 L. 393         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _bucket_name_param
                4  LOAD_FAST                'bucket_name'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'bucket_name'

 L. 394        10  SETUP_FINALLY        28  'to 28'

 L. 395        12  LOAD_FAST                'self'
               14  LOAD_METHOD              get_object_head
               16  LOAD_FAST                'key'
               18  LOAD_FAST                'bucket_name'
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          
               24  POP_BLOCK        
               26  JUMP_FORWARD        126  'to 126'
             28_0  COME_FROM_FINALLY    10  '10'

 L. 396        28  DUP_TOP          
               30  LOAD_GLOBAL              botocore
               32  LOAD_ATTR                exceptions
               34  LOAD_ATTR                ClientError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE   124  'to 124'
               40  POP_TOP          
               42  STORE_FAST               'e'
               44  POP_TOP          
               46  SETUP_FINALLY       112  'to 112'

 L. 397        48  LOAD_GLOBAL              int
               50  LOAD_FAST                'e'
               52  LOAD_ATTR                response
               54  LOAD_STR                 'Error'
               56  BINARY_SUBSCR    
               58  LOAD_STR                 'Code'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'error_code'

 L. 398        66  LOAD_FAST                'error_code'
               68  LOAD_CONST               403
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    90  'to 90'

 L. 399        74  LOAD_GLOBAL              AuthenticationError
               76  LOAD_STR                 'Authorization Error testing key='
               78  LOAD_FAST                'key'
               80  FORMAT_VALUE          0  ''
               82  BUILD_STRING_2        2 
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
               88  JUMP_FORWARD        108  'to 108'
             90_0  COME_FROM            72  '72'

 L. 400        90  LOAD_FAST                'error_code'
               92  LOAD_CONST               404
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L. 401        98  POP_BLOCK        
              100  POP_EXCEPT       
              102  CALL_FINALLY        112  'to 112'
              104  LOAD_CONST               False
              106  RETURN_VALUE     
            108_0  COME_FROM            96  '96'
            108_1  COME_FROM            88  '88'
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM           102  '102'
            112_1  COME_FROM_FINALLY    46  '46'
              112  LOAD_CONST               None
              114  STORE_FAST               'e'
              116  DELETE_FAST              'e'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            38  '38'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            26  '26'

 L. 402       126  LOAD_CONST               True
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 100

    def has_object_matching_etag--- This code section failed: ---

 L. 405         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _bucket_name_param
                4  LOAD_FAST                'bucket_name'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'bucket_name'

 L. 406        10  SETUP_FINALLY        28  'to 28'

 L. 407        12  LOAD_FAST                'self'
               14  LOAD_METHOD              get_object_etag
               16  LOAD_FAST                'key'
               18  LOAD_FAST                'bucket_name'
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               's3_etag'
               24  POP_BLOCK        
               26  JUMP_FORWARD        126  'to 126'
             28_0  COME_FROM_FINALLY    10  '10'

 L. 408        28  DUP_TOP          
               30  LOAD_GLOBAL              botocore
               32  LOAD_ATTR                exceptions
               34  LOAD_ATTR                ClientError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE   124  'to 124'
               40  POP_TOP          
               42  STORE_FAST               'e'
               44  POP_TOP          
               46  SETUP_FINALLY       112  'to 112'

 L. 409        48  LOAD_GLOBAL              int
               50  LOAD_FAST                'e'
               52  LOAD_ATTR                response
               54  LOAD_STR                 'Error'
               56  BINARY_SUBSCR    
               58  LOAD_STR                 'Code'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'error_code'

 L. 410        66  LOAD_FAST                'error_code'
               68  LOAD_CONST               403
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    90  'to 90'

 L. 411        74  LOAD_GLOBAL              AuthenticationError
               76  LOAD_STR                 'Authorization Error testing key='
               78  LOAD_FAST                'key'
               80  FORMAT_VALUE          0  ''
               82  BUILD_STRING_2        2 
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
               88  JUMP_FORWARD        108  'to 108'
             90_0  COME_FROM            72  '72'

 L. 412        90  LOAD_FAST                'error_code'
               92  LOAD_CONST               404
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L. 413        98  POP_BLOCK        
              100  POP_EXCEPT       
              102  CALL_FINALLY        112  'to 112'
              104  LOAD_CONST               False
              106  RETURN_VALUE     
            108_0  COME_FROM            96  '96'
            108_1  COME_FROM            88  '88'
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM           102  '102'
            112_1  COME_FROM_FINALLY    46  '46'
              112  LOAD_CONST               None
              114  STORE_FAST               'e'
              116  DELETE_FAST              'e'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            38  '38'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            26  '26'

 L. 414       126  LOAD_FAST                'etag'
              128  LOAD_FAST                's3_etag'
              130  COMPARE_OP               ==
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 100

    def has_object_matching_meta--- This code section failed: ---

 L. 417         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _bucket_name_param
                4  LOAD_FAST                'bucket_name'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'bucket_name'

 L. 418        10  SETUP_FINALLY        38  'to 38'

 L. 419        12  LOAD_FAST                'self'
               14  LOAD_ATTR                get_object_head
               16  LOAD_FAST                'key'
               18  LOAD_FAST                'bucket_name'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                META_KEY
               24  BUILD_LIST_1          1 
               26  LOAD_CONST               ('only',)
               28  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               30  UNPACK_SEQUENCE_1     1 
               32  STORE_FAST               'meta'
               34  POP_BLOCK        
               36  JUMP_FORWARD        136  'to 136'
             38_0  COME_FROM_FINALLY    10  '10'

 L. 420        38  DUP_TOP          
               40  LOAD_GLOBAL              botocore
               42  LOAD_ATTR                exceptions
               44  LOAD_ATTR                ClientError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE   134  'to 134'
               50  POP_TOP          
               52  STORE_FAST               'e'
               54  POP_TOP          
               56  SETUP_FINALLY       122  'to 122'

 L. 421        58  LOAD_GLOBAL              int
               60  LOAD_FAST                'e'
               62  LOAD_ATTR                response
               64  LOAD_STR                 'Error'
               66  BINARY_SUBSCR    
               68  LOAD_STR                 'Code'
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'error_code'

 L. 422        76  LOAD_FAST                'error_code'
               78  LOAD_CONST               403
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   100  'to 100'

 L. 423        84  LOAD_GLOBAL              AuthenticationError
               86  LOAD_STR                 'Authorization Error testing key='
               88  LOAD_FAST                'key'
               90  FORMAT_VALUE          0  ''
               92  BUILD_STRING_2        2 
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
               98  JUMP_FORWARD        118  'to 118'
            100_0  COME_FROM            82  '82'

 L. 424       100  LOAD_FAST                'error_code'
              102  LOAD_CONST               404
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   118  'to 118'

 L. 425       108  POP_BLOCK        
              110  POP_EXCEPT       
              112  CALL_FINALLY        122  'to 122'
              114  LOAD_CONST               False
              116  RETURN_VALUE     
            118_0  COME_FROM           106  '106'
            118_1  COME_FROM            98  '98'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM           112  '112'
            122_1  COME_FROM_FINALLY    56  '56'
              122  LOAD_CONST               None
              124  STORE_FAST               'e'
              126  DELETE_FAST              'e'
              128  END_FINALLY      
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM            48  '48'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM            36  '36'

 L. 427       136  LOAD_FAST                'meta'
              138  LOAD_METHOD              get
              140  LOAD_FAST                'tag'
              142  CALL_METHOD_1         1  ''
              144  LOAD_FAST                'value'
              146  COMPARE_OP               ==
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 110

    def get_object(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        return self.resource.Object(bucket_name=bucket_name, key=key)

    def get_object_head(self, key, bucket_name=None, unserialize_etag=True, only=None):
        bucket_name = self._bucket_name_param(bucket_name)
        response = self.client.head_object(Bucket=bucket_name, Key=key)
        if unserialize_etag:
            if 'ETag' in response.keys():
                response['ETag'] = json.loads(response['ETag'])
        if only is not None:
            return [value for key, value in response.items() if key in only]
        return response

    def get_object_stat(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        return HeadStat(self.get_object_head(key, bucket_name))

    def get_object_etag(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        return self.get_object_stat(key, bucket_name).etag

    def put_text_object(self, key, content, bucket_name=None, **kwargs):
        """ records a simple text file """
        bucket_name = self._bucket_name_param(bucket_name)
        (self.client.put_object)(Bucket=bucket_name, 
         Key=key, Body=content.encode('UTF-8'), **kwargs)

    def allow_public_downloads_on(self, bucket_name=None):
        """ sets policy on bucket to allow anyone to GET objects (downloads)

            TODO: add this policy instead of overwriting everything """
        if not self.is_wasabi:
            raise NotImplementedError('Only Wasabi at the moment.')
        bucket_name = self._bucket_name_param(bucket_name)
        policy = self.PUBLIC_ACCESS_POLICY.replace('{bucket_name}', bucket_name)
        self.get_bucket(bucket_name).Policy().put(Policy=policy)

    def set_bucket_autodelete_after(self, nb_days, bucket_name=None):
        """ apply compliance setting RetentionDays and DeleteAfterRetention """
        if not self.is_wasabi:
            raise NotImplementedError('Only Wasabi at the moment')
        bucket_name = self._bucket_name_param(bucket_name)
        compliance = '<BucketComplianceConfiguration>\n\t<Status>enabled</Status>\n\t<LockTime>off</LockTime>\n\t<RetentionDays>{nb_days}</RetentionDays>\n\t<DeleteAfterRetention>true</DeleteAfterRetention>\n</BucketComplianceConfiguration>'.format(nb_days=nb_days)
        return self.set_wasabi_compliance(compliance, key=None, bucket_name=bucket_name)

    def set_object_autodelete_on(self, key, on, bucket_name=None):
        """ apply compliance setting RetentionTime

             """
        if not self.is_wasabi:
            raise NotImplementedError('Only Wasabi at the moment')
        if on.tzinfo != datetime.timezone.utc:
            on = on.astimezone(datetime.timezone.utc)
        bucket_name = self._bucket_name_param(bucket_name)
        compliance = '<ObjectComplianceConfiguration>\n\t<ConditionalHold>false</ConditionalHold>\n\t<RetentionTime>{retention_time}</RetentionTime>\n</ObjectComplianceConfiguration>'.format(retention_time=(on.isoformat(timespec='seconds').replace('+00:00', 'Z')))
        return self.set_wasabi_compliance(compliance, key=key, bucket_name=bucket_name)

    def delete_bucket(self, bucket_name=None, force=False):
        """ delete a bucket

            force (bool) only for Wasabi: delete even if there are objects in bucket """
        bucket_name = self._bucket_name_param(bucket_name)
        if not force:
            return self.client.delete_bucket(Bucket=bucket_name)
        if not self.is_wasabi:
            raise NotImplementedError('Only Wasabi allows force delete')
        url = f"{self.wasabi_url}/{bucket_name}?force_delete=true"
        req = requests.delete(url, auth=(self.aws_auth))
        req.raise_for_status()

    def rename_bucket(self, new_bucket_name, bucket_name=None):
        """ change name or a bucket """
        if not self.is_wasabi:
            raise NotImplementedError('Only Wasabi allows bucket rename')
        bucket_name = self._bucket_name_param(bucket_name)
        url = f"{self.wasabi_url}/{bucket_name}"
        req = requests.request('MOVE',
          url, headers={'Destination': new_bucket_name}, auth=(self.aws_auth))
        req.raise_for_status()
        return req.text

    def rename_objects(self, key, new_key, overwrite=False, as_prefix=False, bucket_name=None):
        """ change key of an object or list of objects

            overwrite (bool) whether to overwrite destination
            as_prefix (bool) rename whole bucket keys starting with `key`
             and replacing this part with `new_key` """
        if not self.is_wasabi:
            raise NotImplementedError('Only Wasabi allows objects rename')
        bucket_name = self._bucket_name_param(bucket_name)
        url = f"{self.wasabi_url}/{bucket_name}/{key}"
        req = requests.request('MOVE',
          url,
          auth=(self.aws_auth),
          headers={'Destination':new_key, 
         'Overwrite':'true' if overwrite else 'false', 
         'X-Wasabi-Quiet':'true', 
         'X-Wasabi-Prefix':'true' if as_prefix else 'false'})
        req.raise_for_status()
        return req.text

    @staticmethod
    def get_aws_auth_for(access_key_id, secret_access_key, host='s3.us-west-1.wasabisys.com', region='', service='s3'):
        """ prepares AWS Signature v4 headers for requests

            Sets: Authorization, x-amz-date and x-amz-content-sha256 """
        return AWSRequestsAuth(aws_access_key=access_key_id,
          aws_secret_access_key=secret_access_key,
          aws_host=host,
          aws_region=region,
          aws_service=service)

    def set_wasabi_compliance(self, compliance, key=None, bucket_name=None):
        """ apply a compliance to a bucket of object """
        if not self.is_wasabi:
            raise NotImplementedError('Only Wasabi feature')
        url = f"{self.wasabi_url}/{bucket_name}"
        if key is not None:
            url += f"/{key}"
        url += '?compliance'
        req = requests.put(url=url, auth=(self.aws_auth), data=compliance)
        req.raise_for_status()
        return req

    def _mix_kwargs(self, meta=None, progress=False, progress_size=None, progress_fpath=None, **kwargs):
        """ parse and mix shortcut args with boto3 ones

            meta (dict): sets Metadata
            progress (bool): enables default progress report
            progress (callable): custom progress report hook
            progress_size: sets size for auto progress reporter
            progress_fpath: sets fpath for auto progress reporter
            """
        if meta:
            if self.EXTRA_ARGS_KEY not in kwargs:
                kwargs[self.EXTRA_ARGS_KEY] = {}
            if self.META_KEY not in kwargs[self.EXTRA_ARGS_KEY]:
                kwargs[self.EXTRA_ARGS_KEY][self.META_KEY] = {}
            kwargs[self.EXTRA_ARGS_KEY][self.META_KEY].update(meta)
        elif progress:
            if self.CALLBACK_KEY not in kwargs:
                if callable(progress):
                    kwargs[self.CALLBACK_KEY] = progress
                else:
                    if progress_fpath:
                        kwargs[self.CALLBACK_KEY] = FileTransferHook(progress_fpath)
                    else:
                        if progress_size:
                            kwargs[self.CALLBACK_KEY] = TransferHook(size=progress_size)
                        else:
                            kwargs[self.CALLBACK_KEY] = TransferHook()
        return kwargs

    def upload_file(self, fpath, key, bucket_name=None, meta=None, progress=False, **kwargs):
        """ upload a file to the bucket

            meta (dict): metadata for the object
            progress (bool): enable default progress report
            progress (callable): your own progress report callback """
        bucket = self.get_bucket(bucket_name) if bucket_name else self.bucket
        kwargs = (self._mix_kwargs)(meta=meta, 
         progress=progress, progress_fpath=fpath, **kwargs)
        print(kwargs)
        (bucket.upload_file)(Filename=str(fpath), Key=key, **kwargs)

    def download_file(self, key, fpath, bucket_name=None, progress=False, **kwargs):
        """ download object to fpath using boto3

            progress (bool): enable default progress report
            progress (callable): your own progress report callback """
        bucket_name = self._bucket_name_param(bucket_name)
        size = self.get_object_stat(key, bucket_name).size if progress is True else None
        kwargs = (self._mix_kwargs)(progress=progress, progress_size=size, **kwargs)
        (self.resource.Bucket(bucket_name).download_file)(Key=key, 
         Filename=str(fpath), **kwargs)

    def get_download_url(self, key, bucket_name=None, prefer_torrent=True):
        """ URL of object for external download

            torrent is a shortcut for calling {key}.torrent which is the uploader's
            responsibility to create.
            if testing this torrent file key results in 404, fallback to {key}.

            this is not using GetObjectTorrent as it is limited to 5G on AWS
            and not supported at all on Wasabi. """
        bucket_name = self._bucket_name_param(bucket_name)
        torrent_key = f"{key}.torrent"
        if prefer_torrent:
            if self.has_object(torrent_key, bucket_name):
                return self.get_download_url(torrent_key, bucket_name, prefer_torrent=False)
        return f"https://{self.url.netloc}/{bucket_name}/{key}"

    def validate_file_etag(self, fpath: pathlib.Path, etag: str):
        """ Validates a server ETag matches a local file

            Using recipe from https://teppen.io/2018/10/23/aws_s3_verify_etags/ """

        def factor_of_1MB(filesize, num_parts):
            x = filesize / int(num_parts)
            y = x % 1048576
            return int(x + 1048576 - y)

        def possible_partsizes(filesize, num_parts):
            return lambda partsize: partsize < filesize and float(filesize) / float(partsize) <= num_parts

        def calc_etag(fpath, partsize):
            md5_digests = []
            with open(fpath, 'rb') as (f):
                for chunk in iter(lambda : f.read(partsize), ''):
                    md5_digests.append(hashlib.md5(chunk).digest())

            return hashlib.md5(''.join(md5_digests)).hexdigest() + '-' + str(len(md5_digests))

        def md5sum(fpath):
            h = hashlib.md5()
            with open(fpath, 'rb') as (f):
                for chunk in iter(lambda : f.read(8388608), ''):
                    h.update(chunk)

            return h.hexdigest()

        filesize = fpath.stat().st_size
        num_parts = etag.rsplit('-', 1)[(-1)]
        if not num_parts.isnumeric():
            num_parts = 1
        num_parts = int(num_parts)
        if num_parts == 1:
            return md5sum(fpath) == etag
        partsizes = [
         8388608,
         15728640,
         factor_of_1MB(filesize, num_parts)]
        for partsize in filter(possible_partsizes(filesize, num_parts), partsizes):
            if etag == calc_etag(fpath, partsize):
                return True
            return False