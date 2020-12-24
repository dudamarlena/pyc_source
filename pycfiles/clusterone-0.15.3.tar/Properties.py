# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/data/projects/gluu/cluster-mgr/clustermgr/core/Properties.py
# Compiled at: 2020-05-09 08:47:08
__doc__ = '\nA Python replacement for java.util.Properties class\nThis is modelled as closely as possible to the Java original.\n\nCreated - Anand B Pillai <abpillai@gmail.com>    \n'
import sys, os, re, time

class IllegalArgumentException(Exception):

    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.msg = msg

    def __str__(self):
        s = 'Exception at line number %d => %s' % (self.lineno, self.msg)
        return s


class Properties(object):
    """ A Python replacement for java.util.Properties """

    def __init__(self, props=None):
        self._props = {}
        self._origprops = {}
        self._keymap = {}
        self.othercharre = re.compile('(?<!\\\\)(\\s*\\=)|(?<!\\\\)(\\s*\\:)')
        self.othercharre2 = re.compile('(\\s*\\=)|(\\s*\\:)')
        self.bspacere = re.compile('\\\\(?!\\s$)')

    def __str__(self):
        s = '{'
        for key, value in self._props.items():
            s = ('').join((s, key, '=', value, ', '))

        s = ('').join((s[:-2], '}'))
        return s

    def __parse(self, lines):
        """ Parse a list of lines and create
        an internal property dictionary """
        lineno = 0
        i = iter(lines)
        for line in i:
            lineno += 1
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            escaped = False
            sepidx = -1
            flag = 0
            m = self.othercharre.search(line)
            if m:
                first, last = m.span()
                start, end = 0, first
                flag = 1
                wspacere = re.compile('(?<![\\\\\\=\\:])(\\s)')
            else:
                if self.othercharre2.search(line):
                    wspacere = re.compile('(?<![\\\\])(\\s)')
                start, end = 0, len(line)
            m2 = wspacere.search(line, start, end)
            if m2:
                first, last = m2.span()
                sepidx = first
            else:
                if m:
                    first, last = m.span()
                    sepidx = last - 1
                while line[(-1)] == '\\':
                    nextline = i.next()
                    nextline = nextline.strip()
                    lineno += 1
                    line = line[:-1] + nextline

            if sepidx != -1:
                key, value = line[:sepidx], line[sepidx + 1:]
            else:
                key, value = line, ''
            self.processPair(key, value)

    def processPair(self, key, value):
        """ Process a (key, value) pair """
        oldkey = key
        oldvalue = value
        keyparts = self.bspacere.split(key)
        strippable = False
        lastpart = keyparts[(-1)]
        if lastpart.find('\\ ') != -1:
            keyparts[-1] = lastpart.replace('\\', '')
        elif lastpart and lastpart[(-1)] == ' ':
            strippable = True
        key = ('').join(keyparts)
        if strippable:
            key = key.strip()
            oldkey = oldkey.strip()
        oldvalue = self.unescape(oldvalue)
        value = self.unescape(value)
        self._props[key] = value.strip()
        if self._keymap.has_key(key):
            oldkey = self._keymap.get(key)
            self._origprops[oldkey] = oldvalue.strip()
        else:
            self._origprops[oldkey] = oldvalue.strip()
            self._keymap[key] = oldkey

    def escape(self, value):
        newvalue = value.replace(':', '\\:')
        newvalue = newvalue.replace('=', '\\=')
        return newvalue

    def unescape(self, value):
        newvalue = value.replace('\\:', ':')
        newvalue = newvalue.replace('\\=', '=')
        return newvalue

    def load(self, stream):
        """ Load properties from an open file stream """
        try:
            lines = stream.readlines()
            self.__parse(lines)
        except IOError as e:
            raise

    def getProperty(self, key):
        """ Return a property for the given key """
        return self._props.get(key, '')

    def setProperty(self, key, value):
        """ Set the property for the given key """
        if type(key) is str and type(value) is str:
            self.processPair(key, value)
        else:
            raise TypeError, 'both key and value should be strings!'

    def propertyNames(self):
        """ Return an iterator over all the keys of the property
        dictionary, i.e the names of the properties """
        return self._props.keys()

    def list(self, out=sys.stdout):
        """ Prints a listing of the properties to the
        stream 'out' which defaults to the standard output """
        out.write('-- listing properties --\n')
        for key, value in self._props.items():
            out.write(('').join((key, '=', value, '\n')))

    def store(self, out, header=''):
        """ Write the properties list to the stream 'out' along
        with the optional 'header' """
        try:
            out.write(('').join(('#', header, '\n')))
            tstamp = time.strftime('%a %b %d %H:%M:%S %Z %Y', time.localtime())
            out.write(('').join(('#', tstamp, '\n')))
            for prop, val in self._origprops.items():
                out.write(('').join((prop, '=', self.escape(val), '\n')))

        except IOError as e:
            raise

    def getPropertyDict(self):
        return self._props

    def __getitem__(self, name):
        """ To support direct dictionary like access """
        return self.getProperty(name)

    def __setitem__(self, name, value):
        """ To support direct dictionary like access """
        self.setProperty(name, value)

    def __getattr__(self, name):
        """ For attributes not found in self, redirect
        to the properties dictionary """
        try:
            return self.__dict__[name]
        except KeyError:
            if hasattr(self._props, name):
                return getattr(self._props, name)

    def __delitem__(self, name):
        if name in self._props:
            self._props.pop(name)
        if name in self._origprops:
            self._origprops.pop(name)
        if name in self._keymap:
            self._keymap.pop(name)


if __name__ == '__main__':
    p = Properties()
    p.load(open('test2.properties'))
    p.list()
    print p
    print p.items()
    print p['name3']
    p['name3'] = 'changed = value'
    print p['name3']
    p['new key'] = 'new value'
    p.store(open('test2.properties', 'w'))