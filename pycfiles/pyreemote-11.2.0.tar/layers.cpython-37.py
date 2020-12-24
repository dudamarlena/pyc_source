# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/layers.py
# Compiled at: 2018-12-10 17:05:14
# Size of source mod 2**32: 8180 bytes
__doc__ = 'Layer system for Engine. Each layer represents a single python file that is run on every tick.'
import types, typing
from typing import List, Tuple
from pathlib import Path
import importlib, sys, traceback
from inotify_simple import INotify, flags, masks
import inotify_simple, time
from PyreeEngine import log
from inotify_simple import INotify, flags, masks
import inotify_simple
from pathlib import Path
import json, pythonosc.dispatcher, pythonosc.udp_client
from PyreeEngine.util import Resolution

class LayerConfig(typing.NamedTuple):
    """LayerConfig"""
    name = None
    name: str
    module = None
    module: str
    filepath = None
    filepath: Path
    entryclass = 'LayerEntry'
    entryclass: str
    onloadoscpath = '/load'
    onloadoscpath: str
    onloadoscmessage = 'LOAD'
    onloadoscmessage: str


class ProgramConfig(typing.NamedTuple):
    layerdefs = []
    layerdefs: List[LayerConfig]
    oscserveraddress = '127.0.0.1'
    oscserveraddress: str
    oscserverport = 1337
    oscserverport: int
    oscclientaddress = '127.0.0.1'
    oscclientaddress: str
    oscclientport = 1337
    oscclientport: int


class LayerContext:
    """LayerContext"""

    def __init__(self):
        self.time = 0.0
        self.dt = 1.0
        self.frame = 0
        self.resolution = Resolution(width=800, height=600)
        self.aspect = self.resolution.width / self.resolution.height
        self.resolutionChangeCallbacks = []
        self.oscdispatcher = None
        self.oscclient = None

    def addresolutioncallback(self, newfunc: types.FunctionType):
        self.resolutionChangeCallbacks.append(newfunc)

    def removeresolutionscallback(self, removefunc: types.FunctionType):
        if removefunc in self.resolutionChangeCallbacks:
            self.resolutionChangeCallbacks.remove(removefunc)

    def setresolution(self, width, height):
        self.resolution = Resolution(width=width, height=height)
        self.aspect = self.resolution.width / self.resolution.height
        for callback in self.resolutionChangeCallbacks:
            callback(self.resolution)


class BaseEntry:

    def __init__(self, context: LayerContext):
        self.context = context

    def __serialize__(self) -> dict:
        return {}

    def __deserialize__(self, data: dict) -> None:
        pass

    def init(self):
        pass

    def tick(self):
        pass


class Layer:
    """Layer"""

    def __init__(self, config: LayerConfig, context: LayerContext):
        self.enabled = False
        self.valid = False
        self.old = False
        self.tickfunction = None
        self.config = config
        self.context = context
        self.inotify = None
        self.watch = None
        self.module = None
        self.entryclass = None
        self.entryinstance = None
        self.entrytick = None
        if self.loadmodule():
            self.valid = True
        else:
            self.valid = False
        self.installfilewatch()

    def tick(self):
        """Check iwatch and replace module if necessary"""
        if self.checkfilewatch():
            self.loadmodule()
        self.entryinstance.tick()

    def loadmodule(self) -> bool:
        """Loads the module and extracts entry point class"""
        importlib.invalidate_caches()
        try:
            if self.module is None:
                log.info('LAYER', 'Importing module %s' % self.config.module)
                self.module = importlib.import_module(self.config.module)
            elif type(self.module) is types.ModuleType:
                log.info('LAYER', 'Reloading module %s' % self.config.module)
                importlib.reload(self.module)
            else:
                log.warning('LAYER', 'Layer module property of layer %s is of type %s' % (self.config.name, type(self.module)))
                self.module = None
        except ModuleNotFoundError:
            log.error('LAYER', 'Module %s not found' % self.config.module)
            return False
        except Exception as exc:
            try:
                print((traceback.format_exc()), file=(sys.stderr))
                print(exc, file=(sys.stderr))
                log.error('LAYER', 'Module %s load exception, old instance persists on Layer %s' % (
                 self.config.module, self.config.name))
                return False
            finally:
                exc = None
                del exc

        if hasattr(self.module, self.config.entryclass):
            self.entryclass = getattr(self.module, self.config.entryclass)
        else:
            log.error('LAYER', 'Module %s has no class %s' % (self.config.module, self.config.entryclass))
            return False
        try:
            newinstance = self.entryclass(self.context)
            if self.entryinstance is not None:
                newinstance.__deserialize__(self.entryinstance.__serialize__())
            del self.entryinstance
            self.entryinstance = newinstance
            self.entryinstance.init()
        except Exception as exc:
            try:
                print((traceback.format_exc()), file=(sys.stderr))
                print(exc, file=(sys.stderr))
                log.error('LAYER', 'Failed to replace old instance with new instance on Layer %s' % self.config.name)
                return False
            finally:
                exc = None
                del exc

        return True

    def installfilewatch(self) -> None:
        fl = flags.CREATE | flags.MODIFY | flags.MOVED_TO
        self.iNotify = INotify()
        self.watch = self.iNotify.add_watch(self.config.filepath.parent, fl)

    def checkfilewatch(self) -> bool:
        retVal = False
        if not self.valid:
            return False
        events = self.iNotify.read(timeout=0)
        for event in events:
            if self.checkevent(event):
                retVal = True

        return retVal

    def checkevent(self, event: inotify_simple.Event) -> bool:
        retVal = False
        if event.name == self.config.filepath.name:
            if event.mask & (flags.CREATE | flags.MODIFY | flags.MOVED_TO):
                log.info('LAYER', 'Layer %s updated' % self.config.name)
                retVal = True
            elif event.mask & (flags.DELETE | flags.DELETE_SELF):
                self.valid = False
                log.info('LAYER', 'Layer %s deleted' % self.config.name)
        return retVal


class LayerManager:

    def __init__(self, config: ProgramConfig, context: LayerContext):
        self.config = config
        self.context = context
        self.layers = []
        self.loadlayers()

    def loadlayers(self) -> None:
        for layerdef in self.config.layerdefs:
            layerdef['filepath'] = Path(layerdef['module'].replace('.', '/') + '.py')
            layerconf = LayerConfig(**layerdef)
            newlayer = Layer(layerconf, self.context)
            self.layers.append(newlayer)

    def tick(self):
        for layer in self.layers:
            layer.tick()