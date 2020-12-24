# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/updater4pyi/upd_sign.py
# Compiled at: 2013-12-20 07:08:28


class UpdateSignatureVerifyer(object):

    def __init__(self, *args, **kwargs):
        pass

    def verify(self, update_info, fn):
        raise NotImplementedError


class UpdateNoSignatureVerifyer(UpdateSignatureVerifyer):

    def verify(self, update_info, fn):
        return True