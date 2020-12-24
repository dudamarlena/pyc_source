# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/javascript.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 60079 bytes
"""
    pygments.lexers.javascript
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for JavaScript and related languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, default, using, this, words, combined
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Other
from pygments.util import get_bool_opt, iteritems
import pygments.unistring as uni
__all__ = [
 'JavascriptLexer', 'KalLexer', 'LiveScriptLexer', 'DartLexer',
 'TypeScriptLexer', 'LassoLexer', 'ObjectiveJLexer',
 'CoffeeScriptLexer', 'MaskLexer', 'EarlGreyLexer', 'JuttleLexer']
JS_IDENT_START = '(?:[$_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') + ']|\\\\u[a-fA-F0-9]{4})'
JS_IDENT_PART = '(?:[$' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Mn', 'Mc', 'Nd', 'Pc') + '\u200c\u200d]|\\\\u[a-fA-F0-9]{4})'
JS_IDENT = JS_IDENT_START + '(?:' + JS_IDENT_PART + ')*'

class JavascriptLexer(RegexLexer):
    __doc__ = '\n    For JavaScript source code.\n    '
    name = 'JavaScript'
    aliases = ['js', 'javascript']
    filenames = ['*.js', '*.jsm']
    mimetypes = ['application/javascript', 'application/x-javascript',
     'text/x-javascript', 'text/javascript']
    flags = re.DOTALL | re.UNICODE | re.MULTILINE
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '<!--', Comment),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline)], 
     'slashstartsregex':[
      include('commentsandwhitespace'),
      (
       '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gimuy]+\\b|\\B)',
       String.Regex, '#pop'),
      (
       '(?=/)', Text, ('#pop', 'badregex')),
      default('#pop')], 
     'badregex':[
      (
       '\\n', Text, '#pop')], 
     'root':[
      (
       '\\A#! ?/.*?\\n', Comment.Hashbang),
      (
       '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
      include('commentsandwhitespace'),
      (
       '(\\.\\d+|[0-9]+\\.[0-9]*)([eE][-+]?[0-9]+)?', Number.Float),
      (
       '0[bB][01]+', Number.Bin),
      (
       '0[oO][0-7]+', Number.Oct),
      (
       '0[xX][0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       '\\.\\.\\.|=>', Punctuation),
      (
       '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?',
       Operator, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(for|in|while|do|break|return|continue|switch|case|default|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|void|yield|this|of)\\b',
       Keyword, 'slashstartsregex'),
      (
       '(var|let|with|function)\\b', Keyword.Declaration, 'slashstartsregex'),
      (
       '(abstract|boolean|byte|char|class|const|debugger|double|enum|export|extends|final|float|goto|implements|import|int|interface|long|native|package|private|protected|public|short|static|super|synchronized|throws|transient|volatile)\\b',
       Keyword.Reserved),
      (
       '(true|false|null|NaN|Infinity|undefined)\\b', Keyword.Constant),
      (
       '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|Promise|Proxy|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|Error|eval|isFinite|isNaN|isSafeInteger|parseFloat|parseInt|document|this|window)\\b',
       Name.Builtin),
      (
       JS_IDENT, Name.Other),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
      (
       '`', String.Backtick, 'interp')], 
     'interp':[
      (
       '`', String.Backtick, '#pop'),
      (
       '\\\\\\\\', String.Backtick),
      (
       '\\\\`', String.Backtick),
      (
       '\\$\\{', String.Interpol, 'interp-inside'),
      (
       '\\$', String.Backtick),
      (
       '[^`\\\\$]+', String.Backtick)], 
     'interp-inside':[
      (
       '\\}', String.Interpol, '#pop'),
      include('root')]}


class KalLexer(RegexLexer):
    __doc__ = '\n    For `Kal`_ source code.\n\n    .. _Kal: http://rzimmerman.github.io/kal\n\n\n    .. versionadded:: 2.0\n    '
    name = 'Kal'
    aliases = ['kal']
    filenames = ['*.kal']
    mimetypes = ['text/kal', 'application/kal']
    flags = re.DOTALL
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '###[^#].*?###', Comment.Multiline),
      (
       '#(?!##[^#]).*?\\n', Comment.Single)], 
     'functiondef':[
      (
       '[$a-zA-Z_][\\w$]*\\s*', Name.Function, '#pop'),
      include('commentsandwhitespace')], 
     'classdef':[
      (
       '\\binherits\\s+from\\b', Keyword),
      (
       '[$a-zA-Z_][\\w$]*\\s*\\n', Name.Class, '#pop'),
      (
       '[$a-zA-Z_][\\w$]*\\s*', Name.Class),
      include('commentsandwhitespace')], 
     'listcomprehension':[
      (
       '\\]', Punctuation, '#pop'),
      (
       '\\b(property|value)\\b', Keyword),
      include('root')], 
     'waitfor':[
      (
       '\\n', Punctuation, '#pop'),
      (
       '\\bfrom\\b', Keyword),
      include('root')], 
     'root':[
      include('commentsandwhitespace'),
      (
       '/(?! )(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
       String.Regex),
      (
       '\\?|:|_(?=\\n)|==?|!=|-(?!>)|[<>+*/-]=?',
       Operator),
      (
       '\\b(and|or|isnt|is|not|but|bitwise|mod|\\^|xor|exists|doesnt\\s+exist)\\b',
       Operator.Word),
      (
       '(?:\\([^()]+\\))?\\s*>', Name.Function),
      (
       '[{(]', Punctuation),
      (
       '\\[', Punctuation, 'listcomprehension'),
      (
       '[})\\].,]', Punctuation),
      (
       '\\b(function|method|task)\\b', Keyword.Declaration, 'functiondef'),
      (
       '\\bclass\\b', Keyword.Declaration, 'classdef'),
      (
       '\\b(safe\\s+)?wait\\s+for\\b', Keyword, 'waitfor'),
      (
       '\\b(me|this)(\\.[$a-zA-Z_][\\w.$]*)?\\b', Name.Variable.Instance),
      (
       '(?<![.$])(for(\\s+(parallel|series))?|in|of|while|until|break|return|continue|when|if|unless|else|otherwise|except\\s+when|throw|raise|fail\\s+with|try|catch|finally|new|delete|typeof|instanceof|super|run\\s+in\\s+parallel|inherits\\s+from)\\b',
       Keyword),
      (
       '(?<![.$])(true|false|yes|no|on|off|null|nothing|none|NaN|Infinity|undefined)\\b',
       Keyword.Constant),
      (
       '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|eval|isFinite|isNaN|isSafeInteger|parseFloat|parseInt|document|window|print)\\b',
       Name.Builtin),
      (
       '[$a-zA-Z_][\\w.$]*\\s*(:|[+\\-*/]?\\=)?\\b', Name.Variable),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       '"""', String, 'tdqs'),
      (
       "'''", String, 'tsqs'),
      (
       '"', String, 'dqs'),
      (
       "'", String, 'sqs')], 
     'strings':[
      (
       '[^#\\\\\\\'"]+', String)], 
     'interpoling_string':[
      (
       '\\}', String.Interpol, '#pop'),
      include('root')], 
     'dqs':[
      (
       '"', String, '#pop'),
      (
       "\\\\.|\\'", String),
      (
       '#\\{', String.Interpol, 'interpoling_string'),
      include('strings')], 
     'sqs':[
      (
       "'", String, '#pop'),
      (
       '#|\\\\.|"', String),
      include('strings')], 
     'tdqs':[
      (
       '"""', String, '#pop'),
      (
       '\\\\.|\\\'|"', String),
      (
       '#\\{', String.Interpol, 'interpoling_string'),
      include('strings')], 
     'tsqs':[
      (
       "'''", String, '#pop'),
      (
       '#|\\\\.|\\\'|"', String),
      include('strings')]}


