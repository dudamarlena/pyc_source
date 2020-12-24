# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/flask_limiter/extension.py
# Compiled at: 2020-02-26 13:44:48
# Size of source mod 2**32: 27566 bytes
"""
the flask extension
"""
import datetime, itertools, logging, sys, time, warnings
from functools import wraps
import six
from flask import request, current_app, g, Blueprint
from limits.errors import ConfigurationError
from limits.storage import storage_from_string, MemoryStorage
from limits.strategies import STRATEGIES
from werkzeug.http import http_date, parse_date
from flask_limiter.wrappers import Limit, LimitGroup
from .errors import RateLimitExceeded
from .util import get_ipaddr

class C:
    ENABLED = 'RATELIMIT_ENABLED'
    HEADERS_ENABLED = 'RATELIMIT_HEADERS_ENABLED'
    STORAGE_URL = 'RATELIMIT_STORAGE_URL'
    STORAGE_OPTIONS = 'RATELIMIT_STORAGE_OPTIONS'
    STRATEGY = 'RATELIMIT_STRATEGY'
    GLOBAL_LIMITS = 'RATELIMIT_GLOBAL'
    DEFAULT_LIMITS = 'RATELIMIT_DEFAULT'
    DEFAULT_LIMITS_PER_METHOD = 'RATELIMIT_DEFAULTS_PER_METHOD'
    APPLICATION_LIMITS = 'RATELIMIT_APPLICATION'
    HEADER_LIMIT = 'RATELIMIT_HEADER_LIMIT'
    HEADER_REMAINING = 'RATELIMIT_HEADER_REMAINING'
    HEADER_RESET = 'RATELIMIT_HEADER_RESET'
    SWALLOW_ERRORS = 'RATELIMIT_SWALLOW_ERRORS'
    IN_MEMORY_FALLBACK = 'RATELIMIT_IN_MEMORY_FALLBACK'
    IN_MEMORY_FALLBACK_ENABLED = 'RATELIMIT_IN_MEMORY_FALLBACK_ENABLED'
    HEADER_RETRY_AFTER = 'RATELIMIT_HEADER_RETRY_AFTER'
    HEADER_RETRY_AFTER_VALUE = 'RATELIMIT_HEADER_RETRY_AFTER_VALUE'
    KEY_PREFIX = 'RATELIMIT_KEY_PREFIX'


class HEADERS:
    RESET = 1
    REMAINING = 2
    LIMIT = 3
    RETRY_AFTER = 4


MAX_BACKEND_CHECKS = 5

