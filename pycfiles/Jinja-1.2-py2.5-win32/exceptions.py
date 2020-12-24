# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jinja\exceptions.py
# Compiled at: 2007-11-10 18:27:18
"""
    jinja.exceptions
    ~~~~~~~~~~~~~~~~

    Jinja exceptions.

    :copyright: 2007 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

class TemplateError(RuntimeError):
    pass


class SecurityException(TemplateError):
    """
    Raise if the template designer tried to do something dangerous.
    """
    pass


class FilterNotFound(KeyError, TemplateError):
    """
    Raised if a filter does not exist.
    """

    def __init__(self, message):
        KeyError.__init__(self, message)


class FilterArgumentError(TypeError, TemplateError):
    """
    An argument passed to the filter was invalid.
    """

    def __init__(self, message):
        TypeError.__init__(self, message)


class TestNotFound(KeyError, TemplateError):
    """
    Raised if a test does not exist.
    """

    def __init__(self, message):
        KeyError.__init__(self, message)


class TestArgumentError(TypeError, TemplateError):
    """
    An argument passed to a test function was invalid.
    """

    def __init__(self, message):
        TypeError.__init__(self, message)


class TemplateNotFound(IOError, TemplateError):
    """
    Raised if a template does not exist.
    """

    def __init__(self, name):
        IOError.__init__(self, name)
        self.name = name


class TemplateSyntaxError(SyntaxError, TemplateError):
    """
    Raised to tell the user that there is a problem with the template.
    """

    def __init__(self, message, lineno, filename):
        SyntaxError.__init__(self, message)
        self.lineno = lineno
        self.filename = filename


class TemplateRuntimeError(TemplateError):
    """
    Raised by the template engine if a tag encountered an error when
    rendering.
    """
    pass


class TemplateIncludeError(TemplateError):
    """
    Raised by the `ControlledLoader` if recursive includes where
    detected.
    """
    pass