class LiveScriptLexer(RegexLexer):
    __doc__ = '\n    For `LiveScript`_ source code.\n\n    .. _LiveScript: http://gkz.github.com/LiveScript/\n\n    .. versionadded:: 1.6\n    '
    name = 'LiveScript'
    aliases = ['live-script', 'livescript']
    filenames = ['*.ls']
    mimetypes = ['text/livescript']
    flags = re.DOTALL
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '#.*?\\n', Comment.Single)], 
     'multilineregex':[
      include('commentsandwhitespace'),
      (
       '//([gim]+\\b|\\B)', String.Regex, '#pop'),
      (
       '/', String.Regex),
      (
       '[^/#]+', String.Regex)], 
     'slashstartsregex':[
      include('commentsandwhitespace'),
      (
       '//', String.Regex, ('#pop', 'multilineregex')),
      (
       '/(?! )(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
       String.Regex, '#pop'),
      default('#pop')], 
     'root':[
      include('commentsandwhitespace'),
      (
       '(?:\\([^()]+\\))?[ ]*[~-]{1,2}>|(?:\\(?[^()\\n]+\\)?)?[ ]*<[~-]{1,2}',
       Name.Function),
      (
       '\\+\\+|&&|(?<![.$])\\b(?:and|x?or|is|isnt|not)\\b|\\?|:|=|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|~(?!\\~?>)|-(?!\\-?>)|<(?!\\[)|(?<!\\])>|[+*`%&|^/])=?',
       Operator, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(?<![.$])(for|own|in|of|while|until|loop|break|return|continue|switch|when|then|if|unless|else|throw|try|catch|finally|new|delete|typeof|instanceof|super|extends|this|class|by|const|var|to|til)\\b',
       Keyword,
       'slashstartsregex'),
      (
       '(?<![.$])(true|false|yes|no|on|off|null|NaN|Infinity|undefined|void)\\b',
       Keyword.Constant),
      (
       '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|eval|isFinite|isNaN|parseFloat|parseInt|document|window)\\b',
       Name.Builtin),
      (
       '[$a-zA-Z_][\\w.\\-:$]*\\s*[:=]\\s', Name.Variable,
       'slashstartsregex'),
      (
       '@[$a-zA-Z_][\\w.\\-:$]*\\s*[:=]\\s', Name.Variable.Instance,
       'slashstartsregex'),
      (
       '@', Name.Other, 'slashstartsregex'),
      (
       '@?[$a-zA-Z_][\\w-]*', Name.Other, 'slashstartsregex'),
      (
       '[0-9]+\\.[0-9]+([eE][0-9]+)?[fd]?(?:[a-zA-Z_]+)?', Number.Float),
      (
       '[0-9]+(~[0-9a-z]+)?(?:[a-zA-Z_]+)?', Number.Integer),
      (
       '"""', String, 'tdqs'),
      (
       "'''", String, 'tsqs'),
      (
       '"', String, 'dqs'),
      (
       "'", String, 'sqs'),
      (
       '\\\\\\S+', String),
      (
       '<\\[.*?\\]>', String)], 
     'strings':[
      (
       '[^#\\\\\\\'"]+', String)], 
     'interpoling_string':[
      (
       '\\}', String.Interpol, '#pop'),
      include('root')], 
     'dqs':[
      (
       '"', String, '#pop'),
      (
       "\\\\.|\\'", String),
      (
       '#\\{', String.Interpol, 'interpoling_string'),
      (
       '#', String),
      include('strings')], 
     'sqs':[
      (
       "'", String, '#pop'),
      (
       '#|\\\\.|"', String),
      include('strings')], 
     'tdqs':[
      (
       '"""', String, '#pop'),
      (
       '\\\\.|\\\'|"', String),
      (
       '#\\{', String.Interpol, 'interpoling_string'),
      (
       '#', String),
      include('strings')], 
     'tsqs':[
      (
       "'''", String, '#pop'),
      (
       '#|\\\\.|\\\'|"', String),
      include('strings')]}


class DartLexer(RegexLexer):
    __doc__ = '\n    For `Dart <http://dartlang.org/>`_ source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'Dart'
    aliases = ['dart']
    filenames = ['*.dart']
    mimetypes = ['text/x-dart']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root':[
      include('string_literal'),
      (
       '#!(.*?)$', Comment.Preproc),
      (
       '\\b(import|export)\\b', Keyword, 'import_decl'),
      (
       '\\b(library|source|part of|part)\\b', Keyword),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '\\b(class)\\b(\\s+)',
       bygroups(Keyword.Declaration, Text), 'class'),
      (
       '\\b(assert|break|case|catch|continue|default|do|else|finally|for|if|in|is|new|return|super|switch|this|throw|try|while)\\b',
       Keyword),
      (
       '\\b(abstract|async|await|const|extends|factory|final|get|implements|native|operator|set|static|sync|typedef|var|with|yield)\\b',
       Keyword.Declaration),
      (
       '\\b(bool|double|dynamic|int|num|Object|String|void)\\b', Keyword.Type),
      (
       '\\b(false|null|true)\\b', Keyword.Constant),
      (
       '[~!%^&*+=|?:<>/-]|as\\b', Operator),
      (
       '[a-zA-Z_$]\\w*:', Name.Label),
      (
       '[a-zA-Z_$]\\w*', Name),
      (
       '[(){}\\[\\],.;]', Punctuation),
      (
       '0[xX][0-9a-fA-F]+', Number.Hex),
      (
       '\\d+(\\.\\d*)?([eE][+-]?\\d+)?', Number),
      (
       '\\.\\d+([eE][+-]?\\d+)?', Number),
      (
       '\\n', Text)], 
     'class':[
      (
       '[a-zA-Z_$]\\w*', Name.Class, '#pop')], 
     'import_decl':[
      include('string_literal'),
      (
       '\\s+', Text),
      (
       '\\b(as|show|hide)\\b', Keyword),
      (
       '[a-zA-Z_$]\\w*', Name),
      (
       '\\,', Punctuation),
      (
       '\\;', Punctuation, '#pop')], 
     'string_literal':[
      (
       'r"""([\\w\\W]*?)"""', String.Double),
      (
       "r'''([\\w\\W]*?)'''", String.Single),
      (
       'r"(.*?)"', String.Double),
      (
       "r'(.*?)'", String.Single),
      (
       '"""', String.Double, 'string_double_multiline'),
      (
       "'''", String.Single, 'string_single_multiline'),
      (
       '"', String.Double, 'string_double'),
      (
       "'", String.Single, 'string_single')], 
     'string_common':[
      (
       '\\\\(x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4}|u\\{[0-9A-Fa-f]*\\}|[a-z\'\\"$\\\\])',
       String.Escape),
      (
       '(\\$)([a-zA-Z_]\\w*)', bygroups(String.Interpol, Name)),
      (
       '(\\$\\{)(.*?)(\\})',
       bygroups(String.Interpol, using(this), String.Interpol))], 
     'string_double':[
      (
       '"', String.Double, '#pop'),
      (
       '[^"$\\\\\\n]+', String.Double),
      include('string_common'),
      (
       '\\$+', String.Double)], 
     'string_double_multiline':[
      (
       '"""', String.Double, '#pop'),
      (
       '[^"$\\\\]+', String.Double),
      include('string_common'),
      (
       '(\\$|\\")+', String.Double)], 
     'string_single':[
      (
       "'", String.Single, '#pop'),
      (
       "[^'$\\\\\\n]+", String.Single),
      include('string_common'),
      (
       '\\$+', String.Single)], 
     'string_single_multiline':[
      (
       "'''", String.Single, '#pop'),
      (
       "[^\\'$\\\\]+", String.Single),
      include('string_common'),
      (
       "(\\$|\\')+", String.Single)]}


