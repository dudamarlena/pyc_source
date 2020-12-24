# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/parse_args.py
# Compiled at: 2019-08-19 15:09:29
from __future__ import print_function
from ast import literal_eval

def parse_args(s, strip_pars=False):
    """
    Parse a string representing arguments to a method to return the
    corresponding args and kwargs.

    :param s: string representing arguments to a method
    :param strip_pars: (bool) If True, expect s to include surrounding
          parenthesis
    :return: args, kwargs (a list of positional arguments and a dict of keyword
             arguments)
    """
    s = s.strip()
    if strip_pars:
        if s.startswith('(') and s.endswith(')'):
            s = s[1:-1].strip()
    if not s:
        return ([], {})
    a = []
    kw = {}
    for e in s.split(','):
        if '=' in e:
            k, v = e.split('=')
            kw[k.strip()] = literal_eval(v.strip())
        else:
            if kw:
                raise SyntaxError('non-keyword arg after keyword arg')
            a.append(literal_eval(e.strip()))

    return (
     a, kw)


if __name__ == '__main__':
    print(parse_args('1, 2, b=3, c=4'))
    print(parse_args(' (1, 2, b=3, c=4 )', strip_pars=True))
    print(parse_args('1, 2, b=3, c=4, 5'))