# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/typoscript.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 8296 bytes
"""
    pygments.lexers.typoscript
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for TypoScript

    `TypoScriptLexer`
        A TypoScript lexer.

    `TypoScriptCssDataLexer`
        Lexer that highlights markers, constants and registers within css.

    `TypoScriptHtmlDataLexer`
        Lexer that highlights markers, constants and registers within html tags.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using
from pygments.token import Text, Comment, Name, String, Number, Operator, Punctuation
__all__ = [
 'TypoScriptLexer', 'TypoScriptCssDataLexer', 'TypoScriptHtmlDataLexer']

class TypoScriptCssDataLexer(RegexLexer):
    __doc__ = '\n    Lexer that highlights markers, constants and registers within css blocks.\n\n    .. versionadded:: 2.2\n    '
    name = 'TypoScriptCssData'
    aliases = ['typoscriptcssdata']
    tokens = {'root': [
              (
               '(.*)(###\\w+###)(.*)', bygroups(String, Name.Constant, String)),
              (
               '(\\{)(\\$)((?:[\\w\\-]+\\.)*)([\\w\\-]+)(\\})',
               bygroups(String.Symbol, Operator, Name.Constant, Name.Constant, String.Symbol)),
              (
               '(.*)(\\{)([\\w\\-]+)(\\s*:\\s*)([\\w\\-]+)(\\})(.*)',
               bygroups(String, String.Symbol, Name.Constant, Operator, Name.Constant, String.Symbol, String)),
              (
               '\\s+', Text),
              (
               '/\\*(?:(?!\\*/).)*\\*/', Comment),
              (
               '(?<!(#|\\\'|"))(?:#(?!(?:[a-fA-F0-9]{6}|[a-fA-F0-9]{3}))[^\\n#]+|//[^\\n]*)',
               Comment),
              (
               '[<>,:=.*%+|]', String),
              (
               '[\\w"\\-!/&;(){}]+', String)]}


class TypoScriptHtmlDataLexer(RegexLexer):
    __doc__ = '\n    Lexer that highlights markers, constants and registers within html tags.\n\n    .. versionadded:: 2.2\n    '
    name = 'TypoScriptHtmlData'
    aliases = ['typoscripthtmldata']
    tokens = {'root': [
              (
               '(INCLUDE_TYPOSCRIPT)', Name.Class),
              (
               '(EXT|FILE|LLL):[^}\\n"]*', String),
              (
               '(.*)(###\\w+###)(.*)', bygroups(String, Name.Constant, String)),
              (
               '(\\{)(\\$)((?:[\\w\\-]+\\.)*)([\\w\\-]+)(\\})',
               bygroups(String.Symbol, Operator, Name.Constant, Name.Constant, String.Symbol)),
              (
               '(.*)(\\{)([\\w\\-]+)(\\s*:\\s*)([\\w\\-]+)(\\})(.*)',
               bygroups(String, String.Symbol, Name.Constant, Operator, Name.Constant, String.Symbol, String)),
              (
               '\\s+', Text),
              (
               '[<>,:=.*%+|]', String),
              (
               '[\\w"\\-!/&;(){}#]+', String)]}


class TypoScriptLexer(RegexLexer):
    __doc__ = '\n    Lexer for TypoScript code.\n\n    http://docs.typo3.org/typo3cms/TyposcriptReference/\n\n    .. versionadded:: 2.2\n    '
    name = 'TypoScript'
    aliases = ['typoscript']
    filenames = ['*.typoscript']
    mimetypes = ['text/x-typoscript']
    flags = re.DOTALL | re.MULTILINE
    priority = 0.0
    tokens = {'root':[
      include('comment'),
      include('constant'),
      include('html'),
      include('label'),
      include('whitespace'),
      include('keywords'),
      include('punctuation'),
      include('operator'),
      include('structure'),
      include('literal'),
      include('other')], 
     'keywords':[
      (
       '(?i)(\\[)(browser|compatVersion|dayofmonth|dayofweek|dayofyear|device|ELSE|END|GLOBAL|globalString|globalVar|hostname|hour|IP|language|loginUser|loginuser|minute|month|page|PIDinRootline|PIDupinRootline|system|treeLevel|useragent|userFunc|usergroup|version)([^\\]]*)(\\])',
       bygroups(String.Symbol, Name.Constant, Text, String.Symbol)),
      (
       '(?=[\\w\\-])(HTMLparser|HTMLparser_tags|addParams|cache|encapsLines|filelink|if|imageLinkWrap|imgResource|makelinks|numRows|numberFormat|parseFunc|replacement|round|select|split|stdWrap|strPad|tableStyle|tags|textStyle|typolink)(?![\\w\\-])',
       Name.Function),
      (
       '(?:(=?\\s*<?\\s+|^\\s*))(cObj|field|config|content|constants|FEData|file|frameset|includeLibs|lib|page|plugin|register|resources|sitemap|sitetitle|styles|temp|tt_[^:.\\s]*|types|xmlnews|INCLUDE_TYPOSCRIPT|_CSS_DEFAULT_STYLE|_DEFAULT_PI_VARS|_LOCAL_LANG)(?![\\w\\-])',
       bygroups(Operator, Name.Builtin)),
      (
       '(?=[\\w\\-])(CASE|CLEARGIF|COA|COA_INT|COBJ_ARRAY|COLUMNS|CONTENT|CTABLE|EDITPANEL|FILE|FILES|FLUIDTEMPLATE|FORM|HMENU|HRULER|HTML|IMAGE|IMGTEXT|IMG_RESOURCE|LOAD_REGISTER|MEDIA|MULTIMEDIA|OTABLE|PAGE|QTOBJECT|RECORDS|RESTORE_REGISTER|SEARCHRESULT|SVG|SWFOBJECT|TEMPLATE|TEXT|USER|USER_INT)(?![\\w\\-])',
       Name.Class),
      (
       '(?=[\\w\\-])(ACTIFSUBRO|ACTIFSUB|ACTRO|ACT|CURIFSUBRO|CURIFSUB|CURRO|CUR|IFSUBRO|IFSUB|NO|SPC|USERDEF1RO|USERDEF1|USERDEF2RO|USERDEF2|USRRO|USR)',
       Name.Class),
      (
       '(?=[\\w\\-])(GMENU_FOLDOUT|GMENU_LAYERS|GMENU|IMGMENUITEM|IMGMENU|JSMENUITEM|JSMENU|TMENUITEM|TMENU_LAYERS|TMENU)',
       Name.Class),
      (
       '(?=[\\w\\-])(PHP_SCRIPT(_EXT|_INT)?)', Name.Class),
      (
       '(?=[\\w\\-])(userFunc)(?![\\w\\-])', Name.Function)], 
     'whitespace':[
      (
       '\\s+', Text)], 
     'html':[
      (
       '<\\S[^\\n>]*>', using(TypoScriptHtmlDataLexer)),
      (
       '&[^;\\n]*;', String),
      (
       '(?s)(_CSS_DEFAULT_STYLE)(\\s*)(\\()(.*(?=\\n\\)))',
       bygroups(Name.Class, Text, String.Symbol, using(TypoScriptCssDataLexer)))], 
     'literal':[
      (
       '0x[0-9A-Fa-f]+t?', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       '(###\\w+###)', Name.Constant)], 
     'label':[
      (
       '(EXT|FILE|LLL):[^}\\n"]*', String),
      (
       '(?![^\\w\\-])([\\w\\-]+(?:/[\\w\\-]+)+/?)(\\S*\\n)',
       bygroups(String, String))], 
     'punctuation':[
      (
       '[,.]', Punctuation)], 
     'operator':[
      (
       '[<>,:=.*%+|]', Operator)], 
     'structure':[
      (
       '[{}()\\[\\]\\\\]', String.Symbol)], 
     'constant':[
      (
       '(\\{)(\\$)((?:[\\w\\-]+\\.)*)([\\w\\-]+)(\\})',
       bygroups(String.Symbol, Operator, Name.Constant, Name.Constant, String.Symbol)),
      (
       '(\\{)([\\w\\-]+)(\\s*:\\s*)([\\w\\-]+)(\\})',
       bygroups(String.Symbol, Name.Constant, Operator, Name.Constant, String.Symbol)),
      (
       '(#[a-fA-F0-9]{6}\\b|#[a-fA-F0-9]{3}\\b)', String.Char)], 
     'comment':[
      (
       '(?<!(#|\\\'|"))(?:#(?!(?:[a-fA-F0-9]{6}|[a-fA-F0-9]{3}))[^\\n#]+|//[^\\n]*)',
       Comment),
      (
       '/\\*(?:(?!\\*/).)*\\*/', Comment),
      (
       '(\\s*#\\s*\\n)', Comment)], 
     'other':[
      (
       '[\\w"\\-!/&;]+', Text)]}