class TypeScriptLexer(RegexLexer):
    __doc__ = '\n    For `TypeScript <http://typescriptlang.org/>`_ source code.\n\n    .. versionadded:: 1.6\n    '
    name = 'TypeScript'
    aliases = ['ts', 'typescript']
    filenames = ['*.ts', '*.tsx']
    mimetypes = ['text/x-typescript']
    flags = re.DOTALL | re.MULTILINE
    priority = 0.5
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '<!--', Comment),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline)], 
     'slashstartsregex':[
      include('commentsandwhitespace'),
      (
       '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
       String.Regex, '#pop'),
      (
       '(?=/)', Text, ('#pop', 'badregex')),
      default('#pop')], 
     'badregex':[
      (
       '\\n', Text, '#pop')], 
     'root':[
      (
       '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
      include('commentsandwhitespace'),
      (
       '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?',
       Operator, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(for|in|while|do|break|return|continue|switch|case|default|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|void|of|this)\\b',
       Keyword, 'slashstartsregex'),
      (
       '(var|let|with|function)\\b', Keyword.Declaration, 'slashstartsregex'),
      (
       '(abstract|boolean|byte|char|class|const|debugger|double|enum|export|extends|final|float|goto|implements|import|int|interface|long|native|package|private|protected|public|short|static|super|synchronized|throws|transient|volatile)\\b',
       Keyword.Reserved),
      (
       '(true|false|null|NaN|Infinity|undefined)\\b', Keyword.Constant),
      (
       '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|Error|eval|isFinite|isNaN|parseFloat|parseInt|document|this|window)\\b',
       Name.Builtin),
      (
       '\\b(module)(\\s*)(\\s*[\\w?.$][\\w?.$]*)(\\s*)',
       bygroups(Keyword.Reserved, Text, Name.Other, Text), 'slashstartsregex'),
      (
       '\\b(string|bool|number)\\b', Keyword.Type),
      (
       '\\b(constructor|declare|interface|as|AS)\\b', Keyword.Reserved),
      (
       '(super)(\\s*)(\\([\\w,?.$\\s]+\\s*\\))',
       bygroups(Keyword.Reserved, Text), 'slashstartsregex'),
      (
       '([a-zA-Z_?.$][\\w?.$]*)\\(\\) \\{', Name.Other, 'slashstartsregex'),
      (
       '([\\w?.$][\\w?.$]*)(\\s*:\\s*)([\\w?.$][\\w?.$]*)',
       bygroups(Name.Other, Text, Keyword.Type)),
      (
       '[$a-zA-Z_]\\w*', Name.Other),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
      (
       '`', String.Backtick, 'interp'),
      (
       '@\\w+', Keyword.Declaration)], 
     'interp':[
      (
       '`', String.Backtick, '#pop'),
      (
       '\\\\\\\\', String.Backtick),
      (
       '\\\\`', String.Backtick),
      (
       '\\$\\{', String.Interpol, 'interp-inside'),
      (
       '\\$', String.Backtick),
      (
       '[^`\\\\$]+', String.Backtick)], 
     'interp-inside':[
      (
       '\\}', String.Interpol, '#pop'),
      include('root')]}


