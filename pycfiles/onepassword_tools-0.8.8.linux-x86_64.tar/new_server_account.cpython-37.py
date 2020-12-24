# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/new_server_account/new_server_account.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 909 bytes
import onepassword_tools.lib.OnePasswordServerItem as OnePasswordServerItem
from onepassword_tools.lib.NewItemCommand import NewItemCommand, new_item_command_options, new_item_command_password
import click

@click.command()
@new_item_command_options
@new_item_command_password
@click.option('--hostname', help='Host where the account is created', prompt=True, required=True)
@click.option('--username', help='Account username', prompt=True, required=True)
def new_server_account(hostname, username, password, password_length, vault, return_field, account, title, notes, do_not_ask_credentials):
    """Create a new Server item in 1Password with the given credentials."""
    NewServerAccount(**locals()).run()


class NewServerAccount(NewItemCommand):
    hostname = None
    hostname: str
    onePasswordItemClass = OnePasswordServerItem
    titleTemplate = 'USER {username} ON {hostname}'
    username = None
    username: str