# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\__init__.py
# Compiled at: 2006-09-23 22:52:29
__doc__ = '\n4Suite: an open-source platform for XML and RDF processing.\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
__all__ = [
 'DEFAULT_ENCODING', 'MAX_PYTHON_RECURSION_DEPTH', '__version__', 'FtException', 'FtWarning', 'GetConfigVars', 'GetConfigVar', 'TranslateMessage']
import sys
if sys.version < '2.2.1':
    raise ImportError('4Suite requires Python 2.2.1 or newer.')
import os
if 'PYTHONCASEOK' in os.environ:
    raise ImportError('4Suite requires case-sensitive imports; unset PYTHONCASEOK environment variable.')
if getattr(sys, 'frozen', False):
    import encodings
import locale
try:
    encoding = locale.getpreferredencoding()
except locale.Error:
    encoding = locale.getpreferredencoding(False)
except AttributeError:
    if sys.platform in ('win32', 'darwin', 'mac'):
        encoding = locale.getdefaultlocale()[1]
    elif hasattr(locale, 'CODESET'):
        encoding = locale.nl_langinfo(locale.CODESET)
    else:
        encoding = locale.getdefaultlocale()[1]

DEFAULT_ENCODING = encoding or 'US-ASCII'
MAX_PYTHON_RECURSION_DEPTH = 10000

class FtException(Exception):
    """
    Base class for all 4Suite-specific exceptions
    """
    __module__ = __name__

    def __init__(self, errorCode, messages, argtuple=(), **kwargs):
        """
        errorCode = Numeric ID for the type of error.
        messages = Mapping of errorCodes to localized error message strings.
        argtuple or keyword args = Values for message string formatting.
        """
        assert not (argtuple and kwargs)
        self.message = messages[errorCode] % (kwargs or argtuple)
        self.errorCode = errorCode
        Exception.__init__(self, self.message, kwargs or argtuple)

    def __getattr__(self, name):
        if name == 'params':
            return self.args[1]
        raise AttributeError(name)

    def __str__(self):
        return self.message

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.message)


class FtWarning(Warning):
    """
    Base class for all 4Suite-specific warnings.
    """
    __module__ = __name__


import warnings
if getattr(warnings.showwarning, '__module__', warnings.showwarning.func_globals['__name__']) == __name__:
    __showwarning = warnings.showwarning
else:

    def __showwarning(message, category, filename, lineno, file=None):
        """
        warnings.showwarning() replacement that word-wraps the message if
        file is a terminal, and doesn't add filename, line, stack info to
        FtWarnings.
        """
        if issubclass(category, FtWarning):
            from Ft.Lib import Wrap, Terminal
            if file is None:
                file = sys.stderr
            terminal = Terminal.Terminal(file)
            message = '%s: %s\n' % (category.__name__, message)
            if terminal.isatty():
                message = Wrap(message, terminal.columns())
            terminal.writetty(message)
            terminal.flush()
        else:
            __showwarning.__base__(message, category, filename, lineno, file)
        return
        return


    __showwarning.__base__ = warnings.showwarning
    warnings.showwarning = __showwarning
try:
    import __config__
except ImportError:
    from distutils.fancy_getopt import wrap_text
    msg = '\n4Suite is having trouble importing the modules it needs.\nThis is usually because the current working directory, which happens\nto be %r at the moment, contains modules with names that are the\nsame as modules that 4Suite is trying to import. For example, 4Suite\ncannot be invoked from the source code directory that contains the\nsetup.py that was used to install 4Suite.\n\nTry changing the current working directory to a suitable location\noutside of the 4Suite source. If you continue to have trouble,\nplease send a message to the 4Suite mailing list at\n4suite@lists.fourthought.com, along with any information that might\nexplain why you got this message.\n' % os.getcwd()
    lines = []
    for chunk in msg.split('\n\n'):
        lines.extend(wrap_text(chunk, 78))
        lines.append('')

    raise SystemExit(('\n').join(lines))

def GetConfigVars(*names):
    """
    With no arguments, return a dictionary of all configuration variables
    relevant for the current installation.  With arguments, return a list
    of values that result from looking up each argument in the configuration
    variable dictionary.

    The following are the currently defined variables and their meaning:

    NAME, FULLNAME, VERSION, URL - fields as given for call to setup()
    BINDIR - directory for user executables
    DATADIR - directory for read-only platform-independent data
    LIBDIR - directory for extra libraries
    LOCALEDIR - directory for message catalogs
    LOCALSTATEDIR - directory for modifiable host-specific data
    SYSCONFIDIR - directory for read-only host-specific data
    """
    if names:
        vals = []
        for name in names:
            vals.append(getattr(__config__, name, None))

        return vals
    else:
        return vars(__config__)
    return


def GetConfigVar(name):
    """
    Return the value of a single variable using the dictionary returned
    by 'get_config_vars()'.  Equivalent to GetConfigVars().get(name)
    """
    return getattr(__config__, name, None)
    return


__version__ = __config__.VERSION
from Ft.Lib import Gettext
if getattr(__config__, 'RESOURCEBUNDLE', False):
    bundle = __name__
else:
    bundle = None
translation = Gettext.GetTranslation(__config__.NAME, __config__.LOCALEDIR, fallback=True, bundle=bundle)
TranslateMessage = translation.gettext
TranslateMessagePlural = translation.ngettext
try:
    import pkg_resources
except ImportError:
    pass
else:
    try:
        pkg_resources.get_distribution(__config__.NAME)
    except pkg_resources.DistributionNotFound:
        pass
    else:
        pkg_resources.declare_namespace(__name__)
        sys.modules[__name__].__dict__.update(globals())