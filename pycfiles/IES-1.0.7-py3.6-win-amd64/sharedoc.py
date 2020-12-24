# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\sharedoc.py
# Compiled at: 2018-01-16 00:30:32
# Size of source mod 2**32: 3675 bytes
"""
Shared docstrings for parameters that should be documented identically
across different functions.
"""
import re
from six import iteritems
from textwrap import dedent
from toolz import curry
PIPELINE_DOWNSAMPLING_FREQUENCY_DOC = dedent("    frequency : {'year_start', 'quarter_start', 'month_start', 'week_start'}\n        A string indicating desired sampling dates:\n\n        * 'year_start'    -> first trading day of each year\n        * 'quarter_start' -> first trading day of January, April, July, October\n        * 'month_start'   -> first trading day of each month\n        * 'week_start'    -> first trading_day of each week\n    ")
PIPELINE_ALIAS_NAME_DOC = dedent('    name : str\n        The name to alias this term as.\n    ')

def pad_lines_after_first(prefix, s):
    """Apply a prefix to each line in s after the first."""
    return ('\n' + prefix).join(s.splitlines())


def format_docstring(owner_name, docstring, formatters):
    """
    Template ``formatters`` into ``docstring``.

    Parameters
    ----------
    owner_name : str
        The name of the function or class whose docstring is being templated.
        Only used for error messages.
    docstring : str
        The docstring to template.
    formatters : dict[str -> str]
        Parameters for a a str.format() call on ``docstring``.

        Multi-line values in ``formatters`` will have leading whitespace padded
        to match the leading whitespace of the substitution string.
    """
    format_params = {}
    for target, doc_for_target in iteritems(formatters):
        regex = re.compile('^(\\s*)({' + target + '})$', re.MULTILINE)
        matches = regex.findall(docstring)
        if not matches:
            raise ValueError("Couldn't find template for parameter {!r} in docstring for {}.\nParameter name must be alone on a line surrounded by braces.".format(target, owner_name))
        else:
            if len(matches) > 1:
                raise ValueError("Couldn't found multiple templates for parameter {!r}in docstring for {}.\nParameter should only appear once.".format(target, owner_name))
        leading_whitespace, _ = matches[0]
        format_params[target] = pad_lines_after_first(leading_whitespace, doc_for_target)

    return (docstring.format)(**format_params)


def templated_docstring(**docs):
    """
    Decorator allowing the use of templated docstrings.

    Examples
    --------
    >>> @templated_docstring(foo='bar')
    ... def my_func(self, foo):
    ...     '''{foo}'''
    ...
    >>> my_func.__doc__
    'bar'
    """

    def decorator(f):
        f.__doc__ = format_docstring(f.__name__, f.__doc__, docs)
        return f

    return decorator


@curry
def copydoc(from_, to):
    """Copies the docstring from one function to another.
    Parameters
    ----------
    from_ : any
        The object to copy the docstring from.
    to : any
        The object to copy the docstring to.
    Returns
    -------
    to : any
        ``to`` with the docstring from ``from_``
    """
    to.__doc__ = from_.__doc__
    return to