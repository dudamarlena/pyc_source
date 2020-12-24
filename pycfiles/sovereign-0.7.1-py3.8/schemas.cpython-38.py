# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/schemas.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 9640 bytes
import zlib, multiprocessing
from collections import defaultdict
from datetime import datetime, timedelta
from functools import cached_property
from pydantic import BaseModel, StrictBool, Field
from typing import List, Any, Dict
from jinja2 import Template
from sovereign.config_loader import load
Instance = Dict
Instances = List[Instance]
Scope = str

class SourceData(BaseModel):
    scopes = defaultdict(list)
    scopes: Dict[(Scope, Instances)]


class ConfiguredSource(BaseModel):
    type: str
    config: dict
    scope = 'default'
    scope: str


class SourceMetadata(BaseModel):
    updated = datetime.fromtimestamp(0)
    updated: datetime
    count = 0
    count: int

    def update_date(self):
        self.updated = datetime.now()

    def update_count(self, iterable):
        self.count = len(iterable)

    @property
    def is_stale(self):
        return self.updated < datetime.now() - timedelta(minutes=2)

    def __str__(self):
        return f"Sources were last updated at {datetime.isoformat(self.updated)}. There are {self.count} instances."


class StatsdConfig(BaseModel):
    host = '127.0.0.1'
    host: str
    port = 8125
    port: int
    tags = dict()
    tags: dict
    namespace = 'sovereign'
    namespace: str
    enabled = False
    enabled: bool
    use_ms = True
    use_ms: bool

    @property
    def loaded_tags(self):
        return {load(v):k for k, v in self.tags.items()}


class XdsTemplate(BaseModel):
    path: str

    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    @property
    def is_python_source(self) -> bool:
        return self.path.startswith('python://')

    @cached_property
    def code(self):
        return load(self.path)

    @cached_property
    def content(self) -> Template:
        return load(self.path)

    @property
    def checksum(self) -> int:
        return zlib.adler32(self.source.encode())

    @cached_property
    def source(self) -> str:
        if 'jinja' in self.path:
            path = self.path.replace('+jinja', '+string')
            return load(path)
        if self.is_python_source:
            path = self.path.replace('python', 'file+string')
            return load(path)
        return str(self.content)


class Locality(BaseModel):
    region = Field(None)
    region: str
    zone = Field(None)
    zone: str
    sub_zone = Field(None)
    sub_zone: str


class SemanticVersion(BaseModel):
    major = 0
    major: int
    minor = 0
    minor: int
    patch = 0
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


class BuildVersion(BaseModel):
    version = SemanticVersion()
    version: SemanticVersion
    metadata = {}
    metadata: dict


class Extension(BaseModel):
    name = None
    name: str
    category = None
    category: str
    version = None
    version: BuildVersion
    disabled = None
    disabled: bool


class Node(BaseModel):
    id = Field('-', title='Hostname')
    id: str
    cluster = Field(...,
      title='Envoy service-cluster',
      description='The ``--service-cluster`` configured by the Envoy client')
    cluster: str
    metadata = Field(None, title='Key:value metadata')
    metadata: dict
    locality = Field((Locality()), title='Locality')
    locality: Locality
    build_version = Field(None,
      title='Envoy build/release version string',
      description='Used to identify what version of Envoy the client is running, and what config to provide in response')
    build_version: str
    user_agent_name = 'envoy'
    user_agent_name: str
    user_agent_version = ''
    user_agent_version: str
    user_agent_build_version = BuildVersion()
    user_agent_build_version: BuildVersion
    extensions = []
    extensions: List[Extension]
    client_features = []
    client_features: List[str]

    @property
    def common(self):
        """
        Returns fields that are the same in adjacent proxies
        ie. proxies that are part of the same logical group
        """
        return (
         self.cluster,
         self.build_version,
         self.user_agent_version,
         self.user_agent_build_version,
         self.locality)


class Resources(list):
    __doc__ = '\n    Acts like a regular list except it returns True\n    for all membership tests when empty.\n    '

    def __contains__(self, item):
        if len(self) == 0:
            return True
        return item in list(self)


class DiscoveryRequest(BaseModel):
    node = Field(..., title='Node information about the envoy proxy')
    node: Node
    version_info = Field('0', title='The version of the envoy clients current configuration')
    version_info: str
    resource_names = Field((Resources()), title='List of requested resource names')
    resource_names: Resources

    @property
    def envoy_version--- This code section failed: ---

 L. 186         0  SETUP_FINALLY        32  'to 32'

 L. 187         2  LOAD_GLOBAL              str
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                node
                8  LOAD_ATTR                user_agent_build_version
               10  LOAD_ATTR                version
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'version'

 L. 188        16  LOAD_FAST                'version'
               18  LOAD_STR                 '0.0.0'
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  LOAD_ASSERT              AssertionError
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'
               28  POP_BLOCK        
               30  JUMP_FORWARD        110  'to 110'
             32_0  COME_FROM_FINALLY     0  '0'

 L. 189        32  DUP_TOP          
               34  LOAD_GLOBAL              AssertionError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE   108  'to 108'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 190        46  SETUP_FINALLY        76  'to 76'

 L. 191        48  LOAD_FAST                'self'
               50  LOAD_ATTR                node
               52  LOAD_ATTR                build_version
               54  STORE_FAST               'build_version'

 L. 192        56  LOAD_FAST                'build_version'
               58  LOAD_METHOD              split
               60  LOAD_STR                 '/'
               62  CALL_METHOD_1         1  ''
               64  UNPACK_EX_2+0           
               66  STORE_FAST               'revision'
               68  STORE_FAST               'version'
               70  STORE_FAST               'other_metadata'
               72  POP_BLOCK        
               74  JUMP_FORWARD        104  'to 104'
             76_0  COME_FROM_FINALLY    46  '46'

 L. 193        76  DUP_TOP          
               78  LOAD_GLOBAL              AttributeError
               80  LOAD_GLOBAL              ValueError
               82  BUILD_TUPLE_2         2 
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   102  'to 102'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 195        94  POP_EXCEPT       
               96  POP_EXCEPT       
               98  LOAD_STR                 'default'
              100  RETURN_VALUE     
            102_0  COME_FROM            86  '86'
              102  END_FINALLY      
            104_0  COME_FROM            74  '74'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            38  '38'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            30  '30'

 L. 196       110  LOAD_FAST                'version'
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_STR' instruction at offset 98

    @property
    def resources(self):
        return Resources(self.resource_names)


