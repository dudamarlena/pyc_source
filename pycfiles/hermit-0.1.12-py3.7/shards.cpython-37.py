# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/ui/shards.py
# Compiled at: 2019-08-15 14:28:42
# Size of source mod 2**32: 9243 bytes
from base64 import b64encode, b64decode
from .base import *
import hermit.ui.state as state
ShardCommands = {}
ShardCommands: Dict

def shard_command(name):
    return command(name, ShardCommands)


@shard_command('build-family-from-phrase')
def build_family_from_phrase():
    """usage: build-family-from-phrase

  Build a shard family from a BIP39 mnemonic phrase.

  Hermit will prompt you in turn for a shard configuration, a BIP39
  phrase, and random data from which to build shards.

  Once the shards have been built, Hermit will ask you to name each
  one and encrypt it with a password.

  These shards will be built in memory. You should run `write` to save
  the shards to the filesystem.

    """
    state.Wallet.shards.create_share_from_wallet_words()


@shard_command('build-family-from-random')
def build_family_from_random():
    """usage: build-family-from-random

  Build a shard family from random data.

  Hermit will prompt you for a shard configuration and then for random
  data to use in building the shards.

  Once the shards have been built, Hermit will ask you to name each
  one and encrypt it with a password.

  These shards will be built in memory. You should run `write` to save
  the shards to the filesystem.

    """
    state.Wallet.shards.create_random_share()


@shard_command('build-family-from-wallet')
def build_family_from_wallet():
    """usage:  build-family-from-wallet

  Build a new shard family from the current wallet.

  Hermit will prompt you to unlock the wallet then for a shard
  configuration and random data to use in building the shards.

  Once the shards have been built, Hermit will ask you to name each
  one and encrypt it with a password.

  These shards will be built in memory. You should run `write` to save
  the shards to the filesystem.

  Running this command will first lock the wallet, forcing you to
  unlock it again.

    """
    state.Wallet.lock()
    state.Wallet.shards.reshard()


@shard_command('list-shards')
def list_shards():
    """usage:  list-shards

  List all shards.

    """
    state.Wallet.shards.list_shards()


@shard_command('import-shard-from-phrase')
def import_shard_from_phrase(name):
    """usage:  import-shard-from-phrase NAME

  Import a shard from an encrypted SLIP39 mnemonic phrase.

  The password for the shard will be the one encoded into the phrase.

  The shard is imported in memory.  You must run the `write` command
  to save shards to the filesystem.

  Examples:

    shards> import-shard-from-phrase shard1
    ...
    shards> write

    """
    state.Wallet.shards.input_shard_words(name)


@shard_command('import-shard-from-qr')
def import_shard_from_qr(name):
    """usage import-shard-from-qr NAME

  Import a shard from a QR code.

  The shard is imported in memory.  You must run the `write` command
  to save shards to the filesystem.

  Examples:

    shards> import-shard-from-qr shard1
    ...
    shards> write

    """
    qr_data = reader.read_qr_code()
    shard_data = b64decode(qr_data)
    state.Wallet.shards.import_shard_qr(name, shard_data)


@shard_command('export-shard-as-phrase')
def export_shard_as_phrase(name):
    """usage:  export-shard-as-phrase NAME

  Print the encrypted SLIP39 mnemonic phrase for the given shard.

    """
    state.Wallet.shards.reveal_shard(name)


@shard_command('export-shard-as-qr')
def export_shard_as_qr(name):
    """usage export-shard-as-qr NAME

  Display a QR code for the given shard.

    """
    shard_data = b64encode(state.Wallet.shards.qr_shard(name)).decode('utf-8')
    displayer.display_qr_code(shard_data, name=name)


@shard_command('copy-shard')
def copy_shard(original, copy):
    """usage:  copy-shard OLD NEW

  Copy a shard, assigning the new copy its own password.

  The new shard is created in memory.  You must run the `write`
  command to save the new shard to the filesystem.

  Examples:

    shards> copy-shard apple pear
    ...
    shards> write

    """
    state.Wallet.shards.copy_shard(original, copy)


