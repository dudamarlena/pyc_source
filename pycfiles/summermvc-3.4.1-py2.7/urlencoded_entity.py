# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/urlencoded_entity.py
# Compiled at: 2018-05-30 22:49:04
__all__ = [
 'URLEncodedEntityParser']
__authors__ = ['Tim Chow']
from urllib import unquote

class URLEncodedEntityParser(object):

    def __init__(self, content):
        self._content = content
        self._arguments = self.__parse()

    def __parse(self):
        arguments = {}
        for item in self._content.split('&'):
            pair = item.split('=', 1)
            if len(pair) != 2:
                continue
            arguments[unquote(pair[0])] = unquote(pair[1])

        return arguments

    @property
    def arguments(self):
        return self._arguments


if __name__ == '__main__':
    from urllib import quote

    def urlencode(arguments):
        return ('&').join([ '%s=%s' % (quote(k), quote(v)) for k, v in arguments.iteritems()
                          ])


    url_encoded_string = urlencode({'a': '!@#$', 'b': '% ^ & *'})
    print 'url_encoded_string: %s' % url_encoded_string
    entity = URLEncodedEntityParser(url_encoded_string)
    print entity.arguments