# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/plugins/manager.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 7239 bytes
__all__ = [
 'get_plugin_manager', 'BaseContext', 'PluginManager']
import pkg_resources, logging, asyncio, copy, sys
from collections import namedtuple
Plugin = namedtuple('Plugin', ['name', 'ep', 'object'])
plugins_manager = dict()

def get_plugin_manager(namespace):
    global plugins_manager
    return plugins_manager.get(namespace, None)


class BaseContext:

    def __init__(self):
        self.loop = None
        self.logger = None


class PluginManager:
    __doc__ = '\n    Wraps setuptools Entry point mechanism to provide a basic plugin system.\n    Plugins are loaded for a given namespace (group).\n    This plugin manager uses coroutines to run plugin call asynchronously in an event queue\n    '

    def __init__(self, namespace, context, loop=None):
        if loop is not None:
            self._loop = loop
        else:
            self._loop = asyncio.get_event_loop()
        self.logger = logging.getLogger(namespace)
        if context is None:
            self.context = BaseContext()
        else:
            self.context = context
        self.context.loop = self._loop
        self._plugins = []
        self._load_plugins(namespace)
        self._fired_events = []
        plugins_manager[namespace] = self

    @property
    def app_context(self):
        return self.context

    def _load_plugins(self, namespace):
        self.logger.debug('Loading plugins for namespace %s' % namespace)
        for ep in pkg_resources.iter_entry_points(group=namespace):
            plugin = self._load_plugin(ep)
            self._plugins.append(plugin)
            self.logger.debug(' Plugin %s ready' % plugin.ep.name)

    def _load_plugin--- This code section failed: ---

 L.  68         0  SETUP_FINALLY        98  'to 98'

 L.  69         2  LOAD_FAST                'self'
                4  LOAD_ATTR                logger
                6  LOAD_METHOD              debug
                8  LOAD_STR                 ' Loading plugin %s'
               10  LOAD_FAST                'ep'
               12  BINARY_MODULO    
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L.  70        18  LOAD_FAST                'ep'
               20  LOAD_ATTR                load
               22  LOAD_CONST               True
               24  LOAD_CONST               ('require',)
               26  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               28  STORE_FAST               'plugin'

 L.  71        30  LOAD_FAST                'self'
               32  LOAD_ATTR                logger
               34  LOAD_METHOD              debug
               36  LOAD_STR                 ' Initializing plugin %s'
               38  LOAD_FAST                'ep'
               40  BINARY_MODULO    
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L.  72        46  LOAD_GLOBAL              copy
               48  LOAD_METHOD              copy
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                app_context
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'plugin_context'

 L.  73        58  LOAD_FAST                'self'
               60  LOAD_ATTR                logger
               62  LOAD_METHOD              getChild
               64  LOAD_FAST                'ep'
               66  LOAD_ATTR                name
               68  CALL_METHOD_1         1  ''
               70  LOAD_FAST                'plugin_context'
               72  STORE_ATTR               logger

 L.  74        74  LOAD_FAST                'plugin'
               76  LOAD_FAST                'plugin_context'
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'obj'

 L.  75        82  LOAD_GLOBAL              Plugin
               84  LOAD_FAST                'ep'
               86  LOAD_ATTR                name
               88  LOAD_FAST                'ep'
               90  LOAD_FAST                'obj'
               92  CALL_FUNCTION_3       3  ''
               94  POP_BLOCK        
               96  RETURN_VALUE     
             98_0  COME_FROM_FINALLY     0  '0'

 L.  76        98  DUP_TOP          
              100  LOAD_GLOBAL              ImportError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   150  'to 150'
              106  POP_TOP          
              108  STORE_FAST               'ie'
              110  POP_TOP          
              112  SETUP_FINALLY       138  'to 138'

 L.  77       114  LOAD_FAST                'self'
              116  LOAD_ATTR                logger
              118  LOAD_METHOD              warning
              120  LOAD_STR                 'Plugin %r import failed: %s'
              122  LOAD_FAST                'ep'
              124  LOAD_FAST                'ie'
              126  BUILD_TUPLE_2         2 
              128  BINARY_MODULO    
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
              134  POP_BLOCK        
              136  BEGIN_FINALLY    
            138_0  COME_FROM_FINALLY   112  '112'
              138  LOAD_CONST               None
              140  STORE_FAST               'ie'
              142  DELETE_FAST              'ie'
              144  END_FINALLY      
              146  POP_EXCEPT       
              148  JUMP_FORWARD        206  'to 206'
            150_0  COME_FROM           104  '104'

 L.  78       150  DUP_TOP          
              152  LOAD_GLOBAL              pkg_resources
              154  LOAD_ATTR                UnknownExtra
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   204  'to 204'
              160  POP_TOP          
              162  STORE_FAST               'ue'
              164  POP_TOP          
              166  SETUP_FINALLY       192  'to 192'

 L.  79       168  LOAD_FAST                'self'
              170  LOAD_ATTR                logger
              172  LOAD_METHOD              warning
              174  LOAD_STR                 'Plugin %r dependencies resolution failed: %s'
              176  LOAD_FAST                'ep'
              178  LOAD_FAST                'ue'
              180  BUILD_TUPLE_2         2 
              182  BINARY_MODULO    
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM_FINALLY   166  '166'
              192  LOAD_CONST               None
              194  STORE_FAST               'ue'
              196  DELETE_FAST              'ue'
              198  END_FINALLY      
              200  POP_EXCEPT       
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           158  '158'
              204  END_FINALLY      
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM           148  '148'

