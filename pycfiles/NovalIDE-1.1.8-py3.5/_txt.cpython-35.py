# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/lexer/_txt.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 2016 bytes
from noval import _
from noval.syntax import syndata, lang
import os, noval.util.appdirs as appdirs
from noval.editor import text as texteditor
import noval.imageutils as imageutils

class SyntaxColorer(syndata.BaseSyntaxcolorer):

    def __init__(self, text):
        syndata.BaseSyntaxcolorer.__init__(self, text)

    def schedule_update(self, event, use_coloring=True):
        """
            文本文件不需要语法着色,故这里方法体为空
        """
        self.allow_colorizing = use_coloring


class SyntaxLexer(syndata.BaseLexer):
    __doc__ = 'SyntaxData object for many C like languages'
    SYNTAX_ITEMS = []

    def __init__(self):
        syndata.BaseLexer.__init__(self, lang.ID_LANG_TXT)

    def GetShowName(self):
        return 'Plain Text'

    def GetDefaultExt(self):
        return 'txt'

    def GetExt(self):
        return 'txt text'

    def GetDocTypeName(self):
        return 'Text Document'

    def GetViewTypeName(self):
        return _('Text Editor')

    def GetDocTypeClass(self):
        return texteditor.TextDocument

    def GetViewTypeClass(self):
        return texteditor.TextView

    def GetDocIcon(self):
        return imageutils.getTextIcon()

    def GetDescription(self):
        return _('Text File')

    def GetSampleCode(self):
        sample_file_path = os.path.join(appdirs.get_app_data_location(), 'sample', 'txt.sample')
        return self.GetSampleCodeFromFile(sample_file_path)

    def GetColorClass(self):
        return SyntaxColorer