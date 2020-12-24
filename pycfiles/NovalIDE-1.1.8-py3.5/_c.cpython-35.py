# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/lexer/_c.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 4459 bytes
from noval import _
from noval.syntax import syndata, lang
import noval.util.appdirs as appdirs, os, noval.editor.code as codeeditor, noval.imageutils as imageutils
from noval.syntax.pat import *
kwlist = [
 'auto', 'double', 'int', 'struct', 'break', 'else', 'long', 'switch', 'case', 'enum',
 'register', 'typedef', 'char', 'extern', 'return', 'union', 'const', 'float', 'short', 'unsigned',
 'continue', 'for', 'signed', 'void', 'default', 'goto', 'sizeof', 'volatile', 'do', 'if', 'while', 'static']
_builtinlist = [
 'printf', 'scanf', 'getchar', 'putchar', 'time', 'strcpy', 'strcmp', 'isupper', 'memset', 'islower', 'isalpha', 'isdigit', 'toupper',
 'tolower', 'ceil', 'floor', 'sqrt', 'pow', 'abs', 'rand', 'system', 'exit', 'srand']

def make_pat(kw_list):
    kw = get_keyword_pat(kw_list)
    builtin = get_builtin_pat(_builtinlist)
    cregx = stringprefix + '/\\*((?!(\\*/)).)*(\\*/)?'
    comment = matches_any('comment', [cregx])
    pretreatment = matches_any('preprocess', ['#((?!\\n).)*'])
    number = get_number_pat()
    sqstring = get_sqstring_pat()
    dqstring = get_dqstring_pat()
    string = matches_any('string', [sqstring, dqstring])
    return kw + '|' + builtin + '|' + comment + '|' + pretreatment + '|' + string + '|' + number + '|' + matches_any('SYNC', ['\\n'])


prog = get_prog(make_pat(kwlist))

class SyntaxColorer(syndata.BaseSyntaxcolorer):

    def __init__(self, text):
        syndata.BaseSyntaxcolorer.__init__(self, text)
        self.prog = prog
        self._config_tags()

    def _config_tags(self):
        self.tagdefs.update({
         'stdin'})

    def AddTag(self, head, match_start, match_end, key, value, chars):
        if key == 'preprocess':
            key = 'stdin'
        syndata.BaseSyntaxcolorer.AddTag(self, head, match_start, match_end, key, value, chars)


class SyntaxLexer(syndata.BaseLexer):
    __doc__ = 'SyntaxData object for Python'
    SYNTAX_ITEMS = []

    def __init__(self):
        lang_id = lang.RegisterNewLangId('ID_LANG_C')
        syndata.BaseLexer.__init__(self, lang_id)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetDescription(self):
        return _('C Source File')

    def GetExt(self):
        return 'c'

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '/*', '*/']

    def GetShowName(self):
        return 'C'

    def GetDefaultExt(self):
        return 'c'

    def GetDocTypeName(self):
        return 'C Document'

    def GetViewTypeName(self):
        return _('C Editor')

    def GetDocTypeClass(self):
        return codeeditor.CodeDocument

    def GetViewTypeClass(self):
        return codeeditor.CodeView

    def GetDocIcon(self):
        return imageutils.load_image('', 'file/c_file.gif')

    def GetCommentTemplate(self):
        return '/*******************************************************************************\n* Name: {File}\n* Copyright: (c) {Author} {Year}\n* Author: {Author}\n* Created: {Date}\n* Description:\n* Licence:     <your licence>\n********************************************************************************/\n'

    def GetColorClass(self):
        return SyntaxColorer

    def IsVisible(self):
        return False

    def GetKeywords(self):
        return kwlist + _builtinlist