# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/pawn.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 8098 bytes
"""
    pygments.lexers.pawn
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Pawn languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
from pygments.util import get_bool_opt
__all__ = [
 'SourcePawnLexer', 'PawnLexer']

class SourcePawnLexer(RegexLexer):
    __doc__ = '\n    For SourcePawn source code with preprocessor directives.\n\n    .. versionadded:: 1.6\n    '
    name = 'SourcePawn'
    aliases = ['sp']
    filenames = ['*.sp']
    mimetypes = ['text/x-sourcepawn']
    _ws = '(?:\\s|//.*?\\n|/\\*.*?\\*/)+'
    _ws1 = '\\s*(?:/[*].*?[*]/\\s*)*'
    tokens = {'root':[
      (
       '^#if\\s+0', Comment.Preproc, 'if0'),
      (
       '^#', Comment.Preproc, 'macro'),
      (
       '^' + _ws1 + '#if\\s+0', Comment.Preproc, 'if0'),
      (
       '^' + _ws1 + '#', Comment.Preproc, 'macro'),
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text),
      (
       '/(\\\\\\n)?/(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
      (
       '/(\\\\\\n)?\\*(.|\\n)*?\\*(\\\\\\n)?/', Comment.Multiline),
      (
       '[{}]', Punctuation),
      (
       'L?"', String, 'string'),
      (
       "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
      (
       '0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
      (
       '0[0-7]+[LlUu]*', Number.Oct),
      (
       '\\d+[LlUu]*', Number.Integer),
      (
       '\\*/', Error),
      (
       '[~!%^&*+=|?:<>/-]', Operator),
      (
       '[()\\[\\],.;]', Punctuation),
      (
       '(case|const|continue|native|default|else|enum|for|if|new|operator|public|return|sizeof|static|decl|struct|switch)\\b',
       Keyword),
      (
       '(bool|Float)\\b', Keyword.Type),
      (
       '(true|false)\\b', Keyword.Constant),
      (
       '[a-zA-Z_]\\w*', Name)], 
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
       '/\\*(.|\\n)*?\\*/', Comment.Multiline),
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
    SM_TYPES = set(('Action', 'bool', 'Float', 'Plugin', 'String', 'any', 'AdminFlag',
                    'OverrideType', 'OverrideRule', 'ImmunityType', 'GroupId', 'AdminId',
                    'AdmAccessMode', 'AdminCachePart', 'CookieAccess', 'CookieMenu',
                    'CookieMenuAction', 'NetFlow', 'ConVarBounds', 'QueryCookie',
                    'ReplySource', 'ConVarQueryResult', 'ConVarQueryFinished', 'Function',
                    'Action', 'Identity', 'PluginStatus', 'PluginInfo', 'DBResult',
                    'DBBindType', 'DBPriority', 'PropType', 'PropFieldType', 'MoveType',
                    'RenderMode', 'RenderFx', 'EventHookMode', 'EventHook', 'FileType',
                    'FileTimeMode', 'PathType', 'ParamType', 'ExecType', 'DialogType',
                    'Handle', 'KvDataTypes', 'NominateResult', 'MapChange', 'MenuStyle',
                    'MenuAction', 'MenuSource', 'RegexError', 'SDKCallType', 'SDKLibrary',
                    'SDKFuncConfSource', 'SDKType', 'SDKPassMethod', 'RayType', 'TraceEntityFilter',
                    'ListenOverride', 'SortOrder', 'SortType', 'SortFunc2D', 'APLRes',
                    'FeatureType', 'FeatureStatus', 'SMCResult', 'SMCError', 'TFClassType',
                    'TFTeam', 'TFCond', 'TFResourceType', 'Timer', 'TopMenuAction',
                    'TopMenuObjectType', 'TopMenuPosition', 'TopMenuObject', 'UserMsg'))

    def __init__(self, **options):
        self.smhighlighting = get_bool_opt(options, 'sourcemod', True)
        self._functions = set()
        if self.smhighlighting:
            from pygments.lexers._sourcemod_builtins import FUNCTIONS
            self._functions.update(FUNCTIONS)
        (RegexLexer.__init__)(self, **options)

    def get_tokens_unprocessed(self, text):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if self.smhighlighting:
                    if value in self.SM_TYPES:
                        token = Keyword.Type
                    elif value in self._functions:
                        token = Name.Builtin
            yield (
             index, token, value)


class PawnLexer(RegexLexer):
    __doc__ = '\n    For Pawn source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Pawn'
    aliases = ['pawn']
    filenames = ['*.p', '*.pwn', '*.inc']
    mimetypes = ['text/x-pawn']
    _ws = '(?:\\s|//.*?\\n|/[*][\\w\\W]*?[*]/)+'
    _ws1 = '\\s*(?:/[*].*?[*]/\\s*)*'
    tokens = {'root':[
      (
       '^#if\\s+0', Comment.Preproc, 'if0'),
      (
       '^#', Comment.Preproc, 'macro'),
      (
       '^' + _ws1 + '#if\\s+0', Comment.Preproc, 'if0'),
      (
       '^' + _ws1 + '#', Comment.Preproc, 'macro'),
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text),
      (
       '/(\\\\\\n)?/(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
      (
       '/(\\\\\\n)?\\*[\\w\\W]*?\\*(\\\\\\n)?/', Comment.Multiline),
      (
       '[{}]', Punctuation),
      (
       'L?"', String, 'string'),
      (
       "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
      (
       '0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
      (
       '0[0-7]+[LlUu]*', Number.Oct),
      (
       '\\d+[LlUu]*', Number.Integer),
      (
       '\\*/', Error),
      (
       '[~!%^&*+=|?:<>/-]', Operator),
      (
       '[()\\[\\],.;]', Punctuation),
      (
       '(switch|case|default|const|new|static|char|continue|break|if|else|for|while|do|operator|enum|public|return|sizeof|tagof|state|goto)\\b',
       Keyword),
      (
       '(bool|Float)\\b', Keyword.Type),
      (
       '(true|false)\\b', Keyword.Constant),
      (
       '[a-zA-Z_]\\w*', Name)], 
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
       '/\\*(.|\\n)*?\\*/', Comment.Multiline),
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