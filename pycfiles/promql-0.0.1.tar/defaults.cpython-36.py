# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/styles/defaults.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 3696 bytes
__doc__ = '\nThe default styling.\n'
from __future__ import unicode_literals
from prompt_tool_kit.token import Token
__all__ = ('DEFAULT_STYLE_EXTENSIONS', 'default_style_extensions')
DEFAULT_STYLE_EXTENSIONS = {Token.SearchMatch: 'noinherit reverse', 
 Token.SearchMatch.Current: 'noinherit #ffffff bg:#448844 underline', 
 Token.SelectedText: 'reverse', 
 Token.CursorColumn: 'bg:#dddddd', 
 Token.CursorLine: 'underline', 
 Token.ColorColumn: 'bg:#ccaacc', 
 Token.MatchingBracket: '', 
 Token.MatchingBracket.Other: '#000000 bg:#aacccc', 
 Token.MatchingBracket.Cursor: '#ff8888 bg:#880000', 
 Token.MultipleCursors.Cursor: '#000000 bg:#ccccaa', 
 Token.LineNumber: '#888888', 
 Token.LineNumber.Current: 'bold', 
 Token.Tilde: '#8888ff', 
 Token.Prompt: '', 
 Token.Prompt.Arg: 'noinherit', 
 Token.Prompt.Search: 'noinherit', 
 Token.Prompt.Search.Text: '', 
 Token.Toolbar.Search: 'bold', 
 Token.Toolbar.Search.Text: 'nobold', 
 Token.Toolbar.System: 'bold', 
 Token.Toolbar.System.Text: 'nobold', 
 Token.Toolbar.Arg: 'bold', 
 Token.Toolbar.Arg.Text: 'nobold', 
 Token.Toolbar.Validation: 'bg:#550000 #ffffff', 
 Token.WindowTooSmall: 'bg:#550000 #ffffff', 
 Token.Toolbar.Completions: 'bg:#bbbbbb #000000', 
 Token.Toolbar.Completions.Arrow: 'bg:#bbbbbb #000000 bold', 
 Token.Toolbar.Completions.Completion: 'bg:#bbbbbb #000000', 
 Token.Toolbar.Completions.Completion.Current: 'bg:#444444 #ffffff', 
 Token.Menu.Completions: 'bg:#bbbbbb #000000', 
 Token.Menu.Completions.Completion: '', 
 Token.Menu.Completions.Completion.Current: 'bg:#888888 #ffffff', 
 Token.Menu.Completions.Meta: 'bg:#999999 #000000', 
 Token.Menu.Completions.Meta.Current: 'bg:#aaaaaa #000000', 
 Token.Menu.Completions.MultiColumnMeta: 'bg:#aaaaaa #000000', 
 Token.Scrollbar: 'bg:#888888', 
 Token.Scrollbar.Button: 'bg:#444444', 
 Token.Scrollbar.Arrow: 'bg:#222222 #888888 bold', 
 Token.AutoSuggestion: '#666666', 
 Token.TrailingWhiteSpace: '#999999', 
 Token.Tab: '#999999', 
 Token.Aborted: '#888888', 
 Token.Digraph: '#4444ff'}
default_style_extensions = DEFAULT_STYLE_EXTENSIONS