@shard_command('delete-shard')
def delete_shard(name):
    """usage:  delete_shard NAME

  Delete a shard.

  Hermit will prompt you to confirm whether or not you really want to
  delete the given shard.

  If you agree, the shard will be deleted in memory.  You must run the
  `write` command to delete the shard from the filesystem.

  Examples:

    shards> delete-shard apple
    ...
    shards> write

    """
    state.Wallet.shards.delete_shard(name)


@shard_command('write')
def write():
    """usage:  write

  Write all shards in memory to the filesystem.

  Metadata (number of shards, shard numbers and names) will be written
  in plain text but all shard content will be encrypted with each
  shard's password.

  You may want to run the `persist` command after running the `write`
  command.

    """
    state.Wallet.shards.save()


@shard_command('persist')
def persist():
    """usage:  persist

  Copies shards from the filesystem to persistent storage.

  Persistent storage defaults to the filesystem but can be configured
  to live in a higher-security location such as a Trusted Platform
  Module (TPM).

    """
    state.Wallet.shards.persist()


@shard_command('backup')
def backup():
    """usage:  backup

  Copies shards from the filesystem to backup storage.

  Backup storage defaults to the filesystem but can be configured as
  necessary.

    """
    state.Wallet.shards.backup()


@shard_command('restore')
def restore():
    """usage:  restore

  Copies shards from backup storage to the filesystem.

    """
    state.Wallet.shards.restore()


@shard_command('reload')
def reload():
    """usage:  reload

  Reload shards in memory from the filesystem.

  This resets any changes made to shards in memory during the current
  session.

    """
    state.Wallet.lock()
    state.Wallet.shards.reload()


@shard_command('quit')
def quit_shards():
    """usage:  quit

Exit shards mode."""
    clear_screen()
    print("You are now in WALLET mode.  Type 'help' for help.\n")
    return True


@shard_command('help')
def shard_help(*args):
    """usage: help [COMMAND]

  Prints out helpful information about Hermit's "shards" mode.

  When called with an argument, prints out helpful information about
  the command with that name.

  Examples:

     shards> help import-shard-from-phrase
     shards> help build-shards-from-random

    """
    if len(args) > 0 and args[0] in ShardCommands:
        print(ShardCommands[args[0]].__doc__)
    else:
        print_formatted_text(HTML('\n  You are in SHARDS mode.  In this mode, Hermit can create and\n  manipulate shards and interact with storage.\n\n  The following commands are supported (try running `help COMMAND` to\n  learn more about each command):\n\n  <b>SHARD FAMILIES</b>\n      <i>build-family-from-phrase</i>\n           Create a shard family from a BIP39 mnemonic phrase\n      <i>build-family-from-random</i>\n           Create a shard family from random data\n      <i>build-family-from-wallet</i>\n           Create a shard family from the current wallet\n  <b>SHARDS</b>\n      <i>list-shards</i>\n          List all existing shards\n      <i>import-shard-from-phrase NAME</i>\n          Input a new shard from an encrypted SLIP39 mnemonic phrase\n      <i>import-shard-from-qr NAME</i>\n          Input a new shard from a QR code\n      <i>export-shard-as-phrase NAME</i>\n          Display the given shard as an encrypted SLIP39 mnemonic phrase\n      <i>export-shard-as-qr NAME</i>\n          Display the given shard as a QR code\n      <i>copy-shard OLD NEW</i>\n          Copy an existing shard with a new password\n      <i>delete-shard NAME</i>\n          Delete a shard\n  <b>STORAGE</b>\n      <i>write</i>\n          Copy shards from memory to the filesystem\n      <i>persist</i>\n          Copy shards from the filesystem to the data store\n      <i>backup</i>\n          Copy shards from filesystem to backup storage\n      <i>restore</i>\n          Copy shards from backup storage to filesystem\n      <i>reload</i>\n          Copy shards from the filesystem into memory\n  <b>WALLET</b>\n      <i>unlock</i>\n          Explicitly unlock the wallet\n      <i>lock</i>\n          Explictly lock the wallet\n  <b>MISC</b>\n      <i>debug</i>\n          Toggle debug mode\n      <i>clear</i>\n          Clear screen\n      <i>quit</i>\n          Return to wallet mode\n\n        '))