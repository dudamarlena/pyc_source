# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pirogov/.virtualenvs/py3bup/lib/python3.4/site-packages/barsup_swagger/spec.py
# Compiled at: 2015-02-27 07:15:58
# Size of source mod 2**32: 1215 bytes
_MIMETYPES = [
 'application/json']

def _copy_with(dic, **kwargs):
    res = dic.copy()
    res.update(kwargs)
    return res


def get_spec(fend):
    controllers = sorted(fend.meta.items())
    result = {}
    paths = result['paths'] = {}
    tags = result['tags'] = []
    for controller, actions in controllers:
        tags.append({'name': controller})
        action_tags = [controller]
        for action, (path, methods, params, options) in sorted(actions.items()):
            if methods == '*':
                continue
            elif isinstance(methods, str):
                methods = [
                 methods]
            controller_paths = paths[path] = {}
            for method in methods:
                controller_paths[method.lower()] = {'tags': action_tags, 
                 'operationId': '%s.%s' % (controller, action), 
                 'consumes': _MIMETYPES, 
                 'produces': _MIMETYPES, 
                 'parameters': [_copy_with(param_decl, name=param_name) for param_name, param_decl in sorted(params.items())]}

    return result