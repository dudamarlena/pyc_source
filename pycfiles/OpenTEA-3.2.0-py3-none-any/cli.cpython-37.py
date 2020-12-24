# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/src/opentea/cli.py
# Compiled at: 2019-07-18 11:38:44
# Size of source mod 2**32: 598 bytes
"""
cli.py

Command line interface for tools in pyavbp
"""
import click
from opentea.noob.check_schema import nob_check_schema, read_serialized_data

@click.command()
@click.argument('schema_f')
def test_schema(schema_f):
    """Test a yaml file for schema."""
    schema = read_serialized_data(schema_f)
    nob_check_schema(schema)
    print('** Congratulations! **')
    print(schema_f + ' SCHEMA structure is valid\nfor opentea requirements.')