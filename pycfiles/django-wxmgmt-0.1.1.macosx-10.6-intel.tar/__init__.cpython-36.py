# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lidayan/pyenv/python3/pypi-distribute/lib/python3.6/site-packages/wxmgmt/__init__.py
# Compiled at: 2018-02-25 20:14:49
# Size of source mod 2**32: 1298 bytes
import logging, hashlib, xml.sax
logger = logging.getLogger(__name__)

def signature(data, _type='sha1', key=None):
    keys = data.keys()
    keys.sort()
    tmpstr = '&'.join('%s=%s' % (k, data[k]) for k in keys)
    if key:
        tmpstr += '&key=' + key
    else:
        logger.debug('signature params string %s %s' % (_type, tmpstr))
        tmpstr = tmpstr
        if _type == 'md5':
            hash_md5 = hashlib.md5(tmpstr.encode('utf-8'))
            sign = hash_md5.hexdigest()
        else:
            hash_sha1 = hashlib.sha1(tmpstr)
        sign = hash_sha1.hexdigest()
    logger.debug('signature %s %s' % (_type, sign))
    return sign


def parsexml(xmlstring):

    class XMLHandler(xml.sax.handler.ContentHandler):

        def __init__(self):
            self.buffer = ''
            self.mapping = {}

        def startElement(self, name, attributes):
            self.buffer = ''

        def characters(self, data):
            self.buffer += data

        def endElement(self, name):
            self.mapping[name] = self.buffer

        def getDict(self):
            return self.mapping

    try:
        xmlh = XMLHandler()
        xml.sax.parseString(xmlstring, xmlh)
        return xmlh.getDict()
    except:
        logger.error('parse xmlstring(%s) failed' % xmlstring)
        return