class LassoLexer(RegexLexer):
    __doc__ = '\n    For `Lasso <http://www.lassosoft.com/>`_ source code, covering both Lasso 9\n    syntax and LassoScript for Lasso 8.6 and earlier. For Lasso embedded in\n    HTML, use the `LassoHtmlLexer`.\n\n    Additional options accepted:\n\n    `builtinshighlighting`\n        If given and ``True``, highlight builtin types, traits, methods, and\n        members (default: ``True``).\n    `requiredelimiters`\n        If given and ``True``, only highlight code between delimiters as Lasso\n        (default: ``False``).\n\n    .. versionadded:: 1.6\n    '
    name = 'Lasso'
    aliases = ['lasso', 'lassoscript']
    filenames = ['*.lasso', '*.lasso[89]']
    alias_filenames = ['*.incl', '*.inc', '*.las']
    mimetypes = ['text/x-lasso']
    flags = re.IGNORECASE | re.DOTALL | re.MULTILINE
    tokens = {'root':[
      (
       '^#![ \\S]+lasso9\\b', Comment.Preproc, 'lasso'),
      (
       '(?=\\[|<)', Other, 'delimiters'),
      (
       '\\s+', Other),
      default(('delimiters', 'lassofile'))], 
     'delimiters':[
      (
       '\\[no_square_brackets\\]', Comment.Preproc, 'nosquarebrackets'),
      (
       '\\[noprocess\\]', Comment.Preproc, 'noprocess'),
      (
       '\\[', Comment.Preproc, 'squarebrackets'),
      (
       '<\\?(lasso(script)?|=)', Comment.Preproc, 'anglebrackets'),
      (
       '<(!--.*?-->)?', Other),
      (
       '[^[<]+', Other)], 
     'nosquarebrackets':[
      (
       '\\[noprocess\\]', Comment.Preproc, 'noprocess'),
      (
       '\\[', Other),
      (
       '<\\?(lasso(script)?|=)', Comment.Preproc, 'anglebrackets'),
      (
       '<(!--.*?-->)?', Other),
      (
       '[^[<]+', Other)], 
     'noprocess':[
      (
       '\\[/noprocess\\]', Comment.Preproc, '#pop'),
      (
       '\\[', Other),
      (
       '[^[]', Other)], 
     'squarebrackets':[
      (
       '\\]', Comment.Preproc, '#pop'),
      include('lasso')], 
     'anglebrackets':[
      (
       '\\?>', Comment.Preproc, '#pop'),
      include('lasso')], 
     'lassofile':[
      (
       '\\]|\\?>', Comment.Preproc, '#pop'),
      include('lasso')], 
     'whitespacecomments':[
      (
       '\\s+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*\\*!.*?\\*/', String.Doc),
      (
       '/\\*.*?\\*/', Comment.Multiline)], 
     'lasso':[
      include('whitespacecomments'),
      (
       '\\d*\\.\\d+(e[+-]?\\d+)?', Number.Float),
      (
       '0x[\\da-f]+', Number.Hex),
      (
       '\\d+', Number.Integer),
      (
       '(infinity|NaN)\\b', Number),
      (
       "'", String.Single, 'singlestring'),
      (
       '"', String.Double, 'doublestring'),
      (
       '`[^`]*`', String.Backtick),
      (
       '\\$[a-z_][\\w.]*', Name.Variable),
      (
       '#([a-z_][\\w.]*|\\d+\\b)', Name.Variable.Instance),
      (
       "(\\.\\s*)('[a-z_][\\w.]*')",
       bygroups(Name.Builtin.Pseudo, Name.Variable.Class)),
      (
       "(self)(\\s*->\\s*)('[a-z_][\\w.]*')",
       bygroups(Name.Builtin.Pseudo, Operator, Name.Variable.Class)),
      (
       '(\\.\\.?\\s*)([a-z_][\\w.]*(=(?!=))?)',
       bygroups(Name.Builtin.Pseudo, Name.Other.Member)),
      (
       '(->\\\\?\\s*|&\\s*)([a-z_][\\w.]*(=(?!=))?)',
       bygroups(Operator, Name.Other.Member)),
      (
       '(?<!->)(self|inherited|currentcapture|givenblock)\\b',
       Name.Builtin.Pseudo),
      (
       '-(?!infinity)[a-z_][\\w.]*', Name.Attribute),
      (
       '::\\s*[a-z_][\\w.]*', Name.Label),
      (
       '(error_(code|msg)_\\w+|Error_AddError|Error_ColumnRestriction|Error_DatabaseConnectionUnavailable|Error_DatabaseTimeout|Error_DeleteError|Error_FieldRestriction|Error_FileNotFound|Error_InvalidDatabase|Error_InvalidPassword|Error_InvalidUsername|Error_ModuleNotFound|Error_NoError|Error_NoPermission|Error_OutOfMemory|Error_ReqColumnMissing|Error_ReqFieldMissing|Error_RequiredColumnMissing|Error_RequiredFieldMissing|Error_UpdateError)\\b',
       Name.Exception),
      (
       '(define)(\\s+)([a-z_][\\w.]*)(\\s*=>\\s*)(type|trait|thread)\\b',
       bygroups(Keyword.Declaration, Text, Name.Class, Operator, Keyword)),
      (
       '(define)(\\s+)([a-z_][\\w.]*)(\\s*->\\s*)([a-z_][\\w.]*=?|[-+*/%])',
       bygroups(Keyword.Declaration, Text, Name.Class, Operator, Name.Function), 'signature'),
      (
       '(define)(\\s+)([a-z_][\\w.]*)',
       bygroups(Keyword.Declaration, Text, Name.Function), 'signature'),
      (
       '(public|protected|private|provide)(\\s+)(([a-z_][\\w.]*=?|[-+*/%])(?=\\s*\\())',
       bygroups(Keyword, Text, Name.Function),
       'signature'),
      (
       '(public|protected|private|provide)(\\s+)([a-z_][\\w.]*)',
       bygroups(Keyword, Text, Name.Function)),
      (
       '(true|false|none|minimal|full|all|void)\\b', Keyword.Constant),
      (
       '(local|var|variable|global|data(?=\\s))\\b', Keyword.Declaration),
      (
       '(array|date|decimal|duration|integer|map|pair|string|tag|xml|null|boolean|bytes|keyword|list|locale|queue|set|stack|staticarray)\\b',
       Keyword.Type),
      (
       '([a-z_][\\w.]*)(\\s+)(in)\\b', bygroups(Name, Text, Keyword)),
      (
       '(let|into)(\\s+)([a-z_][\\w.]*)', bygroups(Keyword, Text, Name)),
      (
       'require\\b', Keyword, 'requiresection'),
      (
       '(/?)(Namespace_Using)\\b', bygroups(Punctuation, Keyword.Namespace)),
      (
       '(/?)(Cache|Database_Names|Database_SchemaNames|Database_TableNames|Define_Tag|Define_Type|Email_Batch|Encode_Set|HTML_Comment|Handle|Handle_Error|Header|If|Inline|Iterate|LJAX_Target|Link|Link_CurrentAction|Link_CurrentGroup|Link_CurrentRecord|Link_Detail|Link_FirstGroup|Link_FirstRecord|Link_LastGroup|Link_LastRecord|Link_NextGroup|Link_NextRecord|Link_PrevGroup|Link_PrevRecord|Log|Loop|Output_None|Portal|Private|Protect|Records|Referer|Referrer|Repeating|ResultSet|Rows|Search_Args|Search_Arguments|Select|Sort_Args|Sort_Arguments|Thread_Atomic|Value_List|While|Abort|Case|Else|Fail_If|Fail_IfNot|Fail|If_Empty|If_False|If_Null|If_True|Loop_Abort|Loop_Continue|Loop_Count|Params|Params_Up|Return|Return_Value|Run_Children|SOAP_DefineTag|SOAP_LastRequest|SOAP_LastResponse|Tag_Name|ascending|average|by|define|descending|do|equals|frozen|group|handle_failure|import|in|into|join|let|match|max|min|on|order|parent|protected|provide|public|require|returnhome|skip|split_thread|sum|take|thread|to|trait|type|where|with|yield|yieldhome)\\b',
       bygroups(Punctuation, Keyword)),
      (
       ',', Punctuation, 'commamember'),
      (
       '(and|or|not)\\b', Operator.Word),
      (
       '([a-z_][\\w.]*)(\\s*::\\s*[a-z_][\\w.]*)?(\\s*=(?!=))',
       bygroups(Name, Name.Label, Operator)),
      (
       '(/?)([\\w.]+)', bygroups(Punctuation, Name.Other)),
      (
       '(=)(n?bw|n?ew|n?cn|lte?|gte?|n?eq|n?rx|ft)\\b',
       bygroups(Operator, Operator.Word)),
      (
       ':=|[-+*/%=<>&|!?\\\\]+', Operator),
      (
       '[{}():;,@^]', Punctuation)], 
     'singlestring':[
      (
       "'", String.Single, '#pop'),
      (
       "[^'\\\\]+", String.Single),
      include('escape'),
      (
       '\\\\', String.Single)], 
     'doublestring':[
      (
       '"', String.Double, '#pop'),
      (
       '[^"\\\\]+', String.Double),
      include('escape'),
      (
       '\\\\', String.Double)], 
     'escape':[
      (
       '\\\\(U[\\da-f]{8}|u[\\da-f]{4}|x[\\da-f]{1,2}|[0-7]{1,3}|:[^:\\n\\r]+:|[abefnrtv?"\\\'\\\\]|$)',
       String.Escape)], 
     'signature':[
      (
       '=>', Operator, '#pop'),
      (
       '\\)', Punctuation, '#pop'),
      (
       '[(,]', Punctuation, 'parameter'),
      include('lasso')], 
     'parameter':[
      (
       '\\)', Punctuation, '#pop'),
      (
       '-?[a-z_][\\w.]*', Name.Attribute, '#pop'),
      (
       '\\.\\.\\.', Name.Builtin.Pseudo),
      include('lasso')], 
     'requiresection':[
      (
       '(([a-z_][\\w.]*=?|[-+*/%])(?=\\s*\\())', Name, 'requiresignature'),
      (
       '(([a-z_][\\w.]*=?|[-+*/%])(?=(\\s*::\\s*[\\w.]+)?\\s*,))', Name),
      (
       '[a-z_][\\w.]*=?|[-+*/%]', Name, '#pop'),
      (
       '::\\s*[a-z_][\\w.]*', Name.Label),
      (
       ',', Punctuation),
      include('whitespacecomments')], 
     'requiresignature':[
      (
       '(\\)(?=(\\s*::\\s*[\\w.]+)?\\s*,))', Punctuation, '#pop'),
      (
       '\\)', Punctuation, '#pop:2'),
      (
       '-?[a-z_][\\w.]*', Name.Attribute),
      (
       '::\\s*[a-z_][\\w.]*', Name.Label),
      (
       '\\.\\.\\.', Name.Builtin.Pseudo),
      (
       '[(,]', Punctuation),
      include('whitespacecomments')], 
     'commamember':[
      (
       '(([a-z_][\\w.]*=?|[-+*/%])(?=\\s*(\\(([^()]*\\([^()]*\\))*[^)]*\\)\\s*)?(::[\\w.\\s]+)?=>))',
       Name.Function, 'signature'),
      include('whitespacecomments'),
      default('#pop')]}

    def __init__(self, **options):
        self.builtinshighlighting = get_bool_opt(options, 'builtinshighlighting', True)
        self.requiredelimiters = get_bool_opt(options, 'requiredelimiters', False)
        self._builtins = set()
        self._members = set()
        if self.builtinshighlighting:
            from pygments.lexers._lasso_builtins import BUILTINS, MEMBERS
            for key, value in iteritems(BUILTINS):
                self._builtins.update(value)

            for key, value in iteritems(MEMBERS):
                self._members.update(value)

        (RegexLexer.__init__)(self, **options)

    def get_tokens_unprocessed(self, text):
        stack = [
         'root']
        if self.requiredelimiters:
            stack.append('delimiters')
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name.Other and value.lower() in self._builtins or token is Name.Other.Member and value.lower().rstrip('=') in self._members:
                yield (
                 index, Name.Builtin, value)
            else:
                yield (
                 index, token, value)

    def analyse_text(text):
        rv = 0.0
        if 'bin/lasso9' in text:
            rv += 0.8
        if re.search('<\\?lasso', text, re.I):
            rv += 0.4
        if re.search('local\\(', text, re.I):
            rv += 0.4
        return rv


