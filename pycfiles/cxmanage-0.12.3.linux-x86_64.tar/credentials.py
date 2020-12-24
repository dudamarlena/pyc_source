# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/credentials.py
# Compiled at: 2017-02-08 04:42:30
""" Definition of the Credentials class """

class Credentials(object):
    """ Container for login credentials """
    defaults = {'ecme_username': 'admin', 
       'ecme_password': 'admin', 
       'linux_username': 'user1', 
       'linux_password': '1Password'}

    def __init__(self, base=None, **kwargs):
        self.__dict__.update(self.defaults)
        if isinstance(base, Credentials):
            self.__dict__.update(vars(base))
        else:
            if base != None:
                self.__dict__.update(base)
            self.__dict__.update(kwargs)
            for key in self.__dict__:
                if key not in self.defaults:
                    raise ValueError('Invalid credential key: %s' % key)

        return

    def __repr__(self):
        return 'Credentials(%s)' % (', ').join('%r: %r' % (key, value) for key, value in vars(self).items())