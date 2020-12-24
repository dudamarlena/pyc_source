# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/beanstalk/errors.py
# Compiled at: 2015-07-11 09:52:37


class FailureError(Exception):
    pass


class JobError(FailureError):
    pass


class BeanStalkError(Exception):
    pass


class ProtoError(BeanStalkError):
    pass


class ServerError(BeanStalkError):
    pass


class NotConnected(BeanStalkError):
    pass


class OutOfMemory(ServerError):
    pass


class InternalError(ServerError):
    pass


class Draining(ServerError):
    pass


class BadFormat(ProtoError):
    pass


class UnknownCommand(ProtoError):
    pass


class ExpectedCrlf(ProtoError):
    pass


class JobTooBig(ProtoError):
    pass


class NotFound(ProtoError):
    pass


class NotIgnored(ProtoError):
    pass


class DeadlineSoon(ProtoError):
    pass


class UnexpectedResponse(ProtoError):
    pass


def checkError(linestr):
    """Note, this will throw an error internally for every case that is a
    response that is NOT an error response, and that error will be caught,
    and checkError will return happily.

    In the case that an error was returned by beanstalkd, an appropriate error
    will be raised"""
    try:
        errname = ('').join([ x.capitalize() for x in linestr.split('_') ])
        err = eval(errname)('Server returned: %s' % (linestr,))
    except Exception as e:
        return

    raise err