# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/stripogram/html2safehtml.py
# Compiled at: 2008-11-27 09:36:34
from HTMLParser import HTMLParser, HTMLParseError, piclose, charref, entityref
from string import lower, find

class HTML2SafeHTML(HTMLParser):
    __module__ = __name__
    can_close = [
     'li', 'p', 'dd', 'dt', 'option']
    never_close = ['br', 'wbr', 'hr', 'input', 'isindex', 'base', 'meta', 'img']

    def __init__(self, valid_tags):
        HTMLParser.__init__(self)
        self.valid_tags = valid_tags
        self.result = ''
        self.openTags = []

    def end_tag(self, tag):
        self.result = '%s</%s>' % (self.result, tag)

    def handle_data(self, data):
        if data:
            self.result = self.result + data

    def handle_charref(self, name):
        self.result = '%s&#%s;' % (self.result, name)

    from htmlentitydefs import entitydefs

    def handle_entityref(self, name):
        if self.entitydefs.has_key(name):
            amp = '&'
        else:
            amp = '&amp;'
        self.result = '%s%s%s;' % (self.result, amp, name)

    def handle_starttag(self, tag, attrs):
        """ Delete all tags except for legal ones """
        if tag in self.valid_tags:
            self.result = self.result + '<' + tag
            for (k, v) in attrs:
                if v is None:
                    self.result += ' ' + k
                elif lower(k[0:2]) != 'on' and lower(v[0:10]) != 'javascript':
                    self.result += ' %s="%s"' % (k, v)

            if tag not in self.never_close:
                self.openTags.append(tag)
            self.result = self.result + '>'
        return

    def handle_endtag(self, tag):
        try:
            while tag != self.openTags[(-1)] and tag in self.openTags:
                if self.openTags[(-1)] in self.can_close:
                    self.openTags.pop()
                else:
                    self.end_tag(self.openTags.pop())

            if tag == self.openTags[(-1)]:
                self.end_tag(self.openTags.pop())
        except IndexError:
            pass

    def cleanup(self):
        """ Append missing closing tags """
        while self.openTags:
            tag = self.openTags.pop()
            if tag not in self.can_close:
                self.end_tag(tag)

    def parse_starttag(self, i):
        try:
            return HTMLParser.parse_starttag(self, i)
        except HTMLParseError:
            try:
                return piclose.search(self.rawdata, i).end()
            except AttributeError:
                return -1

    def parse_endtag(self, i):
        try:
            return HTMLParser.parse_endtag(self, i)
        except HTMLParseError:
            try:
                return piclose.search(self.rawdata, i).end()
            except:
                return -1

    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        newdata = ''
        while i < n:
            j = find(rawdata, '&', i)
            if j == -1:
                break
            newdata = newdata + rawdata[i:j]
            if charref.match(rawdata, j) or entityref.match(rawdata, j):
                newdata = newdata + '&'
            else:
                newdata = newdata + '&amp;'
            i = j + 1

        self.rawdata = newdata + rawdata[i:]
        try:
            return HTMLParser.goahead(self, end)
        except HTMLParseError:
            pass