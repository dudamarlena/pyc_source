# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/_utils/table_print.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 5404 bytes
"""
Utilities for table pretty printing using click
"""
from itertools import count, zip_longest
import textwrap
from functools import wraps
import click
MIN_OFFSET = 20

def pprint_column_names(format_string, format_kwargs, margin=None, table_header=None, color='yellow'):
    """

    :param format_string: format string to be used that has the strings, minimum width to be replaced
    :param format_kwargs: dictionary that is supplied to the format_string to format the string
    :param margin: margin that is to be reduced from column width for columnar text.
    :param table_header: Supplied table header
    :param color: color supplied for table headers and column names.
    :return: boilerplate table string
    """
    min_width = 100
    min_margin = 2

    def pprint_wrap(func):
        width, _ = click.get_terminal_size()
        width = max(width, min_width)
        total_args = len(format_kwargs)
        if not total_args:
            raise ValueError('Number of arguments supplied should be > 0 , format_kwargs: {}'.format(format_kwargs))
        width = width - width % total_args
        usable_width_no_margin = int(width) - 1
        usable_width = int(usable_width_no_margin - (margin if margin else min_margin))
        if total_args > int(usable_width / 2):
            raise ValueError('Total number of columns exceed available width')
        width_per_column = int(usable_width / total_args)
        final_arg_width = width_per_column - 1
        format_args = [width_per_column for _ in range(total_args - 1)]
        format_args.extend([final_arg_width])

        @wraps(func)
        def wrap(*args, **kwargs):
            if table_header:
                click.secho('\n' + table_header)
            click.secho(('-' * usable_width), fg=color)
            click.secho((format_string.format)(*format_args, **format_kwargs), fg=color)
            click.secho(('-' * usable_width), fg=color)
            kwargs['format_args'] = format_args
            kwargs['width'] = width_per_column
            kwargs['margin'] = margin if margin else min_margin
            result = func(*args, **kwargs)
            click.secho(('-' * usable_width), fg=color)
            return result

        return wrap

    return pprint_wrap


def wrapped_text_generator(texts, width, margin, **textwrap_kwargs):
    """

    Return a generator where the contents are wrapped text to a specified width.

    :param texts: list of text that needs to be wrapped at specified width
    :param width: width of the text to be wrapped
    :param margin: margin to be reduced from width for cleaner UX
    :param textwrap_kwargs: keyword arguments that are passed to textwrap.wrap
    :return: generator of wrapped text
    """
    for text in texts:
        yield (textwrap.wrap)(text, width=width - margin, **textwrap_kwargs)


def pprint_columns(columns, width, margin, format_string, format_args, columns_dict, color='yellow', **textwrap_kwargs):
    """

    Print columns based on list of columnar text, associated formatting string and associated format arguments.

    :param columns: list of columnnar text that go into columns as specified by the format_string
    :param width: width of the text to be wrapped
    :param margin: margin to be reduced from width for cleaner UX
    :param format_string: A format string that has both width and text specifiers set.
    :param format_args: list of offset specifiers
    :param columns_dict: arguments dictionary that have dummy values per column
    :param color: color supplied for rows within the table.
    :param textwrap_kwargs: keyword arguments that are passed to textwrap.wrap
    :return:
    """
    for columns_text in zip_longest(*wrapped_text_generator(columns, width, margin, **textwrap_kwargs), **{'fillvalue': ''}):
        counter = count()
        for k, _ in columns_dict.items():
            columns_dict[k] = columns_text[next(counter)]

        click.secho((format_string.format)(*format_args, **columns_dict), fg=color)


def newline_per_item(iterable, counter):
    """
    Adds a new line based on the index of a given iterable
    Parameters
    ----------
    iterable: Any iterable that implements __len__
    counter: Current index within the iterable

    Returns
    -------

    """
    if counter < len(iterable) - 1:
        click.echo(message='', nl=True)