# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypeerassets/exceptions.py
# Compiled at: 2018-10-13 10:16:37
# Size of source mod 2**32: 1913 bytes
"""all custom exceptions should go here"""

class EmptyP2THDirectory(Exception):
    __doc__ = 'no transactions on this P2TH directory'


class P2THImportFailed(Exception):
    __doc__ = 'Importing of PeerAssets P2TH privkeys failed.'


class InvalidDeckIssueModeCombo(Exception):
    __doc__ = 'When verfiying deck issue_mode combinations.'


class UnsupportedNetwork(Exception):
    __doc__ = 'This network is not suppored by pypeerassets.'


class InvalidDeckSpawn(Exception):
    __doc__ = 'Invalid deck_spawn, deck is not properly tagged.'


class InvalidDeckMetainfo(Exception):
    __doc__ = 'Deck metainfo incomplete, deck must have a name.'


class InvalidDeckVersion(Exception):
    __doc__ = 'Deck version mistmatch.'


class InvalidDeckIssueMode(Exception):
    __doc__ = 'Deck Issue mode is wrong.'


class DeckP2THImportError(Exception):
    __doc__ = 'When Deck P2TH import goes wrong.'


class InvalidCardTransferP2TH(Exception):
    __doc__ = 'card_transfer does not pay to deck p2th in vout[0]'


class CardVersionMismatch(Exception):
    __doc__ = 'card_transfers version must match deck.version'


class CardNumberOfDecimalsMismatch(Exception):
    __doc__ = 'card_tranfer number of decimals does not match deck rules.'


class InvalidCardIssue(Exception):
    __doc__ = "deck issuer can't issue cards to the deck issuing address"


class RecieverAmountMismatch(Exception):
    __doc__ = 'card_transfer list of recievers is not equal to list of amounts'


class InsufficientFunds(Exception):
    __doc__ = 'this address does not have enough assigned UTXOs'


class InvalidNulldataOutput(Exception):
    __doc__ = 'mallformed OP_RETURN transaction output.'


class InvalidVoutOrder(Exception):
    __doc__ = 'mallformed vout sequence'


class OverSizeOPReturn(Exception):
    __doc__ = 'op_return size is exceeding the maximum size allowed by this network.'


class InvalidVoteVersion(Exception):
    __doc__ = 'invalid Vote version'


class InvalidVoteEndBlock(Exception):
    __doc__ = 'Invalid Vote end block'