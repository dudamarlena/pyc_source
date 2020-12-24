# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/Data/MimeDict.py
# Compiled at: 2008-10-19 12:19:52


class MimeDict(dict):

    def __init__(self, **args):
        super(MimeDict, self).__init__(**args)
        self.insertionorder = []
        self.invalidSource = False
        for k in self.keys():
            if isinstance(self[k], list):
                if self[k] == []:
                    self.insertionorder.append(k)
                else:
                    for i in self[k]:
                        self.insertionorder.append(k)

            else:
                self.insertionorder.append(k)

        try:
            self['__BODY__']
        except KeyError:
            self['__BODY__'] = ''

    def __setitem__(self, i, y):
        super(MimeDict, self).__setitem__(i, y)
        if i != '__BODY__':
            self.insertionorder = [ x for x in self.insertionorder if x != i ]
            if isinstance(y, list):
                for _ in y:
                    self.insertionorder.append(i)

            else:
                self.insertionorder.append(i)

    def __delitem__(self, y):
        self.insertionorder = [ x for x in self.insertionorder if x != y ]
        super(MimeDict, self).__delitem__(y)

    def __str__(self):
        result = []
        seen = {}
        for k in self.insertionorder:
            if k == '__BODY__':
                continue
            try:
                seen[k] += 1
            except KeyError:
                seen[k] = 0

            if isinstance(self[k], list):
                try:
                    value = self[k][seen[k]]
                except IndexError:
                    value = ''

            else:
                value = self[k]
            result.append('%s: %s\r\n' % (k, value))

        result.append('\r\n')
        result.append(self['__BODY__'])
        resultString = ('').join(result)
        if self.invalidSource:
            return resultString[2:]
        else:
            return resultString

    def fromString(source):
        import sre
        result = {}
        insertionorder = []
        fail = False
        originalsource = source
        headervalueRE_s = '^([^: ]+[^:]*):( ?)([^\r]+)\r\n'
        continuationHeaderRE_s = '^( +[^\r\n]*)\r\n'
        match = sre.search(headervalueRE_s, source)
        inHeader = True
        key = None
        while True:
            if match:
                (key, spaces, value) = match.groups()
                if value == ' ' and not spaces:
                    value = ''
                try:
                    result[key].append(value)
                except KeyError:
                    result[key] = value
                except AttributeError:
                    result[key] = [
                     result[key], value]
                else:
                    insertionorder.append(key)
            if not match and key:
                match = sre.search(continuationHeaderRE_s, source)
                if not match:
                    break
                (value,) = match.groups()
                if isinstance(result[key], list):
                    result[key][(len(result[key]) - 1)] += '\r\n' + value
                else:
                    result[key] += '\r\n' + value
            if not match:
                break
            source = source[match.end():]
            match = sre.search(headervalueRE_s, source)

        if source[:2] == '\r\n':
            source = source[2:]
        else:
            source = originalsource
            result = {}
            insertionorder = []
            fail = True
        result['__BODY__'] = source
        md = MimeDict(**result)
        md.insertionorder = insertionorder
        md.invalidSource = fail
        return md

    fromString = staticmethod(fromString)