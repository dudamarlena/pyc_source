# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/ui/repl.py
# Compiled at: 2019-08-15 14:28:42
# Size of source mod 2**32: 2681 bytes
import asyncio, traceback
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
import prompt_toolkit.patch_stdout as patch_stdout
from .base import *
from .toolbar import *
import hermit.ui.state as state
Bindings = KeyBindings()

def repl(commands: Dict, mode='', help_command=None):
    commandCompleter = WordCompleter([c for c in commands],
      sentence=True)
    oldSession = state.Session
    state.Session = PromptSession(key_bindings=Bindings, bottom_toolbar=bottom_toolbar,
      refresh_interval=0.1)
    state.Wallet.shards.interface.options = {'bottom_toolbar': bottom_toolbar}
    done = None
    with patch_stdout():
        while not done:
            try:
                unlocked = ' '
                if state.Wallet.unlocked():
                    unlocked = '*'
                else:
                    command_line = state.Session.prompt((HTML('<b>{}{}></b> '.format(unlocked, mode))), completer=commandCompleter).split()
                    if len(command_line) == 0:
                        continue
                    if command_line[0] in commands:
                        command_fn = commands[command_line[0]]
                        try:
                            done = command_fn(*command_line[1:])
                        except TypeError as err:
                            try:
                                if state.Debug:
                                    raise err
                                if help_command is not None:
                                    help_command(command_line[0])
                            finally:
                                err = None
                                del err

                    else:
                        raise HermitError('Unknown command')
            except KeyboardInterrupt:
                continue
            except HermitError as e:
                try:
                    print(e)
                    if state.Debug:
                        traceback.print_exc()
                    continue
                finally:
                    e = None
                    del e

            except EOFError:
                break
            except Exception as err:
                try:
                    print(err)
                    if state.Debug:
                        traceback.print_exc()
                    break
                finally:
                    err = None
                    del err

    state.Session = oldSession


@Condition
def check_timer():
    state.Live = True
    if state.Wallet.unlocked():
        state.Timeout = DeadTime
    return False


@Bindings.add('<any>', filter=check_timer)
def escape_binding(event):
    pass


@Bindings.add('`', eager=True)
def force_check_timer(event):
    check_timer()


@Bindings.add('escape', eager=True)
def force_lock(event):
    state.Wallet.lock()