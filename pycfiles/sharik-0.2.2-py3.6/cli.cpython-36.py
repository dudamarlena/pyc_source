# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sharik/cli.py
# Compiled at: 2019-12-14 09:29:54
# Size of source mod 2**32: 1968 bytes
import click
from typing import Tuple, Any, BinaryIO
from .data_sources import InlineDataSource, FileDataSource
from .builder import SharikBuilder

def _process_inline(_ctx: click.Context, _param: Any, values: Tuple[str]) -> Tuple[(Tuple[(str, bytes)], ...)]:

    def _gen_element(value):
        first_equals = value.find('=')
        if first_equals <= 0:
            raise click.BadParameter('Must be of the form key=value')
        return (
         value[:first_equals], value[first_equals + 1:].encode('utf-8'))

    return tuple(_gen_element(value) for value in values)


@click.command()
@click.option('-x', 'trace', is_flag=True, required=False, default=False, help='Print each step to standard output')
@click.option('--command', type=str, required=True, help='Shell command to be run after unpacking')
@click.option('--add', type=click.Path(exists=True), multiple=True, help='File to be added')
@click.option('--inline', type=str, multiple=True, help='Inline parameters to be added', callback=_process_inline)
@click.option('--clear-glob', type=str, multiple=True, help='Files to be represented without compression/encoding')
@click.option('-o', '--output', type=click.File(mode='wb'), required=True, help='File to which to output the result, can be - for stdout')
def cli_main(trace: bool=False, command: str='/bin/false', add: Tuple[(str, ...)]=(), inline: Tuple[(Tuple[(str, bytes)], ...)]=(), clear_glob: Tuple[(str, ...)]=(), output: BinaryIO=None):
    builder = SharikBuilder(command.encode('utf-8'), trace)
    for element in add:
        builder.add_data_source(FileDataSource(element))

    if len(inline) > 0:
        builder.add_data_source(InlineDataSource(inline))
    for element in clear_glob:
        builder.add_clear_glob(element)

    output.write(builder.build())


if __name__ == '__main__':
    cli_main()