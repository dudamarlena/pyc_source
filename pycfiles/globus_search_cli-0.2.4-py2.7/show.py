# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/commands/task/show.py
# Compiled at: 2018-12-18 10:41:58
import click
from globus_search_cli.config import get_search_client
from globus_search_cli.parsing import globus_cmd
from globus_search_cli.printing import format_output

@globus_cmd('show', help='Display a Task')
@click.argument('task_id')
def show_cmd(task_id):
    search_client = get_search_client()
    format_output(search_client.get_task(task_id).data)