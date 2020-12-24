# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/ui/common.py
# Compiled at: 2019-11-20 10:59:30
# Size of source mod 2**32: 1541 bytes
from .base import *
from .wallet import wallet_command
from .shards import shard_command
import hermit.ui.state as state
import traceback, sys
from hermit import __version__

@wallet_command('unlock')
@shard_command('unlock')
def unlock():
    """usage:  unlock

  Explicity unlock the wallet, prompting for shard passwords.

  Many commands will do this implicitly.

    """
    try:
        state.Wallet.unlock()
    except HermitError as e:
        try:
            print_formatted_text('Unable to unlock wallet: ', e)
        finally:
            e = None
            del e

    if state.Wallet.unlocked:
        state.Timeout = DeadTime


@wallet_command('lock')
@shard_command('lock')
def lock():
    """usage:  lock

  Explicity lock the wallet, requiring passwords to be re-entered as
  necessary.

  The wallet will automatically lock after 30 seconds.

    """
    state.Wallet.lock()


@shard_command('clear')
@wallet_command('clear')
def clear():
    """usage:  clear

  Clear screen.
    """
    clear_screen()


@wallet_command('debug')
@shard_command('debug')
def toggle_debug():
    """usage:  debug

  Toggle debug mode on or off.

  When debug mode is active, more information is displayed about
  errors and some additional commands are available.

  The word DEBUG will also appear in Hermit's bottom toolbar.

    """
    state.Debug = not state.Debug


@wallet_command('version')
@shard_command('version')
def unlock():
    """usage:  version

  Print out the version of hermit currently running.
  
  
    """
    print_formatted_text(__version__)