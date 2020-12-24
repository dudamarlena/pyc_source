# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/config_loader.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 4693 bytes
"""
Configuration Loader
--------------------
Various functions that assist in loading initial configuration for the
control plane.

The control plane accepts a main configuration file from the environment
variable ``SOVEREIGN_CONFIG`` which follows the format:

.. code-block:: none

   <scheme>://path[,<scheme>://path,...]

Examples:

.. code-block:: none

   # Single file
     file:///etc/sovereign.yaml

   # Multiple files (comma separated)
     file:///etc/sovereign/common.yaml,file:///etc/sovereign/dev.yaml

   # Other types of sources
     http://config.myserver.com/environments/dev.yaml

   # Other types of formats
     http+json://config.myserver.com/environments/dev.json
     http+jinja://config.myserver.com/environments/dev.j2
     http+yaml://config.myserver.com/environments/dev.yaml

"""
import os, json, yaml, jinja2, requests, importlib
from importlib.machinery import SourceFileLoader
from pathlib import Path
from pkg_resources import resource_string
jinja_env = jinja2.Environment(enable_async=True, autoescape=True)
serializers = {'yaml':yaml.safe_load, 
 'json':json.loads, 
 'jinja':jinja_env.from_string, 
 'string':str}

def raise_(e):
    raise e


try:
    import ujson
    serializers['ujson'] = ujson.loads
    jinja_env.policies['json.dumps_function'] = ujson.dumps
except ImportError:
    serializers['ujson'] = lambda *a, **kw: raise_(ImportError('ujson must be installed to use in config_loaders'))

try:
    import orjson
    serializers['orjson'] = orjson.loads
    jinja_env.policies['json.dumps_function'] = lambda *a, **kw: (orjson.dumps)(*a, **kw).decode()
    jinja_env.policies['json.dumps_kwargs'] = {'option': orjson.OPT_SORT_KEYS}
except ImportError:
    serializers['orjson'] = lambda *a, **kw: raise_(ImportError('orjson must be installed to use in config_loaders'))
else:
    try:
        import boto3
    except ImportError:
        boto3 = None
    else:

        def load_file--- This code section failed: ---

 L.  83         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'path'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           42  'to 42'
                8  STORE_FAST               'f'

 L.  84        10  LOAD_FAST                'f'
               12  LOAD_METHOD              read
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'contents'

 L.  85        18  LOAD_GLOBAL              serializers
               20  LOAD_FAST                'loader'
               22  BINARY_SUBSCR    
               24  LOAD_FAST                'contents'
               26  CALL_FUNCTION_1       1  ''
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH        6  '6'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 30


        def load_package_data(path, loader):
            pkg, pkg_file = path.split(':')
            data = resource_string(pkg, pkg_file)
            try:
                data = data.decode()
            except AttributeError:
                pass
            else:
                return serializers[loader](data)


        def load_http(path, loader):
            response = requests.get(path)
            response.raise_for_status()
            data = response.text
            return serializers[loader](data)


        def load_env(variable, loader=None):
            data = os.getenv(variable)
            try:
                return serializers[loader](data)
                    except AttributeError as e:
                try:
                    raise AttributeError(f"Unable to read environment variable {variable}: {repr(e)}")
                finally:
                    e = None
                    del e


        def load_module(name, _=None):
            return importlib.import_module(name)


        def load_s3(path: str, loader=None):
            if isinstance(boto3, type(None)):
                raise ImportError('boto3 must be installed to load S3 paths. Use ``pip install sovereign[boto]``')
            bucket, key = path.split('/', maxsplit=1)
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=bucket, Key=key)
            data = ''.join([chunk.decode() for chunk in response['Body']])
            return serializers[loader](data)


        def load_python(path, _=None):
            p = Path(path).absolute()
            loader = SourceFileLoader((p.name), path=(str(p)))
            return loader.load_module(p.name)


        loaders = {'file':load_file, 
         'pkgdata':load_package_data, 
         'http':load_http, 
         'https':load_http, 
         'env':load_env, 
         'module':load_module, 
         's3':load_s3, 
         'python':load_python}

        def parse_spec(spec, default_serialization='yaml'):
            serialization = default_serialization
            scheme, path = spec.split('://')
            if '+' in scheme:
                scheme, serialization = scheme.split('+')
            if 'http' in scheme:
                path = '://'.join([scheme, path])
            return (
             scheme, path, serialization)


        def is_parseable(spec):
            if '://' not in spec:
                return False
            scheme, _, serialization = parse_spec(spec)
            return scheme in loaders and serialization in serializers


        def load--- This code section failed: ---

 L. 166         0  LOAD_STR                 '://'
                2  LOAD_FAST                'spec'
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 167         8  LOAD_FAST                'spec'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 168        12  LOAD_GLOBAL              parse_spec
               14  LOAD_FAST                'spec'
               16  CALL_FUNCTION_1       1  ''
               18  UNPACK_SEQUENCE_3     3 
               20  STORE_FAST               'scheme'
               22  STORE_FAST               'path'
               24  STORE_FAST               'serialization'

 L. 170        26  SETUP_FINALLY        44  'to 44'

 L. 171        28  LOAD_GLOBAL              loaders
               30  LOAD_FAST                'scheme'
               32  BINARY_SUBSCR    
               34  LOAD_FAST                'path'
               36  LOAD_FAST                'serialization'
               38  CALL_FUNCTION_2       2  ''
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    26  '26'

 L. 172        44  DUP_TOP          
               46  LOAD_GLOBAL              Exception
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    80  'to 80'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 173        58  LOAD_FAST                'default'
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 174        66  LOAD_FAST                'default'
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
             74_0  COME_FROM            64  '64'

 L. 175        74  RAISE_VARARGS_0       0  'reraise'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            50  '50'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'

Parse error at or near `POP_TOP' instruction at offset 54