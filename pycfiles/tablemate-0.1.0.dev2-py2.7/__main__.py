# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tablemate/__main__.py
# Compiled at: 2015-04-12 20:32:05
""" Command line interface.
"""
from __future__ import absolute_import, unicode_literals, print_function
import re, click
from . import config
__app_name__ = b'tbm'
config.APP_NAME = __app_name__
CONTEXT_SETTINGS = dict(help_option_names=[
 b'-h', b'--help'], auto_envvar_prefix=__app_name__.upper().replace(b'-', b'_'))

def license_option(*param_decls, **attrs):
    """``--license`` option that prints license information and then exits."""

    def decorator(func):
        """decorator inner wrapper"""

        def callback(ctx, _dummy, value):
            """click option callback"""
            if not value or ctx.resilient_parsing:
                return
            from . import __doc__ as license_text
            license_text = re.sub(b'``([^`]+?)``', lambda m: click.style(m.group(1), bold=True), license_text)
            click.echo(license_text)
            ctx.exit()

        attrs.setdefault(b'is_flag', True)
        attrs.setdefault(b'expose_value', False)
        attrs.setdefault(b'is_eager', True)
        attrs.setdefault(b'help', b'Show the license and exit.')
        attrs[b'callback'] = callback
        return click.option(*(param_decls or ('--license', )), **attrs)(func)

    return decorator


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(message=config.VERSION_INFO)
@license_option()
@click.option(b'-q', b'--quiet', is_flag=True, default=False, help=b'Be quiet (show only errors).')
@click.option(b'-v', b'--verbose', is_flag=True, default=False, help=b'Create extra verbose output.')
@click.option(b'-c', b'--config', metavar=b'FILE', multiple=True, type=click.Path(), help=b'Load given configuration file.')
def cli(quiet=False, verbose=False, config=None):
    """'tablemate' command line tool."""
    pass


config.cli = cli
from . import commands as _
if __name__ == b'__main__':
    __package__ = b'tablemate'
    cli()