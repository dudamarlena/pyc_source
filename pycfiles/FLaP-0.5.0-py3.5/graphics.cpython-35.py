# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\substitutions\graphics.py
# Compiled at: 2016-10-02 02:00:12
# Size of source mod 2**32: 2908 bytes
from re import compile
from flap.substitutions.commons import Substitution, LinkSubstitution

class GraphicsPath(Substitution):
    __doc__ = '\n    Detect the \\graphicspath directive and adjust the following \\includegraphics\n    inclusions accordingly.\n    '

    def __init__(self, delegate, flap):
        super().__init__(delegate, flap)

    def prepare_pattern(self):
        return compile('\\\\graphicspath{{?([^}]+)}?}')

    def replacements_for(self, fragment, match):
        r"""
        A \graphicspath directive is not replaced by anything.
        """
        self.flap.set_graphics_directory(match.group(1))
        return []


class IncludeGraphics(LinkSubstitution):
    __doc__ = '\n    Detects "\\includegraphics". When one is detected, it produces a new fragment\n    where the link to the file is corrected.\n    '

    def __init__(self, delegate, flap):
        super().__init__(delegate, flap)

    def prepare_pattern(self):
        pattern = '\\\\includegraphics(?:\\s*\\[[^\\]]+\\])?\\s*\\{([^\\}]+)\\}'
        return compile(pattern)

    def find(self, fragment, reference):
        return self.flap.find_graphics(fragment, reference, self.extensions_by_priority())

    def extensions_by_priority(self):
        return [
         'pdf', 'eps', 'png', 'jpg']

    def notify(self, fragment, graphic):
        return self.flap.on_include_graphics(fragment, graphic)


class Overpic(IncludeGraphics):
    __doc__ = "\n    Adjust 'overpic' environment. Only the opening clause is adjusted.\n    "

    def __init__(self, delegate, proxy):
        super().__init__(delegate, proxy)

    def prepare_pattern(self):
        pattern = '\\\\begin{overpic}\\s*(?:\\[(?:[^\\]]+)\\])*\\{([^\\}]+)\\}'
        return compile(pattern)


class IncludeSVG(IncludeGraphics):
    __doc__ = '\n    Detects "\\includesvg". When one is detected, it produces a new fragment\n    where the link to the file is corrected.\n    '

    def prepare_pattern(self):
        pattern = '\\\\includesvg\\s*(?:\\[(?:[^\\]]+)\\])*\\{([^\\}]+)\\}'
        return compile(pattern)

    def extensions_by_priority(self):
        return [
         'svg']

    def notify(self, fragment, graphic):
        return self.flap.on_include_SVG(fragment, graphic)