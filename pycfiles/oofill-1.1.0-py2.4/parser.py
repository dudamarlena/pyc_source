# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/oofill/parser.py
# Compiled at: 2010-06-11 04:48:22
"""
$Id$
"""
__author__ = 'Jean-Nicolas Bès <contact@atreal.net>'
__docformat__ = 'plaintext'
__licence__ = 'GPL'
import os
from os.path import isfile, exists, dirname
import StringIO, zipfile
from xml.sax import ContentHandler
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces

class LogWrapper:
    __module__ = __name__

    def __init__(self, fileobj):
        self.fileobj = fileobj

    def write(self, data):
        print 'WROTE', repr(data)
        return self.fileobj.write(data)

    def seek(self, *args):
        print 'SEEK', args
        return self.fileobj.seek(*args)

    def read(self, *args):
        print 'READ', args
        return self.fileobj.read(*args)


class Finder(ContentHandler):
    __module__ = __name__

    def __init__(self, newContent, view, protected):
        self.newContent = newContent
        self.view = view
        self.level = 0
        self.inprotected = []
        self.replace = False
        self.protected = protected

    def printOut(self, line):
        print '  ' * (self.level + 2) + line

    def startElement(self, name, attrs):
        if name == 'text:section' and attrs.get('text:protected', not self.protected) and attrs.get('text:name', None).startswith('replace'):
            self.replace = True
        if not (self.inprotected or self.replace):
            newTag = '<' + name
            for (key, val) in attrs._attrs.items():
                newTag += ' %s="%s"' % (key, val)

            newTag += '>'
            self.newContent.write(newTag.encode('utf-8'))
        if name == 'text:section' and attrs.get('text:protected', not self.protected):
            self.inprotected.append(self.level)
            sectname = attrs._attrs['text:name']
            getter = getattr(self.view, sectname, None)
            if getter is None:
                self.inprotected.pop()
            else:
                text = getter().encode('utf-8')
                self.newContent.write(text)
        self.level += 1
        return

    def characters(self, data):
        if not self.inprotected:
            self.newContent.write(data.encode('utf-8'))

    def endElement(self, name):
        self.level -= 1
        if self.inprotected and self.level == self.inprotected[(-1)]:
            self.inprotected.pop()
        if not self.inprotected:
            if self.replace:
                self.replace = False
                return
            newTag = '</' + name
            newTag += '>'
            self.newContent.write(newTag.encode('utf-8'))


class OOFill:
    """
    """
    __module__ = __name__

    def __init__(self, odt):
        if isinstance(odt, (str, unicode)) and exists(odt):
            odtfile = file(odt, 'r')
        else:
            if isinstance(odt, (file, StringIO.StringIO)):
                odtfile = odt
            odtfile = StringIO.StringIO()
            for block in odt:
                odtfile.write(block)

        self.odtzip = zipfile.ZipFile(odtfile, 'r')

    def render(self, view, outfile=None, protected=True):
        if isinstance(outfile, (file, StringIO.StringIO)):
            newodtfile = outfile
        elif outfile and exists(dirname(outfile)):
            newodtfile = file(outfile, 'w+')
        else:
            newodtfile = StringIO.StringIO()
        newodtzip = zipfile.ZipFile(newodtfile, 'w')
        for innerfile in self.odtzip.namelist():
            if innerfile == 'content.xml':
                continue
            newodtzip.writestr(innerfile, self.odtzip.read(innerfile))

        content = StringIO.StringIO(self.odtzip.read('content.xml'))
        self.odtzip.close()
        newContent = StringIO.StringIO()
        newContent.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        parser = make_parser()
        dh = Finder(newContent, view, protected)
        parser.setContentHandler(dh)
        parser.parse(content)
        newContent.seek(0)
        newodtzip.writestr('content.xml', newContent.read())
        newodtzip.close()
        newodtfile.seek(0)
        return newodtfile


if __name__ == '__main__':
    import unittest
    TestRunner = unittest.TextTestRunner
    suite = unittest.TestSuite()
    if os.path.exists('tests'):
        tests = os.listdir('tests')
        tests = [ n[:-3] for n in tests if n.startswith('test') if n.endswith('.py') ]
    else:
        tests = ()
    for test in tests:
        print 'testing', test
        m = __import__('tests.' + test, None, None, [1])
        if hasattr(m, 'test_suite'):
            suite.addTest(m.test_suite())

    TestRunner().run(suite)
    print 'Tests done.'