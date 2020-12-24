# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/transports/http/search.py
# Compiled at: 2016-10-17 19:06:50


class XMLSearchResult(object):
    fieldtags = [
     'str', 'int', 'date']

    def __init__(self):
        self.num_found = 0
        self.max_score = 0.0
        self.docs = []
        self.currdoc = None
        self.currfield = None
        self.currvalue = None
        return

    def start(self, tag, attrib):
        if tag == 'result':
            self.num_found = int(attrib['numFound'])
            self.max_score = float(attrib['maxScore'])
        elif tag == 'doc':
            self.currdoc = {}
        elif tag in self.fieldtags and self.currdoc is not None:
            self.currfield = attrib['name']
        return

    def end(self, tag):
        if tag == 'doc' and self.currdoc is not None:
            self.docs.append(self.currdoc)
            self.currdoc = None
        elif tag in self.fieldtags and self.currdoc is not None:
            if tag == 'int':
                self.currvalue = int(self.currvalue)
            self.currdoc[self.currfield] = self.currvalue
            self.currfield = None
            self.currvalue = None
        return

    def data(self, data):
        if self.currfield:
            data = data.rstrip()
            if self.currvalue:
                self.currvalue += data
            else:
                self.currvalue = data

    def close(self):
        return {'num_found': self.num_found, 'max_score': self.max_score, 'docs': self.docs}