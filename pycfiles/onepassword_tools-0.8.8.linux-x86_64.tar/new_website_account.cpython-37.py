# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/new_website_account/new_website_account.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 929 bytes
import onepassword_tools.lib.OnePasswordLoginItem as OnePasswordLoginItem
from onepassword_tools.lib.NewItemCommand import NewItemCommand, new_item_command_options, new_item_command_password
import click

@click.command()
@new_item_command_options
@new_item_command_password
@click.option('--url', help='URL of the website where the account is created', prompt=True, required=True)
@click.option('--username', help='Account username', prompt=True, required=True)
def new_website_account(url, title, username, password, password_length, return_field, vault, account, notes, do_not_ask_credentials):
    """Create a new Login item in 1Password with the given credentials."""
    NewWebsiteAccount(**locals()).run()


class NewWebsiteAccount(NewItemCommand):
    hostname = None
    hostname: str
    onePasswordItemClass = OnePasswordLoginItem
    titleTemplate = 'ACCOUNT {username} ON {url}'
    url = None
    url: str
    username = None
    username: str