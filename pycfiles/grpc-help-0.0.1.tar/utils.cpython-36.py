# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/utils.py
# Compiled at: 2019-02-11 04:58:19
# Size of source mod 2**32: 2881 bytes
import concurrent, functools, threading
from importlib import import_module
import asyncio
try:
    import ujson as jsonlib
    has_ujson = True
except ImportError:
    import json as jsonlib
    has_ujson = False

def json_encode(value, cls=None):
    if not has_ujson:
        options = {'ensure_ascii':False,  'allow_nan':False, 
         'indent':None, 
         'separators':(',', ':')}
        if cls:
            options['cls'] = cls
        return (jsonlib.dumps)(value, **options)
    else:
        return jsonlib.dumps(value, escape_forward_slashes=False)


def json_decode(value):
    return jsonlib.loads(value)


def import_object(obj_name):
    if obj_name is None:
        return obj_name
    else:
        if callable(obj_name):
            return obj_name
        elif not isinstance(obj_name, str):
            obj_name = obj_name.encode('utf-8')
        else:
            if obj_name.count('.') == 0:
                return __import__(obj_name, None, None)
            try:
                module_path, class_name = obj_name.rsplit('.', 1)
            except ValueError:
                msg = "%s doesn't look like a module path" % obj_name
                raise ImportError(msg)

        obj = import_module(module_path)
        try:
            return getattr(obj, class_name)
        except AttributeError:
            msg = 'Module "%s" does not define a "%s" attribute/class"' % (module_path, class_name)
            raise ImportError(msg)


class ResultIterator:

    def __init__(self, loop, async_wrapper):
        self.async_wrapper = async_wrapper
        self._loop = loop

    def __iter__(self):
        return self

    def next(self):

        async def _next--- This code section failed: ---

 L.  73         0  SETUP_LOOP           54  'to 54'
                2  LOAD_DEREF               'self'
                4  LOAD_ATTR                async_wrapper
                6  GET_AITER        
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  SETUP_EXCEPT         26  'to 26'
               14  GET_ANEXT        
               16  LOAD_CONST               None
               18  YIELD_FROM       
               20  STORE_FAST               'r'
               22  POP_BLOCK        
               24  JUMP_FORWARD         48  'to 48'
             26_0  COME_FROM_EXCEPT     12  '12'
               26  DUP_TOP          
               28  LOAD_GLOBAL              StopAsyncIteration
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          
               40  POP_EXCEPT       
               42  POP_BLOCK        
               44  JUMP_ABSOLUTE        54  'to 54'
               46  END_FINALLY      
             48_0  COME_FROM            24  '24'

 L.  74        48  LOAD_FAST                'r'
               50  RETURN_VALUE     
               52  JUMP_ABSOLUTE        54  'to 54'
             54_0  COME_FROM_LOOP        0  '0'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 52

        result = self._loop.run_until_complete(_next())
        if result is None:
            raise StopIteration()
        return result

    __next__ = next


class AsyncToSync:

    def __init__(self, awaitable):
        self.awaitable = awaitable

    def __call__(self, *args, **kwargs):
        call_result = concurrent.futures.Future()
        thread = threading.current_thread()
        if not getattr(thread, 'loop', None):
            new_loop = asyncio.new_event_loop()
            thread.loop = new_loop
        thread.loop.run_until_complete(self.main_wrap(args, kwargs, call_result, thread.loop))
        result = call_result.result()
        return result

    def __get__(self, parent, objtype):
        return functools.partial(self.__call__, parent)

    async def main_wrap(self, args, kwargs, call_result, loop):
        try:
            result = (self.awaitable)(*args, **kwargs)
            if hasattr(result, '__aiter__'):
                call_result.set_result(ResultIterator(loop, result))
            else:
                call_result.set_result(await result)
        except Exception as e:
            call_result.set_exception(e)


async_to_sync = AsyncToSync