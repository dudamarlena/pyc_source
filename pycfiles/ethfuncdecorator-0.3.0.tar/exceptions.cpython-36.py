# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/exceptions.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 2290 bytes
import datetime, time

class BadFunctionCallOutput(Exception):
    __doc__ = '\n    We failed to decode ABI output.\n\n    Most likely ABI mismatch.\n    '


class BlockNumberOutofRange(Exception):
    __doc__ = '\n    block_identifier passed does not match known block.\n    '


class CannotHandleRequest(Exception):
    __doc__ = '\n    Raised by a provider to signal that it cannot handle an RPC request and\n    that the manager should proceed to the next provider.\n    '


class InvalidAddress(ValueError):
    __doc__ = '\n    The supplied address does not have a valid checksum, as defined in EIP-55\n    '


class NameNotFound(ValueError):
    __doc__ = '\n    Raised when a caller provides an Ethereum Name Service name that\n    does not resolve to an address.\n    '


class StaleBlockchain(Exception):
    __doc__ = '\n    Raised by the stalecheck_middleware when the latest block is too old.\n    '

    def __init__(self, block, allowable_delay):
        last_block_date = datetime.datetime.fromtimestamp(block.timestamp).strftime('%c')
        message = 'The latest block, #%d, is %d seconds old, but is only allowed to be %d s old. The date of the most recent block is %s. Continue syncing and try again...' % (
         block.number, time.time() - block.timestamp, allowable_delay, last_block_date)
        super().__init__(message, block, allowable_delay)

    def __str__(self):
        return self.args[0]


class UnhandledRequest(Exception):
    __doc__ = "\n    Raised by the manager when none of it's providers responds to a request.\n    "


class MismatchedABI(Exception):
    __doc__ = '\n    Raised when an ABI does not match with supplied parameters, or when an\n    attempt is made to access a function/event that does not exist in the ABI.\n    '


class FallbackNotFound(Exception):
    __doc__ = "\n    Raised when fallback function doesn't exist in contract.\n    "


class ValidationError(Exception):
    __doc__ = '\n    Raised when a supplied value is invalid.\n    '


class NoABIFunctionsFound(AttributeError):
    __doc__ = "\n    Raised when an ABI doesn't contain any functions.\n    "


class NoABIEventsFound(AttributeError):
    __doc__ = "\n    Raised when an ABI doesn't contain any events.\n    "