class ObjectiveJLexer(RegexLexer):
    __doc__ = '\n    For Objective-J source code with preprocessor directives.\n\n    .. versionadded:: 1.3\n    '
    name = 'Objective-J'
    aliases = ['objective-j', 'objectivej', 'obj-j', 'objj']
    filenames = ['*.j']
    mimetypes = ['text/x-objective-j']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)*'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'root':[
      include('whitespace'),
      (
       '^(' + _ws + '[+-]' + _ws + ')([(a-zA-Z_].*?[^(])(' + _ws + '\\{)',
       bygroups(using(this), using(this, state='function_signature'), using(this))),
      (
       '(@interface|@implementation)(\\s+)', bygroups(Keyword, Text),
       'classname'),
      (
       '(@class|@protocol)(\\s*)', bygroups(Keyword, Text),
       'forward_classname'),
      (
       '(\\s*)(@end)(\\s*)', bygroups(Text, Keyword, Text)),
      include('statements'),
      (
       '[{()}]', Punctuation),
      (
       ';', Punctuation)], 
     'whitespace':[
      (
       '(@import)(\\s+)("(?:\\\\\\\\|\\\\"|[^"])*")',
       bygroups(Comment.Preproc, Text, String.Double)),
      (
       '(@import)(\\s+)(<(?:\\\\\\\\|\\\\>|[^>])*>)',
       bygroups(Comment.Preproc, Text, String.Double)),
      (
       '(#(?:include|import))(\\s+)("(?:\\\\\\\\|\\\\"|[^"])*")',
       bygroups(Comment.Preproc, Text, String.Double)),
      (
       '(#(?:include|import))(\\s+)(<(?:\\\\\\\\|\\\\>|[^>])*>)',
       bygroups(Comment.Preproc, Text, String.Double)),
      (
       '#if\\s+0', Comment.Preproc, 'if0'),
      (
       '#', Comment.Preproc, 'macro'),
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text),
      (
       '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
      (
       '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
      (
       '<!--', Comment)], 
     'slashstartsregex':[
      include('whitespace'),
      (
       '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
       String.Regex, '#pop'),
      (
       '(?=/)', Text, ('#pop', 'badregex')),
      default('#pop')], 
     'badregex':[
      (
       '\\n', Text, '#pop')], 
     'statements':[
      (
       '(L|@)?"', String, 'string'),
      (
       "(L|@)?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'",
       String.Char),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
      (
       '0x[0-9a-fA-F]+[Ll]?', Number.Hex),
      (
       '0[0-7]+[Ll]?', Number.Oct),
      (
       '\\d+[Ll]?', Number.Integer),
      (
       '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
      (
       '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?',
       Operator, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(for|in|while|do|break|return|continue|switch|case|default|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|void|prototype|__proto__)\\b',
       Keyword, 'slashstartsregex'),
      (
       '(var|with|function)\\b', Keyword.Declaration, 'slashstartsregex'),
      (
       '(@selector|@private|@protected|@public|@encode|@synchronized|@try|@throw|@catch|@finally|@end|@property|@synthesize|@dynamic|@for|@accessors|new)\\b',
       Keyword),
      (
       '(int|long|float|short|double|char|unsigned|signed|void|id|BOOL|bool|boolean|IBOutlet|IBAction|SEL|@outlet|@action)\\b',
       Keyword.Type),
      (
       '(self|super)\\b', Name.Builtin),
      (
       '(TRUE|YES|FALSE|NO|Nil|nil|NULL)\\b', Keyword.Constant),
      (
       '(true|false|null|NaN|Infinity|undefined)\\b', Keyword.Constant),
      (
       '(ABS|ASIN|ACOS|ATAN|ATAN2|SIN|COS|TAN|EXP|POW|CEIL|FLOOR|ROUND|MIN|MAX|RAND|SQRT|E|LN2|LN10|LOG2E|LOG10E|PI|PI2|PI_2|SQRT1_2|SQRT2)\\b',
       Keyword.Constant),
      (
       '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|Error|eval|isFinite|isNaN|parseFloat|parseInt|document|this|window)\\b',
       Name.Builtin),
      (
       '([$a-zA-Z_]\\w*)(' + _ws + ')(?=\\()',
       bygroups(Name.Function, using(this))),
      (
       '[$a-zA-Z_]\\w*', Name)], 
     'classname':[
      (
       '([a-zA-Z_]\\w*)(' + _ws + ':' + _ws + ')([a-zA-Z_]\\w*)?',
       bygroups(Name.Class, using(this), Name.Class), '#pop'),
      (
       '([a-zA-Z_]\\w*)(' + _ws + '\\()([a-zA-Z_]\\w*)(\\))',
       bygroups(Name.Class, using(this), Name.Label, Text), '#pop'),
      (
       '([a-zA-Z_]\\w*)', Name.Class, '#pop')], 
     'forward_classname':[
      (
       '([a-zA-Z_]\\w*)(\\s*,\\s*)',
       bygroups(Name.Class, Text), '#push'),
      (
       '([a-zA-Z_]\\w*)(\\s*;?)',
       bygroups(Name.Class, Text), '#pop')], 
     'function_signature':[
      include('whitespace'),
      (
       '(\\(' + _ws + ')([a-zA-Z_]\\w+)(' + _ws + '\\)' + _ws + ')([$a-zA-Z_]\\w+' + _ws + ':)',
       bygroups(using(this), Keyword.Type, using(this), Name.Function), 'function_parameters'),
      (
       '(\\(' + _ws + ')([a-zA-Z_]\\w+)(' + _ws + '\\)' + _ws + ')([$a-zA-Z_]\\w+)',
       bygroups(using(this), Keyword.Type, using(this), Name.Function), '#pop'),
      (
       '([$a-zA-Z_]\\w+' + _ws + ':)',
       bygroups(Name.Function), 'function_parameters'),
      (
       '([$a-zA-Z_]\\w+)',
       bygroups(Name.Function), '#pop'),
      default('#pop')], 
     'function_parameters':[
      include('whitespace'),
      (
       '(\\(' + _ws + ')([^)]+)(' + _ws + '\\)' + _ws + ')([$a-zA-Z_]\\w+)',
       bygroups(using(this), Keyword.Type, using(this), Text)),
      (
       '([$a-zA-Z_]\\w+' + _ws + ':)',
       Name.Function),
      (
       '(:)', Name.Function),
      (
       '(,' + _ws + '\\.\\.\\.)', using(this)),
      (
       '([$a-zA-Z_]\\w+)', Text)], 
     'expression':[
      (
       '([$a-zA-Z_]\\w*)(\\()',
       bygroups(Name.Function, Punctuation)),
      (
       '(\\))', Punctuation, '#pop')], 
     'string':[
      (
       '"', String, '#pop'),
      (
       '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
      (
       '[^\\\\"\\n]+', String),
      (
       '\\\\\\n', String),
      (
       '\\\\', String)], 
     'macro':[
      (
       '[^/\\n]+', Comment.Preproc),
      (
       '/[*](.|\\n)*?[*]/', Comment.Multiline),
      (
       '//.*?\\n', Comment.Single, '#pop'),
      (
       '/', Comment.Preproc),
      (
       '(?<=\\\\)\\n', Comment.Preproc),
      (
       '\\n', Comment.Preproc, '#pop')], 
     'if0':[
      (
       '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
      (
       '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
      (
       '.*?\\n', Comment)]}

    def analyse_text(text):
        if re.search('^\\s*@import\\s+[<"]', text, re.MULTILINE):
            return True
        else:
            return False


class CoffeeScriptLexer(RegexLexer):
    __doc__ = '\n    For `CoffeeScript`_ source code.\n\n    .. _CoffeeScript: http://coffeescript.org\n\n    .. versionadded:: 1.3\n    '
    name = 'CoffeeScript'
    aliases = ['coffee-script', 'coffeescript', 'coffee']
    filenames = ['*.coffee']
    mimetypes = ['text/coffeescript']
    _operator_re = '\\+\\+|~|&&|\\band\\b|\\bor\\b|\\bis\\b|\\bisnt\\b|\\bnot\\b|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?(?!>)|!=?|=(?!>)|-(?!>)|[<>+*`%&\\|\\^/])=?'
    flags = re.DOTALL
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '###[^#].*?###', Comment.Multiline),
      (
       '#(?!##[^#]).*?\\n', Comment.Single)], 
     'multilineregex':[
      (
       '[^/#]+', String.Regex),
      (
       '///([gim]+\\b|\\B)', String.Regex, '#pop'),
      (
       '#\\{', String.Interpol, 'interpoling_string'),
      (
       '[/#]', String.Regex)], 
     'slashstartsregex':[
      include('commentsandwhitespace'),
      (
       '///', String.Regex, ('#pop', 'multilineregex')),
      (
       '/(?! )(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
       String.Regex, '#pop'),
      (
       '/', Operator),
      default('#pop')], 
     'root':[
      include('commentsandwhitespace'),
      (
       '^(?=\\s|/)', Text, 'slashstartsregex'),
      (
       _operator_re, Operator, 'slashstartsregex'),
      (
       '(?:\\([^()]*\\))?\\s*[=-]>', Name.Function, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(?<![.$])(for|own|in|of|while|until|loop|break|return|continue|switch|when|then|if|unless|else|throw|try|catch|finally|new|delete|typeof|instanceof|super|extends|this|class|by)\\b',
       Keyword, 'slashstartsregex'),
      (
       '(?<![.$])(true|false|yes|no|on|off|null|NaN|Infinity|undefined)\\b',
       Keyword.Constant),
      (
       '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|eval|isFinite|isNaN|parseFloat|parseInt|document|window)\\b',
       Name.Builtin),
      (
       '[$a-zA-Z_][\\w.:$]*\\s*[:=]\\s', Name.Variable,
       'slashstartsregex'),
      (
       '@[$a-zA-Z_][\\w.:$]*\\s*[:=]\\s', Name.Variable.Instance,
       'slashstartsregex'),
      (
       '@', Name.Other, 'slashstartsregex'),
      (
       '@?[$a-zA-Z_][\\w$]*', Name.Other),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       '"""', String, 'tdqs'),
      (
       "'''", String, 'tsqs'),
      (
       '"', String, 'dqs'),
      (
       "'", String, 'sqs')], 
     'strings':[
      (
       '[^#\\\\\\\'"]+', String)], 
     'interpoling_string':[
      (
       '\\}', String.Interpol, '#pop'),
      include('root')], 
     'dqs':[
      (
       '"', String, '#pop'),
      (
       "\\\\.|\\'", String),
      (
       '#\\{', String.Interpol, 'interpoling_string'),
      (
       '#', String),
      include('strings')], 
     'sqs':[
      (
       "'", String, '#pop'),
      (
       '#|\\\\.|"', String),
      include('strings')], 
     'tdqs':[
      (
       '"""', String, '#pop'),
      (
       '\\\\.|\\\'|"', String),
      (
       '#\\{', String.Interpol, 'interpoling_string'),
      (
       '#', String),
      include('strings')], 
     'tsqs':[
      (
       "'''", String, '#pop'),
      (
       '#|\\\\.|\\\'|"', String),
      include('strings')]}