class Limiter(object):
    __doc__ = '\n    :param app: :class:`flask.Flask` instance to initialize the extension\n     with.\n    :param list default_limits: a variable list of strings or callables returning strings denoting global\n     limits to apply to all routes. :ref:`ratelimit-string` for  more details.\n    :param bool default_limits_per_method: whether default limits are applied per method, per route or as a combination\n     of all method per route.\n    :param list application_limits: a variable list of strings or callables returning strings for limits that\n     are applied to the entire application (i.e a shared limit for all routes)\n    :param function key_func: a callable that returns the domain to rate limit by.\n    :param bool headers_enabled: whether ``X-RateLimit`` response headers are written.\n    :param str strategy: the strategy to use. refer to :ref:`ratelimit-strategy`\n    :param str storage_uri: the storage location. refer to :ref:`ratelimit-conf`\n    :param dict storage_options: kwargs to pass to the storage implementation upon\n      instantiation.\n    :param bool auto_check: whether to automatically check the rate limit in the before_request\n     chain of the application. default ``True``\n    :param bool swallow_errors: whether to swallow errors when hitting a rate limit.\n     An exception will still be logged. default ``False``\n    :param list in_memory_fallback: a variable list of strings or callables returning strings denoting fallback\n     limits to apply when the storage is down.\n    :param bool in_memory_fallback_enabled: simply falls back to in memory storage\n     when the main storage is down and inherits the original limits.\n    :param str key_prefix: prefix prepended to rate limiter keys.\n    '

    def __init__(self, app=None, key_func=None, global_limits=[], default_limits=[], default_limits_per_method=False, application_limits=[], headers_enabled=False, strategy=None, storage_uri=None, storage_options={}, auto_check=True, swallow_errors=False, in_memory_fallback=[], in_memory_fallback_enabled=False, retry_after=None, key_prefix='', enabled=True):
        self.app = app
        self.logger = logging.getLogger('flask-limiter')
        self.enabled = enabled
        self._default_limits = []
        self._default_limits_per_method = default_limits_per_method
        self._application_limits = []
        self._in_memory_fallback = []
        self._in_memory_fallback_enabled = in_memory_fallback_enabled or len(in_memory_fallback) > 0
        self._exempt_routes = set()
        self._request_filters = []
        self._headers_enabled = headers_enabled
        self._header_mapping = {}
        self._retry_after = retry_after
        self._strategy = strategy
        self._storage_uri = storage_uri
        self._storage_options = storage_options
        self._auto_check = auto_check
        self._swallow_errors = swallow_errors
        if not key_func:
            warnings.warn('Use of the default `get_ipaddr` function is discouraged. Please refer to https://flask-limiter.readthedocs.org/#rate-limit-domain for the recommended configuration', UserWarning)
        if global_limits:
            self.raise_global_limits_warning()
        self._key_func = key_func or get_ipaddr
        self._key_prefix = key_prefix
        for limit in set(global_limits + default_limits):
            self._default_limits.extend([
             LimitGroup(limit, self._key_func, None, False, None, None, None, None)])
        else:
            for limit in application_limits:
                self._application_limits.extend([
                 LimitGroup(limit, self._key_func, 'global', False, None, None, None, None)])
            else:
                for limit in in_memory_fallback:
                    self._in_memory_fallback.extend([
                     LimitGroup(limit, self._key_func, None, False, None, None, None, None)])
                else:
                    self._route_limits = {}
                    self._dynamic_route_limits = {}
                    self._blueprint_limits = {}
                    self._blueprint_dynamic_limits = {}
                    self._blueprint_exempt = set()
                    self._storage = self._limiter = None
                    self._storage_dead = False
                    self._fallback_limiter = None
                    self._Limiter__check_backend_count = 0
                    self._Limiter__last_check_backend = time.time()
                    self._Limiter__marked_for_limiting = {}

                    class BlackHoleHandler(logging.StreamHandler):

                        def emit(*_):
                            pass

                    self.logger.addHandler(BlackHoleHandler())
                    if app:
                        self.init_app(app)

    def init_app(self, app):
        """
        :param app: :class:`flask.Flask` instance to rate limit.
        """
        self.enabled = app.config.setdefault(C.ENABLED, self.enabled)
        self._default_limits_per_method = app.config.setdefault(C.DEFAULT_LIMITS_PER_METHOD, self._default_limits_per_method)
        self._swallow_errors = app.config.setdefault(C.SWALLOW_ERRORS, self._swallow_errors)
        self._headers_enabled = self._headers_enabled or app.config.setdefault(C.HEADERS_ENABLED, False)
        self._storage_options.update(app.config.get(C.STORAGE_OPTIONS, {}))
        self._storage = storage_from_string(
         (self._storage_uri or app.config.setdefault(C.STORAGE_URL, 'memory://')), **self._storage_options)
        strategy = self._strategy or app.config.setdefault(C.STRATEGY, 'fixed-window')
        if strategy not in STRATEGIES:
            raise ConfigurationError('Invalid rate limiting strategy %s' % strategy)
        self._limiter = STRATEGIES[strategy](self._storage)
        self._header_mapping.update({HEADERS.RESET: self._header_mapping.get(HEADERS.RESET, None) or app.config.setdefault(C.HEADER_RESET, 'X-RateLimit-Reset'), 
         
         HEADERS.REMAINING: self._header_mapping.get(HEADERS.REMAINING, None) or app.config.setdefault(C.HEADER_REMAINING, 'X-RateLimit-Remaining'), 
         
         HEADERS.LIMIT: self._header_mapping.get(HEADERS.LIMIT, None) or app.config.setdefault(C.HEADER_LIMIT, 'X-RateLimit-Limit'), 
         
         HEADERS.RETRY_AFTER: self._header_mapping.get(HEADERS.RETRY_AFTER, None) or app.config.setdefault(C.HEADER_RETRY_AFTER, 'Retry-After')})
        self._retry_after = self._retry_after or app.config.get(C.HEADER_RETRY_AFTER_VALUE)
        self._key_prefix = self._key_prefix or app.config.get(C.KEY_PREFIX)
        app_limits = app.config.get(C.APPLICATION_LIMITS, None)
        if not self._application_limits:
            if app_limits:
                self._application_limits = [LimitGroup(app_limits, self._key_func, 'global', False, None, None, None, None)]
        if app.config.get(C.GLOBAL_LIMITS, None):
            self.raise_global_limits_warning()
        conf_limits = app.config.get(C.GLOBAL_LIMITS, app.config.get(C.DEFAULT_LIMITS, None))
        if not self._default_limits:
            if conf_limits:
                self._default_limits = [LimitGroup(conf_limits, self._key_func, None, False, None, None, None, None)]
        for limit in self._default_limits:
            limit.per_method = self._default_limits_per_method
        else:
            fallback_enabled = app.config.get(C.IN_MEMORY_FALLBACK_ENABLED, False)
            fallback_limits = app.config.get(C.IN_MEMORY_FALLBACK, None)
            if not self._in_memory_fallback:
                if fallback_limits:
                    self._in_memory_fallback = [LimitGroup(fallback_limits, self._key_func, None, False, None, None, None, None)]
            if not self._in_memory_fallback_enabled:
                self._in_memory_fallback_enabled = fallback_enabled or len(self._in_memory_fallback) > 0
            if self._in_memory_fallback_enabled:
                self._fallback_storage = MemoryStorage()
                self._fallback_limiter = STRATEGIES[strategy](self._fallback_storage)
            if not hasattr(app, 'extensions'):
                app.extensions = {}
            if not app.extensions.get('limiter'):
                if self._auto_check:
                    app.before_request(self._Limiter__check_request_limit)
                app.after_request(self._Limiter__inject_headers)
            app.extensions['limiter'] = self

    def __should_check_backend(self):
        if self._Limiter__check_backend_count > MAX_BACKEND_CHECKS:
            self._Limiter__check_backend_count = 0
        if time.time() - self._Limiter__last_check_backend > pow(2, self._Limiter__check_backend_count):
            self._Limiter__last_check_backend = time.time()
            self._Limiter__check_backend_count += 1
            return True
        return False

    def check(self):
        """
        check the limits for the current request

        :raises: RateLimitExceeded
        """
        self._Limiter__check_request_limit(False)

    def reset(self):
        """
        resets the storage if it supports being reset
        """
        try:
            self._storage.reset()
            self.logger.info('Storage has been reset and all limits cleared')
        except NotImplementedError:
            self.logger.warning('This storage type does not support being reset')

    @property
    def limiter(self):
        if self._storage_dead:
            if self._in_memory_fallback_enabled:
                return self._fallback_limiter
        return self._limiter

    def __inject_headers(self, response):
        current_limit = getattr(g, 'view_rate_limit', None)
        if self.enabled:
            if self._headers_enabled:
                if current_limit:
                    try:
                        window_stats = (self.limiter.get_window_stats)(*current_limit)
                        reset_in = 1 + window_stats[0]
                        response.headers.add(self._header_mapping[HEADERS.LIMIT], str(current_limit[0].amount))
                        response.headers.add(self._header_mapping[HEADERS.REMAINING], window_stats[1])
                        response.headers.add(self._header_mapping[HEADERS.RESET], reset_in)
                        existing_retry_after_header = response.headers.get('Retry-After')
                        if existing_retry_after_header is not None:
                            retry_after = parse_date(existing_retry_after_header)
                            if retry_after is None:
                                retry_after = time.time() + int(existing_retry_after_header)
                            if isinstance(retry_after, datetime.datetime):
                                retry_after = time.mktime(retry_after.timetuple())
                            reset_in = max(retry_after, reset_in)
                        response.headers.set(self._header_mapping[HEADERS.RETRY_AFTER], self._retry_after == 'http-date' and http_date(reset_in) or int(reset_in - time.time()))
                    except:
                        if self._in_memory_fallback:
                            if not self._storage_dead:
                                self.logger.warn('Rate limit storage unreachable - falling back to in-memory storage')
                                self._storage_dead = True
                                response = self._Limiter__inject_headers(response)
                        elif self._swallow_errors:
                            self.logger.exception('Failed to update rate limit headers. Swallowing error')
                        else:
                            (six.reraise)(*sys.exc_info())

        return response

    def __evaluate_limits(self, endpoint, limits):
        failed_limit = None
        limit_for_header = None
        for lim in limits:
            limit_scope = lim.scope or endpoint
            if lim.is_exempt or lim.method_exempt:
                pass
            else:
                if lim.per_method:
                    limit_scope += ':%s' % request.method
                limit_key = lim.key_func()
                args = [
                 limit_key, limit_scope]
                if all(args):
                    if self._key_prefix:
                        args = [
                         self._key_prefix] + args
                    if not limit_for_header or lim.limit < limit_for_header[0]:
                        limit_for_header = [
                         lim.limit] + args
                    if not (self.limiter.hit)(lim.limit, *args):
                        self.logger.warning('ratelimit %s (%s) exceeded at endpoint: %s', lim.limit, limit_key, limit_scope)
                        failed_limit = lim
                        limit_for_header = [lim.limit] + args
                        break
                else:
                    self.logger.error('Skipping limit: %s. Empty value found in parameters.', lim.limit)
        else:
            g.view_rate_limit = limit_for_header
            if failed_limit:
                raise RateLimitExceeded(failed_limit)

    def __check_request_limit--- This code section failed: ---

 L. 413         0  LOAD_GLOBAL              request
                2  LOAD_ATTR                endpoint
                4  JUMP_IF_TRUE_OR_POP     8  'to 8'
                6  LOAD_STR                 ''
              8_0  COME_FROM             4  '4'
                8  STORE_FAST               'endpoint'

 L. 414        10  LOAD_GLOBAL              current_app
               12  LOAD_ATTR                view_functions
               14  LOAD_METHOD              get
               16  LOAD_FAST                'endpoint'
               18  LOAD_CONST               None
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'view_func'

 L. 417        24  LOAD_FAST                'view_func'

 L. 416        26  POP_JUMP_IF_FALSE    44  'to 44'
               28  LOAD_STR                 '%s.%s'
               30  LOAD_FAST                'view_func'
               32  LOAD_ATTR                __module__
               34  LOAD_FAST                'view_func'
               36  LOAD_ATTR                __name__
               38  BUILD_TUPLE_2         2 
               40  BINARY_MODULO    
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            26  '26'

 L. 417        44  LOAD_STR                 ''
             46_0  COME_FROM            42  '42'

 L. 415        46  STORE_FAST               'name'

 L. 419        48  LOAD_GLOBAL              request
               50  LOAD_ATTR                endpoint
               52  POP_JUMP_IF_FALSE   122  'to 122'

 L. 420        54  LOAD_FAST                'self'
               56  LOAD_ATTR                enabled

 L. 419        58  POP_JUMP_IF_FALSE   122  'to 122'

 L. 421        60  LOAD_FAST                'view_func'
               62  LOAD_GLOBAL              current_app
               64  LOAD_ATTR                send_static_file
               66  COMPARE_OP               ==

 L. 419        68  POP_JUMP_IF_TRUE    122  'to 122'

 L. 422        70  LOAD_FAST                'name'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _exempt_routes
               76  COMPARE_OP               in

 L. 419        78  POP_JUMP_IF_TRUE    122  'to 122'

 L. 423        80  LOAD_GLOBAL              request
               82  LOAD_ATTR                blueprint
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _blueprint_exempt
               88  COMPARE_OP               in

 L. 419        90  POP_JUMP_IF_TRUE    122  'to 122'

 L. 424        92  LOAD_GLOBAL              any
               94  LOAD_GENEXPR             '<code_object <genexpr>>'
               96  LOAD_STR                 'Limiter.__check_request_limit.<locals>.<genexpr>'
               98  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _request_filters
              104  GET_ITER         
              106  CALL_FUNCTION_1       1  ''
              108  CALL_FUNCTION_1       1  ''

 L. 419       110  POP_JUMP_IF_TRUE    122  'to 122'

 L. 425       112  LOAD_GLOBAL              g
              114  LOAD_METHOD              get
              116  LOAD_STR                 '_rate_limiting_complete'
              118  CALL_METHOD_1         1  ''

 L. 419       120  POP_JUMP_IF_FALSE   126  'to 126'
            122_0  COME_FROM           110  '110'
            122_1  COME_FROM            90  '90'
            122_2  COME_FROM            78  '78'
            122_3  COME_FROM            68  '68'
            122_4  COME_FROM            58  '58'
            122_5  COME_FROM            52  '52'

 L. 427       122  LOAD_CONST               None
              124  RETURN_VALUE     
            126_0  COME_FROM           120  '120'

 L. 428       126  BUILD_LIST_0          0 
              128  BUILD_LIST_0          0 
              130  ROT_TWO          
              132  STORE_FAST               'limits'
              134  STORE_FAST               'dynamic_limits'

 L. 446       136  LOAD_FAST                'view_func'
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                _Limiter__marked_for_limiting
              142  LOAD_METHOD              get

 L. 447       144  LOAD_FAST                'name'

 L. 447       146  BUILD_LIST_0          0 

 L. 446       148  CALL_METHOD_2         2  ''
              150  COMPARE_OP               in
              152  STORE_FAST               'implicit_decorator'

 L. 450       154  LOAD_FAST                'in_middleware'
              156  POP_JUMP_IF_FALSE   164  'to 164'
              158  LOAD_FAST                'implicit_decorator'
          160_162  POP_JUMP_IF_FALSE   292  'to 292'
            164_0  COME_FROM           156  '156'

 L. 452       164  LOAD_FAST                'name'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _route_limits
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   184  'to 184'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                _route_limits
              178  LOAD_FAST                'name'
              180  BINARY_SUBSCR    
              182  JUMP_IF_TRUE_OR_POP   186  'to 186'
            184_0  COME_FROM           172  '172'
              184  BUILD_LIST_0          0 
            186_0  COME_FROM           182  '182'

 L. 451       186  STORE_FAST               'limits'

 L. 454       188  BUILD_LIST_0          0 
              190  STORE_FAST               'dynamic_limits'

 L. 455       192  LOAD_FAST                'name'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                _dynamic_route_limits
              198  COMPARE_OP               in
          200_202  POP_JUMP_IF_FALSE   292  'to 292'

 L. 456       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _dynamic_route_limits
              208  LOAD_FAST                'name'
              210  BINARY_SUBSCR    
              212  GET_ITER         
              214  FOR_ITER            292  'to 292'
              216  STORE_FAST               'lim'

 L. 457       218  SETUP_FINALLY       238  'to 238'

 L. 458       220  LOAD_FAST                'dynamic_limits'
              222  LOAD_METHOD              extend
              224  LOAD_GLOBAL              list
              226  LOAD_FAST                'lim'
              228  CALL_FUNCTION_1       1  ''
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          
              234  POP_BLOCK        
              236  JUMP_BACK           214  'to 214'
            238_0  COME_FROM_FINALLY   218  '218'

 L. 459       238  DUP_TOP          
              240  LOAD_GLOBAL              ValueError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   288  'to 288'
              248  POP_TOP          
              250  STORE_FAST               'e'
              252  POP_TOP          
              254  SETUP_FINALLY       276  'to 276'

 L. 460       256  LOAD_FAST                'self'
              258  LOAD_ATTR                logger
              260  LOAD_METHOD              error

 L. 461       262  LOAD_STR                 'failed to load ratelimit for view function %s (%s)'

 L. 462       264  LOAD_FAST                'name'

 L. 462       266  LOAD_FAST                'e'

 L. 460       268  CALL_METHOD_3         3  ''
              270  POP_TOP          
              272  POP_BLOCK        
              274  BEGIN_FINALLY    
            276_0  COME_FROM_FINALLY   254  '254'
              276  LOAD_CONST               None
              278  STORE_FAST               'e'
              280  DELETE_FAST              'e'
              282  END_FINALLY      
              284  POP_EXCEPT       
              286  JUMP_BACK           214  'to 214'
            288_0  COME_FROM           244  '244'
              288  END_FINALLY      
              290  JUMP_BACK           214  'to 214'
            292_0  COME_FROM           200  '200'
            292_1  COME_FROM           160  '160'

 L. 464       292  LOAD_GLOBAL              request
              294  LOAD_ATTR                blueprint
          296_298  POP_JUMP_IF_FALSE   458  'to 458'

 L. 465       300  LOAD_GLOBAL              request
              302  LOAD_ATTR                blueprint
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                _blueprint_dynamic_limits
              308  COMPARE_OP               in
          310_312  POP_JUMP_IF_FALSE   420  'to 420'

 L. 466       314  LOAD_FAST                'dynamic_limits'

 L. 465   316_318  POP_JUMP_IF_TRUE    420  'to 420'

 L. 468       320  LOAD_FAST                'self'
              322  LOAD_ATTR                _blueprint_dynamic_limits

 L. 469       324  LOAD_GLOBAL              request
              326  LOAD_ATTR                blueprint

 L. 468       328  BINARY_SUBSCR    
              330  GET_ITER         
              332  FOR_ITER            420  'to 420'
              334  STORE_FAST               'limit_group'

 L. 471       336  SETUP_FINALLY       362  'to 362'

 L. 472       338  LOAD_FAST                'dynamic_limits'
              340  LOAD_METHOD              extend

 L. 473       342  LOAD_LISTCOMP            '<code_object <listcomp>>'
              344  LOAD_STR                 'Limiter.__check_request_limit.<locals>.<listcomp>'
              346  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 479       348  LOAD_FAST                'limit_group'

 L. 473       350  GET_ITER         
              352  CALL_FUNCTION_1       1  ''

 L. 472       354  CALL_METHOD_1         1  ''
              356  POP_TOP          
              358  POP_BLOCK        
              360  JUMP_BACK           332  'to 332'
            362_0  COME_FROM_FINALLY   336  '336'

 L. 482       362  DUP_TOP          
              364  LOAD_GLOBAL              ValueError
              366  COMPARE_OP               exception-match
          368_370  POP_JUMP_IF_FALSE   414  'to 414'
              372  POP_TOP          
              374  STORE_FAST               'e'
              376  POP_TOP          
              378  SETUP_FINALLY       402  'to 402'

 L. 483       380  LOAD_FAST                'self'
              382  LOAD_ATTR                logger
              384  LOAD_METHOD              error

 L. 484       386  LOAD_STR                 'failed to load ratelimit for blueprint %s (%s)'

 L. 485       388  LOAD_GLOBAL              request
              390  LOAD_ATTR                blueprint

 L. 485       392  LOAD_FAST                'e'

 L. 483       394  CALL_METHOD_3         3  ''
              396  POP_TOP          
              398  POP_BLOCK        
              400  BEGIN_FINALLY    
            402_0  COME_FROM_FINALLY   378  '378'
              402  LOAD_CONST               None
              404  STORE_FAST               'e'
              406  DELETE_FAST              'e'
              408  END_FINALLY      
              410  POP_EXCEPT       
              412  JUMP_BACK           332  'to 332'
            414_0  COME_FROM           368  '368'
              414  END_FINALLY      
          416_418  JUMP_BACK           332  'to 332'
            420_0  COME_FROM           316  '316'
            420_1  COME_FROM           310  '310'

 L. 487       420  LOAD_GLOBAL              request
              422  LOAD_ATTR                blueprint
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                _blueprint_limits
              428  COMPARE_OP               in
          430_432  POP_JUMP_IF_FALSE   458  'to 458'
              434  LOAD_FAST                'limits'
          436_438  POP_JUMP_IF_TRUE    458  'to 458'

 L. 488       440  LOAD_FAST                'limits'
              442  LOAD_METHOD              extend
              444  LOAD_FAST                'self'
              446  LOAD_ATTR                _blueprint_limits
              448  LOAD_GLOBAL              request
              450  LOAD_ATTR                blueprint
              452  BINARY_SUBSCR    
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          
            458_0  COME_FROM           436  '436'
            458_1  COME_FROM           430  '430'
            458_2  COME_FROM           296  '296'

 L. 490       458  SETUP_FINALLY       712  'to 712'

 L. 491       460  BUILD_LIST_0          0 
              462  STORE_FAST               'all_limits'

 L. 492       464  LOAD_FAST                'self'
              466  LOAD_ATTR                _storage_dead
          468_470  POP_JUMP_IF_FALSE   564  'to 564'
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                _fallback_limiter
          476_478  POP_JUMP_IF_FALSE   564  'to 564'

 L. 493       480  LOAD_FAST                'in_middleware'
          482_484  POP_JUMP_IF_FALSE   500  'to 500'
              486  LOAD_FAST                'name'
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                _Limiter__marked_for_limiting
              492  COMPARE_OP               in
          494_496  POP_JUMP_IF_FALSE   500  'to 500'

 L. 494       498  BREAK_LOOP          564  'to 564'
            500_0  COME_FROM           494  '494'
            500_1  COME_FROM           482  '482'

 L. 496       500  LOAD_FAST                'self'
              502  LOAD_METHOD              _Limiter__should_check_backend
              504  CALL_METHOD_0         0  ''
          506_508  POP_JUMP_IF_FALSE   548  'to 548'
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                _storage
              514  LOAD_METHOD              check
              516  CALL_METHOD_0         0  ''
          518_520  POP_JUMP_IF_FALSE   548  'to 548'

 L. 497       522  LOAD_FAST                'self'
              524  LOAD_ATTR                logger
              526  LOAD_METHOD              info
              528  LOAD_STR                 'Rate limit storage recovered'
              530  CALL_METHOD_1         1  ''
              532  POP_TOP          

 L. 498       534  LOAD_CONST               False
              536  LOAD_FAST                'self'
              538  STORE_ATTR               _storage_dead

 L. 499       540  LOAD_CONST               0
              542  LOAD_FAST                'self'
              544  STORE_ATTR               _Limiter__check_backend_count
              546  JUMP_FORWARD        564  'to 564'
            548_0  COME_FROM           518  '518'
            548_1  COME_FROM           506  '506'

 L. 501       548  LOAD_GLOBAL              list

 L. 502       550  LOAD_GLOBAL              itertools
              552  LOAD_ATTR                chain
              554  LOAD_FAST                'self'
              556  LOAD_ATTR                _in_memory_fallback
              558  CALL_FUNCTION_EX      0  'positional arguments only'

 L. 501       560  CALL_FUNCTION_1       1  ''
              562  STORE_FAST               'all_limits'
            564_0  COME_FROM           546  '546'
            564_1  COME_FROM           498  '498'
            564_2  COME_FROM           476  '476'
            564_3  COME_FROM           468  '468'

 L. 504       564  LOAD_FAST                'all_limits'
          566_568  POP_JUMP_IF_TRUE    696  'to 696'

 L. 505       570  LOAD_FAST                'limits'
              572  LOAD_FAST                'dynamic_limits'
              574  BINARY_ADD       
              576  STORE_FAST               'route_limits'

 L. 506       578  LOAD_FAST                'in_middleware'
          580_582  POP_JUMP_IF_FALSE   600  'to 600'
              584  LOAD_GLOBAL              list
              586  LOAD_GLOBAL              itertools
              588  LOAD_ATTR                chain
              590  LOAD_FAST                'self'
              592  LOAD_ATTR                _application_limits
              594  CALL_FUNCTION_EX      0  'positional arguments only'
              596  CALL_FUNCTION_1       1  ''
              598  JUMP_FORWARD        602  'to 602'
            600_0  COME_FROM           580  '580'
              600  BUILD_LIST_0          0 
            602_0  COME_FROM           598  '598'
              602  STORE_FAST               'all_limits'

 L. 507       604  LOAD_FAST                'all_limits'
              606  LOAD_FAST                'route_limits'
              608  INPLACE_ADD      
              610  STORE_FAST               'all_limits'

 L. 510       612  LOAD_GLOBAL              all
              614  LOAD_GENEXPR             '<code_object <genexpr>>'
              616  LOAD_STR                 'Limiter.__check_request_limit.<locals>.<genexpr>'
              618  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              620  LOAD_FAST                'route_limits'
              622  GET_ITER         
              624  CALL_FUNCTION_1       1  ''
              626  CALL_FUNCTION_1       1  ''

 L. 508   628_630  POP_JUMP_IF_TRUE    652  'to 652'

 L. 511       632  LOAD_GLOBAL              all
              634  LOAD_GENEXPR             '<code_object <genexpr>>'
              636  LOAD_STR                 'Limiter.__check_request_limit.<locals>.<genexpr>'
              638  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              640  LOAD_FAST                'route_limits'
              642  GET_ITER         
              644  CALL_FUNCTION_1       1  ''
              646  CALL_FUNCTION_1       1  ''

 L. 508   648_650  POP_JUMP_IF_FALSE   670  'to 670'
            652_0  COME_FROM           628  '628'

 L. 513       652  LOAD_FAST                'in_middleware'

 L. 508   654_656  POP_JUMP_IF_FALSE   676  'to 676'

 L. 513       658  LOAD_FAST                'name'
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                _Limiter__marked_for_limiting
              664  COMPARE_OP               in

 L. 508   666_668  POP_JUMP_IF_FALSE   676  'to 676'
            670_0  COME_FROM           648  '648'

 L. 514       670  LOAD_FAST                'implicit_decorator'

 L. 508   672_674  POP_JUMP_IF_FALSE   696  'to 696'
            676_0  COME_FROM           666  '666'
            676_1  COME_FROM           654  '654'

 L. 516       676  LOAD_FAST                'all_limits'
              678  LOAD_GLOBAL              list
              680  LOAD_GLOBAL              itertools
              682  LOAD_ATTR                chain
              684  LOAD_FAST                'self'
              686  LOAD_ATTR                _default_limits
              688  CALL_FUNCTION_EX      0  'positional arguments only'
              690  CALL_FUNCTION_1       1  ''
              692  INPLACE_ADD      
              694  STORE_FAST               'all_limits'
            696_0  COME_FROM           672  '672'
            696_1  COME_FROM           566  '566'

 L. 517       696  LOAD_FAST                'self'
              698  LOAD_METHOD              _Limiter__evaluate_limits
              700  LOAD_FAST                'endpoint'
              702  LOAD_FAST                'all_limits'
              704  CALL_METHOD_2         2  ''
              706  POP_TOP          
              708  POP_BLOCK        
              710  JUMP_FORWARD        856  'to 856'
            712_0  COME_FROM_FINALLY   458  '458'

 L. 518       712  DUP_TOP          
              714  LOAD_GLOBAL              Exception
              716  COMPARE_OP               exception-match
          718_720  POP_JUMP_IF_FALSE   854  'to 854'
              722  POP_TOP          
              724  STORE_FAST               'e'
              726  POP_TOP          
              728  SETUP_FINALLY       842  'to 842'

 L. 519       730  LOAD_GLOBAL              isinstance
              732  LOAD_FAST                'e'
              734  LOAD_GLOBAL              RateLimitExceeded
              736  CALL_FUNCTION_2       2  ''
          738_740  POP_JUMP_IF_FALSE   756  'to 756'

 L. 520       742  LOAD_GLOBAL              six
              744  LOAD_ATTR                reraise
              746  LOAD_GLOBAL              sys
              748  LOAD_METHOD              exc_info
              750  CALL_METHOD_0         0  ''
              752  CALL_FUNCTION_EX      0  'positional arguments only'
              754  POP_TOP          
            756_0  COME_FROM           738  '738'

 L. 521       756  LOAD_FAST                'self'
              758  LOAD_ATTR                _in_memory_fallback_enabled
          760_762  POP_JUMP_IF_FALSE   802  'to 802'
              764  LOAD_FAST                'self'
              766  LOAD_ATTR                _storage_dead
          768_770  POP_JUMP_IF_TRUE    802  'to 802'

 L. 522       772  LOAD_FAST                'self'
              774  LOAD_ATTR                logger
              776  LOAD_METHOD              warn

 L. 523       778  LOAD_STR                 'Rate limit storage unreachable - falling back to in-memory storage'

 L. 522       780  CALL_METHOD_1         1  ''
              782  POP_TOP          

 L. 526       784  LOAD_CONST               True
              786  LOAD_FAST                'self'
              788  STORE_ATTR               _storage_dead

 L. 527       790  LOAD_FAST                'self'
              792  LOAD_METHOD              _Limiter__check_request_limit
              794  LOAD_FAST                'in_middleware'
              796  CALL_METHOD_1         1  ''
              798  POP_TOP          
              800  JUMP_FORWARD        838  'to 838'
            802_0  COME_FROM           768  '768'
            802_1  COME_FROM           760  '760'

 L. 529       802  LOAD_FAST                'self'
              804  LOAD_ATTR                _swallow_errors
          806_808  POP_JUMP_IF_FALSE   824  'to 824'

 L. 530       810  LOAD_FAST                'self'
              812  LOAD_ATTR                logger
              814  LOAD_METHOD              exception

 L. 531       816  LOAD_STR                 'Failed to rate limit. Swallowing error'

 L. 530       818  CALL_METHOD_1         1  ''
              820  POP_TOP          
              822  JUMP_FORWARD        838  'to 838'
            824_0  COME_FROM           806  '806'

 L. 534       824  LOAD_GLOBAL              six
              826  LOAD_ATTR                reraise
              828  LOAD_GLOBAL              sys
              830  LOAD_METHOD              exc_info
              832  CALL_METHOD_0         0  ''
              834  CALL_FUNCTION_EX      0  'positional arguments only'
              836  POP_TOP          
            838_0  COME_FROM           822  '822'
            838_1  COME_FROM           800  '800'
              838  POP_BLOCK        
              840  BEGIN_FINALLY    
            842_0  COME_FROM_FINALLY   728  '728'
              842  LOAD_CONST               None
              844  STORE_FAST               'e'
              846  DELETE_FAST              'e'
              848  END_FINALLY      
              850  POP_EXCEPT       
              852  JUMP_FORWARD        856  'to 856'
            854_0  COME_FROM           718  '718'
              854  END_FINALLY      
            856_0  COME_FROM           852  '852'
            856_1  COME_FROM           710  '710'

