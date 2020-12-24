# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pangu2.py
# Compiled at: 2019-08-02 03:41:38
# Size of source mod 2**32: 8009 bytes
"""
Paranoid text spacing for good readability, to automatically insert whitespace between CJK (Chinese, Japanese, Korean) and half-width characters (alphabetical letters, numerical digits and symbols).

>>> import pangu2
>>> nwe_text = pangu2.spacing_text('當你凝視著bug，bug也凝視著你')
>>> print(nwe_text)
'當你凝視著 bug，bug 也凝視著你'
>>> nwe_content = pangu2.spacing_file('path/to/file.txt')
>>> print(nwe_content)
'與 PM 戰鬥的人，應當小心自己不要成為 PM'
"""
import argparse, os, re, sys
__version__ = '5.0'
__all__ = ['spacing_text', 'spacing_file', 'spacing', 'cli']
CJK = '\\u2e80-\\u2eff\\u2f00-\\u2fdf\\u3040-\\u309f\\u30a0-\\u30fa\\u30fc-\\u30ff\\u3100-\\u312f\\u3200-\\u32ff\\u3400-\\u4dbf\\u4e00-\\u9fff\\uf900-\\ufaff'
ANY_CJK = re.compile('[{CJK}]'.format(CJK=CJK))
CONVERT_TO_FULLWIDTH_CJK_SYMBOLS_CJK = re.compile('([{CJK}])([ ]*(?:[\\:]+|\\.)[ ]*)([{CJK}])'.format(CJK=CJK))
CONVERT_TO_FULLWIDTH_CJK_SYMBOLS = re.compile('([{CJK}])[ ]*([~\\!;,\\?]+)[ ]*'.format(CJK=CJK))
DOTS_CJK = re.compile('([\\.]{{2,}}|…)([{CJK}])'.format(CJK=CJK))
FIX_CJK_COLON_ANS = re.compile('([{CJK}])\\:([A-Z0-9\\(\\)])'.format(CJK=CJK))
CJK_QUOTE = re.compile('([{CJK}])([`"״])'.format(CJK=CJK))
QUOTE_CJK = re.compile('([`"״])([{CJK}])'.format(CJK=CJK))
FIX_QUOTE_ANY_QUOTE = re.compile('([`"\\u05f4]+)(\\s*)(.+?)(\\s*)([`"\\u05f4]+)')
CJK_SINGLE_QUOTE_BUT_POSSESSIVE = re.compile("([{CJK}])('[^s])".format(CJK=CJK))
SINGLE_QUOTE_CJK = re.compile("(')([{CJK}])".format(CJK=CJK))
FIX_POSSESSIVE_SINGLE_QUOTE = re.compile("([{CJK}A-Za-z0-9])( )('s)".format(CJK=CJK))
HASH_ANS_CJK_HASH = re.compile('([{CJK}])(#)([{CJK}]+)(#)([{CJK}])'.format(CJK=CJK))
CJK_HASH = re.compile('([{CJK}])(#([^ ]))'.format(CJK=CJK))
HASH_CJK = re.compile('(([^ ])#)([{CJK}])'.format(CJK=CJK))
CJK_OPERATOR_ANS = re.compile('([{CJK}])([\\+\\-\\*\\/=&\\|<>])([A-Za-z0-9])'.format(CJK=CJK))
ANS_OPERATOR_CJK = re.compile('([A-Za-z0-9])([\\+\\-\\*\\/=&\\|<>])([{CJK}])'.format(CJK=CJK))
FIX_SLASH_AS = re.compile('([/]) ([a-z\\-_\\./]+)')
FIX_SLASH_AS_SLASH = re.compile('([/\\.])([A-Za-z\\-_\\./]+) ([/])')
CJK_LEFT_BRACKET = re.compile('([{CJK}])([\\(\\[\\{{<>“])'.format(CJK=CJK))
RIGHT_BRACKET_CJK = re.compile('([\\)\\]\\}}<>”])([{CJK}])'.format(CJK=CJK))
FIX_LEFT_BRACKET_ANY_RIGHT_BRACKET = re.compile('([\\(\\[\\{<\\u201c]+)(\\s*)(.+?)(\\s*)([\\)\\]\\}>\\u201d]+)')
ANS_CJK_LEFT_BRACKET_ANY_RIGHT_BRACKET = re.compile('([A-Za-z0-9{CJK}])[ ]*([“])([A-Za-z0-9{CJK}\\-_ ]+)([”])'.format(CJK=CJK))
LEFT_BRACKET_ANY_RIGHT_BRACKET_ANS_CJK = re.compile('([“])([A-Za-z0-9{CJK}\\-_ ]+)([”])[ ]*([A-Za-z0-9{CJK}])'.format(CJK=CJK))
AN_LEFT_BRACKET = re.compile('([A-Za-z0-9])([\\(\\[\\{])')
RIGHT_BRACKET_AN = re.compile('([\\)\\]\\}])([A-Za-z0-9])')
CJK_ANS = re.compile('([{CJK}])([A-Za-zͰ-Ͽ0-9@\\$%\\^&\\*\\-\\+\\\\=\\|/¡-ÿ⅐-\u218f✀—➿])'.format(CJK=CJK))
ANS_CJK = re.compile('([A-Za-zͰ-Ͽ0-9~\\!\\$%\\^&\\*\\-\\+\\\\=\\|;:,\\./\\?¡-ÿ⅐-\u218f✀—➿])([{CJK}])'.format(CJK=CJK))
S_A = re.compile('(%)([A-Za-z])')
MIDDLE_DOT = re.compile('([ ]*)([\\u00b7\\u2022\\u2027])([ ]*)')
TILDES = re.compile('~+')
EXCLAMATION_MARKS = re.compile('!+')
SEMICOLONS = re.compile(';+')
COLONS = re.compile(':+')
COMMAS = re.compile(',+')
PERIODS = re.compile('\\.+')
QUESTION_MARKS = re.compile('\\?+')

