# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.5/site-packages/bankpassweb/bpwexceptions.py
# Compiled at: 2007-12-03 09:03:33


class BPWException(Exception):
    """
        Base class for exceptions specific to the bankpassweb module.
        """


class BPWParmException(BPWException):
    pass


class BPWProtocolException(BPWException):
    pass


class BPWCryptoException(BPWException):
    pass