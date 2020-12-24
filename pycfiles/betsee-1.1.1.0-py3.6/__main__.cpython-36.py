# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/__main__.py
# Compiled at: 2019-09-27 02:43:45
# Size of source mod 2**32: 9706 bytes
"""
Main entry point of this application's command line interface (CLI).

This submodule is a thin wrapper intended to be:

* Indirectly imported and run from external entry point scripts installed by
  setuptools (e.g., the ``betsee`` command).
* Directly imported and run from the command line (e.g., via
  ``python -m betsee.cli``).
"""
import sys
from betsee import guimetadata, guimetadeps

class _BetseNotFoundException(Exception):
    __doc__ = "\n    Exception raised on detecting BETSE (i.e., this application's core\n    mandatory dependency) to be unimportable by the active Python interpreter.\n\n    Design\n    ----------\n    This subclass intentionally complies with the public API of the\n    :class:`betsee.guiexception.BetseeException` superclass to enable duck\n    typing between the two classes (e.g., by the\n    :func:`betsee.util.io.ioerr.show_exception` function). As the\n    :mod:`betsee.guiexception` submodule necessarily imports from and hence\n    assumes the importability of the mandatory third-party :mod:`PySide2`\n    package whose importability has *not* yet been validated at this early time\n    in the application lifecycle, this submodule *cannot* safely import from\n    that submodule and hence explicitly subclass that superclass.\n    "

    def __init__(self, title, synopsis, exegesis):
        super().__init__(synopsis)
        self.title = title
        self.synopsis = synopsis
        self.exegesis = exegesis


def main(arg_list: list=None) -> int:
    """
    Run this application's command-line interface (CLI) with the passed
    arguments if non-``None`` *or* with the arguments passed on the command
    line (i.e., :attr:`sys.argv`) otherwise.

    This function is provided as a convenience to callers requiring procedural
    functions rather than conventional methods (e.g., :mod:`setuptools`).

    Parameters
    ----------
    arg_list : list
        List of zero or more arguments to pass to this interface. Defaults to
        ``None``, in which case arguments passed on the command line (i.e.,
        :attr:`sys.argv`) will be used instead.

    Returns
    ----------
    int
        Exit status of this interface and hence this process as an unsigned
        byte (i.e., integer in the range ``[0, 255]``).
    """
    try:
        _die_unless_betse()
    except _BetseNotFoundException as exception:
        return _show_betse_exception(exception)

    from betsee.guiappmeta import BetseeAppMeta
    from betsee.cli.guicli import BetseeCLI
    BetseeAppMeta()
    return BetseeCLI().run(arg_list)


def _die_unless_betse() -> None:
    """
    Raise an exception unless BETSE, the principal mandatory dependency of this
    application, is **satisfied** (i.e., both importable and of a version
    greater than or equal to that required by this application).

    Raises
    ----------
    _BetseNotFoundException
        If BETSE is unsatisfied (i.e., either unimportable or of a version
        less than that required by this application).
    """
    EXCEPTION_TITLE = 'BETSE Unsatisfied'
    try:
        import betse
    except ImportError as import_error:
        raise _BetseNotFoundException(title=EXCEPTION_TITLE,
          synopsis='Mandatory dependency BETSE not found.',
          exegesis='Python package "betse" unimportable.') from import_error

    BETSE_VERSION_PARTS = guimetadata._convert_version_str_to_tuple(guimetadeps.BETSE_VERSION)
    if betse.__version_info__ != BETSE_VERSION_PARTS:
        raise _BetseNotFoundException(title=EXCEPTION_TITLE,
          synopsis='BETSE version mismatch.',
          exegesis=('{} {} requires BETSE {}, but only BETSE {} is currently installed.'.format(guimetadata.NAME, guimetadata.VERSION, guimetadeps.BETSE_VERSION, betse.__version__)))


def _show_betse_exception(exception: _BetseNotFoundException) -> int:
    """
    Display the passed exception signifying BETSE to be unsatisfied in an
    appropriate manner.

    Parameters
    ----------
    exception : _BetseNotFoundException
        Exception to be displayed.

    Returns
    ----------
    int
        Exit status implying failure (i.e., 1).
    """
    assert isinstance(exception, _BetseNotFoundException), '"{}" not a BETSE-not-found exception.'.format(exception)
    exception_stderr_message = '{} (i.e., {}).'.format(_remove_suffix_if_found(text=(exception.synopsis), suffix='.'), _remove_suffix_if_found(text=(exception.exegesis), suffix='.'))
    print(exception_stderr_message, file=(sys.stderr))
    try:
        from betsee.util.io import guierror
        guierror.show_exception(exception)
    except ImportError as import_error:
        print((str(import_error)), file=(sys.stderr))

    return 1


def _remove_suffix_if_found(text: str, suffix: str) -> str:
    """
    Passed string with the passed suffix removed if present *or* the passed
    string as is otherwise.

    Parameters
    ----------
    text : str
        String to be examined. Since strings are immutable in Python, this
        string remains unmodified.
    suffix : str
        Suffix to remove from this string.

    Returns
    ----------
    str
        Resulting string as described above.

    See Also
    ----------
    :func:`betse.util.type.text.strs.remove_suffix_if_found`
        Original function from which this function is copy-and-pasted. Although
        BETSE is a mandatory dependency of this application, BETSE is *not*
        guaranteed to exist this "early" in the application startup.
    """
    if suffix:
        if text.endswith(suffix):
            return text[:-len(suffix)]
    return text


if __name__ == '__main__':
    sys.exit(main())