class MaskLexer(RegexLexer):
    __doc__ = '\n    For `Mask <http://github.com/atmajs/MaskJS>`__ markup.\n\n    .. versionadded:: 2.0\n    '
    name = 'Mask'
    aliases = ['mask']
    filenames = ['*.mask']
    mimetypes = ['text/x-mask']
    flags = re.MULTILINE | re.IGNORECASE | re.DOTALL
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '[{};>]', Punctuation),
      (
       "'''", String, 'string-trpl-single'),
      (
       '"""', String, 'string-trpl-double'),
      (
       "'", String, 'string-single'),
      (
       '"', String, 'string-double'),
      (
       '([\\w-]+)', Name.Tag, 'node'),
      (
       '([^.#;{>\\s]+)', Name.Class, 'node'),
      (
       '(#[\\w-]+)', Name.Function, 'node'),
      (
       '(\\.[\\w-]+)', Name.Variable.Class, 'node')], 
     'string-base':[
      (
       '\\\\.', String.Escape),
      (
       '~\\[', String.Interpol, 'interpolation'),
      (
       '.', String.Single)], 
     'string-single':[
      (
       "'", String.Single, '#pop'),
      include('string-base')], 
     'string-double':[
      (
       '"', String.Single, '#pop'),
      include('string-base')], 
     'string-trpl-single':[
      (
       "'''", String.Single, '#pop'),
      include('string-base')], 
     'string-trpl-double':[
      (
       '"""', String.Single, '#pop'),
      include('string-base')], 
     'interpolation':[
      (
       '\\]', String.Interpol, '#pop'),
      (
       '\\s*:', String.Interpol, 'expression'),
      (
       '\\s*\\w+:', Name.Other),
      (
       '[^\\]]+', String.Interpol)], 
     'expression':[
      (
       '[^\\]]+', using(JavascriptLexer), '#pop')], 
     'node':[
      (
       '\\s+', Text),
      (
       '\\.', Name.Variable.Class, 'node-class'),
      (
       '\\#', Name.Function, 'node-id'),
      (
       'style[ \\t]*=', Name.Attribute, 'node-attr-style-value'),
      (
       '[\\w:-]+[ \\t]*=', Name.Attribute, 'node-attr-value'),
      (
       '[\\w:-]+', Name.Attribute),
      (
       '[>{;]', Punctuation, '#pop')], 
     'node-class':[
      (
       '[\\w-]+', Name.Variable.Class),
      (
       '~\\[', String.Interpol, 'interpolation'),
      default('#pop')], 
     'node-id':[
      (
       '[\\w-]+', Name.Function),
      (
       '~\\[', String.Interpol, 'interpolation'),
      default('#pop')], 
     'node-attr-value':[
      (
       '\\s+', Text),
      (
       '\\w+', Name.Variable, '#pop'),
      (
       "'", String, 'string-single-pop2'),
      (
       '"', String, 'string-double-pop2'),
      default('#pop')], 
     'node-attr-style-value':[
      (
       '\\s+', Text),
      (
       "'", String.Single, 'css-single-end'),
      (
       '"', String.Single, 'css-double-end'),
      include('node-attr-value')], 
     'css-base':[
      (
       '\\s+', Text),
      (
       ';', Punctuation),
      (
       '[\\w\\-]+\\s*:', Name.Builtin)], 
     'css-single-end':[
      include('css-base'),
      (
       "'", String.Single, '#pop:2'),
      (
       "[^;']+", Name.Entity)], 
     'css-double-end':[
      include('css-base'),
      (
       '"', String.Single, '#pop:2'),
      (
       '[^;"]+', Name.Entity)], 
     'string-single-pop2':[
      (
       "'", String.Single, '#pop:2'),
      include('string-base')], 
     'string-double-pop2':[
      (
       '"', String.Single, '#pop:2'),
      include('string-base')]}


