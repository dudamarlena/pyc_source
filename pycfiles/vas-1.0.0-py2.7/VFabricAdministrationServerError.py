# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/VFabricAdministrationServerError.py
# Compiled at: 2012-11-01 11:35:36


class VFabricAdministrationServerError(Exception):
    """Raised to indicate a failure has occurred when communicating with the vFabric Administration Server

    :ivar int   code:       the HTTP error code returned by the server
    :ivar list  messages:   the error messages, if any, returned by the server
    """

    @property
    def code(self):
        return self.__code

    @property
    def messages(self):
        return self.__messages

    def __init__(self, messages, code=None):
        self.__messages = []
        if isinstance(messages, list):
            self.__messages.extend(messages)
        else:
            self.messages.append(messages)
        self.__code = code

    def __str__(self):
        return ('{}: {}').format(self.code, (', ').join(self.messages))

    def __repr__(self):
        return ('{}([{}], code={})').format(self.__class__.__name__, (',').join(map(lambda x: repr(x), self.messages)), self.code)