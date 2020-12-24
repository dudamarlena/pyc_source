# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matthew/Documents/rets/env/lib/python3.8/site-packages/rets/session.py
# Compiled at: 2020-05-13 11:01:17
# Size of source mod 2**32: 19325 bytes
import hashlib, logging, requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from six.moves.urllib.parse import urlparse, quote
from rets.exceptions import NotLoggedIn, MissingVersion, HTTPException, RETSException, MaxrowException
from rets.parsers.get_object import MultipleObjectParser
from rets.parsers.get_object import SingleObjectParser
from rets.parsers.login import OneXLogin
from rets.parsers.metadata import CompactMetadata, StandardXMLMetadata
from rets.parsers.search import OneXSearchCursor
from rets.utils import DMQLHelper
from rets.utils.get_object import GetObject
logger = logging.getLogger('rets')

class Session(object):
    __doc__ = 'The Session object that makes requests to the RETS Server'
    allowed_auth = [
     'basic', 'digest']

    def __init__(self, login_url, username, password=None, version=None, http_auth='digest', user_agent='Python RETS', user_agent_password=None, cache_metadata=True, follow_redirects=True, use_post_method=True, metadata_format='COMPACT-DECODED', session_id_cookie_name='RETS-Session-ID', search_parser=None, timeout=15):
        """
        Session constructor
        :param login_url: The login URL for the RETS feed
        :param version: The RETS version to use. Default is 1.5
        :param username: The username for the RETS feed
        :param password: The password for the RETS feed
        :param user_agent: The useragent for the RETS feed
        :param user_agent_password: The useragent password for the RETS feed
        :param follow_redirects: Follow HTTP redirects or not. The default is to follow them, True.
        :param use_post_method: Use HTTP POST method when making requests instead of GET. The default is True
        :param metadata_format: COMPACT_DECODED or STANDARD_XML. The client will attempt to set this automatically
        based on response codes from the RETS server.
        :param session_id_cookie_name: The session cookie name returned by the RETS server. Default is RETS-Session-ID
        :param search_parser: A search parser object that implements a method named generator
        """
        self.client = requests.Session()
        self.login_url = login_url
        self.username = username
        self.password = password
        self.user_agent = user_agent
        self.user_agent_password = user_agent_password
        self.http_authentication = http_auth
        self.cache_metadata = cache_metadata
        self.session_id_cookie_name = session_id_cookie_name
        self.search_parser = search_parser
        self.timeout = timeout
        self.capabilities = {}
        self.version = version
        self.metadata_responses = {}
        self.metadata_format = metadata_format
        self.capabilities = {}
        self.client = requests.Session()
        self.session_id = None
        if self.http_authentication == 'basic':
            self.client.auth = HTTPBasicAuth(self.username, self.password)
        else:
            self.client.auth = HTTPDigestAuth(self.username, self.password)
        self.client.headers = {'User-Agent':self.user_agent, 
         'Accept-Encoding':'gzip', 
         'Accept':'*/*'}
        if self.version:
            self.client.headers['RETS-Version'] = '{0!s}'.format(self.version)
        self.follow_redirects = follow_redirects
        self.use_post_method = use_post_method
        self.add_capability(name='Login', uri=(self.login_url))

    def __enter__(self):
        """Context Manager: Login when entering context"""
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context Manager: Logout when leaving context"""
        self.logout()

    def add_capability(self, name, uri):
        """
        Add a capability of the RETS board
        :param name: The name of the capability
        :param uri: The capability URI given by the RETS board
        :return: None
        """
        parse_results = urlparse(uri)
        if parse_results.hostname is None:
            login_url = self.capabilities.get('Login')
            if not login_url:
                logger.error('There is no login URL stored, so additional capabilities cannot be added.')
                raise ValueError('Cannot automatically determine absolute path for {0!s} given.'.format(uri))
            parts = urlparse(login_url)
            port = ':{}'.format(parts.port) if parts.port else ''
            uri = parts.scheme + '://' + parts.hostname + port + '/' + uri.lstrip('/')
        self.capabilities[name] = uri

    def login(self):
        """
        Login to the RETS board and return an instance of Bulletin
        :return: Bulletin instance
        """
        response = self._request('Login')
        parser = OneXLogin()
        parser.parse(response)
        self.session_id = response.cookies.get(self.session_id_cookie_name, '')
        if parser.headers.get('RETS-Version') is not None:
            self.version = str(parser.headers.get('RETS-Version'))
            self.client.headers['RETS-Version'] = self.version
        for k, v in parser.capabilities.items():
            self.add_capability(k, v)
        else:
            if self.capabilities.get('Action'):
                self._request('Action')
            return True

    def logout(self):
        """
        Logs out of the RETS feed destroying the HTTP session.
        :return: True
        """
        logger.debug('Logging out of RETS session.')
        self._request(capability='Logout')
        return True

    def get_system_metadata(self):
        """
        Get the top level metadata
        :return: dict
        """
        result = self._make_metadata_request(meta_id=0, metadata_type='METADATA-SYSTEM')
        return result.pop()

    def get_resource_metadata(self, resource=None):
        """
        Get resource metadata
        :param resource: The name of the resource to get metadata for
        :return: list
        """
        result = self._make_metadata_request(meta_id=0,
          metadata_type='METADATA-RESOURCE')
        if resource:
            result = next((item for item in result if item['ResourceID'] == resource), None)
        return result

    def get_class_metadata(self, resource):
        """
        Get classes for a given resource
        :param resource: The resource name to get class metadata for
        :return: list
        """
        return self._make_metadata_request(meta_id=resource,
          metadata_type='METADATA-CLASS')

    def get_table_metadata(self, resource, resource_class):
        """
        Get metadata for a given resource: class
        :param resource: The name of the resource
        :param resource_class: The name of the class to get metadata from
        :return: list
        """
        return self._make_metadata_request(meta_id=(resource + ':' + resource_class),
          metadata_type='METADATA-TABLE')

    def get_object_metadata(self, resource):
        """
        Get object metadata from a resource
        :param resource: The resource name to get object metadata for
        :return: list
        """
        return self._make_metadata_request(meta_id=resource,
          metadata_type='METADATA-OBJECT')

    def get_lookup_values(self, resource, lookup_name):
        """
        Get possible lookup values for a given field
        :param resource: The name of the resource
        :param lookup_name: The name of the the field to get lookup values for
        :return: list
        """
        return self._make_metadata_request(meta_id=(resource + ':' + lookup_name),
          metadata_type='METADATA-LOOKUP_TYPE')

    def _make_metadata_request--- This code section failed: ---

 L. 250         0  LOAD_STR                 '{0!s}:{1!s}'
                2  LOAD_METHOD              format
                4  LOAD_FAST                'metadata_type'
                6  LOAD_FAST                'meta_id'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'key'

 L. 251        12  LOAD_FAST                'key'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                metadata_responses
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    40  'to 40'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                cache_metadata
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 252        28  LOAD_FAST                'self'
               30  LOAD_ATTR                metadata_responses
               32  LOAD_FAST                'key'
               34  BINARY_SUBSCR    
               36  STORE_FAST               'response'
               38  JUMP_FORWARD         78  'to 78'
             40_0  COME_FROM            26  '26'
             40_1  COME_FROM            20  '20'

 L. 254        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _request

 L. 255        44  LOAD_STR                 'GetMetadata'

 L. 257        46  LOAD_STR                 'query'

 L. 258        48  LOAD_FAST                'metadata_type'

 L. 259        50  LOAD_FAST                'meta_id'

 L. 260        52  LOAD_FAST                'self'
               54  LOAD_ATTR                metadata_format

 L. 257        56  LOAD_CONST               ('Type', 'ID', 'Format')
               58  BUILD_CONST_KEY_MAP_3     3 

 L. 256        60  BUILD_MAP_1           1 

 L. 254        62  LOAD_CONST               ('capability', 'options')
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  STORE_FAST               'response'

 L. 264        68  LOAD_FAST                'response'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                metadata_responses
               74  LOAD_FAST                'key'
               76  STORE_SUBSCR     
             78_0  COME_FROM            38  '38'

 L. 266        78  LOAD_FAST                'self'
               80  LOAD_ATTR                metadata_format
               82  LOAD_STR                 'COMPACT-DECODED'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE    96  'to 96'

 L. 267        88  LOAD_GLOBAL              CompactMetadata
               90  CALL_FUNCTION_0       0  ''
               92  STORE_FAST               'parser'
               94  JUMP_FORWARD        102  'to 102'
             96_0  COME_FROM            86  '86'

 L. 269        96  LOAD_GLOBAL              StandardXMLMetadata
               98  CALL_FUNCTION_0       0  ''
              100  STORE_FAST               'parser'
            102_0  COME_FROM            94  '94'

 L. 271       102  SETUP_FINALLY       124  'to 124'

 L. 273       104  LOAD_GLOBAL              list
              106  LOAD_FAST                'parser'
              108  LOAD_ATTR                parse
              110  LOAD_FAST                'response'
              112  LOAD_FAST                'metadata_type'
              114  LOAD_CONST               ('response', 'metadata_type')
              116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              118  CALL_FUNCTION_1       1  ''
              120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_FINALLY   102  '102'

 L. 274       124  DUP_TOP          
              126  LOAD_GLOBAL              RETSException
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   246  'to 246'
              132  POP_TOP          
              134  STORE_FAST               'rets_er'
              136  POP_TOP          
              138  SETUP_FINALLY       234  'to 234'

 L. 276       140  LOAD_FAST                'self'
              142  LOAD_ATTR                metadata_responses
              144  LOAD_METHOD              pop
              146  LOAD_FAST                'key'
              148  LOAD_CONST               None
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          

 L. 279       154  LOAD_FAST                'self'
              156  LOAD_ATTR                metadata_format
              158  LOAD_STR                 'STANDARD-XML'
              160  COMPARE_OP               !=
              162  POP_JUMP_IF_FALSE   216  'to 216'
              164  LOAD_FAST                'rets_er'
              166  LOAD_ATTR                reply_code
              168  LOAD_CONST               ('20513', '20514')
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   216  'to 216'

 L. 283       174  LOAD_FAST                'self'
              176  LOAD_ATTR                metadata_responses
              178  LOAD_METHOD              pop
              180  LOAD_FAST                'key'
              182  LOAD_CONST               None
              184  CALL_METHOD_2         2  ''
              186  POP_TOP          

 L. 284       188  LOAD_STR                 'STANDARD-XML'
              190  LOAD_FAST                'self'
              192  STORE_ATTR               metadata_format

 L. 285       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _make_metadata_request

 L. 286       198  LOAD_FAST                'meta_id'

 L. 286       200  LOAD_FAST                'metadata_type'

 L. 285       202  LOAD_CONST               ('meta_id', 'metadata_type')
              204  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              206  ROT_FOUR         
              208  POP_BLOCK        
              210  POP_EXCEPT       
              212  CALL_FINALLY        234  'to 234'
              214  RETURN_VALUE     
            216_0  COME_FROM           172  '172'
            216_1  COME_FROM           162  '162'

 L. 288       216  LOAD_GLOBAL              RETSException
              218  LOAD_FAST                'rets_er'
              220  LOAD_ATTR                reply_text
              222  LOAD_FAST                'rets_er'
              224  LOAD_ATTR                reply_code
              226  CALL_FUNCTION_2       2  ''
              228  RAISE_VARARGS_1       1  'exception instance'
              230  POP_BLOCK        
              232  BEGIN_FINALLY    
            234_0  COME_FROM           212  '212'
            234_1  COME_FROM_FINALLY   138  '138'
              234  LOAD_CONST               None
              236  STORE_FAST               'rets_er'
              238  DELETE_FAST              'rets_er'
              240  END_FINALLY      
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           130  '130'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'

Parse error at or near `POP_BLOCK' instruction at offset 208

    def get_preferred_object(self, resource, object_type, content_id, location=0):
        """
        Get the first object from a Resource
        :param resource: The name of the resource
        :param object_type: The type of object to fetch
        :param content_id: The unique id of the item to get objects for
        :param location: The path to get Objects from
        :return: Object
        """
        collection = self.get_object(resource=resource,
          object_type=object_type,
          content_ids=content_id,
          object_ids='0',
          location=location)
        return next(collection)

    def get_object(self, resource, object_type, content_ids, object_ids='*', location=0):
        """
        Get a list of Objects from a resource
        :param resource: The resource to get objects from
        :param object_type: The type of object to fetch
        :param content_ids: The unique id of the item to get objects for
        :param object_ids: ids of the objects to download
        :param location: The path to get Objects from
        :return: list
        """
        object_helper = GetObject()
        request_ids = object_helper.ids(content_ids=content_ids, object_ids=object_ids)
        response = self._request(capability='GetObject',
          options={'query': {'Resource':resource, 
                   'Type':object_type, 
                   'ID':','.join(request_ids), 
                   'Location':location}})
        if 'multipart' in response.headers.get('Content-Type'):
            parser = MultipleObjectParser()
        else:
            parser = SingleObjectParser()
        collection = parser.parse_image_response(response)
        return collection

    def search--- This code section failed: ---

 L. 373         0  LOAD_FAST                'search_filter'
                2  POP_JUMP_IF_FALSE     8  'to 8'
                4  LOAD_FAST                'dmql_query'
                6  POP_JUMP_IF_TRUE     16  'to 16'
              8_0  COME_FROM             2  '2'
                8  LOAD_FAST                'search_filter'
               10  POP_JUMP_IF_TRUE     24  'to 24'
               12  LOAD_FAST                'dmql_query'
               14  POP_JUMP_IF_TRUE     24  'to 24'
             16_0  COME_FROM             6  '6'

 L. 374        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'You may specify either a search_filter or dmql_query'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM            10  '10'

 L. 376        24  LOAD_GLOBAL              DMQLHelper
               26  CALL_FUNCTION_0       0  ''
               28  STORE_FAST               'search_helper'

 L. 378        30  LOAD_FAST                'dmql_query'
               32  POP_JUMP_IF_FALSE    48  'to 48'

 L. 379        34  LOAD_FAST                'search_helper'
               36  LOAD_ATTR                dmql
               38  LOAD_FAST                'dmql_query'
               40  LOAD_CONST               ('query',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  STORE_FAST               'dmql_query'
               46  JUMP_FORWARD         60  'to 60'
             48_0  COME_FROM            32  '32'

 L. 381        48  LOAD_FAST                'search_helper'
               50  LOAD_ATTR                filter_to_dmql
               52  LOAD_FAST                'search_filter'
               54  LOAD_CONST               ('filter_dict',)
               56  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               58  STORE_FAST               'dmql_query'
             60_0  COME_FROM            46  '46'

 L. 384        60  LOAD_FAST                'resource'

 L. 385        62  LOAD_FAST                'resource_class'

 L. 386        64  LOAD_FAST                'dmql_query'

 L. 387        66  LOAD_FAST                'query_type'

 L. 388        68  LOAD_CONST               1

 L. 389        70  LOAD_FAST                'response_format'

 L. 390        72  LOAD_FAST                'standard_names'

 L. 383        74  LOAD_CONST               ('SearchType', 'Class', 'Query', 'QueryType', 'Count', 'Format', 'StandardNames')
               76  BUILD_CONST_KEY_MAP_7     7 
               78  STORE_FAST               'parameters'

 L. 393        80  LOAD_FAST                'optional_parameters'
               82  POP_JUMP_IF_TRUE     88  'to 88'

 L. 394        84  BUILD_MAP_0           0 
               86  STORE_FAST               'optional_parameters'
             88_0  COME_FROM            82  '82'

 L. 395        88  LOAD_FAST                'parameters'
               90  LOAD_METHOD              update
               92  LOAD_FAST                'optional_parameters'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 398        98  LOAD_STR                 'Select'
              100  LOAD_FAST                'parameters'
              102  COMPARE_OP               in
              104  POP_JUMP_IF_FALSE   140  'to 140'
              106  LOAD_GLOBAL              isinstance
              108  LOAD_FAST                'parameters'
              110  LOAD_METHOD              get
              112  LOAD_STR                 'Select'
              114  CALL_METHOD_1         1  ''
              116  LOAD_GLOBAL              list
              118  CALL_FUNCTION_2       2  ''
              120  POP_JUMP_IF_FALSE   140  'to 140'

 L. 399       122  LOAD_STR                 ','
              124  LOAD_METHOD              join
              126  LOAD_FAST                'parameters'
              128  LOAD_STR                 'Select'
              130  BINARY_SUBSCR    
              132  CALL_METHOD_1         1  ''
              134  LOAD_FAST                'parameters'
              136  LOAD_STR                 'Select'
              138  STORE_SUBSCR     
            140_0  COME_FROM           120  '120'
            140_1  COME_FROM           104  '104'

 L. 401       140  LOAD_FAST                'limit'
              142  POP_JUMP_IF_FALSE   152  'to 152'

 L. 402       144  LOAD_FAST                'limit'
              146  LOAD_FAST                'parameters'
              148  LOAD_STR                 'Limit'
              150  STORE_SUBSCR     
            152_0  COME_FROM           142  '142'

 L. 404       152  LOAD_FAST                'offset'
              154  POP_JUMP_IF_FALSE   164  'to 164'

 L. 405       156  LOAD_FAST                'offset'
              158  LOAD_FAST                'parameters'
              160  LOAD_STR                 'Offset'
              162  STORE_SUBSCR     
            164_0  COME_FROM           154  '154'

 L. 407       164  LOAD_FAST                'self'
              166  LOAD_ATTR                search_parser
              168  POP_JUMP_IF_FALSE   178  'to 178'

 L. 408       170  LOAD_FAST                'self'
              172  LOAD_ATTR                search_parser
              174  STORE_FAST               'search_cursor'
              176  JUMP_FORWARD        184  'to 184'
            178_0  COME_FROM           168  '168'

 L. 410       178  LOAD_GLOBAL              OneXSearchCursor
              180  CALL_FUNCTION_0       0  ''
              182  STORE_FAST               'search_cursor'
            184_0  COME_FROM           176  '176'

 L. 412       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _request

 L. 413       188  LOAD_STR                 'Search'

 L. 413       190  LOAD_STR                 'query'
              192  LOAD_FAST                'parameters'
              194  BUILD_MAP_1           1 

 L. 413       196  LOAD_CONST               True

 L. 412       198  LOAD_CONST               ('capability', 'options', 'stream')
              200  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              202  STORE_FAST               'response'

 L. 416       204  SETUP_FINALLY       240  'to 240'

 L. 417       206  LOAD_FAST                'search_cursor'
              208  LOAD_ATTR                generator
              210  LOAD_FAST                'response'
              212  LOAD_CONST               ('response',)
              214  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              216  GET_ITER         
              218  FOR_ITER            230  'to 230'
              220  STORE_FAST               'res'

 L. 418       222  LOAD_FAST                'res'
              224  YIELD_VALUE      
              226  POP_TOP          
              228  JUMP_BACK           218  'to 218'

 L. 419       230  POP_BLOCK        
          232_234  BREAK_LOOP          356  'to 356'
              236  POP_BLOCK        
              238  JUMP_BACK           204  'to 204'
            240_0  COME_FROM_FINALLY   204  '204'

 L. 421       240  DUP_TOP          
              242  LOAD_GLOBAL              MaxrowException
              244  COMPARE_OP               exception-match
          246_248  POP_JUMP_IF_FALSE   352  'to 352'
              250  POP_TOP          
              252  STORE_FAST               'max_exception'
              254  POP_TOP          
              256  SETUP_FINALLY       340  'to 340'

 L. 423       258  LOAD_FAST                'auto_offset'
          260_262  POP_JUMP_IF_FALSE   326  'to 326'
              264  LOAD_FAST                'limit'
              266  LOAD_FAST                'max_exception'
              268  LOAD_ATTR                rows_returned
              270  COMPARE_OP               >
          272_274  POP_JUMP_IF_FALSE   326  'to 326'

 L. 424       276  LOAD_FAST                'limit'
              278  LOAD_FAST                'max_exception'
              280  LOAD_ATTR                rows_returned
              282  BINARY_SUBTRACT  
              284  LOAD_FAST                'parameters'
              286  LOAD_STR                 'Limit'
              288  STORE_SUBSCR     

 L. 425       290  LOAD_FAST                'offset'
              292  LOAD_FAST                'max_exception'
              294  LOAD_ATTR                rows_returned
              296  BINARY_ADD       
              298  LOAD_FAST                'parameters'
              300  LOAD_STR                 'Offset'
              302  STORE_SUBSCR     

 L. 426       304  LOAD_FAST                'self'
              306  LOAD_ATTR                _request

 L. 427       308  LOAD_STR                 'Search'

 L. 427       310  LOAD_STR                 'query'
              312  LOAD_FAST                'parameters'
              314  BUILD_MAP_1           1 

 L. 427       316  LOAD_CONST               True

 L. 426       318  LOAD_CONST               ('capability', 'options', 'stream')
              320  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              322  STORE_FAST               'response'
              324  JUMP_FORWARD        336  'to 336'
            326_0  COME_FROM           272  '272'
            326_1  COME_FROM           260  '260'

 L. 430       326  POP_BLOCK        
              328  POP_EXCEPT       
              330  CALL_FINALLY        340  'to 340'
          332_334  BREAK_LOOP          356  'to 356'
            336_0  COME_FROM           324  '324'
              336  POP_BLOCK        
              338  BEGIN_FINALLY    
            340_0  COME_FROM           330  '330'
            340_1  COME_FROM_FINALLY   256  '256'
              340  LOAD_CONST               None
              342  STORE_FAST               'max_exception'
              344  DELETE_FAST              'max_exception'
              346  END_FINALLY      
              348  POP_EXCEPT       
              350  JUMP_BACK           204  'to 204'
            352_0  COME_FROM           246  '246'
              352  END_FINALLY      
              354  JUMP_BACK           204  'to 204'

Parse error at or near `POP_EXCEPT' instruction at offset 328

    def _request(self, capability, options=None, stream=False):
        """
        Make a _request to the RETS server
        :param capability: The name of the capability to use to get the URI
        :param options: Options to put into the _request
        :return: Response
        """
        if options is None:
            options = {}
        else:
            options.update({'headers': self.client.headers.copy()})
            url = self.capabilities.get(capability)
            if not url:
                msg = '{0!s} tried but no valid endpoints was found. Did you forget to Login?'.format(capability)
                raise NotLoggedIn(msg)
            if self.user_agent_password:
                ua_digest = self._user_agent_digest_hash()
                options['headers']['RETS-UA-Authorization'] = 'Digest {0!s}'.format(ua_digest)
            if self.use_post_method and capability != 'Action':
                query = options.get('query')
                response = self.client.post(url,
                  data=query, headers=(options['headers']), stream=stream, timeout=(self.timeout))
            else:
                if 'query' in options:
                    url += '?' + '&'.join(('{0!s}={1!s}'.format(k, quote(str(v))) for k, v in options['query'].items()))
            response = self.client.get(url, headers=(options['headers']), stream=stream, timeout=(self.timeout))
        if response.status_code in (400, 401):
            if capability == 'Login':
                if self.http_authentication == 'digest':
                    self.http_authentication = 'basic'
                    self.client.auth = HTTPBasicAuth(self.username, self.password)
                    return self._request(capability, options, stream)
                m = 'Could not log into the RETS server with the provided credentials in basic or digest.'
            else:
                m = 'The RETS server returned a 401 status code. You must be logged in to make this request.'
            raise NotLoggedIn(m)
        else:
            if response.status_code == 404:
                if self.use_post_method:
                    raise HTTPException('Got a 404 when making a POST request. Try setting use_post_method=False when initializing the Session.')
            return response

    def _user_agent_digest_hash(self):
        """
        Hash the user agent and user agent password
        Section 3.10 of https://www.nar.realtor/retsorg.nsf/retsproto1.7d6.pdf
        :return: md5
        """
        if not self.version:
            raise MissingVersion('A version is required for user agent auth. The RETS server should set thisautomatically but it has not. Please instantiate the session with a version argumentto provide the version.')
        version_number = self.version.strip('RETS/')
        user_str = '{0!s}:{1!s}'.format(self.user_agent, self.user_agent_password).encode('utf-8')
        a1 = hashlib.md5(user_str).hexdigest()
        session_id = self.session_id if self.session_id is not None else ''
        digest_str = '{0!s}::{1!s}:{2!s}'.format(a1, session_id, version_number).encode('utf-8')
        digest = hashlib.md5(digest_str).hexdigest()
        return digest