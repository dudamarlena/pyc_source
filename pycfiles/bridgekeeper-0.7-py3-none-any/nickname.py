# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/nickname.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = 'Parsers for bridge nicknames.\n\n.. py:module:: bridgedb.parse.nickname\n   :synopsis: Parsers for Tor bridge nicknames.\n\nbridgedb.parse.nicknames\n========================\n::\n\n  nicknames\n   |_ isValidRouterNickname - Determine if a nickname is according to spec\n..\n'
import logging, string

class InvalidRouterNickname(ValueError):
    """Router nickname doesn't follow tor-spec."""


def isValidRouterNickname(nickname):
    """Determine if a router's given nickname meets the specification.

    :param string nickname: An OR's nickname.
    :rtype: bool
    :returns: ``True`` if the nickname is valid, ``False`` otherwise.
    """
    ALPHANUMERIC = string.letters + string.digits
    try:
        if not 1 <= len(nickname) <= 19:
            raise InvalidRouterNickname('Nicknames must be between 1 and 19 characters: %r' % nickname)
        for letter in nickname:
            if letter not in ALPHANUMERIC:
                raise InvalidRouterNickname('Nicknames must only use [A-Za-z0-9]: %r' % nickname)

    except InvalidRouterNickname as error:
        logging.error(str(error))
    except TypeError:
        pass
    else:
        return True

    return False