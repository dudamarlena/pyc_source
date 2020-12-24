# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/completers.py
# Compiled at: 2016-05-04 07:56:27
from . import xmlutil

def choice(lst):
    """
    Static completion from a list
    """

    def completer(args):
        return lst

    return completer


null = choice([])

def call(fn, *fnargs):
    """
    Call the given function with the given arguments.
    The function has to return a list of completions.
    """

    def completer(args):
        return fn(*fnargs)

    return completer


def join(*fns):
    """
    Combine the output of several completers
    into a single completer.
    """

    def completer(args):
        ret = []
        for fn in fns:
            ret += fn(args)

        return ret

    return completer


booleans = choice(['yes', 'no', 'true', 'false', 'on', 'off'])

def resources(args):
    cib_el = xmlutil.resources_xml()
    if cib_el is None:
        return []
    else:
        nodes = xmlutil.get_interesting_nodes(cib_el, [])
        return [ x.get('id') for x in nodes if xmlutil.is_resource(x) ]


def primitives(args):
    cib_el = xmlutil.resources_xml()
    if cib_el is None:
        return []
    else:
        nodes = xmlutil.get_interesting_nodes(cib_el, [])
        return [ x.get('id') for x in nodes if xmlutil.is_primitive(x) ]


nodes = call(xmlutil.listnodes)
shadows = call(xmlutil.listshadows)