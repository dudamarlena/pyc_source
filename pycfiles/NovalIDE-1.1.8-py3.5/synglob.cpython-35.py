# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/synglob.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 2157 bytes
import os, noval.util.singleton as singleton, noval.util.utils as utils, noval.util.strutils as strutils, sys
from noval.syntax import syntax
import noval.imageutils as imageutils, noval.core as core

@singleton.Singleton
class LexerFactory(object):
    __doc__ = 'description of class'

    def CreateLexers(self, lang=''):
        if lang == '':
            lexer_path = os.path.join(utils.get_app_path(), 'noval', 'syntax', 'lexer')
        else:
            lexer_path = os.path.join(utils.get_app_path(), 'noval', lang, 'syntax', 'lexer')
        sys.path.append(lexer_path)
        try:
            for fname in os.listdir(lexer_path):
                if not fname.endswith('.py'):
                    pass
                else:
                    modname = strutils.get_filename_without_ext(fname)
                    module = __import__(modname)
                    if not hasattr(module, 'SyntaxLexer'):
                        pass
                    else:
                        cls_lexer = getattr(module, 'SyntaxLexer')
                        lexer_instance = cls_lexer()
                        lexer_instance.Register()

        except Exception as e:
            utils.get_logger().exception('')
            utils.get_logger().error('load lexer error:%s', e)

    def CreateLexerTemplates(self, docManager, lang=''):
        self.CreateLexers(lang)

    def LoadLexerTemplates(self, docManager):
        for lexer in syntax.SyntaxThemeManager().Lexers:
            utils.get_logger().info('load lexer id:%d description %s ', lexer.LangId, lexer.GetDescription())
            templateIcon = lexer.GetDocIcon()
            if templateIcon is None:
                templateIcon = imageutils.getBlankIcon()
            docTemplate = core.DocTemplate(docManager, lexer.GetDescription(), lexer.GetExtStr(), os.getcwd(), '.' + lexer.GetDefaultExt(), lexer.GetDocTypeName(), lexer.GetViewTypeName(), lexer.GetDocTypeClass(), lexer.GetViewTypeClass(), icon=templateIcon)
            docManager.AssociateTemplate(docTemplate)