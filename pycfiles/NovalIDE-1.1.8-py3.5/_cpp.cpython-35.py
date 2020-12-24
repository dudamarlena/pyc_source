# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/lexer/_cpp.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 3899 bytes
from noval import _
from noval.syntax import syndata, lang
import noval.util.appdirs as appdirs, os, noval.editor.code as codeeditor, noval.imageutils as imageutils, _c
from noval.syntax.pat import *
kwlist = _c.kwlist + ['class', 'namespace', 'public', 'private', 'protected', 'virtual', 'friend']

def make_pat(kw_list):
    pat = _c.make_pat(kw_list)
    comment_uniline = matches_any('comment_uniline', ['//((?!\\n).)*'])
    return pat + '|' + comment_uniline


prog = get_prog(make_pat(kwlist))
idprog = get_id_prog()

class SyntaxColorer(_c.SyntaxColorer):

    def __init__(self, text):
        _c.SyntaxColorer.__init__(self, text)
        self.prog = prog
        self.idprog = idprog

    def AddTag(self, head, match_start, match_end, key, value, chars):
        if key == 'comment_uniline':
            key = 'comment'
        _c.SyntaxColorer.AddTag(self, head, match_start, match_end, key, value, chars)
        if value in ('class', ):
            m1 = self.idprog.match(chars, match_end)
            if m1:
                a, b = m1.span(1)
                self.text.tag_add('definition', head + '+%dc' % match_start, head + '+%dc' % match_end)

    def _config_tags(self):
        _c.SyntaxColorer._config_tags(self)
        self.tagdefs.update({
         'definition'})


class SyntaxLexer(syndata.BaseLexer):
    __doc__ = 'SyntaxData object for Python'
    SYNTAX_ITEMS = []

    def __init__(self):
        lang_id = lang.RegisterNewLangId('ID_LANG_CPP')
        syndata.BaseLexer.__init__(self, lang_id)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetDescription(self):
        return _('C++ Source File')

    def GetExt(self):
        return 'cc c++ cpp cxx hh h++ hpp hxx'

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '//']

    def GetShowName(self):
        return 'C/C++'

    def GetDefaultExt(self):
        return 'cpp'

    def GetDocTypeName(self):
        return 'C++ Document'

    def GetViewTypeName(self):
        return _('C++ Editor')

    def GetDocTypeClass(self):
        return codeeditor.CodeDocument

    def GetViewTypeClass(self):
        return codeeditor.CodeView

    def GetDocIcon(self):
        return imageutils.load_image('', 'file/cpp.png')

    def GetSampleCode(self):
        sample_file_path = os.path.join(appdirs.get_app_data_location(), 'sample', 'cpp.sample')
        return self.GetSampleCodeFromFile(sample_file_path)

    def GetCommentTemplate(self):
        return '//******************************************************************************\n// Name: {File}\n// Copyright: (c) {Author} {Year}\n// Author: {Author}\n// Created: {Date}\n// Description:\n// Licence:     <your licence>\n//******************************************************************************\n'

    def GetColorClass(self):
        return SyntaxColorer

    def GetKeywords(self):
        return kwlist + _c._builtinlist