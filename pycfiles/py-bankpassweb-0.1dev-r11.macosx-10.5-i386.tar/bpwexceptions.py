# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.5/site-packages/bankpassweb/bpwexceptions.py
# Compiled at: 2007-12-03 09:03:33


class BPWException(Exception):
    """
        Base class for exceptions specific to the bankpassweb module.
        """
    pass


class BPWParmException(BPWException):
    pass


class BPWProtocolException(BPWException):
    pass


class BPWCryptoException(BPWException):
    pass