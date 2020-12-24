# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/parse/token_matchers.py
# Compiled at: 2018-04-09 04:30:46
# Size of source mod 2**32: 771 bytes
from exactly_lib.util.cli_syntax import option_syntax
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.parse.token import Token, TokenMatcher

def is_unquoted_and_equals(value: str) -> TokenMatcher:
    return _Equals(value, True)


def is_option(option: a.OptionName) -> TokenMatcher:
    return _Equals(option_syntax.long_option_syntax(option.long), True)


class _Equals(TokenMatcher):

    def __init__(self, value: str, must_be_unquoted: bool=False):
        self.value = value
        self.must_be_unquoted = must_be_unquoted

    def matches(self, token: Token) -> bool:
        if self.must_be_unquoted and token.is_quoted:
            return False
        return self.value == token.string