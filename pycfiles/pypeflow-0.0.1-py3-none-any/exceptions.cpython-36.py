# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypeerassets/exceptions.py
# Compiled at: 2018-10-13 10:16:37
# Size of source mod 2**32: 1913 bytes
__doc__ = 'all custom exceptions should go here'

class EmptyP2THDirectory(Exception):
    """EmptyP2THDirectory"""
    pass


class P2THImportFailed(Exception):
    """P2THImportFailed"""
    pass


class InvalidDeckIssueModeCombo(Exception):
    """InvalidDeckIssueModeCombo"""
    pass


class UnsupportedNetwork(Exception):
    """UnsupportedNetwork"""
    pass


class InvalidDeckSpawn(Exception):
    """InvalidDeckSpawn"""
    pass


class InvalidDeckMetainfo(Exception):
    """InvalidDeckMetainfo"""
    pass


class InvalidDeckVersion(Exception):
    """InvalidDeckVersion"""
    pass


class InvalidDeckIssueMode(Exception):
    """InvalidDeckIssueMode"""
    pass


class DeckP2THImportError(Exception):
    """DeckP2THImportError"""
    pass


class InvalidCardTransferP2TH(Exception):
    """InvalidCardTransferP2TH"""
    pass


class CardVersionMismatch(Exception):
    """CardVersionMismatch"""
    pass


class CardNumberOfDecimalsMismatch(Exception):
    """CardNumberOfDecimalsMismatch"""
    pass


class InvalidCardIssue(Exception):
    """InvalidCardIssue"""
    pass


class RecieverAmountMismatch(Exception):
    """RecieverAmountMismatch"""
    pass


class InsufficientFunds(Exception):
    """InsufficientFunds"""
    pass


class InvalidNulldataOutput(Exception):
    """InvalidNulldataOutput"""
    pass


class InvalidVoutOrder(Exception):
    """InvalidVoutOrder"""
    pass


class OverSizeOPReturn(Exception):
    """OverSizeOPReturn"""
    pass


class InvalidVoteVersion(Exception):
    """InvalidVoteVersion"""
    pass


class InvalidVoteEndBlock(Exception):
    """InvalidVoteEndBlock"""
    pass