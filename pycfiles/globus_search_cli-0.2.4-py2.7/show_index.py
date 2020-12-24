# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/commands/show_index.py
# Compiled at: 2018-12-14 13:47:34
from globus_search_cli.config import get_search_client
from globus_search_cli.parsing import globus_cmd, index_argument
from globus_search_cli.printing import format_output

@globus_cmd('show-index', help='Display information about an index')
@index_argument
def show_index_cmd(index_id):
    search_client = get_search_client()
    format_output(search_client.get_index(index_id).data)