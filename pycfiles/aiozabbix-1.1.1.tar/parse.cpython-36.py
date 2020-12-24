# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aioyoyo\oyoyo\parse.py
# Compiled at: 2017-03-02 00:29:48
# Size of source mod 2**32: 3575 bytes
import logging, sys
from .ircevents import *
if sys.version_info < (3, ):

    class bytes(object):

        def __new__(self, b='', encoding='utf8'):
            return str(b)


def parse_raw_irc_command(element):
    """
    This function parses a raw irc command and returns a tuple
    of (prefix, command, args).
    The following is a psuedo BNF of the input text:

    <message>  ::= [':' <prefix> <SPACE> ] <command> <params> <crlf>
    <prefix>   ::= <servername> | <nick> [ '!' <user> ] [ '@' <host> ]
    <command>  ::= <letter> { <letter> } | <number> <number> <number>
    <SPACE>    ::= ' ' { ' ' }
    <params>   ::= <SPACE> [ ':' <trailing> | <middle> <params> ]

    <middle>   ::= <Any *non-empty* sequence of octets not including SPACE
                   or NUL or CR or LF, the first of which may not be ':'>
    <trailing> ::= <Any, possibly *empty*, sequence of octets not including
                     NUL or CR or LF>

    <crlf>     ::= CR LF
    """
    if isinstance(element, str):
        element = element.encode()
    else:
        parts = element.strip().split(' '.encode())
        if parts[0].startswith(':'.encode()):
            prefix = parts[0][1:]
            command = parts[1]
            args = parts[2:]
        else:
            prefix = None
            command = parts[0]
            args = parts[1:]
        if command.isdigit():
            try:
                command = numeric_events[command.zfill(3)]
            except KeyError:
                logging.warn('unknown numeric event %s' % command)

        command = command.lower()
        if args[0].startswith(':'.encode()):
            args = [
             ' '.encode().join(args)[1:]]
        else:
            for idx, arg in enumerate(args):
                if arg.startswith(':'.encode()):
                    args = args[:idx] + [' '.encode().join(args[idx:])[1:]]
                    break

    return (
     prefix, command, args)


def parse_nick(name):
    """ parse a nickname and return a tuple of (nick, mode, user, host)

    <nick> [ '!' [<mode> = ] <user> ] [ '@' <host> ]
    """
    try:
        nick, rest = name.split('!')
    except ValueError:
        return (
         name, None, None, None)
    else:
        try:
            mode, rest = rest.split('=')
        except ValueError:
            mode, rest = None, rest

        try:
            user, host = rest.split('@')
        except ValueError:
            return (
             name, mode, rest, None)
        else:
            return (
             nick, mode, user, host)