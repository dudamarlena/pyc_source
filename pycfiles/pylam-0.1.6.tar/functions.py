# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/utils/functions.py
# Compiled at: 2011-03-17 01:26:04
import inspect, weakref

def isfamily(obj, cls):
    try:
        bases = inspect.getmro(obj.__class__)
    except AttributeError:
        return False

    if bases.count(cls):
        return True
    else:
        return False


def kw(**kw):
    return kw


def args(*args, **kw):
    return (
     args, kw)


def parse_port_args(arg):
    if not type(arg) == tuple:
        return ((arg,), {})
    if not len(arg) == 2:
        return (arg, {})
    if not (type(arg[0]) == tuple and type(arg[1]) == dict):
        return (arg, {})
    return args(*arg[0], **arg[1])


def test_parse():
    print parse_port_args('item')
    print parse_port_args(('item', 'item2', 'item3'))
    print parse_port_args((('item', 'item2', 'item3'), {'key1': 'item1'}))


def caller():
    u"""
    下記ブログに掲載されていたコードを使わせてもらった
    http://d.hatena.ne.jp/Kazumi007/20090914/1252915940
    !!!EzPortの中で使ったらコンポーネントが解放されなくなったので、要注意!!!
    """
    try:
        framerecords = inspect.stack()
        framerecord = framerecords[2]
        frame = framerecord[0]
        arginfo = inspect.getargvalues(frame)
        if 'self' in arginfo.locals:
            return arginfo.locals['self']
        return
    finally:
        del frame

    return


class Dummy:
    pass


Wnone = weakref.ref(Dummy())