class EarlGreyLexer(RegexLexer):
    __doc__ = '\n    For `Earl-Grey`_ source code.\n\n    .. _Earl-Grey: https://breuleux.github.io/earl-grey/\n\n    .. versionadded: 2.1\n    '
    name = 'Earl Grey'
    aliases = ['earl-grey', 'earlgrey', 'eg']
    filenames = ['*.eg']
    mimetypes = ['text/x-earl-grey']
    tokens = {'root':[
      (
       '\\n', Text),
      include('control'),
      (
       '[^\\S\\n]+', Text),
      (
       ';;.*\\n', Comment),
      (
       '[\\[\\]{}:(),;]', Punctuation),
      (
       '\\\\\\n', Text),
      (
       '\\\\', Text),
      include('errors'),
      (
       words(('with', 'where', 'when', 'and', 'not', 'or', 'in', 'as', 'of', 'is'),
         prefix='(?<=\\s|\\[)',
         suffix='(?![\\w$\\-])'),
       Operator.Word),
      (
       '[*@]?->', Name.Function),
      (
       '[+\\-*/~^<>%&|?!@#.]*=', Operator.Word),
      (
       '\\.{2,3}', Operator.Word),
      (
       '([+*/~^<>&|?!]+)|([#\\-](?=\\s))|@@+(?=\\s)|=+', Operator),
      (
       '(?<![\\w$\\-])(var|let)(?:[^\\w$])', Keyword.Declaration),
      include('keywords'),
      include('builtins'),
      include('assignment'),
      (
       '(?x)\n                (?:()([a-zA-Z$_](?:[\\w$\\-]*[\\w$])?)|\n                   (?<=[\\s{\\[(])(\\.)([a-zA-Z$_](?:[\\w$\\-]*[\\w$])?))\n                (?=.*%)',
       bygroups(Punctuation, Name.Tag, Punctuation, Name.Class.Start), 'dbs'),
      (
       '[rR]?`', String.Backtick, 'bt'),
      (
       '[rR]?```', String.Backtick, 'tbt'),
      (
       '(?<=[\\s\\[{(,;])\\.([a-zA-Z$_](?:[\\w$\\-]*[\\w$])?)(?=[\\s\\]}),;])',
       String.Symbol),
      include('nested'),
      (
       '(?:[rR]|[rR]\\.[gmi]{1,3})?"', String, combined('stringescape', 'dqs')),
      (
       "(?:[rR]|[rR]\\.[gmi]{1,3})?\\'", String, combined('stringescape', 'sqs')),
      (
       '"""', String, combined('stringescape', 'tdqs')),
      include('tuple'),
      include('import_paths'),
      include('name'),
      include('numbers')], 
     'dbs':[
      (
       '(\\.)([a-zA-Z$_](?:[\\w$\\-]*[\\w$])?)(?=[.\\[\\s])',
       bygroups(Punctuation, Name.Class.DBS)),
      (
       '(\\[)([\\^#][a-zA-Z$_](?:[\\w$\\-]*[\\w$])?)(\\])',
       bygroups(Punctuation, Name.Entity.DBS, Punctuation)),
      (
       '\\s+', Text),
      (
       '%', Operator.DBS, '#pop')], 
     'import_paths':[
      (
       '(?<=[\\s:;,])(\\.{1,3}(?:[\\w\\-]*/)*)(\\w(?:[\\w\\-]*\\w)*)(?=[\\s;,])',
       bygroups(Text.Whitespace, Text))], 
     'assignment':[
      (
       '(\\.)?([a-zA-Z$_](?:[\\w$\\-]*[\\w$])?)(?=\\s+[+\\-*/~^<>%&|?!@#.]*\\=\\s)',
       bygroups(Punctuation, Name.Variable))], 
     'errors':[
      (
       words(('Error', 'TypeError', 'ReferenceError'), prefix='(?<![\\w\\-$.])',
         suffix='(?![\\w\\-$.])'),
       Name.Exception),
      (
       '(?x)\n                (?<![\\w$])\n                E\\.[\\w$](?:[\\w$\\-]*[\\w$])?\n                (?:\\.[\\w$](?:[\\w$\\-]*[\\w$])?)*\n                (?=[({\\[?!\\s])',
       Name.Exception)], 
     'control':[
      (
       '(?x)\n                ([a-zA-Z$_](?:[\\w$-]*[\\w$])?)\n                (?!\\n)\\s+\n                (?!and|as|each\\*|each|in|is|mod|of|or|when|where|with)\n                (?=(?:[+\\-*/~^<>%&|?!@#.])?[a-zA-Z$_](?:[\\w$-]*[\\w$])?)',
       Keyword.Control),
      (
       '([a-zA-Z$_](?:[\\w$-]*[\\w$])?)(?!\\n)\\s+(?=[\\\'"\\d{\\[(])',
       Keyword.Control),
      (
       '(?x)\n                (?:\n                    (?<=[%=])|\n                    (?<=[=\\-]>)|\n                    (?<=with|each|with)|\n                    (?<=each\\*|where)\n                )(\\s+)\n                ([a-zA-Z$_](?:[\\w$-]*[\\w$])?)(:)',
       bygroups(Text, Keyword.Control, Punctuation)),
      (
       '(?x)\n                (?<![+\\-*/~^<>%&|?!@#.])(\\s+)\n                ([a-zA-Z$_](?:[\\w$-]*[\\w$])?)(:)',
       bygroups(Text, Keyword.Control, Punctuation))], 
     'nested':[
      (
       '(?x)\n                (?<=[\\w$\\]})])(\\.)\n                ([a-zA-Z$_](?:[\\w$-]*[\\w$])?)\n                (?=\\s+with(?:\\s|\\n))',
       bygroups(Punctuation, Name.Function)),
      (
       '(?x)\n                (?<!\\s)(\\.)\n                ([a-zA-Z$_](?:[\\w$-]*[\\w$])?)\n                (?=[}\\]).,;:\\s])',
       bygroups(Punctuation, Name.Field)),
      (
       '(?x)\n                (?<=[\\w$\\]})])(\\.)\n                ([a-zA-Z$_](?:[\\w$-]*[\\w$])?)\n                (?=[\\[{(:])',
       bygroups(Punctuation, Name.Function))], 
     'keywords':[
      (
       words(('each', 'each*', 'mod', 'await', 'break', 'chain', 'continue', 'elif', 'expr-value',
       'if', 'match', 'return', 'yield', 'pass', 'else', 'require', 'var', 'let',
       'async', 'method', 'gen'),
         prefix='(?<![\\w\\-$.])',
         suffix='(?![\\w\\-$.])'),
       Keyword.Pseudo),
      (
       words(('this', 'self', '@'), prefix='(?<![\\w\\-$.])',
         suffix='(?![\\w\\-$])'),
       Keyword.Constant),
      (
       words(('Function', 'Object', 'Array', 'String', 'Number', 'Boolean', 'ErrorFactory',
       'ENode', 'Promise'),
         prefix='(?<![\\w\\-$.])',
         suffix='(?![\\w\\-$])'),
       Keyword.Type)], 
     'builtins':[
      (
       words(('send', 'object', 'keys', 'items', 'enumerate', 'zip', 'product', 'neighbours',
       'predicate', 'equal', 'nequal', 'contains', 'repr', 'clone', 'range', 'getChecker',
       'get-checker', 'getProperty', 'get-property', 'getProjector', 'get-projector',
       'consume', 'take', 'promisify', 'spawn', 'constructor'),
         prefix='(?<![\\w\\-#.])',
         suffix='(?![\\w\\-.])'),
       Name.Builtin),
      (
       words(('true', 'false', 'null', 'undefined'),
         prefix='(?<![\\w\\-$.])',
         suffix='(?![\\w\\-$.])'),
       Name.Constant)], 
     'name':[
      (
       '@([a-zA-Z$_](?:[\\w$-]*[\\w$])?)', Name.Variable.Instance),
      (
       '([a-zA-Z$_](?:[\\w$-]*[\\w$])?)(\\+\\+|\\-\\-)?',
       bygroups(Name.Symbol, Operator.Word))], 
     'tuple':[
      (
       '#[a-zA-Z_][\\w\\-]*(?=[\\s{(,;])', Name.Namespace)], 
     'interpoling_string':[
      (
       '\\}', String.Interpol, '#pop'),
      include('root')], 
     'stringescape':[
      (
       '\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
       String.Escape)], 
     'strings':[
      (
       '[^\\\\\\\'"]', String),
      (
       '[\\\'"\\\\]', String),
      (
       '\\n', String)], 
     'dqs':[
      (
       '"', String, '#pop'),
      (
       '\\\\\\\\|\\\\"|\\\\\\n', String.Escape),
      include('strings')], 
     'sqs':[
      (
       "'", String, '#pop'),
      (
       "\\\\\\\\|\\\\'|\\\\\\n", String.Escape),
      (
       '\\{', String.Interpol, 'interpoling_string'),
      include('strings')], 
     'tdqs':[
      (
       '"""', String, '#pop'),
      include('strings')], 
     'bt':[
      (
       '`', String.Backtick, '#pop'),
      (
       '(?<!`)\\n', String.Backtick),
      (
       '\\^=?', String.Escape),
      (
       '.+', String.Backtick)], 
     'tbt':[
      (
       '```', String.Backtick, '#pop'),
      (
       '\\n', String.Backtick),
      (
       '\\^=?', String.Escape),
      (
       '[^`]+', String.Backtick)], 
     'numbers':[
      (
       '\\d+\\.(?!\\.)\\d*([eE][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+[eE][+-]?[0-9]+', Number.Float),
      (
       '8r[0-7]+', Number.Oct),
      (
       '2r[01]+', Number.Bin),
      (
       '16r[a-fA-F0-9]+', Number.Hex),
      (
       '([3-79]|[12][0-9]|3[0-6])r[a-zA-Z\\d]+(\\.[a-zA-Z\\d]+)?', Number.Radix),
      (
       '\\d+', Number.Integer)]}


