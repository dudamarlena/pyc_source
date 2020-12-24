# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/grakopp/exceptions.py
# Compiled at: 2014-08-01 20:39:34


class GrakoException(Exception):

    def __init__(self, msg):
        super(GrakoException, self).__init__(msg)


class ParseError(GrakoException):

    def __init__(self, msg):
        super(ParseError, self).__init__(msg)


class FailedParseBase(ParseError):

    def __init__(self, msg):
        super(FailedParseBase, self).__init__(msg)
        self.msg = msg

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.msg))

    @property
    def message(self):
        return self.msg


class FailedParse(FailedParseBase):

    def __init__(self, msg):
        super(FailedParse, self).__init__(msg)


class FailedToken(FailedParseBase):

    def __init__(self, msg):
        super(FailedToken, self).__init__(msg)

    @property
    def message(self):
        return 'expecting %s' % repr(self.msg).lstrip('u')


class FailedPattern(FailedParseBase):

    def __init__(self, msg):
        super(FailedPattern, self).__init__(msg)

    @property
    def message(self):
        return 'expecting %s' % repr(self.msg).lstrip('u')


class FailedLookahead(FailedParseBase):

    def __init__(self, msg):
        super(FailedLookahead, self).__init__(msg)

    @property
    def message(self):
        return 'failed lookahead'