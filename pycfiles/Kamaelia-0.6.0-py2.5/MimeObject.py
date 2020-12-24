# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/Data/MimeObject.py
# Compiled at: 2008-10-19 12:19:52


class mimeObject(object):
    """Accepts a Mime header represented as a dictionary object, and a body
   as a string. Provides a way of handling as a coherant unit.
   ATTRIBUTES:
      header : dictionary. (keys == fields, values = field values)
      body : body of MIME object
   """

    def __init__(self, header={}, body='', preambleLine=None):
        """Creates a mimeObect"""
        self.header = dict(header)
        self.body = body
        if preambleLine:
            self.preambleLine = preambleLine
        else:
            self.preambleLine = None
        return

    def __str__(self):
        """Dumps the Mime object in printable format - specifically as a formatted
      mime object"""
        result = ''
        for anItem in self.header.iteritems():
            (key, (origkey, value)) = anItem
            result = result + origkey + ': ' + value + '\n'

        result = result + '\n'
        result = result + self.body
        if self.preambleLine:
            result = str(self.preambleLine) + '\n' + result + self.body
        return result


if __name__ == '__main__':
    print 'No test harness as yet'
    print 'This file was spun out from the Mime request parsing component'