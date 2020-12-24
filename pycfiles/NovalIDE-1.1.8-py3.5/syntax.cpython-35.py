# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/syntax.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 4339 bytes
import os, noval.util.singleton as singleton, re, noval.util.appdirs as appdirs, json, noval.util.strutils as strutils, noval.util.utils as utils, noval.consts as consts
from noval.syntax_themes import *

@singleton.Singleton
class SyntaxThemeManager(object):
    __doc__ = 'Class Object for managing loaded syntax data. The manager\n    is only created once as a singleton and shared amongst all\n    editor windows\n\n    '
    SYNTAX_THEMES = dict()

    def __init__(self, config=None):
        """Initialize a syntax manager. If the optional
        value config is set the mapping of extensions to
        lexers will be loaded from a config file.
        @keyword config: path of config file to load file extension config from

        """
        self.syntax_set = []
        self.lexers = []
        self.style_set = ''
        self._syntax_themes = {}
        self._ui_themes = {}
        self.LoadSyntaxThemes()
        self.ApplySyntaxTheme(utils.profile_get(consts.SYNTAX_THEME_KEY, consts.DEFAULT_SYNTAX_THEME))

    def LoadSyntaxThemes(self):
        self.AddSyntaxTheme(consts.DEFAULT_SYNTAX_THEME, None, default_light)
        self.AddSyntaxTheme('Default Dark', None, default_dark)
        self.AddSyntaxTheme('Default Dark Green', 'Default Dark', default_dark_green)
        self.AddSyntaxTheme('Default Dark Blue', 'Default Dark', default_dark_blue)
        self.AddSyntaxTheme('Desert Sunset', 'Default Dark', desert_sunset)
        self.AddSyntaxTheme('Zenburn', 'Default Dark', zenburn)
        self.AddSyntaxTheme('IDLE Classic', consts.DEFAULT_SYNTAX_THEME, idle_classic)
        self.AddSyntaxTheme('IDLE Dark', consts.DEFAULT_SYNTAX_THEME, idle_dark)

    def Register(self, lang_lexer):
        for lexer in self.lexers:
            if lang_lexer == lexer:
                return False

        self.lexers.append(lang_lexer)
        return True

    def UnRegister(self, lang_lexer):
        if -1 == self.lexers.index(lang_lexer):
            return False
        self.lexers.remove(lang_lexer)
        return True

    def GetLexer(self, lang_id):
        for lexer in self.lexers:
            if lexer.LangId == lang_id:
                return lexer

        return self.GetLexer(lang.ID_LANG_TXT)

    def GetLangLexerFromExt(self, ext):
        for lexer in self.lexers:
            if lexer.ContainExt(ext):
                return lexer

        return self.GetLexer(lang.ID_LANG_TXT)

    def IsExtSupported(self, ext):
        for lexer in self.lexers:
            if lexer.ContainExt(ext):
                return True

        return False

    def GetLangLexerFromShowname(self, showname):
        for lexer in self.lexers:
            if lexer.GetShowName() == showname:
                return lexer

        return self.GetLexer(lang.ID_LANG_TXT)

    @property
    def Lexers(self):
        return self.lexers

    def AddSyntaxTheme(self, name, parent, settings):
        if name in self._syntax_themes:
            utils.get_logger().warn("Overwriting theme '%s'", name)
        self._syntax_themes[name] = (
         parent, settings)

    def ApplySyntaxTheme(self, name):

        def get_settings(name):
            try:
                parent, settings = self._syntax_themes[name]
            except KeyError:
                utils.get_logger().exception("Can't find theme '%s'" % name)
                return {}

            if callable(settings):
                settings = settings()
            if parent is None:
                return settings
            else:
                result = get_settings(parent)
                for key in settings:
                    if key in result:
                        result[key].update(settings[key])
                    else:
                        result[key] = settings[key]

                return result

        self.SetSyntaxTheme(get_settings(name))

    @classmethod
    def SetSyntaxTheme(cls, style_set):
        cls.SYNTAX_THEMES = style_set

    def get_syntax_options_for_tag(self, tag, **base_options):
        if tag in self.SYNTAX_THEMES:
            base_options.update(self.SYNTAX_THEMES[tag])
        return base_options