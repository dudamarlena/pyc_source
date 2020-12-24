# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/commands/subject/delete.py
# Compiled at: 2018-12-11 21:16:05
import click
from globus_search_cli.config import get_search_client
from globus_search_cli.parsing import globus_cmd, index_argument
from globus_search_cli.printing import format_output

@globus_cmd('delete', help='Remove all metadata about a subject')
@index_argument
@click.argument('subject')
def delete_func(index_id, subject):
    search_client = get_search_client()
    format_output(search_client.delete_subject(index_id, subject).data)