Parse error at or near `DUP_TOP' instruction at offset 150

    def get_plugin(self, name):
        """
        Get a plugin by its name from the plugins loaded for the current namespace
        :param name:
        :return:
        """
        for p in self._plugins:
            if p.name == name:
                return p

    @asyncio.coroutine
    def close(self):
        """
        Free PluginManager resources and cancel pending event methods
        This method call a close() coroutine for each plugin, allowing plugins to close and free resources
        :return:
        """
        (yield from self.map_plugin_coro('close'))
        for task in self._fired_events:
            task.cancel()

        if False:
            yield None

    @property
    def plugins(self):
        """
        Get the loaded plugins list
        :return:
        """
        return self._plugins

    def _schedule_coro(self, coro):
        return asyncio.ensure_future(coro, loop=(self._loop))

    @asyncio.coroutine
    def fire_event(self, event_name, wait=False, *args, **kwargs):
        """
        Fire an event to plugins.
        PluginManager schedule @asyncio.coroutinecalls for each plugin on method called "on_" + event_name
        For example, on_connect will be called on event 'connect'
        Method calls are schedule in the asyn loop. wait parameter must be set to true to wait until all
        mehtods are completed.
        :param event_name:
        :param args:
        :param kwargs:
        :param wait: indicates if fire_event should wait for plugin calls completion (True), or not
        :return:
        """
        tasks = []
        event_method_name = 'on_' + event_name
        for plugin in self._plugins:
            event_method = getattrplugin.objectevent_method_nameNone
            if event_method:
                try:
                    task = self._schedule_coro(event_method(*args, **kwargs))
                    tasks.append(task)

                    def clean_fired_events(future):
                        try:
                            self._fired_events.remove(task)
                        except (KeyError, ValueError):
                            pass

                    task.add_done_callback(clean_fired_events)
                except AssertionError:
                    self.logger.error("Method '%s' on plugin '%s' is not a coroutine" % (
                     event_method_name, plugin.name))

            self._fired_events.extend(tasks)
            if wait:
                if tasks:
                    (yield from asyncio.wait(tasks, loop=(self._loop)))

        if False:
            yield None

    @asyncio.coroutine
    def map(self, coro, *args, **kwargs):
        """
        Schedule a given coroutine call for each plugin.
        The coro called get the Plugin instance as first argument of its method call
        :param coro: coro to call on each plugin
        :param filter_plugins: list of plugin names to filter (only plugin whose name is in filter are called).
        None will call all plugins. [] will call None.
        :param args: arguments to pass to coro
        :param kwargs: arguments to pass to coro
        :return: dict containing return from coro call for each plugin
        """
        p_list = kwargs.pop('filter_plugins', None)
        if p_list is None:
            p_list = [p.name for p in self.plugins]
        tasks = []
        plugins_list = []
        for plugin in self._plugins:
            if plugin.name in p_list:
                coro_instance = coro(plugin, *args, **kwargs)
                if coro_instance:
                    try:
                        tasks.append(self._schedule_coro(coro_instance))
                        plugins_list.append(plugin)
                    except AssertionError:
                        self.logger.error("Method '%r' on plugin '%s' is not a coroutine" % (
                         coro, plugin.name))

                if tasks:
                    ret_list = yield from (asyncio.gather)(*tasks, **{'loop': self._loop})
                    ret_dict = {v:k for k, v in zip(plugins_list, ret_list)}
                else:
                    ret_dict = {}
            return ret_dict

        if False:
            yield None

    @staticmethod
    @asyncio.coroutine
    def _call_coro--- This code section failed: ---

 L. 191         0  SETUP_FINALLY        34  'to 34'

 L. 192         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'plugin'
                6  LOAD_ATTR                object
                8  LOAD_FAST                'coro_name'
               10  LOAD_CONST               None
               12  CALL_FUNCTION_3       3  ''
               14  LOAD_FAST                'args'
               16  LOAD_FAST                'kwargs'
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'coro'

 L. 193        22  LOAD_FAST                'coro'
               24  GET_YIELD_FROM_ITER
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY     0  '0'

 L. 194        34  DUP_TOP          
               36  LOAD_GLOBAL              TypeError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 196        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 44

    @asyncio.coroutine
    def map_plugin_coro(self, coro_name, *args, **kwargs):
        """
        Call a plugin declared by plugin by its name
        :param coro_name:
        :param args:
        :param kwargs:
        :return:
        """
        return (yield from (self.map)(self._call_coro, coro_name, *args, **kwargs))
        if False:
            yield None