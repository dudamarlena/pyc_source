# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pytracremote/exceptions.py
# Compiled at: 2014-01-02 16:11:05


class TracError(Exception):
    DESCRIPTION_MAPPER = {5: 'Trac already exists', 
       10: 'Password was not specified or generated', 
       12: "htpasswd can't create user", 
       13: 'User is in htpasswd', 
       20: 'list of users was not returned', 
       255: 'Unknown error, or ssh connection problem'}

    def __init__(self, code, errors=None, output=''):
        self.code = code
        self.errors = errors or []
        self.output = output
        if not isinstance(self.errors, (list, tuple)):
            self.errors = [
             self.errors]
        super(TracError, self).__init__(self.message())

    def message(self):
        if self.code:
            description = TracError.DESCRIPTION_MAPPER.get(self.code, 'Unknown code')
        else:
            description = ''
        if self.errors:
            return 'Code %d: %s\n%s' % (
             self.code, ('; ').join(self.errors), description)
        return 'Track error, code %d,\ndescription: %s,\nall output:\n%s' % (
         self.code, description, self.output)