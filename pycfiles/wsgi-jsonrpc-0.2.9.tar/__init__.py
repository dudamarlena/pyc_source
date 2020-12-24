# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikeal/Documents/projects/tools/wsgi_jsonrpc/trunk/wsgi_jsonrpc/__init__.py
# Compiled at: 2007-09-20 12:20:53
from datetime import datetime
from StringIO import StringIO
import simplejson, sys, traceback, logging, json_tools, test_jsonrpc
logger = logging.getLogger(__name__)
_descriptions = set(['summary', 'help', 'idempotent', 'params', 'return'])

def describe_method(method):
    """Check is a callable object has description params set"""
    description = {}
    for key in _descriptions:
        if hasattr(method, key):
            description[key] = getattr(method, key)

    return description


class JSONRPCError(Exception):
    """JSONRPC Error"""
    pass


class JSONRPCDispatcher(object):

    def __init__(self, instance=None, methods=None, name='Python JSONRPC Service', summary='Service dispatched by python JSONRPCDispatcher', help=None, address=None):
        """Initialization. Can take an instance to register upon initialization"""
        self.instances = []
        self.name = name
        self.help = help
        self.address = address
        self.summary = summary
        self.base_attributes = set(dir(self))
        self.base_attributes.add('base_attributes')
        if instance is not None:
            self.register_instance(instance)
        if methods is not None:
            for method in methods:
                self.register_method(method)

        self.__dict__['system.list_methods'] = self.system_list_methods
        self.__dict__['system.describe'] = self.system_describe
        return

    def get_valid_methods(self):
        valid_methods = {}
        for (key, value) in self.__dict__.items():
            if key.startswith('_') is False:
                if key not in self.base_attributes:
                    valid_methods[key] = value

        return valid_methods

    def register_instance(self, instance):
        """Registers all attributes of class instance to dispatcher"""
        for attribute in dir(instance):
            if attribute.startswith('_') is False:
                self.register_method(getattr(instance, attribute), name=attribute)

        self.instances.append(instance)

    def register_method(self, function, name=None):
        """Registers a method with the dispatcher"""
        if name is None:
            try:
                name = function.__name__
            except:
                if hasattr(function, __call__):
                    raise 'Callable class instances must be passed with name parameter'
                else:
                    raise 'Not a function'

        if self.__dict__.has_key(name) is False:
            self.__dict__[unicode(name)] = function
        else:
            print 'Attribute name conflict -- %s must be removed before attribute of the same name can be added'
        return

    def system_list_methods(self):
        """List all the available methods and return a object parsable that conforms to the JSONRPC Service Procedure Description specification"""
        method_list = []
        for (key, value) in self.get_valid_methods().items():
            method = {}
            method['name'] = key
            method.update(describe_method(value))
            method_list.append(method)

        method_list.sort()
        logger.debug('system.list_methods created list %s' % str(method_list))
        return method_list

    def system_describe(self):
        """Service description"""
        description = {}
        description['sdversion'] = '1.0'
        description['name'] = self.name
        description['summary'] = self.summary
        if self.help is not None:
            description['help'] = self.help
        if self.address is not None:
            description['address'] = self.address
        description['procs'] = self.system_list_methods()
        return description

    def dispatch(self, json):
        """Public dispatcher, verifies that a method exists in it's method dictionary and calls it"""
        rpc_request = self._decode(json)
        logger.debug('decoded to python object %s' % str(rpc_request))
        if self.__dict__.has_key(rpc_request['method']):
            logger.debug('dispatcher has key %s' % rpc_request['method'])
            return self._dispatch(rpc_request)
        else:
            logger.debug('returning jsonrpc error')
            return self._encode(result=None, error=JSONRPCError('no such method'))
        return

    def _dispatch(self, rpc_request):
        """Internal dispatcher, handles all the error checking and calling of methods"""
        result = None
        error = None
        jsonrpc_id = None
        if rpc_request['params'] is not None and len(rpc_request['params']) is 0:
            rpc_request['params'] = None
        logged_failure = False
        try:
            if type(rpc_request['params']) is list or type(rpc_request['params']) is tuple:
                try:
                    result = self.__dict__[rpc_request['method']](*rpc_request['params'])
                except Exception, e:
                    if type(rpc_request['params'][(-1)]) is dict:
                        result = self.__dict__[rpc_request['method']](*rpc_request['params'], **rpc_request['params'][(-1)])
                    else:
                        logger.exception('JSONRPC Dispatcher encountered exception')
                        logged_failure = True
                        raise Exception, e

            elif type(rpc_request['params']) is dict:
                ascii_params = {}
                [ ascii_params.__setitem__(str(key), rpc_request['params'][key]) for key in rpc_request['params'].keys() ]
                result = self.__dict__[rpc_request['method']](**ascii_params)
            elif rpc_request['params'] is None:
                result = self.__dict__[rpc_request['method']]()
            else:
                logger.warning('received params type %s ' % type(rpc_request['params']))
                raise JSONRPCError, 'params not array or object type'
        except JSONRPCError, e:
            logger.exception('JSONRPCError %s' % e)
        except Exception, e:
            error = JSONRPCError('Server Exception :: %s' % e)
            error.type = e.__class__
            if logged_failure is False:
                logger.exception('JSONRPC Dispatcher encountered exception')

        if rpc_request.has_key('id'):
            jsonrpc_id = rpc_request['id']
        if result is None and error is None:
            result = 200
        return self._encode(result=result, error=error, jsonrpc_id=jsonrpc_id)

    def _encode(self, result=None, error=None, jsonrpc_id=None):
        """Internal encoder method, handles error formatting, id persistence, and encoding via simplejson"""
        response = {}
        response['result'] = result
        if jsonrpc_id is not None:
            response['id'] = jsonrpc_id
        if error is not None:
            if hasattr(error, 'type'):
                error_type = str(error.type)
                error_message = str(error)
            else:
                error_type = 'JSONRPCError'
                error_message = str(error).strip('JSONRPC Error in: ')
            response['error'] = {'type': error_type, 'message': error_message}
        logger.debug('serializing %s' % str(response))
        return simplejson.dumps(response)

    def _decode(self, json):
        """Internal method for decoding json objects, uses simplejson"""
        return simplejson.loads(json)


class WSGIJSONRPCApplication(JSONRPCDispatcher):
    """A WSGI Application for generic JSONRPC requests."""

    def handler(self, environ, start_response):
        """A WSGI handler for generic JSONRPC requests."""
        if environ['REQUEST_METHOD'] == 'POST':
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
            try:
                logger.debug('Sending %s to dispatcher' % body)
                response = self.dispatch(body)
                start_response('200 OK', [('Cache-Control', 'no-cache'), ('Pragma', 'no-cache'),
                 ('Content-Type', 'application/json')])
                return [response]
            except Exception, e:
                logger.exception('WSGIJSONRPCApplication Dispatcher excountered exception')
                start_response('500 Internal Server Error', [('Cache-Control', 'no-cache'), ('Content-Type', 'text/plain')])
                return ['500 Internal Server Error']

        else:
            start_response('405 Method Not Allowed', [('Cache-Control', 'no-cache'), ('Content-Type', 'text/plain')])
            return ['405 Method Not Allowed. This JSONRPC interface only supports POST.']
        return

    def __call__(self, environ, start_response):
        return self.handler(environ, start_response)