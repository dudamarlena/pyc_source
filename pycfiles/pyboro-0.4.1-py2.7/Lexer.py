# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyboro/src/Lexer.py
# Compiled at: 2013-07-30 19:06:25
import re
from collections import OrderedDict
VERBAL = True

class ParseMapError(Exception):

    def __init__(self):
        self.value = ''

    def __str__(self):
        return self.value


class InputMatchError(ParseMapError):

    def __init__(self, regex, input_str):
        self.value = '"%s" not a valid regular expression for "%s"' % (regex, input_str)


class MissingTokenError(ParseMapError):

    def __init__(self, missing, input_string, regex):
        self.missing = missing
        self.value = 'Couldn\'t find matches for unignored tokens: %s, with regex "%s" and input "%s"' % (missing, regex, input_string)


class RegexMismatchError(ParseMapError):

    def __init__(self, mapped_regex, raw_regex):
        self.value = 'mapped regex %s is not equal to %s' % (mapped_regex, raw_regex)


class NoMatchError(ParseMapError):

    def __init__(self, regex, substring):
        self.value = 'Parsing cannot continue. There is no match for regex "%s" in substring "%s"' % (regex, substring)


class ParseMap(object):
    IGNORE = 0
    LITERAL = 1

    def __init__(self, regextable, strip=False, flags=0):
        r"""
        regextable is a tuple (or list) that describes the 
        symbol names and the regular expressions to be used,
        in the order they are to be consumed, as well as
        what to do with the corresponding text that is found.
    
        The last part (text to be found), can be either:
            1) ParseMap.IGNORE (consume the text without storing it)
            2) ParseMap.LITERAL (store the text as-is)
            3) Any function (store the output from the function, using the text as a single-argument input)

        for example, with the regular expression:
            "def ?[^ \(]+ ?\([^\)]\) ?:
"
        (
            ("definition"   , "def ?"       , ParseMap.IGNORE),
            ("func_name"    , "[^ ?\(]+"    , ParseMap.LITERAL),
            ("args_open"    , "\("          , ParseMap.IGNORE),
            ("args"         , "[^\)]"       , arg_parser)
            ("args_close"   , "\)"          , ParseMap.IGNORE),
            ("colon"        , " ?:"         , ParseMap.IGNORE)
        )

        arg_parser would have to be a function that takes one argument, 
        and returns SOMETHING that can be stored in the symbol table. 

        """
        assert isinstance(regextable, (list, tuple))
        self.regex_table = regextable
        self.strip = strip
        self.flags = flags
        tmp_list = [ entry[1] for entry in regextable ]
        self.regex = ('').join(tmp_list)
        self.parsed_token = ''
        self.input = ''
        self.raw_length = 0

    def create_empty_map(self):
        """
        Sets the current result map to hold null values
        for all tokens that will not be ignored.
        """
        self.symbols = OrderedDict()
        for entry in self.regex_table:
            if entry[2] is not ParseMap.IGNORE:
                self.symbols[entry[0]] = None

        return

    def parse(self, input_string):
        """
        Running the parse method will check the input string against
        this parser's regular expression, making sure that it's a match.
        It will then go chunk by chunk, based on the parse map, consuming
        the input and storing the symbols requested.
        The return value will be a map of the stored symbols and their values.
        """
        self.input = input_string
        self.offset = 0
        self.create_empty_map()
        if self.strip:
            input_string = input_string.strip()
            self.offset = len(self.input) - len(input_string)
        match_result = re.match(self.regex, input_string, self.flags)
        if not match_result:
            raise InputMatchError(self.regex, input_string)
        self.parsed_token = match_result.group()
        table_index = 0
        str_index = 0
        while table_index < len(self.regex_table):
            table_index, str_index = self.consume_input(self.parsed_token, table_index, str_index)

        if None in self.symbols.values():
            raise MissingTokenError([ token for token in self.symbols if self.symbols[token] is None ], input_string, self.regex)
        return self.symbols

    def consume_input(self, input_string, table_index, start_index):
        global VERBAL
        substring = input_string[start_index:]
        if VERBAL:
            print 'Lexer now consuming ::= %s' % re.escape(substring.strip())
        table_row = self.regex_table[table_index]
        identifier = table_row[0]
        regex = table_row[1]
        handler = table_row[2]
        result = re.match(regex, substring)
        if not result:
            raise NoMatchError(regex, substring)
        match = result.group()
        if VERBAL:
            print 'INPUT: %(input)s\nMatched Name: %(name)s\nMatched Regex: %(regex)s\n' % {'input': match.strip(), 
               'regex': regex, 
               'name': identifier}
        if handler is ParseMap.LITERAL:
            assert self.symbols[identifier] is None
            self.symbols[identifier] = match
        elif hasattr(handler, '__call__'):
            self.symbols[identifier] = handler(match)
        table_index += 1
        start_index = start_index + len(match)
        return (
         table_index, start_index)

    def assert_match(self, regex):
        """
        While it's probably easiest to simply use the piecemeal parser, 
        for more complex expressions you want to test elsewhere first, you
        can double-check that the regex you're testing matches the map
        you've created by passing the complete regex here to be sure that
        you haven't forgotten any of it.
        """
        if self.regex != regex:
            raise RegexMismatchError(self.regex, regex)