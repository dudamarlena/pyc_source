# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/nickname.py
# Compiled at: 2015-11-05 10:40:17
"""Parsers for bridge nicknames.

.. py:module:: bridgedb.parse.nickname
   :synopsis: Parsers for Tor bridge nicknames.

bridgedb.parse.nicknames
========================
::

  nicknames
   |_ isValidRouterNickname - Determine if a nickname is according to spec
..
"""
import logging, string

class InvalidRouterNickname(ValueError):
    """Router nickname doesn't follow tor-spec."""
    pass


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