# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/commands/entry/create.py
# Compiled at: 2018-12-11 21:16:05
import click
from globus_search_cli.config import get_search_client
from globus_search_cli.parsing import globus_cmd, index_argument
from globus_search_cli.printing import format_output

@globus_cmd('create', help='Create a single GMetaEntry')
@index_argument
@click.argument('source')
def create_func(index_id, source):
    search_client = get_search_client()
    with open(source) as (f):
        format_output(search_client.create_entry(index_id, f.read()).data)