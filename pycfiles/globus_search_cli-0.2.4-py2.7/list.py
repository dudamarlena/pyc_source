# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/commands/task/list.py
# Compiled at: 2018-12-18 10:44:51
import click
from globus_search_cli.config import get_search_client
from globus_search_cli.parsing import globus_cmd
from globus_search_cli.printing import format_output

@globus_cmd('list', help='List the 1000 most recent Tasks for an index')
@click.argument('index_id')
def list_cmd(index_id):
    search_client = get_search_client()
    format_output(search_client.get_task_list(index_id).data)