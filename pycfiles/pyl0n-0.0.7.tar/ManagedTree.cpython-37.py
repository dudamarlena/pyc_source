# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/ManagedTree.py
# Compiled at: 2019-10-27 05:30:43
# Size of source mod 2**32: 13396 bytes
import asyncio, collections, functools, inspect, logging
from pyimmutable import ImmutableDict, ImmutableList
from pykzee.common import PathType, Undefined, call_soon, makePath, pathToString, setDataForPath, getDataForPath
from pykzee import AttachedInfo
import pykzee.Plugin as Plugin
import pykzee.Tree as Tree
SubscriptionSlot = collections.namedtuple('SubscriptionSlot', ('path', 'directory',
                                                               'resolve_symlinks'))

class Subscription:
    __slots__ = ('plugin', 'slots', 'callback', '__currentState', '__reportedState',
                 'disabled')

    def __init__--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'slots'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              tuple
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_TRUE     58  'to 58'

 L.  41        12  LOAD_GLOBAL              any
               14  LOAD_GENEXPR             '<code_object <genexpr>>'
               16  LOAD_STR                 'Subscription.__init__.<locals>.<genexpr>'
               18  MAKE_FUNCTION_0          ''
               20  LOAD_FAST                'slots'
               22  GET_ITER         
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_1       1  ''
               28  POP_JUMP_IF_TRUE     58  'to 58'

 L.  42        30  LOAD_GLOBAL              type
               32  LOAD_FAST                'state'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_GLOBAL              ImmutableList
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_TRUE     58  'to 58'

 L.  43        42  LOAD_GLOBAL              len
               44  LOAD_FAST                'slots'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              len
               50  LOAD_FAST                'state'
               52  CALL_FUNCTION_1       1  ''
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_TRUE    108  'to 108'
             58_0  COME_FROM            40  '40'
             58_1  COME_FROM            28  '28'
             58_2  COME_FROM            10  '10'

 L.  45        58  LOAD_GLOBAL              logging
               60  LOAD_METHOD              error

 L.  46        62  LOAD_STR                 'Subscription constructor called with invalid arguments: slots='
               64  LOAD_FAST                'slots'
               66  FORMAT_VALUE          2  '!r'
               68  LOAD_STR                 ' len(state)='
               70  LOAD_GLOBAL              len
               72  LOAD_FAST                'state'
               74  CALL_FUNCTION_1       1  ''
               76  FORMAT_VALUE          0  ''
               78  BUILD_STRING_4        4 
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L.  49        84  LOAD_GLOBAL              Exception

 L.  50        86  LOAD_STR                 'Subscription constructor called with invalid arguments: slots='
               88  LOAD_FAST                'slots'
               90  FORMAT_VALUE          2  '!r'
               92  LOAD_STR                 ' len(state)='
               94  LOAD_GLOBAL              len
               96  LOAD_FAST                'state'
               98  CALL_FUNCTION_1       1  ''
              100  FORMAT_VALUE          0  ''
              102  BUILD_STRING_4        4 
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  ''
            108_0  COME_FROM            56  '56'

 L.  53       108  LOAD_FAST                'plugin'
              110  LOAD_FAST                'self'
              112  STORE_ATTR               plugin

 L.  54       114  LOAD_FAST                'slots'
              116  LOAD_FAST                'self'
              118  STORE_ATTR               slots

 L.  55       120  LOAD_FAST                'callback'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               callback

 L.  56       126  LOAD_FAST                'state'
              128  LOAD_FAST                'self'
              130  STORE_ATTR               _Subscription__currentState

 L.  58       132  LOAD_FAST                'initial'
              134  POP_JUMP_IF_FALSE   154  'to 154'
              136  LOAD_GLOBAL              ImmutableList
              138  LOAD_GENEXPR             '<code_object <genexpr>>'
              140  LOAD_STR                 'Subscription.__init__.<locals>.<genexpr>'
              142  MAKE_FUNCTION_0          ''
              144  LOAD_FAST                'slots'
              146  GET_ITER         
              148  CALL_FUNCTION_1       1  ''
              150  CALL_FUNCTION_1       1  ''
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           134  '134'
              154  LOAD_FAST                'state'
            156_0  COME_FROM           152  '152'
              156  LOAD_FAST                'self'
              158  STORE_ATTR               _Subscription__reportedState

 L.  60       160  LOAD_CONST               False
              162  LOAD_FAST                'self'
              164  STORE_ATTR               disabled

