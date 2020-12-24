# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/djubby/uri.py
# Compiled at: 2010-04-27 11:00:35
from configuration import Configuration
from rdflib import URIRef
import urllib

class URI:

    def __init__(self, uri):
        conf = Configuration()
        if type(uri) == URIRef:
            self.uri = unicode(uri)
        else:
            self.uri = uri
        self.label = uri2curie(self.uri, conf.data.namespaces())
        self.url = uri2url(self.uri)

    def __str__(self):
        return self.uri

    def __cmp__(self, o):
        return cmp(self.uri, o.uri)

    def __eq__(self, o):
        return self.uri.__eq__(o.uri)

    def __hash__(self):
        return self.uri.__hash__()


def str2uri(uri):
    if type(uri) == str or type(uri) == unicode:
        return URIRef(uri)
    else:
        return uri


def uri2str(uri):
    if type(uri) == URIRef(uri):
        uri = unicode(uri)
    return urllib.unquote(uri)


def quote(uri):
    uri = uri2str(uri)
    conf = Configuration()
    fixUnescapedCharacters = conf.get_value('fixUnescapedCharacters')
    for c in fixUnescapedCharacters:
        uri = uri.replace(c, urllib.quote(c))

    return uri


def uri2curie(uri, namespaces):
    (url, fragment) = splitUri(uri)
    for (prefix, ns) in namespaces:
        if unicode(ns) == url:
            return '%s:%s' % (prefix, fragment)

    return uri


def splitUri(uri):
    if '#' in uri:
        splitted = uri.split('#')
        return ('%s#' % splitted[0], splitted[1])
    else:
        splitted = uri.split('/')
        return (('/').join(splitted[:-1]) + '/', splitted[(-1)])


def uri2url(uri):
    conf = Configuration()
    datasetBase = conf.get_value('datasetBase')
    webBase = conf.get_value('webBase')
    return uri.replace(datasetBase, webBase)