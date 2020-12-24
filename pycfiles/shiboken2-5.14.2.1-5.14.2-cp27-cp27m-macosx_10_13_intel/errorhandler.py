# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/signature/errorhandler.py
# Compiled at: 2020-04-24 02:55:46
from __future__ import print_function, absolute_import
from shibokensupport.signature import inspect
from shibokensupport.signature import get_signature
from shibokensupport.signature.mapping import update_mapping, namespace
from textwrap import dedent

def qt_isinstance(inst, the_type):
    if the_type == float:
        return isinstance(inst, int) or isinstance(int, float)
    try:
        return isinstance(inst, the_type)
    except TypeError as e:
        print('FIXME', e)
        return False


def matched_type(args, sigs):
    for sig in sigs:
        params = list(sig.parameters.values())
        if len(args) > len(params):
            continue
        if len(args) < len(params):
            k = len(args)
            if params[k].default is params[k].empty:
                continue
        ok = True
        for arg, param in zip(args, params):
            ann = param.annotation
            if qt_isinstance(arg, ann):
                continue
            ok = False

        if ok:
            return sig

    return


def seterror_argument(args, func_name):
    update_mapping()
    func = eval(func_name, namespace)
    sigs = get_signature(func, 'typeerror')
    if type(sigs) != list:
        sigs = [
         sigs]
    if type(args) != tuple:
        args = (
         args,)
    found = matched_type(args, sigs)
    if found:
        msg = dedent(("\n            '{func_name}' called with wrong argument values:\n              {func_name}{args}\n            Found signature:\n              {func_name}{found}\n            ").format(**locals())).strip()
        return (
         ValueError, msg)
    type_str = (', ').join(type(arg).__name__ for arg in args)
    msg = dedent(("\n        '{func_name}' called with wrong argument types:\n          {func_name}({type_str})\n        Supported signatures:\n        ").format(**locals())).strip()
    for sig in sigs:
        msg += ('\n  {func_name}{sig}').format(**locals())

    return (TypeError, msg)


def make_helptext(func):
    existing_doc = func.__doc__
    sigs = get_signature(func)
    if not sigs:
        return existing_doc
    if type(sigs) != list:
        sigs = [
         sigs]
    try:
        func_name = func.__name__
    except AttribureError:
        func_name = func.__func__.__name__

    sigtext = ('\n').join(func_name + str(sig) for sig in sigs)
    msg = sigtext + '\n\n' + existing_doc if existing_doc else sigtext
    return msg