Parse error at or near `COME_FROM' instruction at offset 108_0

    def setCurrentState(self, idx, state):
        self._Subscription__currentState = self._Subscription__currentState.set(idx, state)

    def needsUpdate(self):
        return self._Subscription__reportedState is not self._Subscription__currentState

    def updated(self):
        self._Subscription__reportedState = self._Subscription__currentState

    def getState(self):
        return self._Subscription__currentState


class Mount:
    __slots__ = ('plugin', 'directory', 'tree', 'disabled')

    def __init__(self, plugin, directory, tree):
        self.plugin = plugin
        self.directory = directory
        self.tree = tree
        self.disabled = False


class Directory:
    __slots__ = 'parent pathElement subdirectories'.split()

    def __init__(self, parent, path_element):
        self.parent = parent
        self.pathElement = path_element
        self.subdirectories = {}

    def get(self, path: PathType, *, create=True):
        d = self
        for p in path:
            sd = d.subdirectories.getp
            if sd is None:
                if create:
                    sd = d.subdirectories[p] = type(self)(d, p)
                else:
                    return
            d = sd

        return d

    def garbageCollect(self):
        parent = self.parent
        if parent is not None:
            if not self.subdirectories:
                if self._canBeRemoved():
                    del parent.subdirectories[self.pathElement]
                    self.parent = None
                    parent.garbageCollect()


class SubscriptionDirectory(Directory):
    __slots__ = ('subscriptions', 'state')

    def __init__(self, parent, path_element):
        super().__init__(parent, path_element)
        self.subscriptions = set()
        self.state = Undefined
        try:
            if type(parent.state) in (ImmutableDict, ImmutableList):
                self.state = parent.state[path_element]
        except Exception:
            pass

    def _canBeRemoved(self):
        return not self.subscriptions

    def update(self, new_state):
        if new_state is self.state:
            return
        for sub, idx in self.subscriptions:
            sub.setCurrentState(idx, new_state)

        for key, subdir in self.subdirectories.items():
            sdata = Undefined
            if type(new_state) in (ImmutableDict, ImmutableList):
                try:
                    sdata = new_state[key]
                except Exception:
                    pass

            subdir.updatesdata

        self.state = new_state


class MountDirectory(Directory):
    __slots__ = ('mount', )

    def __init__(self, parent, path_element):
        super().__init__(parent, path_element)
        self.mount = None

    def _canBeRemoved(self):
        return self.mount is None


class Command:
    __slots__ = ('path', 'name', 'function', 'doc', 'disabled')

    def __init__(self, path, name, function, doc):
        self.path = path
        self.name = name
        self.function = function
        self.doc = doc
        self.disabled = False


class PluginInfo:
    __slots__ = ('subscriptions', 'mounts', 'plugInsAdded', 'disabled', 'plugin')

    def __init__(self):
        self.subscriptions = set()
        self.mounts = set()
        self.plugInsAdded = set()
        self.disabled = False


class ManagedTree:
    __slots__ = '\n    __state __resolvedState __root __resolvedRoot __realpath\n    __mountRoot __pluginInfos __commands\n    __subscriptionCheckScheduled __subscriptionCheckLock\n    __coreSet\n    '.strip().split()

    def __init__(self):
        self._ManagedTree__state = self._ManagedTree__resolvedState = ImmutableDict()
        self._ManagedTree__root = SubscriptionDirectory(None, None)
        self._ManagedTree__resolvedRoot = SubscriptionDirectory(None, None)
        self._ManagedTree__realpath = makePath
        self._ManagedTree__mountRoot = MountDirectory(None, None)
        self._ManagedTree__pluginInfos = set()
        self._ManagedTree__commands = {}
        self._ManagedTree__subscriptionCheckScheduled = False
        self._ManagedTree__subscriptionCheckLock = asyncio.Lock()
        self._ManagedTree__mountRoot.get('core', ).mount = True
        self._ManagedTree__coreSet = lambda path, value: self.set(('core', ) + path, value)

    def get(self, path: PathType, *, resolve_symlinks=True):
        return getDataForPath(self._ManagedTree__resolvedState if resolve_symlinks else self._ManagedTree__state, path)

    def set(self, path: PathType, value):
        new_state = setDataForPath(self._ManagedTree__state, path, value)
        if not new_state.isImmutableJson:
            raise Exception('invalid data')
        if self._ManagedTree__state is new_state:
            return
        new_state = setDataForPath(new_state, ('core', 'symlinks'), AttachedInfo.symlinkInfoDictnew_state)
        self._ManagedTree__resolvedState = AttachedInfo.resolvednew_state
        self._ManagedTree__realpath = lambda func: lambda path: func(makePath(path))(AttachedInfo.realpathnew_state)
        self._ManagedTree__state = new_state
        self._ManagedTree__scheduleSubscriptionCheck()
        print(sorted(new_state.meta))

    def command(self, path, cmd):
        return self._ManagedTree__commands[path][cmd].function

    def subscribe(self, plugin_info, paths, callback, *, initial=True, resolve_symlinks=True):
        if plugin_info.disabled or plugin_info not in self._ManagedTree__pluginInfos:
            raise Exception('disabled/unregistered plugin must not subscribe')
        slots = tuple((SubscriptionSlot(path, (self._ManagedTree__resolvedRoot if resolve_symlinks else self._ManagedTree__root).getpath, resolve_symlinks) for path in paths))
        state = ImmutableList((slot.directory.state for slot in slots))
        sub = Subscription(plugin_info, slots, callback, state, initial)
        plugin_info.subscriptions.addsub
        for idx, slot in enumerate(slots):
            slot.directory.subscriptions.add(sub, idx)

        if initial:
            self._ManagedTree__scheduleSubscriptionCheck()
        return lambda : self.unsubscribesub

    def unsubscribe(self, sub):
        sub.disabled = True
        for idx, slot in enumerate(sub.slots):
            slot.directory.subscriptions.discard(sub, idx)
            slot.directory.garbageCollect()

        sub.plugin.subscriptions.discardsub

    def mount(self, plugin_info, path):
        directory = self._ManagedTree__mountRoot.getpath
        if any((d.mount for d in self._ManagedTree__relatedDirectoriesdirectory)):
            directory.garbageCollect()
            raise Exception('conflicting mount')
        mount = Mount(plugin_info, directory, Tree(self, path))
        plugin_info.mounts.addmount
        directory.mount = mount
        return mount.tree.getAccessProxy()._replace(deactivate=(functools.partial(self.unmount, mount)))

    def unmount(self, mount):
        if mount.disabled:
            return
        mount.disabled = True
        mount.directory.mount = None
        mount.plugin.mounts.discardmount
        mount.tree.deactivate()
        mount.directory.garbageCollect()

    def registerCommand(self, path, name, function, doc=Undefined):
        if doc is Undefined:
            doc = function.__doc__
        sig = inspect.signaturefunction
        cmd = Command(path, name, function, doc)
        try:
            path_commands = self._ManagedTree__commands[path]
        except KeyError:
            path_commands = self._ManagedTree__commands[path] = {}

        if name in path_commands:
            raise Exception('Command { path }:{ name } already registered')
        path_commands[name] = cmd
        self._ManagedTree__coreSet((
         'commands', pathToString(path), name), {'doc':doc, 
         'signature':str(sig)})

        def unregisterCommand():
            if cmd.disabled:
                return
            else:
                cmd.disabled = True
                path_commands = self._ManagedTree__commands[cmd.path]
                path_commands.popcmd.name
                if not path_commands:
                    del self._ManagedTree__commands[cmd.path]
                    self._ManagedTree__coreSet(('commands', pathToString(cmd.path)), Undefined)
                else:
                    self._ManagedTree__coreSet((
                     'commands', pathToString(cmd.path), cmd.name), Undefined)

        return unregisterCommand

    def addPlugin--- This code section failed: ---

 L. 333         0  LOAD_FAST                'added_by'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    40  'to 40'

 L. 334         8  LOAD_FAST                'added_by'
               10  LOAD_ATTR                disabled
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 335        14  LOAD_GLOBAL              Exception
               16  LOAD_STR                 'Disabled plugin tried to register a plugin'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  ''
             22_0  COME_FROM            12  '12'

 L. 336        22  LOAD_FAST                'added_by'
               24  LOAD_DEREF               'self'
               26  LOAD_ATTR                _ManagedTree__pluginInfos
               28  COMPARE_OP               not-in
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 337        32  LOAD_GLOBAL              Exception
               34  LOAD_STR                 'Parent plugin not registered with this tree'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  ''
             40_0  COME_FROM            30  '30'
             40_1  COME_FROM             6  '6'

 L. 338        40  LOAD_GLOBAL              issubclass
               42  LOAD_FAST                'PluginType'
               44  LOAD_GLOBAL              Plugin
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_TRUE     58  'to 58'

 L. 339        50  LOAD_GLOBAL              TypeError
               52  LOAD_STR                 'Plugin type must derive from Plugin class'
               54  CALL_FUNCTION_1       1  ''
               56  RAISE_VARARGS_1       1  ''
             58_0  COME_FROM            48  '48'

 L. 340        58  LOAD_GLOBAL              PluginInfo
               60  CALL_FUNCTION_0       0  ''
               62  STORE_DEREF              'plugin_info'

 L. 341        64  LOAD_FAST                'PluginType'

 L. 342        66  LOAD_CLOSURE             'self'
               68  BUILD_TUPLE_1         1 
               70  LOAD_LAMBDA              '<code_object <lambda>>'
               72  LOAD_STR                 'ManagedTree.addPlugin.<locals>.<lambda>'
               74  MAKE_FUNCTION_8          'closure'

 L. 343        76  LOAD_CONST               True
               78  LOAD_CONST               ('initial',)
               80  BUILD_CONST_KEY_MAP_1     1 
               82  LOAD_CLOSURE             'plugin_info'
               84  LOAD_CLOSURE             'self'
               86  BUILD_TUPLE_2         2 
               88  LOAD_LAMBDA              '<code_object <lambda>>'
               90  LOAD_STR                 'ManagedTree.addPlugin.<locals>.<lambda>'
               92  MAKE_FUNCTION_10         'keyword-only, closure'

 L. 346        94  LOAD_CLOSURE             'plugin_info'
               96  LOAD_CLOSURE             'self'
               98  BUILD_TUPLE_2         2 
              100  LOAD_LAMBDA              '<code_object <lambda>>'
              102  LOAD_STR                 'ManagedTree.addPlugin.<locals>.<lambda>'
              104  MAKE_FUNCTION_8          'closure'

 L. 347       106  LOAD_CLOSURE             'plugin_info'
              108  LOAD_CLOSURE             'self'
              110  BUILD_TUPLE_2         2 
              112  LOAD_LAMBDA              '<code_object <lambda>>'
              114  LOAD_STR                 'ManagedTree.addPlugin.<locals>.<lambda>'
              116  MAKE_FUNCTION_8          'closure'

 L. 350       118  LOAD_CLOSURE             'plugin_info'
              120  LOAD_CLOSURE             'self'
              122  BUILD_TUPLE_2         2 
              124  LOAD_LAMBDA              '<code_object <lambda>>'
              126  LOAD_STR                 'ManagedTree.addPlugin.<locals>.<lambda>'
              128  MAKE_FUNCTION_8          'closure'

 L. 351       130  LOAD_CLOSURE             'self'
              132  BUILD_TUPLE_1         1 
              134  LOAD_LAMBDA              '<code_object <lambda>>'
              136  LOAD_STR                 'ManagedTree.addPlugin.<locals>.<lambda>'
              138  MAKE_FUNCTION_8          'closure'
              140  LOAD_CONST               ('get', 'subscribe', 'mount', 'addPlugin', 'removePlugin', 'command')
              142  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              144  LOAD_DEREF               'plugin_info'
              146  STORE_ATTR               plugin

 L. 353       148  LOAD_DEREF               'self'
              150  LOAD_ATTR                _ManagedTree__pluginInfos
              152  LOAD_METHOD              add
              154  LOAD_DEREF               'plugin_info'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L. 354       160  LOAD_FAST                'added_by'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   180  'to 180'

 L. 355       168  LOAD_FAST                'added_by'
              170  LOAD_ATTR                plugInsAdded
              172  LOAD_METHOD              add
              174  LOAD_DEREF               'plugin_info'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
            180_0  COME_FROM           166  '166'

 L. 356       180  LOAD_GLOBAL              getattr
              182  LOAD_DEREF               'plugin_info'
              184  LOAD_ATTR                plugin
              186  LOAD_STR                 'init'
              188  LOAD_CONST               None
              190  CALL_FUNCTION_3       3  ''
              192  STORE_FAST               'init'

 L. 357       194  LOAD_FAST                'init'
              196  LOAD_CONST               None
              198  COMPARE_OP               is-not
              200  POP_JUMP_IF_FALSE   220  'to 220'

 L. 358       202  LOAD_GLOBAL              call_soon
              204  LOAD_FAST                'init'
              206  BUILD_TUPLE_1         1 
              208  LOAD_FAST                'args'
              210  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              212  LOAD_FAST                'kwargs'
              214  CALL_FUNCTION_EX_KW     1  'keyword args'
              216  POP_TOP          
              218  JUMP_FORWARD        238  'to 238'
            220_0  COME_FROM           200  '200'

 L. 359       220  LOAD_FAST                'args'
              222  POP_JUMP_IF_TRUE    228  'to 228'
              224  LOAD_FAST                'kwargs'
              226  POP_JUMP_IF_FALSE   238  'to 238'
            228_0  COME_FROM           222  '222'

 L. 360       228  LOAD_GLOBAL              logging
              230  LOAD_METHOD              warning
              232  LOAD_STR                 'plugin has no init method - ignoring arguments'
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          
            238_0  COME_FROM           226  '226'
            238_1  COME_FROM           218  '218'

 L. 361       238  LOAD_CLOSURE             'plugin_info'
              240  LOAD_CLOSURE             'self'
              242  BUILD_TUPLE_2         2 
              244  LOAD_LAMBDA              '<code_object <lambda>>'
              246  LOAD_STR                 'ManagedTree.addPlugin.<locals>.<lambda>'
              248  MAKE_FUNCTION_8          'closure'
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `STORE_ATTR' instruction at offset 146

    def __removePlugin(self, plugin_info):
        if plugin_info.disabled:
            return
        self._ManagedTree__pluginInfos.removeplugin_info
        plugin_info.disabled = True
        for p in plugin_info.plugInsAdded:
            self._ManagedTree__removePluginp

        plugin_info.subscriptions = set()
        for sub in plugin_info.subscriptions:
            self.unsubscribesub

        plugin_info.mounts = set()
        for mount in plugin_info.mounts:
            self.unmountmount

        shutdown = getattr(plugin_info.plugin, 'shutdown', None)
        if shutdown is not None:
            call_soon(shutdown)

    def __scheduleSubscriptionCheck(self):
        if not self._ManagedTree__subscriptionCheckScheduled:
            self._ManagedTree__subscriptionCheckScheduled = True
            call_soon(self._ManagedTree__subscriptionCheck)

    async def __subscriptionCheck(self):
        async with self._ManagedTree__subscriptionCheckLock:
            self._ManagedTree__subscriptionCheckScheduled = False
            self._ManagedTree__root.updateself._ManagedTree__state
            self._ManagedTree__resolvedRoot.updateself._ManagedTree__resolvedState
            for sub in list((sub for plugin_info in self._ManagedTree__pluginInfos for sub in plugin_info.subscriptions)):
                if sub.disabled:
                    continue
                if sub.needsUpdate():
                    call_soon(sub.callback, *sub.getState())
                    sub.updated()

    def __relatedDirectories(self, directory):
        yield directory
        parent = directory.parent
        while parent is not None:
            yield parent
            parent = parent.parent

        subdirs = list(directory.subdirectories.values())
        while subdirs:
            sd = subdirs.pop()
            yield sd
            subdirs.extendsd.subdirectories.values()