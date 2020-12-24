# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/imports.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import pkgutil, six
MODEL_MOVES = {'sentry.models.tagkey.TagKey': 'sentry.tagstore.legacy.models.tagkey.TagKey', 
   'sentry.models.tagvalue.tagvalue': 'sentry.tagstore.legacy.models.tagvalue.TagValue', 
   'sentry.models.grouptagkey.GroupTagKey': 'sentry.tagstore.legacy.models.grouptagkey.GroupTagKey', 
   'sentry.models.grouptagvalue.GroupTagValue': 'sentry.tagstore.legacy.models.grouptagvalue.GroupTagValue', 
   'sentry.models.eventtag.EventTag': 'sentry.tagstore.legacy.models.eventtag.EventTag'}

class ModuleProxyCache(dict):

    def __missing__(self, key):
        if '.' not in key:
            return __import__(key)
        module_name, class_name = key.rsplit('.', 1)
        module = __import__(module_name, {}, {}, [class_name])
        handler = getattr(module, class_name)
        self[key] = handler
        return handler


_cache = ModuleProxyCache()

def import_string(path):
    """
    Path must be module.path.ClassName

    >>> cls = import_string('sentry.models.Group')
    """
    path = MODEL_MOVES.get(path, path)
    result = _cache[path]
    return result


def import_submodules(context, root_module, path):
    """
    Import all submodules and register them in the ``context`` namespace.

    >>> import_submodules(locals(), __name__, __path__)
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(path, root_module + '.'):
        module = __import__(module_name, globals(), locals(), ['__name__'])
        for k, v in six.iteritems(vars(module)):
            if not k.startswith('_'):
                context[k] = v

        context[module_name] = module