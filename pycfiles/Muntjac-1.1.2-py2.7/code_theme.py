# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/codemirror/client/code_theme.py
# Compiled at: 2013-04-04 15:36:36


class CodeTheme(object):
    DEFAULT = None
    COBALT = None
    ECLIPSE = None
    ELEGANT = None
    MONOKAI = None
    NEAT = None
    NIGHT = None
    RUBYBLUE = None

    def __init__(self, name, Id, theme):
        self._name = name
        self._id = Id
        self._theme = None
        self.setTheme(theme)
        return

    def __str__(self):
        return self._name

    @classmethod
    def byId(cls, Id):
        for s in CodeTheme.values():
            if s.getId() == Id:
                return s

        return

    def setTheme(self, theme):
        self._theme = theme

    def getTheme(self):
        return self._theme

    def getId(self):
        return self._id

    _values = []

    @classmethod
    def values(cls):
        return cls._values


CodeTheme.DEFAULT = CodeTheme('Default', 1, 'default')
CodeTheme.COBALT = CodeTheme('Cobalt', 2, 'cobalt')
CodeTheme.ECLIPSE = CodeTheme('Eclipse', 3, 'eclipse')
CodeTheme.ELEGANT = CodeTheme('Elegant', 4, 'elegant')
CodeTheme.MONOKAI = CodeTheme('Monokai', 5, 'monokai')
CodeTheme.NEAT = CodeTheme('Neat', 6, 'neat')
CodeTheme.NIGHT = CodeTheme('Night', 7, 'night')
CodeTheme.RUBYBLUE = CodeTheme('Ruby Blue', 8, 'rubyblue')
CodeTheme._values = [
 CodeTheme.DEFAULT, CodeTheme.COBALT, CodeTheme.ECLIPSE,
 CodeTheme.ELEGANT, CodeTheme.MONOKAI, CodeTheme.NEAT, CodeTheme.NIGHT,
 CodeTheme.RUBYBLUE]