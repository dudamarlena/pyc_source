# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/new_database_account/new_database_account.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 1164 bytes
import onepassword_tools.lib.OnePasswordDatabaseItem as OnePasswordDatabaseItem
from onepassword_tools.lib.NewItemCommand import NewItemCommand, new_item_command_options, new_item_command_password
import click

@click.command()
@new_item_command_options
@new_item_command_password
@click.option('--database', help='Database name', prompt=False, required=True)
@click.option('--hostname', help='Host where the account is created', prompt=True, required=True)
@click.option('--port', help='Database port', prompt=False, required=False, default='')
@click.option('--username', help='Account username', prompt=True, required=True)
def new_database_account(hostname, database, port, username, account, notes, password, password_length, return_field, title, vault, do_not_ask_credentials):
    """Create a new Database item in 1Password with the given credentials."""
    NewDatabaseAccount(**locals()).run()


class NewDatabaseAccount(NewItemCommand):
    database = None
    database: str
    hostname = None
    hostname: str
    port = None
    port: str
    titleTemplate = 'USER {username} DB {database} ON {hostname}'
    username = None
    username: str
    onePasswordItemClass = OnePasswordDatabaseItem