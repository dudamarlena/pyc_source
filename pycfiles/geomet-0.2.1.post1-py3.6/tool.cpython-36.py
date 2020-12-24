# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/geomet/tool.py
# Compiled at: 2018-12-02 19:19:55
# Size of source mod 2**32: 3796 bytes
"""Simple CLI for converting between WKB/WKT and GeoJSON

Example usage:

  $ echo "POINT (0.9999999 0.9999999)"   > | geomet --wkb -   > | geomet --wkt --precision 7 -
  POINT (0.9999999 0.9999999)

"""
from binascii import a2b_hex
from binascii import b2a_hex
import json, logging, sys, click
from geomet import util, wkb, wkt
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def configure_logging(verbosity):
    log_level = max(10, 30 - 10 * verbosity)
    logging.basicConfig(stream=(sys.stderr), level=log_level)


def translate(text, output_format='json', indent=None, precision=-1):
    if text.startswith('{'):
        geom = json.loads(text)
    else:
        if text.startswith(('G', 'L', 'M', 'P')):
            geom = wkt.loads(text)
        else:
            geom = wkb.loads(a2b_hex(text))
        if output_format == 'wkb':
            output = b2a_hex(wkb.dumps(geom))
        else:
            if output_format == 'wkt':
                kwds = {}
                if precision >= 0:
                    kwds['decimals'] = precision
                output = (wkt.dumps)(geom, **kwds)
            else:
                if precision >= 0:
                    geom = util.round_geom(geom, precision)
                output = json.dumps(geom, indent=indent, sort_keys=True)
    return output


@click.command(short_help='Convert between WKT or hex-encoded WKB and GeoJSON.',
  context_settings=CONTEXT_SETTINGS)
@click.argument('input', default='-', required=False)
@click.option('--verbose', '-v', count=True, help='Increase verbosity.')
@click.option('--quiet', '-q', count=True, help='Decrease verbosity.')
@click.option('--json', 'output_format', flag_value='json', default=True, help='JSON output.')
@click.option('--wkb', 'output_format', flag_value='wkb', help='Hex-encoded WKB output.')
@click.option('--wkt', 'output_format', flag_value='wkt', help='WKT output.')
@click.option('--precision', type=int, default=(-1), help='Decimal precision of JSON and WKT coordinates.')
@click.option('--indent', default=None, type=int, help='Indentation level for pretty printed output')
def cli(input, verbose, quiet, output_format, precision, indent):
    """Convert text read from the first positional argument, stdin, or
    a file to GeoJSON and write to stdout."""
    verbosity = verbose - quiet
    configure_logging(verbosity)
    logger = logging.getLogger('geomet')
    try:
        src = click.open_file(input).readlines()
    except IOError:
        src = [
         input]

    stdout = click.get_text_stream('stdout')
    try:
        for line in src:
            text = line.strip()
            logger.debug('Input: %r', text)
            output = translate(text,
              output_format=output_format,
              indent=indent,
              precision=precision)
            logger.debug('Output: %r', output)
            stdout.write(output)
            stdout.write('\n')

        sys.exit(0)
    except Exception:
        logger.exception('Failed. Exception caught')
        sys.exit(1)


if __name__ == '__main__':
    cli()