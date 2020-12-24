# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/syntax/lexer/_python.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 5378 bytes
from noval import _
import keyword
from noval.syntax import syndata, lang
import noval.util.appdirs as appdirs, os, noval.python.pyeditor as pyeditor, noval.imageutils as imageutils, six.moves.builtins as builtins
from noval.syntax.pat import *
builtinlist = [str(name) for name in dir(builtins) if not name.startswith('_') and name not in keyword.kwlist]

def make_pat():
    kw = get_keyword_pat(keyword.kwlist)
    builtin = get_builtin_pat(builtinlist)
    comment = matches_any('comment', ['#[^\\n]*'])
    number = get_number_pat()
    sqstring = get_sqstring_pat()
    dqstring = get_dqstring_pat()
    sq3string = stringprefix + "'''[^'\\\\]*((\\\\.|'(?!''))[^'\\\\]*)*(''')?"
    dq3string = stringprefix + '"""[^"\\\\]*((\\\\.|"(?!""))[^"\\\\]*)*(""")?'
    string = matches_any('string', [sq3string, dq3string, sqstring, dqstring])
    return kw + '|' + builtin + '|' + comment + '|' + string + '|' + number + '|' + matches_any('SYNC', ['\\n'])


prog = get_prog(make_pat())
idprog = get_id_prog()

class SyntaxColorer(syndata.BaseSyntaxcolorer):

    def __init__(self, text):
        syndata.BaseSyntaxcolorer.__init__(self, text)
        self._config_tags()
        self.prog = prog
        self.idprog = idprog

    def _config_tags(self):
        self.tagdefs.update({
         'open_string',
         'definition'})

    def AddTag(self, head, match_start, match_end, key, value, chars):
        syndata.BaseSyntaxcolorer.AddTag(self, head, match_start, match_end, key, value, chars)
        if value in ('def', 'class'):
            m1 = self.idprog.match(chars, match_end)
            if m1:
                a, b = m1.span(1)
                self.text.tag_add('definition', head + '+%dc' % match_start, head + '+%dc' % match_end)


class ShellSyntaxColorer(SyntaxColorer):

    def __init__(self, text):
        SyntaxColorer.__init__(self, text)
        magic_command = matches_any('magic', ['^%[^\\n]*'])
        self.prog = get_prog(make_pat() + '|' + magic_command)

    def _config_tags(self):
        SyntaxColorer._config_tags(self)
        self.tagdefs.update({
         'magic'})

    def _update_coloring(self):
        self.text.tag_remove('TODO', '1.0', 'end')
        self.text.tag_add('SYNC', '1.0', 'end')
        SyntaxColorer._update_coloring(self)


class SyntaxLexer(syndata.BaseLexer):
    __doc__ = 'SyntaxData object for Python'
    SYNTAX_ITEMS = []

    def __init__(self):
        lang_id = lang.RegisterNewLangId('ID_LANG_PYTHON')
        syndata.BaseLexer.__init__(self, lang_id)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         PY_KW, PY_BIN]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetDescription(self):
        return _('Python Script')

    def GetExt(self):
        return 'py pyw'

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '#']

    def GetShowName(self):
        return 'Python'

    def GetDefaultExt(self):
        return 'py'

    def GetDocTypeName(self):
        return 'Python Document'

    def GetViewTypeName(self):
        return _('Python Editor')

    def GetDocTypeClass(self):
        return pyeditor.PythonDocument

    def GetViewTypeClass(self):
        return pyeditor.PythonView

    def GetDocIcon(self):
        return imageutils.getPythonIcon()

    def GetSampleCode(self):
        sample_file_path = os.path.join(appdirs.get_app_data_location(), 'sample', 'python.sample')
        return self.GetSampleCodeFromFile(sample_file_path)

    def GetCommentTemplate(self):
        return '#-------------------------------------------------------------------------------\n# Name:        {File}\n# Purpose:\n#\n# Author:      {Author}\n#\n# Created:     {Date}\n# Copyright:   (c) {Author} {Year}\n# Licence:     <your licence>\n#-------------------------------------------------------------------------------\n'

    def GetColorClass(self):
        return SyntaxColorer

    def GetShellColorClass(self):
        return ShellSyntaxColorer

    def GetKeywords(self):
        return keyword.kwlist + builtinlist