# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/lib/print.py
# Compiled at: 2013-03-17 23:03:38
import inspect, types

def print_dict(s, obj, title):
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__
    if isinstance(obj, types.DictType) or isinstance(obj, types.DictProxyType):
        s += '\n%s:\n' % title
        keys = obj.keys()
        keys.sort()
        for key in keys:
            s += '  %s:\t%s\n' % (repr(key), obj[key])

    return s


def print_argspec(obj, obj_name):
    """A slightly decorated version of inspect.format_argspec"""
    try:
        return obj_name + inspect.formatargspec(*inspect.getargspec(obj))
    except:
        return

    return


def print_obj(arg, frame, format=None, short=False):
    """Return a string representation of an object """
    try:
        if not frame:
            obj = eval(arg, None, None)
        else:
            obj = eval(arg, frame.f_globals, frame.f_locals)
    except:
        return 'No symbol "' + arg + '" in current context.'

    what = arg
    if format:
        what = format + ' ' + arg
        obj = printf(obj, format)
    s = '%s = %s' % (what, obj)
    if not short:
        s += '\ntype = %s' % type(obj)
        if callable(obj):
            argspec = print_argspec(obj, arg)
            if argspec:
                s += ':\n\t'
                if inspect.isclass(obj):
                    s += 'Class constructor information:\n\t'
                    obj = obj.__init__
                elif type(obj) is types.InstanceType:
                    obj = obj.__call__
                s += argspec
        s = print_dict(s, obj, 'object variables')
        if hasattr(obj, '__class__'):
            s = print_dict(s, obj.__class__, 'class variables')
    return s


pconvert = {'c': chr, 'x': hex, 'o': oct, 'f': float, 's': str}
twos = ('0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001',
        '1010', '1011', '1100', '1101', '1110', '1111')

def printf(val, fmt):
    global pconvert
    global twos
    if not fmt:
        fmt = ' '
    if fmt[0] == '/':
        fmt = fmt[1:]
    f = fmt[0]
    if f in pconvert.keys():
        try:
            return apply(pconvert[f], (val,))
        except:
            return str(val)

    if f == 't':
        try:
            res = ''
            while val:
                res = twos[(val & 15)] + res
                val = val >> 4

            return res
        except:
            return str(val)

    return str(val)


if __name__ == '__main__':
    print print_dict('', globals(), 'my globals')
    print '-' * 40
    print print_obj('print_obj', None)
    print '-' * 30
    print print_obj('Exception', None)
    print '-' * 30
    print print_argspec('Exception', None)

    class Foo:
        __module__ = __name__

        def __init__(self, bar=None):
            pass


    print print_obj('Foo.__init__', None)
    print '-' * 30
    print print_argspec(Foo.__init__, '__init__')
    assert printf(31, '/o') == '037'
    assert printf(31, '/t') == '00011111'
    assert printf(33, '/c') == '!'
    assert printf(33, '/x') == '0x21'