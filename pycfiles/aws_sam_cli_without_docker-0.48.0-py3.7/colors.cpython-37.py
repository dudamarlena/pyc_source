# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/colors.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2249 bytes
"""
Wrapper to generated colored messages for printing in Terminal
"""
import click

class Colored:
    __doc__ = '\n    Helper class to add ANSI colors and decorations to text. Given a string, ANSI colors are added with special prefix\n    and suffix characters that are specially interpreted by Terminals to display colors.\n\n        Ex: "message" -> add red color -> \x1b[31mmessage\x1b[0m\n\n    This class serves two purposes:\n        - Hide the underlying library used to provide colors: In this case, we use ``click`` library which is usually\n            used to build a CLI interface. We use ``click`` just to minimize the number of dependencies we add to this\n            project. This class allows us to replace click with any other color library like ``pygments`` without\n            changing callers.\n\n        - Transparently turn off colors: In cases when the string is not written to Terminal (ex: log file) the ANSI\n            color codes should not be written. This class supports the scenario by allowing you to turn off colors.\n            Calls to methods like `red()` will simply return the input string.\n    '

    def __init__(self, colorize=True):
        """
        Initialize the object

        Parameters
        ----------
        colorize : bool
            Optional. Set this to True to turn on coloring. False will turn off coloring
        """
        self.colorize = colorize

    def red(self, msg):
        """Color the input red"""
        return self._color(msg, 'red')

    def green(self, msg):
        """Color the input green"""
        return self._color(msg, 'green')

    def cyan(self, msg):
        """Color the input cyan"""
        return self._color(msg, 'cyan')

    def white(self, msg):
        """Color the input white"""
        return self._color(msg, 'white')

    def yellow(self, msg):
        """Color the input yellow"""
        return self._color(msg, 'yellow')

    def underline(self, msg):
        """Underline the input"""
        if self.colorize:
            return click.style(msg, underline=True)
        return msg

    def _color(self, msg, color):
        """Internal helper method to add colors to input"""
        kwargs = {'fg': color}
        if self.colorize:
            return (click.style)(msg, **kwargs)
        return msg