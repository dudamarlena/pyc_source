# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/eps/utilits.py
# Compiled at: 2014-07-01 01:06:58
# Size of source mod 2**32: 4680 bytes
import inspect, os
from itertools import chain
from . import hook
from . import EPS
if hasattr(inspect, 'getfullargspec'):
    getargspec = inspect.getfullargspec
else:
    getargspec = inspect.getargspec

def get_args(node):
    method = node['method']
    if not inspect.isfunction(method):
        return ''
    else:
        gas = getargspec(method)
        delta = len(gas.defaults or []) - len(gas.args)

        def inject(d):
            i, value = d
            i += delta
            if i >= 0:
                value += '=' + repr(gas.defaults[i])
            return value

        vargs = map(inject, enumerate(gas.args))
        kargs = []
        if hasattr(gas, 'kwonlyargs'):
            defaults = gas.kwonlydefaults or {}
            for k in gas.kwonlyargs:
                if k in defaults:
                    kargs.append(k + '=' + repr(gas.kwonlydefaults[k]))
                else:
                    kargs.append(k)

        if kargs:
            return ', '.join(chain(vargs, ['*'], kargs))
        return ', '.join(vargs)


def node_to_dict(node, name=None):
    method = node['method']
    comment = node['comment']
    if not comment:
        if hasattr(method, '__doc__'):
            comment = method.__doc__ or ''
            if isinstance(comment, bytes):
                comment = comment.decode('utf8')
    if not name:
        if hasattr(method, '__name__'):
            name = method.__name__
    package = ''
    module = inspect.getmodule(method)
    if module:
        package = module.__package__
    return {'name': name or '<no_name>',  'type': 'method', 
     'priority': node['priority'], 
     'args': get_args(node), 
     'located': os.path.relpath(node['located'][0]) + ':' + str(node['located'][1]), 
     'full_path': node['located'][0], 
     'path': os.path.relpath(node['located'][0]), 
     'comment': comment, 
     'package': package, 
     'node': node}


def info_eps_dict(instance):
    """Print EPS functional"""
    for name, line in sorted(instance._api.items(), key=lambda x: x[0]):
        if len(line) == 1:
            yield node_to_dict(line[0], name=name)
        else:
            lp = {'name': name, 
             'type': 'loop', 
             'list': map(node_to_dict, line)}
            yield lp


def pre_group(instance):
    tree = set()
    for node in info_eps_dict(instance):
        keys = node['name'].split('.')
        prefix = ''
        level = 0
        for key in keys[:-1]:
            prefix += key + '.'
            level += 1
            if prefix not in tree:
                tree.add(prefix)
                yield ('class', level, key)
                continue

        node['name'] = keys[(-1)]
        yield ('node', level, node)


def make_import(node):
    if node['path'].startswith('../'):
        if not node['package']:
            return ''
        d = node['package'].split('.')
    else:
        s = node['path']
        assert s[-3:] == '.py'
        s = s[:-3]
        d = s.split('/')
    if d[(-1)] == '__init__':
        d = d[:-1]
    if not d:
        return ''
    if len(d) == 1:
        return 'import ' + d[0]
    return 'from %s import %s' % ('.'.join(d[:-1]), d[(-1)])


def info_pypredef(self, name='EPS'):
    src = []
    src.append('class %s:' % name)
    for t, level, node in pre_group(self.eps):
        if t == 'class':
            margin = '    ' * level
            src.append('%sclass %s:' % (margin, node))
        elif t == 'node':
            level += 1
            if node['type'] == 'method':
                margin = '    ' * level
                src.append('%sdef %s(%s):' % (margin, node['name'], node['args']))
                src.append('%s    """' % margin)
                src.append('%s        %s' % (margin, node['comment']))
                src.append('%s        %s' % (margin, node['located']))
                src.append('%s    """' % margin)
                src.append(margin + '    ' + make_import(node))
                src.append('')
            else:
                if node['type'] == 'loop':
                    margin = '    ' * level
                    src.append('%sdef %s():' % (margin, node['name']))
                    src.append('%s    pass' % margin)
                    margin += '    '
                    for cn in node['list']:
                        src.append('%s" %d %s(%s) from %s"' % (margin, cn['priority'], cn['name'], cn['args'], cn['located']))
                        src.append(margin + make_import(cn))

                    src.append('')
                else:
                    continue

    return '\n'.join(src)


EPS.bind('eps.info_pypredef', info_pypredef)
EPS.bind('eps.Looper', hook.Looper, comment='class Looper')
EPS.bind('eps.set_looper', lambda cls: setattr(hook, 'DefaultLooper', cls), comment='Change default looper')