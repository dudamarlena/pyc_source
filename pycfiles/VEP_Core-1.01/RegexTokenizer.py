# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\vep_core\Ity\Tokenizers\RegexTokenizer.py
# Compiled at: 2013-12-05 13:11:49
__author__ = 'kohlmannj'
import re, HTMLParser
from Ity.Tokenizers import Tokenizer

class RegexTokenizer(Tokenizer):
    """
    A Tokenizer subclass that captures several types of tokens using five
    regular expression groups, in the following priority:

    * "Coalesced word fragments", that is, words, and then some. "Words" that
      contain single non-word characters separating other words characters will
      be captured as single tokens. This capture excludes edge punctuation.
      For example: "'tis" is captured as ("'", "tis"), but "north-north-west"
      stays together.
    * "Entities", or strings that each represent a single encoded HTML entity.
      These can sneak into plain text files due to processing errors. There is
      also a flag (convert_entities) that changes them back to the appropriate
      Unicode character/s. Tokenized as type Tokenizer.TYPES["PUNCTUATION"].
    * "Remnants", which captures potentially repeated characters not captured
      by the "coalesced word fragments" regular expression. This means that
      "--" (two consecutive hyphens) is captured as one token, for example.
      Tokenized as type Tokenizer.TYPES["PUNCTUATION"].
    * "Whitespace", which captures non-newline whitespace characters. Again,
      coalescing occurs, so "                   " or "    " (four spaces) are both captured
      as single tokens (independently of each other, of course).
    * "Newlines", which one or more of "
", "
", or "
".

    Output may be customized at instantiation time to disable case-sensitivity
    or have words (yes, words), entities, whitespace, punctuation, or newline
    tokens omitted from the output of self.tokenize() or self.batch_tokenize().
    """
    __pattern_str_inner_word_hyphen = '\\b-\\b'
    _pattern_str_hyphen_break = '\n        (?P<hyphen_break>\n            # A hyphen following one or more word characters.\n            (?P<hyphen_break_remnant>\n                -\n            )\n            # "Whitespace" between that hyphen and the next word fragment.\n            (?P<hyphen_break_whitespace>\n                # 0 or more "Not-not-whitespace and not newline" after the hyphen.\n                [^\\S\\n]*\n                # 1 or or more newlines.\n                \\n+\n                # 0 or more whitespace characters before the next word fragment.\n                \\s*\n            )\n        )\n    '
    _pattern_str_entity = '\n        # "Entity": an HTML entity (i.e. `&amp;` or `&#21512;`) that happens to\n        # be hanging out here.\n        (?P<entity>\n            # An ampersand...\n            &\n            # Followed by a group that contains either...\n            (\n                # A pound sign and numbers indicating a hex or decimal unicode\n                # entity (i.e. &#x0108; or &#21512;).\n                (\\#x?\\d+)\n                # or...\n                |\n                # Two or more letters, as in an aliased entity (i.e. &amp;).\n                # I\'m not aware of any name-aliased HTML entities that have\n                # single-letter aliases.\n                \\w\\w+\n            )\n            ;\n        )\n    '
    _pattern_str_word_fragment = '\n        # A word boundary, which thereby omits edge punctuation.\n        \\b\n        # An ampersand, as might appear in an HTML entity inside a word.\n        &?\n        # "Interior punctuation": zero or one non-whitespace characters.\n        \\S?\n        # One or more word characters.\n        \\w+\n    '
    _pattern_str_word_with_hyphen_breaks = '\n        # One or more "coalesced word fragments".\n        # This group captures multiple "fragments" together, so "cap-a-pe", for\n        # example, is one capture.\n        (?P<word>(\n            ' + _pattern_str_word_fragment + "\n            # Below we concatenate the hyphen break pattern and add a ? after it.\n            # That ? is important---otherwise, we won't correctly match\n            # non-hyphen-broken words.\n            " + _pattern_str_hyphen_break + '?\n        )+)\n    '
    _pattern_str_word = '\n        # One or more "coalesced word fragments".\n        # This group captures multiple "fragments" together, so "cap-a-pe", for\n        # example, is one capture.\n        (?P<word>(\n            ' + _pattern_str_word_fragment + '\n        )+)\n    '
    _pattern_str_remnant = '\n        # "Remnants": remaining non-whitespace chars (coalesced if repeated).\n        (?P<remnant>\n            # This named group captures any non-whitespace character.\n            (?P<remnant_char>\\S)\n            # Captures zero or more of the above "remnant" character.\n            (?P=remnant_char)*\n        )\n    '
    _pattern_str_whitespace = '\n        # "Whitespace": non-newline whitespace.\n        (?P<whitespace>\n            # This named group captures "not-not-whitespace or not-newline (both kinds)".\n            # Hat tip: http://stackoverflow.com/a/3469155/1991086\n            (?P<whitespace_char>[^\\S\\r\\n])\n            # Captures zero or more of the whitespace character from above.\n            (?P=whitespace_char)*\n        )\n    '
    _pattern_str_single_newline = '\\r\\n|(?<!\\r)\\n|\\r(?!\\n)'
    _pattern_str_newline = '\n        # Newlines (coalesced if repeated).\n        (?P<newline>\n            # (?P<newline_char>\\n)\n            # Captures zero or more newlines:\n            #   * \\r\\n (CRLF line endings)\n            #   * \\n without preceding \\r\n            #   * \\r without proceeding \\n\n            (' + _pattern_str_single_newline + ')*\n        )\n    '

    def __init__(self, debug=False, label=None, excluded_token_types=(), case_sensitive=True, preserve_original_strs=False, remove_hyphen_breaks=True, convert_entities=True, convert_newlines=True, condense_whitespace=None, condense_newlines=None):
        """
        Instantiates a RegexTokenizer. The initialization options below affect
        the output of the self.tokenize() and self.batch_tokenize() methods.

        self.tokenize() produces a list of lists containing token information.
        Refer to the docstring for self.tokenize() for more details.

        Keyword arguments:
        excluded_token_types-- A tuple of token type integers to exclude from
                               the tokenizer's output. Refer to Tokenizer.TYPES
                               for a dict of valid TYPE integers.
                               (default ())
        case_sensitive      -- Whether or not the tokens from self.tokenize() or
                               self.batch_tokenize() are case-sensitive.
                               (default True)
        preserve_original_strs  -- Whether or not to keep track of a token string's
                               history of transformations, if any. For example,
                               if a token string is dehyphenated, then that
                               token will contain
        remove_hyphen_breaks-- Whether or not to recombine captured words that
                               have been split across consecutive lines.
                               (default True)
        convert_entities    -- Whether or not to convert any captured HTML
                               entities back into Unicode characters. Note that
                               this setting applies to both "word" and "entity"
                               captures, i.e. convert_entities=True and
                               omit_entities=False will still convert any HTML
                               entities found within word captures.
                               (default True)
        omit_words          -- Whether or not to skip "word" tokens. Chances
                               are this won't get used much. (default False)
        omit_entities       -- Whether or not to skip "entity" tokens, which
                               only contain single HTML entities that did not
                               appear "inside" a word capture.
                               (default False)
        omit_whitespace     -- Whether or not to skip tokens entirely
                               consisting of non-newline whitespace characters.
                               (default False)
        omit_remnants       -- Whether or not to skip tokens entirely
                               consisting of non-HTML-entity "remnants" (i.e.
                               punctuation, etc.), so neither words, nor
                               whitespace, nor newline characters.
                               (default False)
        omit_newlines       -- Whether or not to skip tokens entirely
                               consisting of newline characters (i.e. "
").
                               (default False)
        condense_whitespace -- A string with which to replace the text content
                               of tokens consisting entirely of non-newline
                               whitespace. No condensing occurs if this
                               argument is set to None.
                               (default None)
        condense_newlines   -- A string with which to replace the text content
                               of tokens consisting entirely of newline
                               characters. No condensing occurs if this
                               argument is set to None.
                               (default None)
        """
        super(RegexTokenizer, self).__init__(debug=debug, label=label, excluded_token_types=excluded_token_types, case_sensitive=case_sensitive, preserve_original_strs=preserve_original_strs)
        self.remove_hyphen_breaks = remove_hyphen_breaks
        self.convert_entities = convert_entities
        self.convert_newlines = convert_newlines
        self.condense_whitespace = condense_whitespace
        self.condense_newlines = condense_newlines
        self._full_label = ('.').join([ str(setting) for setting in [
         self.excluded_token_types,
         self.case_sensitive, self.preserve_original_strs,
         self.remove_hyphen_breaks, self.convert_entities,
         self.convert_newlines, self.condense_whitespace,
         self.condense_newlines]
                                      ])
        self.__compile_tokenize_pattern()
        self.html_parser = None
        if self.convert_entities:
            self.html_parser = HTMLParser.HTMLParser()
        return

    def __compile_tokenize_pattern(self):
        """
        Compiles the regular expression used by self.tokenize() and stores
        a reference to it in self.tokenize_pattern. The full regular expression
        used here is a concatenation of several patterns (as written above
        self.__init__() and conditionally using either the word pattern that
        matches hyphen-broken words, or the pattern that only captures "whole"
        words.

        """
        word_pattern_str = self._pattern_str_word_with_hyphen_breaks
        if not self.remove_hyphen_breaks:
            word_pattern_str = self._pattern_str_word
        final_tokenize_pattern_str = ('|').join([
         word_pattern_str,
         self._pattern_str_entity,
         self._pattern_str_remnant,
         self._pattern_str_whitespace,
         self._pattern_str_newline])
        self.tokenize_pattern = re.compile(final_tokenize_pattern_str, re.I | re.VERBOSE)

    def _format_token_entity(self, m, token_data):
        """
        Modifies the contents of token_data according to how we want to handle
        a token containing an HTML entity. Most of the time we want to convert
        the HTML entity back to unicode characters for both "entity" captures
        and "word" captures.

        Keyword arguments:
        m           -- the regular expression match for the token
        token_data  -- list containing the token data produced from the
                       original regular expression match

        """
        token_strs = token_data[self.INDEXES['STRS']]
        token_data[self.INDEXES['TYPE']] = self.TYPES['PUNCTUATION']
        if self.html_parser is not None:
            converted_token_str = self.html_parser.unescape(token_strs[0])
            if self.preserve_original_strs and converted_token_str != token_strs[0]:
                token_strs.insert(0, converted_token_str)
            else:
                token_strs[0] = converted_token_str
        return

    def _format_token_word(self, m, token_data):
        """
        Modifies the contents of token_data according to how we want to handle
        a token containing words. We may want to convert HTML entities found in
        the word, make the word case-insensitive (i.e. lowercase), or remove
        "hyphen breaks" from the word as appropriate.

        Keyword arguments:
        m           -- the regular expression match for the token
        token_data  -- list containing the token data produced from the
                       original regular expression match

        """
        if self.convert_entities:
            self._format_token_entity(m, token_data)
        token_strs = token_data[self.INDEXES['STRS']]
        token_data[self.INDEXES['TYPE']] = self.TYPES['WORD']
        if not self.case_sensitive:
            token_str_lowercase = token_strs[0].lower()
            if self.preserve_original_strs and token_str_lowercase != token_strs[0]:
                token_strs.insert(0, token_str_lowercase)
            else:
                token_strs[0] = token_str_lowercase
        if m.group('hyphen_break') is not None:
            if self.remove_hyphen_breaks:
                inner_word_hyphens = re.findall(self.__pattern_str_inner_word_hyphen, token_strs[0])
                if len(inner_word_hyphens) == 0:
                    token_str = re.sub(self._pattern_str_hyphen_break, '', token_strs[0], flags=re.I | re.VERBOSE)
                else:
                    token_str = re.sub(self._pattern_str_hyphen_break, '-', token_strs[0], flags=re.I | re.VERBOSE)
                if self.preserve_original_strs:
                    token_strs.insert(0, token_str)
                else:
                    token_strs[0] = token_str
            else:
                raise ValueError("Somehow found a hyphen_break group when we shouldn't have.")
        return

    def _format_token_whitespace(self, m, token_data):
        """
        Modifies the contents of token_data according to how we want to handle
        a token containing whitespace. We may want to "condense" a token
        containing more than one whitespace character down to a single user-
        specified char (i.e. the non-None value of self.condense_newlines).

        Keyword arguments:
        m           -- the regular expression match for the token
        token_data  -- list containing the token data produced from the
                       original regular expression match

        """
        token_strs = token_data[self.INDEXES['STRS']]
        token_data[self.INDEXES['TYPE']] = self.TYPES['WHITESPACE']
        if self.condense_whitespace and token_strs[(-1)] != self.condense_whitespace:
            if self.preserve_original_strs:
                token_strs.insert(0, self.condense_whitespace)
            else:
                token_strs[0] = self.condense_whitespace

    def _format_token_newline(self, m, token_data):
        """
        Modifies the contents of token_data according to how we want to handle
        a token containing newlines. We may want to "condense" a token
        containing more than one newline down to a single user-specified char
        (i.e. the non-None value of self.condense_newlines).

        Keyword arguments:
        m           -- the regular expression match for the token
        token_data  -- list containing the token data produced from the
                       original regular expression match

        """
        token_strs = token_data[self.INDEXES['STRS']]
        token_data[self.INDEXES['TYPE']] = self.TYPES['NEWLINE']
        if self.convert_newlines and not self.condense_newlines and not reduce(lambda x, y: x & y, [ c == '\n' for c in token_strs[(-1)] ]):
            converted_newlines_string = re.sub(self._pattern_str_single_newline, '\n', token_strs[(-1)])
            if self.preserve_original_strs:
                token_strs.insert(0, converted_newlines_string)
            else:
                token_strs[0] = converted_newlines_string
        if self.condense_newlines and token_strs[(-1)] != self.condense_newlines:
            if self.preserve_original_strs:
                token_strs.insert(0, self.condense_newlines)
            else:
                token_strs[0] = self.condense_newlines

    def tokenize(self, s):
        """
        Returns a list of lists representing all the tokens captured from the
        input string, s.

        The data structure returned looks like this:

        # List of All Tokens
        [
            # List of Data for an Individual Token
            [
                # List of token strings, with the preferred string always at
                # index 0 and the original string always at index -1.
                [preferred_token_str, [...], original_token_str],  # token[0]
                original_token_start_position,                     # token[1]
                original_token_str_length,                         # token[2]
                # An integer from self.TYPES.
                token_type                                         # token[3]
            ]
        ]

        Note that self.batch_tokenize() is not implemented here; the Tokenizer
        superclass will call this subclass's implementation of self.tokenize()
        when invoked.

        Keyword arguments:
        s -- str to tokenize

        """
        tokens = []
        for m in self.tokenize_pattern.finditer(s):
            start = m.start()
            token_str = m.group()
            if token_str == '':
                continue
            length = len(m.group())
            single_token_list = [
             None] * len(self.INDEXES.keys())
            single_token_list[self.INDEXES['STRS']] = [token_str]
            single_token_list[self.INDEXES['POS']] = start
            single_token_list[self.INDEXES['LENGTH']] = length
            if m.group('word') is not None and Tokenizer.TYPES['WORD'] not in self.excluded_token_types:
                self._format_token_word(m, single_token_list)
            elif m.group('entity') is not None and Tokenizer.TYPES['PUNCTUATION'] not in self.excluded_token_types:
                self._format_token_entity(m, single_token_list)
            elif m.group('remnant') is not None and Tokenizer.TYPES['PUNCTUATION'] not in self.excluded_token_types:
                single_token_list[self.INDEXES['TYPE']] = self.TYPES['PUNCTUATION']
            elif m.group('whitespace') is not None and Tokenizer.TYPES['WHITESPACE'] not in self.excluded_token_types:
                self._format_token_whitespace(m, single_token_list)
            elif m.group('newline') is not None and Tokenizer.TYPES['NEWLINE'] not in self.excluded_token_types:
                self._format_token_newline(m, single_token_list)
            else:
                continue
            tokens.append(single_token_list)

        return tokens