class JuttleLexer(RegexLexer):
    __doc__ = '\n    For `Juttle`_ source code.\n\n    .. _Juttle: https://github.com/juttle/juttle\n\n    '
    name = 'Juttle'
    aliases = ['juttle', 'juttle']
    filenames = ['*.juttle']
    mimetypes = ['application/juttle', 'application/x-juttle',
     'text/x-juttle', 'text/juttle']
    flags = re.DOTALL | re.UNICODE | re.MULTILINE
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline)], 
     'slashstartsregex':[
      include('commentsandwhitespace'),
      (
       '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
       String.Regex, '#pop'),
      (
       '(?=/)', Text, ('#pop', 'badregex')),
      default('#pop')], 
     'badregex':[
      (
       '\\n', Text, '#pop')], 
     'root':[
      (
       '^(?=\\s|/)', Text, 'slashstartsregex'),
      include('commentsandwhitespace'),
      (
       ':\\d{2}:\\d{2}:\\d{2}(\\.\\d*)?:', String.Moment),
      (
       ':(now|beginning|end|forever|yesterday|today|tomorrow|(\\d+(\\.\\d*)?|\\.\\d+)(ms|[smhdwMy])?):',
       String.Moment),
      (
       ':\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2}(\\.\\d*)?)?(Z|[+-]\\d{2}:\\d{2}|[+-]\\d{4})?:',
       String.Moment),
      (
       ':((\\d+(\\.\\d*)?|\\.\\d+)[ ]+)?(millisecond|second|minute|hour|day|week|month|year)[s]?(([ ]+and[ ]+(\\d+[ ]+)?(millisecond|second|minute|hour|day|week|month|year)[s]?)|[ ]+(ago|from[ ]+now))*:',
       String.Moment),
      (
       '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(==?|!=?|[-<>+*%&|^/])=?',
       Operator, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(import|return|continue|if|else)\\b', Keyword, 'slashstartsregex'),
      (
       '(var|const|function|reducer|sub|input)\\b', Keyword.Declaration, 'slashstartsregex'),
      (
       '(batch|emit|filter|head|join|keep|pace|pass|put|read|reduce|remove|sequence|skip|sort|split|tail|unbatch|uniq|view|write)\\b',
       Keyword.Reserved),
      (
       '(true|false|null|Infinity)\\b', Keyword.Constant),
      (
       '(Array|Date|Juttle|Math|Number|Object|RegExp|String)\\b', Name.Builtin),
      (
       JS_IDENT, Name.Other),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '[0-9]+', Number.Integer),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]}