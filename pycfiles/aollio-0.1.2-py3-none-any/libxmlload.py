# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aojtools/libxmlload.py
# Compiled at: 2014-11-04 09:55:25
import urllib
from xml.etree.ElementTree import *

class Node(object):

    def __init__(self, name, info):
        self.__dict__['_info'] = info
        self.__dict__['_name'] = name

    def __getattr__(self, name):
        if name in self.__dict__['_info']:
            return self.__dict__['_info'][name]
        return self.__dict__[name]

    def __setattr__(self, name, value):
        self.__dict__['_info'][name] = value

    def __iter__(self):
        return self._info.iteritems()

    def __repr__(self):
        args = (self._name, (',').join(self._info.keys()))
        return '<%s keys=%s>' % args


def xmltrans(xmlnode):
    node = Node(xmlnode.tag, {})
    for child in xmlnode:
        key = child.tag
        if len(child) == 0:
            val = child.text
            if val is not None:
                val = val.strip()
            assign(node._info, key, val)
        else:
            assign(node._info, key, xmltrans(child))

    return node


def assign(info, key, value):
    if key in info:
        if isinstance(info[key], list):
            info[key].append(value)
        else:
            info[key] = [
             info[key], value]
    else:
        info[key] = value


def urlopen(url):
    conn = urllib.urlopen(url)
    xmlstr = conn.read()
    xmldoc = fromstring(xmlstr)
    otree = xmltrans(xmldoc)
    return otree


def parse(filepath):
    fobj = open(filepath)
    xmlstr = fobj.read()
    xmldoc = fromstring(xmlstr)
    otree = xmltrans(xmldoc)
    return otree