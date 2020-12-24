# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/linguist/libs/tokenizer.py
# Compiled at: 2013-11-19 10:35:06
from re import compile, escape
from scanner import StringScanner, StringRegexp
BYTE_LIMIT = 100000
SINGLE_LINE_COMMENTS = [
 '//',
 '#',
 '%']
MULTI_LINE_COMMENTS = [
 [
  '/*', '*/'],
 [
  '<!--', '-->'],
 [
  '{-', '-}'],
 [
  '(*', '*)'],
 [
  '"""', '"""'],
 [
  "'''", "'''"]]
MULTI_LINE_COMMENT_DICT = dict([ (s, StringRegexp(escape(e))) for s, e in MULTI_LINE_COMMENTS
                               ])
START_SINGLE_LINE_COMMENT = StringRegexp(('|').join(map(lambda c: '\\s*%s ' % escape(c), SINGLE_LINE_COMMENTS)))
START_MULTI_LINE_COMMENT = StringRegexp(('|').join(map(lambda c: escape(c[0]), MULTI_LINE_COMMENTS)))
REGEX_SHEBANG = StringRegexp('^#!.+')
REGEX_BOL = StringRegexp('\\n|\\Z')
REGEX_DOUBLE_QUOTE = StringRegexp('"')
REGEX_SINGLE_QUOTE = StringRegexp("'")
REGEX_DOUBLE_END_QUOTE = StringRegexp('[^\\\\]"')
REGEX_SINGLE_END_QUOTE = StringRegexp("[^\\\\]'")
REGEX_NUMBER_LITERALS = StringRegexp('(0x)?\\d(\\d|\\.)*')
REGEX_SGML = StringRegexp('<[^\\s<>][^<>]*>')
REGEX_COMMON_PUNCTUATION = StringRegexp(';|\\{|\\}|\\(|\\)|\\[|\\]')
REGEX_REGULAR_TOKEN = StringRegexp('[\\w\\.@#\\/\\*]+')
REGEX_COMMON_OPERATORS = StringRegexp('<<?|\\+|\\-|\\*|\\/|%|&&?|\\|\\|?')
REGEX_EMIT_START_TOKEN = StringRegexp('<\\/?[^\\s>]+')
REGEX_EMIT_TRAILING = StringRegexp('\\w+=')
REGEX_EMIT_WORD = StringRegexp('\\w+')
REGEX_EMIT_END_TAG = StringRegexp('>')
REGEX_SHEBANG_FULL = StringRegexp('^#!\\s*\\S+')
REGEX_SHEBANG_WHITESPACE = StringRegexp('\\s+')
REGEX_SHEBANG_NON_WHITESPACE = StringRegexp('\\S+')

class Tokenizer(object):

    def __repr__(self):
        return '<Tokenizer>'

    @classmethod
    def tokenize(cls, data):
        """
        Public: Extract tokens from data

        data - String to tokenize

        Returns Array of token Strings.
        """
        return cls().extract_tokens(data)

    def extract_tokens(self, data):
        """
        Internal: Extract generic tokens from data.

        data - String to scan.

        Examples

          extract_tokens("printf('Hello')")
          # => ['printf', '(', ')']

        Returns Array of token Strings.
        """
        s = StringScanner(data)
        tokens = []
        while not s.is_eos:
            if s.pos >= BYTE_LIMIT:
                break
            token = s.scan(REGEX_SHEBANG)
            if token:
                name = self.extract_shebang(token)
                if name:
                    tokens.append('SHEBANG#!%s' % name)
                continue
            if s.is_bol and s.scan(START_SINGLE_LINE_COMMENT):
                s.skip_until(REGEX_BOL)
                continue
            token = s.scan(START_MULTI_LINE_COMMENT)
            if token:
                close_token = MULTI_LINE_COMMENT_DICT[token]
                s.skip_until(close_token)
                continue
            if s.scan(REGEX_DOUBLE_QUOTE):
                if s.peek(1) == '"':
                    s.getch
                else:
                    s.skip_until(REGEX_DOUBLE_END_QUOTE)
                continue
            if s.scan(REGEX_SINGLE_QUOTE):
                if s.peek(1) == "'":
                    s.getch
                else:
                    s.skip_until(REGEX_SINGLE_END_QUOTE)
                continue
            if s.scan(REGEX_NUMBER_LITERALS):
                continue
            token = s.scan(REGEX_SGML)
            if token:
                for t in self.extract_sgml_tokens(token):
                    tokens.append(t)

                continue
            token = s.scan(REGEX_COMMON_PUNCTUATION)
            if token:
                tokens.append(token)
                continue
            token = s.scan(REGEX_REGULAR_TOKEN)
            if token:
                tokens.append(token)
                continue
            token = s.scan(REGEX_COMMON_OPERATORS)
            if token:
                tokens.append(token)
                continue
            s.getch

        return tokens

    @classmethod
    def extract_shebang(cls, data):
        """
        Internal: Extract normalized shebang command token.

        Examples

          extract_shebang("#!/usr/bin/ruby")
          # => "ruby"

          extract_shebang("#!/usr/bin/env node")
          # => "node"

        Returns String token or nil it couldn't be parsed.
        """
        s = StringScanner(data)
        path = s.scan(REGEX_SHEBANG_FULL)
        if path:
            script = path.split('/')[(-1)]
            if script == 'env':
                s.scan(REGEX_SHEBANG_WHITESPACE)
                script = s.scan(REGEX_SHEBANG_NON_WHITESPACE)
            if script:
                script = compile('[^\\d]+').match(script).group(0)
            return script

    def extract_sgml_tokens(self, data):
        """
        Internal: Extract tokens from inside SGML tag.

        data - SGML tag String.

            Examples

              extract_sgml_tokens("<a href='' class=foo>")
              # => ["<a>", "href="]

        Returns Array of token Strings.
        """
        s = StringScanner(data)
        tokens = []
        append = tokens.append
        while not s.is_eos:
            token = s.scan(REGEX_EMIT_START_TOKEN)
            if token:
                append(token + '>')
                continue
            token = s.scan(REGEX_EMIT_TRAILING)
            if token:
                append(token)
                if s.scan(REGEX_DOUBLE_QUOTE):
                    s.skip_until(REGEX_DOUBLE_END_QUOTE)
                    continue
                if s.scan(REGEX_SINGLE_QUOTE):
                    s.skip_until(REGEX_SINGLE_END_QUOTE)
                    continue
                s.skip_until(REGEX_EMIT_WORD)
                continue
            token = s.scan(REGEX_EMIT_WORD)
            if token:
                append(token)
            if s.scan(REGEX_EMIT_END_TAG):
                s.terminate
                continue
            s.getch

        return tokens