# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boo_box/boo_box.py
# Compiled at: 2009-06-12 10:08:55
import urllib, sys

class Box(object):
    __module__ = __name__

    def __init__(self, aff, uid):
        """ You should suply your affiliate and your user id"""
        self.limit = 6
        self.aff = aff
        self.uid = uid

    def _do_get(self, tags, limit):
        """
        This will make the real API call
        API format: http://boo-box.com/api/format:formato/aff:ecommid/uid:userid/tags:searchterms/limit:number
        docs: http://www.boo-box.com/blog/br/2009/boo-api-nova-versao/
        """
        import sys
        caller = sys._getframe(1).f_code.co_name
        method = caller.split('_')[(-1)]
        tags = urllib.quote(tags)
        url_base = 'http://boo-box.com/api/format:%(method)s/aff:%(aff)s/uid:%(uid)s/tags:%(tags)s/limit:%(limit)s'
        url = url_base % {'method': method, 'aff': self.aff, 'uid': self.uid, 'tags': tags, 'limit': limit}
        content = urllib.urlopen(url).read()
        return content.strip()

    def _do_get_xml(self, tags, limit):
        content = self._do_get(tags, limit)
        return content

    def _do_get_json(self, tags, limit):
        content = self._do_get(tags, limit)
        return content

    def _do_get_object(self, tags, limit):
        content = self._do_get_json(tags, limit)
        content = content.replace('jsonBooboxApi(', '')
        import simplejson
        return simplejson.loads(content[:-2])

    def get(self, format, tags, limit=6):
        """get the response for your tags. Three formats supported by now:
        object, that returns a dict, json, that returns a json string
        and XML, that returns XML"""
        handler = getattr(self, '_do_get_%s' % format.lower(), None)
        if handler:
            return handler(tags, limit)
        else:
            raise NotImplementedError
        return