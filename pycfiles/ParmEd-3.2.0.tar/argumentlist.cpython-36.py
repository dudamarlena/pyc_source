# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/tools/argumentlist.py
# Compiled at: 2017-12-01 13:25:12
# Size of source mod 2**32: 8410 bytes
"""
This stores a list of arguments, tokenizing a string into a list of arguments.
"""
import logging, warnings
from .exceptions import NoArgument, InputError
LOGGER = logging.getLogger(__name__)

class Argument(object):
    __doc__ = ' Is an argument '

    def __init__(self, string):
        """ Input string for the argument """
        self.string = string.strip()
        self.marked = False
        self.keep_quotes = False
        if len(string) == 0 or len(string) == 1 and string in ("'", '"'):
            LOGGER.warning('Unclosed quotation detected! Ignoring lone quote')

    def lower(self):
        """ Make the argument lower-case """
        return self.string.lower()

    def isfloat(self):
        """ Determines if it can be a double """
        try:
            tmp = float(self.string)
            del tmp
            return True
        except ValueError:
            return False

    def isint(self):
        """ Determines if it can be an integer """
        try:
            tmp = int(self.string)
            del tmp
            return True
        except ValueError:
            return False

    def ismask(self):
        """ Determines if we can be an Amber mask or not """
        return self.string == '*' or ':' in self.string or '@' in self.string

    def __float__(self):
        self.marked = True
        return float(self.string)

    def __int__(self):
        self.marked = True
        return int(self.string)

    def __str__(self):
        self.marked = True
        if self.keep_quotes:
            return self.string
        else:
            if self.string[0] == "'":
                if self.string[(-1)] == "'":
                    return self.string[1:-1]
            if self.string[0] == '"':
                if self.string[(-1)] == '"':
                    return self.string[1:len(self.string) - 1]
            return self.string

    def __eq__(self, other):
        """ String comparison """
        return self.string == str(other)

    def mark(self):
        """ Provide a way of forcibly marking an argument """
        self.marked = True

    def unmark(self):
        """ Provide a way of forcibly unmarking an argument """
        self.marked = False


class ArgumentList(object):
    __doc__ = " \n    List of arguments.  \n    The arguments should be parsed in the following order to ensure it's done\n    correctly:\n        get_key_*\n        get_next_int\n        get_next_float\n        get_next_mask\n        get_next_string\n    "

    def __init__(self, inp):
        """ Defines the string """
        if isinstance(inp, tuple) or isinstance(inp, list):
            _inp = [l for l in inp if l is not None if l != '']
            self.original = ' '.join([str(l) for l in _inp])
            self.tokenlist = [Argument(str(l)) for l in _inp]
        else:
            if isinstance(inp, ArgumentList):
                self.tokenlist = []
                try:
                    while True:
                        arg = Argument(inp.get_next_string())
                        self.tokenlist.append(arg)

                except NoArgument:
                    pass

                self.original = ' '.join([str(a) for a in inp.tokenlist])
            else:
                self.original = ' %s ' % inp
                self.tokenize(self.original)

    def tokenize(self, instring):
        """ 
        Tokenizes the line, everything between quotes is a single token,
        including whitespace
        """
        import re
        tokenre = re.compile('((?:\\s+".*?"\\s+?)|(?:\\s+\'.*?\'\\s+?)|(?:\\S+))')
        tokenlist = tokenre.findall(instring)
        if len(tokenre.sub('', instring).strip()) > 0:
            warnings.warn('Not all of argument string were handled: [%s]' % tokenre.sub('', instring).strip())
        self.tokenlist = [Argument(token.strip()) for token in tokenlist]

    def __str__(self):
        """ Return the original input string """
        return self.original

    def get_next_int(self, optional=False, default=None):
        """ Returns the next unmarked integer in the token list """
        for token in self.tokenlist:
            if token.isint():
                if not token.marked:
                    return int(token)

        if optional:
            return default
        raise NoArgument('Missing integer argument!')

    def get_next_float(self, optional=False, default=None):
        """ Returns the next unmarked float in the token list """
        for token in self.tokenlist:
            if token.isfloat():
                if not token.marked:
                    return float(token)

        if optional:
            return default
        raise NoArgument('Missing floating point argument!')

    def get_next_mask(self, optional=False, default=None):
        """ Returns the next string as long as it matches a mask """
        for token in self.tokenlist:
            if token.marked:
                pass
            else:
                if token.ismask():
                    return str(token)

        if optional:
            return default
        raise NoArgument('Missing Amber mask!')

    def get_next_string(self, optional=False, keep_quotes=False, default=None):
        """ Returns the next unmarked float in the token list """
        for token in self.tokenlist:
            if not token.marked:
                token.keep_quotes = keep_quotes
                return str(token)

        if optional:
            return default
        raise NoArgument('Missing string!')

    def unmarked(self):
        """ Returns all unmarked arguments as a list of strings """
        unmarked_tokens = []
        for token in self.tokenlist:
            if not token.marked:
                unmarked_tokens.append(token.string)

        return unmarked_tokens

    def _get_key_arg(self, key, argtype):
        """ Gets a key with a given argument type """
        for i, token in enumerate(self.tokenlist):
            if token.marked:
                pass
            else:
                if token == key:
                    if self.tokenlist[(i + 1)].marked:
                        raise RuntimeError('Expected token already marked! Should not happen. This means a buggy action...')
                    token.marked = True
                    try:
                        return argtype(self.tokenlist[(i + 1)])
                    except ValueError as err:
                        raise InputError(str(err))

        raise NoArgument('Catch me!')

    def get_key_int(self, key, default):
        """ Get an integer that follows a keyword """
        try:
            return self._get_key_arg(key, int)
        except NoArgument:
            return default

    def get_key_float(self, key, default):
        """ Get a float that follows a keyword """
        try:
            return self._get_key_arg(key, float)
        except NoArgument:
            return default

    def get_key_mask(self, key, default):
        """ Get a mask that follows a keyword """
        for i, token in enumerate(self.tokenlist):
            if token == key:
                raise self.tokenlist[(i + 1)].ismask() or InputError('Expected mask to follow %s. Got %s instead' % (
                 key, self.tokenlist[(i + 1)].string))

        try:
            return self._get_key_arg(key, str)
        except NoArgument:
            return default

    def get_key_string(self, key, default):
        """ Get a string that follows a keyword """
        try:
            return self._get_key_arg(key, str)
        except NoArgument:
            return default

    def has_key(self, key, mark=True):
        """ See if a particular keyword is present (optionally mark it) """
        for token in self.tokenlist:
            if not token.marked:
                if token == key:
                    if mark:
                        token.mark()
                    return True

        return False