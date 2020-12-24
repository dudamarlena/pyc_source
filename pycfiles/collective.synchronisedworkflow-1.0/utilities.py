# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/sylvester/browser/utilities.py
# Compiled at: 2009-06-29 15:53:49
import twitter
from zope.interface import implements
from interfaces import ITwitterAPI

def wrapper(func_name, username, password, *args, **kwargs):
    api = twitter.Api(username, password)
    func = getattr(api, func_name)
    return func(*args, **kwargs)


class TwitterAPI(object):
    """
    Abstract python-twitter API. This class effectively modifies
    every callable method signature in python-twitter to expect
    username and password as parameters.
    """
    __module__ = __name__
    implements(ITwitterAPI)
    __callable_functions__ = []

    def __getattr__(self, name):
        if hasattr(twitter.Api, name):
            attr = getattr(twitter.Api, name)
            if callable(attr):
                if name not in self.__callable_functions__:
                    self.__callable_functions__.append(name)
                return lambda username, password, *args, **kwargs: wrapper(name, username, password, *args, **kwargs)
            else:
                return attr
        return getattr(object, name)