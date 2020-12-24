# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/APNSWrapper/apnsexceptions.py
# Compiled at: 2010-04-24 05:09:37


class APNSNotImplementedMethod(Exception):
    """
    This exception raised when you method of ssl context
    was not implemented. Only for testing purposes.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSNoSSLContextFound(Exception):
    """
    This exception raised when you haven't available SSL context
    in your environment
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSNoCommandFound(Exception):
    """
    This exception raised when you try to find SSL executable but
    it will not be found in your PATH
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSTypeError(Exception):
    """
    This exception raised when you try to add an argument with
    unexpected type.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSPayloadLengthError(Exception):
    """
    If length of payload more than 256 (by APNS specification) generate this exception
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSCertificateNotFoundError(Exception):
    """
    This exception raised when you try to add an argument with
    certificate file but certificate not found.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSValueError(Exception):
    """
    This exception raised when you try to add value to method
    which expect concrete type of argument.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSUndefinedDeviceToken(Exception):
    """
    This exception raised when you try to send notifications by wrapper
    but one of notification don't have deviceToken.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APNSConnectionError(Exception):
    """
    This is a simple exception which generated when
    you can't connect to APNS service or your
    certificate is not valid.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)