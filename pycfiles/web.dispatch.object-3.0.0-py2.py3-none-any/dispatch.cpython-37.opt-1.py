# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/dispatch/object/dispatch.py
# Compiled at: 2019-06-09 15:09:52
# Size of source mod 2**32: 4605 bytes
from inspect import isclass, isbuiltin, isroutine, getmembers, signature
from ..core import Crumb, nodefault, ipeek, prepare_path, opts
log = __import__('logging').getLogger(__name__)

class ObjectDispatch:
    __doc__ = 'Dispatch simulating the use of classes as collections, and attributes as resources.\n\t\n\tUnderscore-prefixed attribute names are protected by default, though these protections can be explicitly disabled.\n\t\n\t\n\t'
    __slots__ = [
     'protect']

    def __init__(self, protect=True):
        self.protect = protect
        log.debug('Object dispatcher prepared.', extra=dict(dispatcher=(repr(self))))
        super(ObjectDispatch, self).__init__()

    def __repr__(self):
        return 'ObjectDispatch(0x{id}, protect={self.protect!r})'.format(id=(id(self)), self=self)

    def trace(self, context, obj):
        """Enumerate the children of the given object, as would be accessible through dispatch."""
        if isroutine(obj):
            yield Crumb(self, obj, endpoint=True, handler=obj, options=(opts(obj)))
            return
        for name, attr in getmembers(obj):
            if name == '__getattr__':
                sig = signature(attr)
                path = '{' + list(sig.parameters.keys())[1] + '}'
                reta = sig.return_annotation
                if reta is not sig.empty:
                    if callable(reta):
                        isclass(reta) or (yield Crumb(self, obj, path, endpoint=True, handler=reta, options=(opts(reta))))
                    else:
                        yield Crumb(self, obj, path, handler=reta)
                else:
                    yield Crumb(self, obj, path, handler=attr)
                del sig
                del path
                del reta
                continue
            else:
                if name == '__call__':
                    yield Crumb(self, obj, None, endpoint=True, handler=obj)
                    continue
                elif self.protect and name[0] == '_':
                    continue
                yield Crumb(self, obj, name, endpoint=(callable(attr) and not isclass(attr)),
                  handler=attr,
                  options=(opts(attr)))

    def __call__(self, context, obj, path):
        protect = self.protect
        origin = obj
        current = None
        LE = {'dispatcher':repr(self), 
         'context':getattr(context, 'id', id(context))}
        log.debug('Preparing object dispatch.', extra=dict(LE, obj=obj, path=path))
        path = prepare_path(path)
        for previous, current in ipeek(path):
            if isclass(obj):
                obj = obj() if context is None else obj(context)
                log.debug('Instantiated class during descent.', extra=dict(LE, obj=obj))
            if protect:
                if current[0] == '_' or isbuiltin(obj):
                    log.debug(('Attempt made to access a protected attribute: ' + current), extra=dict(LE, handler=obj,
                      current=current))
                    break
            new = getattr(obj, current, nodefault)
            if new is nodefault:
                break
            log.debug(('Retrieved attribute: ' + current), extra=dict(LE, obj=new))
            yield Crumb(self, origin, path=previous, handler=obj)
            obj = new
        else:
            if isclass(obj):
                obj = obj() if context is None else obj(context)
                log.debug('Instantiated class at path terminus.', extra=dict(LE, obj=obj))
            log.debug('Dispatch complete due to exhausted path.', extra=dict(LE, obj=obj))
            yield Crumb(self, origin, path=current, endpoint=True, handler=obj)
            return

        log.debug(('Dispatch interrupted attempting to resolve attribute: ' + current), extra=dict(LE, handler=(repr(obj)),
          endpoint=(callable(obj)),
          previous=previous,
          attribute=current))
        if callable(obj):
            yield Crumb(self, origin, path=previous, endpoint=True, handler=obj, options=(opts(obj)))
        else:
            yield Crumb(self, origin, path=previous, endpoint=False, handler=obj, options=(opts(obj)))