def convert_to_fullwidth(symbols):
    symbols = TILDES.sub('～', symbols)
    symbols = EXCLAMATION_MARKS.sub('！', symbols)
    symbols = SEMICOLONS.sub('；', symbols)
    symbols = COLONS.sub('：', symbols)
    symbols = COMMAS.sub('，', symbols)
    symbols = PERIODS.sub('。', symbols)
    symbols = QUESTION_MARKS.sub('？', symbols)
    return symbols.strip()


def spacing(text):
    """
    Perform paranoid text spacing on text.
    """
    return len(text) <= 1 or ANY_CJK.search(text) or text
    new_text = text
    matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS_CJK.search(new_text)
    while matched:
        start, end = matched.span()
        new_text = ''.join((new_text[:start + 1], convert_to_fullwidth(new_text[start + 1:end - 1]), new_text[end - 1:]))
        matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS_CJK.search(new_text)

    matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS.search(new_text)
    while matched:
        start, end = matched.span()
        new_text = ''.join((new_text[:start + 1].strip(), convert_to_fullwidth(new_text[start + 1:end]), new_text[end:].strip()))
        matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS.search(new_text)

    new_text = DOTS_CJK.sub('\\1 \\2', new_text)
    new_text = FIX_CJK_COLON_ANS.sub('\\1：\\2', new_text)
    new_text = CJK_QUOTE.sub('\\1 \\2', new_text)
    new_text = QUOTE_CJK.sub('\\1 \\2', new_text)
    new_text = FIX_QUOTE_ANY_QUOTE.sub('\\1\\3\\5', new_text)
    new_text = CJK_SINGLE_QUOTE_BUT_POSSESSIVE.sub('\\1 \\2', new_text)
    new_text = SINGLE_QUOTE_CJK.sub('\\1 \\2', new_text)
    new_text = FIX_POSSESSIVE_SINGLE_QUOTE.sub("\\1's", new_text)
    new_text = HASH_ANS_CJK_HASH.sub('\\1 \\2\\3\\4 \\5', new_text)
    new_text = CJK_HASH.sub('\\1 \\2', new_text)
    new_text = HASH_CJK.sub('\\1 \\3', new_text)
    new_text = CJK_OPERATOR_ANS.sub('\\1 \\2 \\3', new_text)
    new_text = ANS_OPERATOR_CJK.sub('\\1 \\2 \\3', new_text)
    new_text = FIX_SLASH_AS.sub('\\1\\2', new_text)
    new_text = FIX_SLASH_AS_SLASH.sub('\\1\\2\\3', new_text)
    new_text = CJK_LEFT_BRACKET.sub('\\1 \\2', new_text)
    new_text = RIGHT_BRACKET_CJK.sub('\\1 \\2', new_text)
    new_text = FIX_LEFT_BRACKET_ANY_RIGHT_BRACKET.sub('\\1\\3\\5', new_text)
    new_text = ANS_CJK_LEFT_BRACKET_ANY_RIGHT_BRACKET.sub('\\1 \\2\\3\\4', new_text)
    new_text = LEFT_BRACKET_ANY_RIGHT_BRACKET_ANS_CJK.sub('\\1\\2\\3 \\4', new_text)
    new_text = RIGHT_BRACKET_AN.sub('\\1 \\2', new_text)
    new_text = CJK_ANS.sub('\\1 \\2', new_text)
    new_text = ANS_CJK.sub('\\1 \\2', new_text)
    new_text = S_A.sub('\\1 \\2', new_text)
    new_text = MIDDLE_DOT.sub('・', new_text)
    return new_text.strip()


def spacing_text(text):
    """
    Perform paranoid text spacing on text. An alias of `spacing()`.
    """
    return spacing(text)


def spacing_file(path):
    """
    Perform paranoid text spacing from file.
    """
    with open(os.path.abspath(path)) as (f):
        return spacing_text(f.read())


def cli(args=None):
    if not args:
        args = sys.argv[1:]
    else:
        parser = argparse.ArgumentParser(prog='pangu2',
          description='pangu2.py -- Paranoid text spacing for good readability, to automatically insert whitespace between CJK and half-width characters (alphabetical letters, numerical digits and symbols).')
        parser.add_argument('-v', '--version', action='version', version=__version__)
        parser.add_argument('-t', '--text', action='store_true', dest='is_text', required=False, help='specify the input value is a text')
        parser.add_argument('-f', '--file', action='store_true', dest='is_file', required=False, help='specify the input value is a file path')
        parser.add_argument('text_or_path', action='store', type=str, help='the text or file path to apply spacing')
        if not sys.stdin.isatty():
            print(spacing_text(sys.stdin.read()))
        else:
            args = parser.parse_args(args)
            if args.is_text:
                print(spacing_text(args.text_or_path))
            else:
                if args.is_file:
                    print(spacing_file(args.text_or_path))
                else:
                    print(spacing_text(args.text_or_path))


if __name__ == '__main__':
    cli()