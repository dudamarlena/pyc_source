# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/harry/harry/harpy/harpy/har.py
# Compiled at: 2015-01-23 19:31:11
import json, os.path
from . import page
from . import entry

class Har(object):

    def __init__(self, f):
        if not isinstance(f, dict):
            if not os.path.isfile(f):
                raise IOError('%s does not exist.' % f)
            fp = open(f, 'r')
            self._raw = json.load(fp)
            fp.close()
        else:
            self._raw = f
        self.version = self._raw['log']['version']
        if not self.version:
            self.version = '1.1'
        else:
            if self.version not in ('1.1', '1.2'):
                raise NotImplementedError('%s is now a supported har version. ' + 'only 1.1. and 1.2 are supported' % self.version)
            self._creator = self._raw['log']['creator']
            if 'browser' in self._raw['log']:
                self._browser = self._raw['log']['browser']
            else:
                self._browser = {'name': '', 'version': '', 'comment': ''}
            self.pages = []
            for p in self._raw['log']['pages']:
                self.pages.append(page.Page(p))

            self.entries = []
            for e in self._raw['log']['entries']:
                self.entries.append(entry.Entry(e))

        if 'comment' in self._raw:
            self.comment = self._raw['comment']
        else:
            self.comment = ''

    @property
    def creator(self):
        _name = self._creator['name']
        _version = self._creator['version']
        if 'comment' in self._creator:
            _comment = self._creator['comment']
        else:
            _comment = ''
        return (
         _name, _version, _comment)

    @property
    def browser(self):
        _name = self._browser['name']
        _version = self._browser['version']
        if 'comment' in self._browser:
            _comment = self._browser['comment']
        else:
            _comment = ''
        return (
         _name, _version, _comment)

    def page_by_id(self, id):
        for p in self.pages:
            if p.id == id:
                return p

        raise KeyError('page with id %s not found' % id)

    def entries_by_page_ref(self, page_ref):
        entries = []
        for e in self.entries:
            if e.page_ref == page_ref:
                entries.append(e)

        if len(entries) == 0:
            raise KeyError('no entries found for page_ref %s' % page_ref)
        return entries