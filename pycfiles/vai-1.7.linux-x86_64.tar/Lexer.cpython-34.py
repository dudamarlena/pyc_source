# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/lexer/Lexer.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 4016 bytes
from pygments import lexers, util
from ..SymbolLookupDb import SymbolLookupDb
from ..models.TextDocument import CharMeta
from . import token
import os
EXTENSION_TO_LEXER = {'.py': lexers.PythonLexer, 
 '.rb': lexers.RubyLexer, 
 '.pl': lexers.PerlLexer, 
 '.tcl': lexers.TclLexer, 
 '.lua': lexers.LuaLexer, 
 '.as': lexers.ActionScriptLexer, 
 '.c': lexers.CLexer, 
 '.h': lexers.CLexer, 
 '.cpp': lexers.CppLexer, 
 '.hpp': lexers.CppLexer, 
 '.f': lexers.FortranLexer, 
 '.f77': lexers.FortranLexer, 
 '.f90': lexers.FortranLexer, 
 '.sh': lexers.BashLexer, 
 '.bat': lexers.BatchLexer}

def _getLexerInstance(filename):
    """Get the lexer instance from the filename"""
    if filename is None:
        return lexers.TextLexer(stripnl=False, stripall=False)
    ext = os.path.splitext(filename)[1]
    cls = EXTENSION_TO_LEXER.get(ext)
    if cls is not None:
        return cls(stripnl=False, stripall=False)
    try:
        lexer = lexers.get_lexer_for_filename(filename, stripnl=False, stripall=False)
    except util.ClassNotFound:
        lexer = lexers.TextLexer(stripnl=False, stripall=False)

    return lexer


class Lexer:
    __doc__ = '\n    Observes the TextDocument for changes, and performs lexing\n    of its contents synchronously. The text is parsed with the\n    lexer as specified by the document meta information FileType.\n    '

    def __init__(self):
        self._document = None
        self._lexer = None

    def setModel(self, document):
        """Sets the textdocument as a model for the lexer"""
        self._document = document
        filename = self._document.documentMetaInfo('Filename').data()
        self._lexer = _getLexerInstance(filename)
        self._document.contentChanged.connect(self._lexContents)
        file_type_meta = self._document.documentMetaInfo('FileType')
        if file_type_meta.data() is None:
            file_type_meta.setData(self._lexer.name)
        self._lexContents()

    def _lexContents(self):
        """
        Perform lexing of the document every time it changes.
        Fills the meta information on the document.
        """
        if self._lexer is None:
            return
        tokens = self._lexer.get_tokens(self._document.documentText())
        current_line = 1
        current_col = 1
        SymbolLookupDb.clear()
        tokens = self._processTokens(tokens)
        for tok in tokens:
            ttype, token_string = tok
            if ttype in [token.Name, token.Name.Class, token.Name.Function]:
                SymbolLookupDb.add(token_string)
            ttype = self._processToken(ttype, token_string)
            token_lines = token_string.splitlines(True)
            for token_line in token_lines:
                meta = [
                 ttype] * len(token_line)
                self._document.updateCharMeta((current_line, current_col), {CharMeta.LexerToken: meta})
                current_col += len(token_line)
                if token_line.endswith('\n'):
                    current_line += 1
                    current_col = 1
                    continue

    def _processToken(self, ttype, token_string):
        if token_string.startswith('__') and token_string.endswith('__') and ttype is token.Name.Function:
            return token.Name.Function.PythonMagic
        if token_string.startswith('_'):
            if ttype is token.Name.Class:
                return token.Name.Class.PythonPrivate
            if ttype is token.Name.Function:
                return token.Name.Function.PythonPrivate
        elif token_string == 'self':
            return token.Name.Builtin.Pseudo.PythonSelf
        return ttype

    def _processTokens(self, tokens):
        return tokens