Parse error at or near `JUMP_FORWARD' instruction at offset 710

    def __limit_decorator(self, limit_value, key_func=None, shared=False, scope=None, per_method=False, methods=None, error_message=None, exempt_when=None, override_defaults=True):
        _scope = scope if shared else None

        def _inner(obj):
            func = key_func or self._key_func
            is_route = not isinstance(obj, Blueprint)
            name = '%s.%s' % (
             obj.__module__, obj.__name__) if is_route else obj.name
            dynamic_limit, static_limits = None, []
            if callable(limit_value):
                dynamic_limit = LimitGroup(limit_value, func, _scope, per_method, methods, error_message, exempt_when, override_defaults)
            else:
                try:
                    static_limits = list(LimitGroup(limit_value, func, _scope, per_method, methods, error_message, exempt_when, override_defaults))
                except ValueError as e:
                    try:
                        self.logger.error('failed to configure %s %s (%s)', 'view function' if is_route else 'blueprint', name, e)
                    finally:
                        e = None
                        del e

                else:
                    if isinstance(obj, Blueprint):
                        if dynamic_limit:
                            self._blueprint_dynamic_limits.setdefault(name, []).append(dynamic_limit)
                        else:
                            self._blueprint_limits.setdefault(name, []).extend(static_limits)
                    else:
                        self._Limiter__marked_for_limiting.setdefault(name, []).append(obj)
                        if dynamic_limit:
                            self._dynamic_route_limits.setdefault(name, []).append(dynamic_limit)
                        else:
                            self._route_limits.setdefault(name, []).extend(static_limits)

                        @wraps(obj)
                        def __inner(*a, **k):
                            if self._auto_check:
                                if not g.get('_rate_limiting_complete'):
                                    self._Limiter__check_request_limit(False)
                                    g._rate_limiting_complete = True
                            return obj(*a, **k)

                        return _Limiter__inner

        return _inner

    def limit(self, limit_value, key_func=None, per_method=False, methods=None, error_message=None, exempt_when=None, override_defaults=True):
        """
        decorator to be used for rate limiting individual routes or blueprints.

        :param limit_value: rate limit string or a callable that returns a string.
         :ref:`ratelimit-string` for more details.
        :param function key_func: function/lambda to extract the unique identifier for
         the rate limit. defaults to remote address of the request.
        :param bool per_method: whether the limit is sub categorized into the http
         method of the request.
        :param list methods: if specified, only the methods in this list will be rate
         limited (default: None).
        :param error_message: string (or callable that returns one) to override the
         error message used in the response.
        :param function exempt_when: function/lambda used to decide if the rate limit
         should skipped.
        :param bool override_defaults:  whether the decorated limit overrides the default
         limits. (default: True)
        """
        return self._Limiter__limit_decorator(limit_value,
          key_func,
          per_method=per_method,
          methods=methods,
          error_message=error_message,
          exempt_when=exempt_when,
          override_defaults=override_defaults)

    def shared_limit(self, limit_value, scope, key_func=None, error_message=None, exempt_when=None, override_defaults=True):
        """
        decorator to be applied to multiple routes sharing the same rate limit.

        :param limit_value: rate limit string or a callable that returns a string.
         :ref:`ratelimit-string` for more details.
        :param scope: a string or callable that returns a string
         for defining the rate limiting scope.
        :param function key_func: function/lambda to extract the unique identifier for
         the rate limit. defaults to remote address of the request.
        :param error_message: string (or callable that returns one) to override the
         error message used in the response.
        :param function exempt_when: function/lambda used to decide if the rate limit
         should skipped.
        :param bool override_defaults:  whether the decorated limit overrides the default
         limits. (default: True)
        """
        return self._Limiter__limit_decorator(limit_value,
          key_func,
          True,
          scope,
          error_message=error_message,
          exempt_when=exempt_when,
          override_defaults=override_defaults)

    def exempt(self, obj):
        """
        decorator to mark a view or all views in a blueprint as exempt from rate limits.
        """
        if not isinstance(obj, Blueprint):
            name = '%s.%s' % (obj.__module__, obj.__name__)

            @wraps(obj)
            def __inner(*a, **k):
                return obj(*a, **k)

            self._exempt_routes.add(name)
            return _Limiter__inner
        self._blueprint_exempt.add(obj.name)

    def request_filter(self, fn):
        """
        decorator to mark a function as a filter to be executed
        to check if the request is exempt from rate limiting.
        """
        self._request_filters.append(fn)
        return fn

    def raise_global_limits_warning(self):
        warnings.warn('global_limits was a badly name configuration since it is actually a default limit and not a globally shared limit. Use default_limits if you want to provide a default or use application_limits if you intend to really have a global shared limit', UserWarning)