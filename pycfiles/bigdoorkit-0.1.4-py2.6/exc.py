# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/bigdoorkit/exc.py
# Compiled at: 2010-08-06 20:48:51


class BigdoorError(Exception):
    """The base type of Bigdoor Exception"""
    pass


class MissingClient(BigdoorError):
    """Raised when there is no client available to service
    the request.
    """
    pass


class MissingParentDetails(BigdoorError):
    """Raised when there are certain attributes missing regarding a resource's
    parent.
    """
    pass


class PayloadError(BigdoorError):
    """Raised when there's a problem with the payload variable"""
    pass