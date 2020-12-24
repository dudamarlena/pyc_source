# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/__main__.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 818 bytes
import click, click_log
import onepassword_tools.ssh_add as ssh_add
import onepassword_tools.new_server_account as new_server_account
import onepassword_tools.new_ssh_key as new_ssh_key
import onepassword_tools.new_website_account as new_website_account
import onepassword_tools.new_database_account as new_database_account
from onepassword_tools.lib.Log import logger
click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
def start():
    pass


start.add_command(ssh_add.ssh_add)
start.add_command(new_server_account.new_server_account)
start.add_command(new_ssh_key.new_ssh_key)
start.add_command(new_website_account.new_website_account)
start.add_command(new_database_account.new_database_account)
if __name__ == '__main__':
    start()