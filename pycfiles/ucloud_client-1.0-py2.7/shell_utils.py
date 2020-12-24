# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/utils/shell_utils.py
# Compiled at: 2015-04-17 09:55:05
import os, six, prettytable, textwrap, json

def add_arg(func, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""
    if not hasattr(func, 'arguments'):
        func.arguments = []
    if (args, kwargs) not in func.arguments:
        func.arguments.insert(0, (args, kwargs))


def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """

    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func

    return _decorator


def multi_arg(*args, **kwargs):
    """Decorator for multiple CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """

    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func

    return _decorator


def print_dict(d, dict_property='Property', dict_value='Value', wrap=0):
    pt = prettytable.PrettyTable([dict_property, dict_value], caching=False)
    pt.align = 'l'
    for k, v in sorted(d.items()):
        if isinstance(v, (dict, list)):
            v = json.dumps(v)
        if wrap > 0:
            v = textwrap.fill(str(v), wrap)
        if v and isinstance(v, six.string_types) and '\\n' in v:
            lines = v.strip().split('\\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''

        else:
            if v is None:
                v = '-'
            pt.add_row([k, v])

    result = pt.get_string()
    if six.PY3:
        result = result.decode()
    print result
    return


def print_list(objs, fields, formatters={}, sortby_index=None):
    if sortby_index is None:
        sortby = None
    else:
        sortby = fields[sortby_index]
    mixed_case_fields = [
     'serverId']
    pt = prettytable.PrettyTable([ f for f in fields ], caching=False)
    pt.align = 'l'
    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                field_name = field
                data = o.get(field_name, '')
                if data is None:
                    data = '-'
                row.append(data)

        pt.add_row(row)

    if sortby is not None:
        result = pt.get_string(sortby=sortby)
    else:
        result = pt.get_string()
    if six.PY3:
        result = result.decode()
    print result
    return


def env(*args, **kwargs):
    """Returns environment variable set."""
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value

    return kwargs.get('default', '')