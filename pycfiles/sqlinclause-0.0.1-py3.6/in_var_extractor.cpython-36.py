# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/sqlinclause/in_var_extractor.py
# Compiled at: 2017-06-08 01:17:38
# Size of source mod 2**32: 7604 bytes
import re, sqlparse
from typing import List, Tuple, Iterator, Iterable, Union, Any, Dict, Set
Token = sqlparse.tokens.Token

def parse_named_placeholder(text: str):
    if text[0] == ':':
        return (text[1:], False)
    else:
        return (
         text[2:-2], True)


class InVar:
    __doc__ = '\n    SQL文中に含まれるIN句を構成する名前付きプレースホルダ情報。\n    IN :x\n    という記述があったら、「:x」部分の開始位置・長さと認識結果を格納しています。\n    :property pos: 開始位置\n    :property length: 長さ\n    :property name: プレースホルダ名\n    :property is_pyformat: %(x)s 形式であったらTrue、:x 形式ならFalse\n    :property is_in_paren: IN (:x) の形なら True, IN :x の形ならFalse\n    '

    def __init__(self, pos: int, text: str, is_in_paren: bool):
        self.pos = pos
        self.length = len(text)
        self.name, self.is_pyformat = parse_named_placeholder(text)
        self.is_in_paren = is_in_paren

    def matches(self, obj):
        """
        指定された名前、またはInVarに一致するプレースホルダであるかを判定します。
        not is_pyformat の場合にはcx_oracleの動作に合わせるため
        大小文字無視して一致判定するようになっています。
        """
        if isinstance(obj, str):
            if self.is_pyformat:
                return self.name == obj
            else:
                return self.name.lower() == obj.lower()
        else:
            if self.is_pyformat:
                return obj.is_pyformat and self.name == obj.name
            else:
                return not obj.is_pyformat and self.name.lower() == obj.name.lower()

    def find_in_dict(self, d: Dict[(str, Any)]):
        """
        辞書中に、自分の名前に一致するキーがあればそのキーと値を出力します。
        """
        if self.is_pyformat:
            if self.name in d:
                return (
                 self.name, d[self.name])
        else:
            for key in d:
                if self.matches(key):
                    return (
                     key, d[key])

    def generate_replace_string(self, new_names: Iterable[str]):
        """
        このプレースホルダを、指定された名前のプレースホルダの列に変換します。
        この結果をSQLの文字列置換に使用します。
        :param new_names: 名前の列
        :return: 必要に応じて括弧を補ったカンマ区切りプレースホルダ列
        """
        if self.is_pyformat:
            result = '%(' + ')s,%('.join(new_names) + ')s'
        else:
            result = ':' + ',:'.join(new_names)
        if self.is_in_paren:
            return result
        else:
            return '(%s)' % result

    def __str__(self):
        return '<%s (%d-%d) %s%s>' % (
         self.name,
         self.pos,
         self.pos + self.length,
         'pyformat' if self.is_pyformat else 'named',
         ' in_paren' if self.is_in_paren else '')


def extract_in_var(statement: str) -> Tuple[(List[InVar], Set[str])]:
    return parse_expression(iter(sqlparse.parse(statement)[0].flatten()))


def parse_expression(token_iterator: Iterator) -> Tuple[(List[InVar], Set[str])]:
    """
    括弧に入っていない地の文。
    """
    pos = 0
    in_vars = []
    names = set()
    while 1:
        try:
            token = next(token_iterator)
        except StopIteration:
            return (
             in_vars, names)
        else:
            pos += len(str(token))
            if is_left_paren(token):
                pos, found_in_vars, found_names = parse_paren(pos, token_iterator)
                in_vars += found_in_vars
                names += found_names
            else:
                if is_keyword_in(token):
                    pos, found_in_vars, found_names = parse_in_clause(pos, token_iterator)
                    in_vars += found_in_vars
                    names += found_names
                else:
                    if is_named_placeholder(token):
                        name, _ = parse_named_placeholder(str(token))
                        names.append(name)


def parse_in_clause_paren(pos: int, token_iterator: Iterator) -> Tuple[(int, List[InVar], Set[str])]:
    """
    INに続く括弧の中。
    """
    print('parse_in_clause_paren')
    in_vars = []
    names = set()
    while 1:
        try:
            token = next(token_iterator)
        except StopIteration:
            return (
             pos, in_vars, names)
        else:
            cur_pos = pos
            pos += len(str(token))
            if is_right_paren(token):
                return (
                 pos, in_vars, names)
            if is_left_paren(token):
                pos, found_in_vars, found_names = parse_paren(pos, token_iterator)
                in_vars += found_in_vars
                names += found_names
            else:
                if is_named_placeholder(token):
                    in_var = InVar(cur_pos, (str(token)), is_in_paren=True)
                    in_vars.append(in_var)
                    names.append(in_var.name)


def parse_paren(pos: int, token_iterator: Iterator) -> Tuple[(int, List[InVar], List[str])]:
    """
    括弧の中。
    """
    print('parse_paren')
    found = []
    names = []
    while 1:
        try:
            token = next(token_iterator)
        except StopIteration:
            return (
             pos, found, names)
        else:
            pos += len(str(token))
            if is_right_paren(token):
                return (
                 pos, found, names)
            if is_left_paren(token):
                pos, found_in_vars, found_names = parse_paren(pos, token_iterator)
                found += found_in_vars
                names += found_names
            else:
                if is_keyword_in(token):
                    pos, found_in_vars, found_names = parse_in_clause(pos, token_iterator)
                    found += found_in_vars
                    names += found_names
                else:
                    if is_named_placeholder(token):
                        name, _ = parse_named_placeholder(str(token))
                        names.append(name)


def parse_in_clause(pos: int, token_iterator: Iterator) -> Tuple[(int, List[InVar], Set[str])]:
    """
    "IN"を呼んだ直後の状態。
    """
    print('parse_in_clause')
    while 1:
        try:
            token = next(token_iterator)
        except StopIteration:
            return (
             pos, [], set())
        else:
            cur_pos = pos
            pos += len(str(token))
            if is_left_paren(token):
                return parse_in_clause_paren(pos, token_iterator)
            if is_named_placeholder(token):
                in_var = InVar(cur_pos, (str(token)), is_in_paren=False)
                return (pos, [in_var], {in_var.name})
            if not is_ignorable(token):
                return (
                 pos, [], set())


def is_keyword_in(token):
    return token.ttype == Token.Keyword and str(token).lower() == 'in'


def is_ignorable(token):
    return token.ttype in (Token.Comment.Multiline,
     Token.Comment.Single,
     Token.Text.Whitespace)


def is_named_placeholder(token):
    s = str(token)
    return token.ttype == Token.Name.Placeholder and (s[0] == ':' and not re.match(':[0-9]+$', s) or s.startswith('%('))


def is_left_paren(token):
    return token.ttype == Token.Punctuation and str(token) == '('


def is_right_paren(token):
    return token.ttype == Token.Punctuation and str(token) == ')'