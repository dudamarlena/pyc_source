# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/jsoncomponent.py
# Compiled at: 2007-05-25 16:54:17
import minjson as json
from interfaces import IJSONReader, IJSONWriter
from zope.interface import implements
try:
    import cjson
    hasCJson = True
except ImportError:
    import logging
    logger = logging.getLogger()
    logger.log(logging.INFO, 'Using minjson only.  cjson is much faster and available at the cheese shop.  easy_install python-cjson')
    hasCJson = False

class JSONReader(object):
    """component implementing JSON reading"""
    __module__ = __name__
    implements(IJSONReader)

    def read(self, aString, encoding=None):
        if hasCJson:
            try:
                return cjson.decode(aString, True)
            except cjson.DecodeError:
                pass

        return json.read(aString, encoding)


class JSONWriter(object):
    """component implementing JSON writing"""
    __module__ = __name__
    implements(IJSONWriter)

    def write(self, anObject):
        if hasCJson:
            try:
                return unicode(cjson.encode(anObject))
            except cjson.EncodeError:
                pass

        return json.write(anObject)