class DiscoveryResponse(BaseModel):
    version_info = Field(..., title='The version of the configuration in the response')
    version_info: str
    resources = Field(..., title='The requested configuration resources')
    resources: List[Any]


class SovereignAsgiConfig(BaseModel):
    host = load('env://SOVEREIGN_HOST', '0.0.0.0')
    host: str
    port = load('env://SOVEREIGN_PORT', 8080)
    port: int
    keepalive = load('env://SOVEREIGN_KEEPALIVE', 5)
    keepalive: int
    workers = load('env://SOVEREIGN_WORKERS', multiprocessing.cpu_count() * 2 + 1)
    workers: int
    reuse_port = True
    reuse_port: bool
    log_level = 'warning'
    log_level: str
    worker_class = 'uvicorn.workers.UvicornWorker'
    worker_class: str

    def as_gunicorn_conf(self):
        return {'bind':':'.join(map(str, [self.host, self.port])), 
         'keepalive':self.keepalive, 
         'reuse_port':self.reuse_port, 
         'loglevel':self.log_level, 
         'workers':self.workers, 
         'worker_class':self.worker_class}


class SovereignConfig(BaseModel):
    sources: List[ConfiguredSource]
    templates: dict
    template_context = {}
    template_context: dict
    eds_priority_matrix = {}
    eds_priority_matrix: dict
    modifiers = []
    modifiers: List[str]
    global_modifiers = []
    global_modifiers: List[str]
    regions = []
    regions: List[str]
    statsd = StatsdConfig()
    statsd: StatsdConfig
    auth_enabled = load('env://SOVEREIGN_AUTH_ENABLED', False)
    auth_enabled: StrictBool
    auth_passwords = load('env://SOVEREIGN_AUTH_PASSWORDS', '')
    auth_passwords: str
    encryption_key = load('env://SOVEREIGN_ENCRYPTION_KEY', '') or load('env://FERNET_ENCRYPTION_KEY', '')
    encryption_key: str
    environment = load('env://SOVEREIGN_ENVIRONMENT_TYPE', '') or load('env://MICROS_ENVTYPE', 'local')
    environment: str
    debug_enabled = load('env://SOVEREIGN_DEBUG', False)
    debug_enabled: StrictBool
    sentry_dsn = load('env://SOVEREIGN_SENTRY_DSN', '')
    sentry_dsn: str
    node_match_key = load('env://SOVEREIGN_NODE_MATCH_KEY', 'cluster')
    node_match_key: str
    node_matching = load('env://SOVEREIGN_MATCHING_ENABLED', True)
    node_matching: StrictBool
    source_match_key = load('env://SOVEREIGN_SOURCE_MATCH_KEY', 'service_clusters')
    source_match_key: str
    sources_refresh_rate = load('env://SOVEREIGN_SOURCES_REFRESH_RATE', 30)
    sources_refresh_rate: int
    refresh_context = load('env://SOVEREIGN_REFRESH_CONTEXT', False)
    refresh_context: StrictBool
    context_refresh_rate = load('env://SOVEREIGN_CONTEXT_REFRESH_RATE', 3600)
    context_refresh_rate: int
    context_cache_size = load('env://SOVEREIGN_CONTEXT_CACHE_SIZE', 1000)
    context_cache_size: int
    dns_hard_fail = load('env://SOVEREIGN_DNS_HARD_FAIL', False)
    dns_hard_fail: StrictBool
    enable_access_logs = load('env://SOVEREIGN_ENABLE_ACCESS_LOGS', True)
    enable_access_logs: StrictBool

    class Config:
        keep_untouched = (
         cached_property,)

    @property
    def passwords(self):
        return self.auth_passwords.split(',') or []

    @cached_property
    def xds_templates(self):
        ret = {'__any__': {}}
        for version, templates in self.templates.items():
            loaded_templates = {XdsTemplate(path=path):_type for _type, path in templates.items()}
            ret[version] = loaded_templates
            ret['__any__'].update(loaded_templates)
        else:
            return ret

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        kwargs = [f"{k}={v}" for k, v in self.show().items()]
        return f"SovereignConfig({kwargs})"

    def show(self):
        safe_items = dict()
        for key, value in self.__dict__.items():
            if key in ('auth_passwords', 'encryption_key', 'passwords', 'sentry_dsn'):
                value = 'redacted'
            safe_items[key] = value
        else:
            return safe_items