# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/commands/remove.py
# Compiled at: 2018-06-21 18:58:03
# Size of source mod 2**32: 1647 bytes
from irk.installers.common import InstallerState
from irk.util.proc import elevate
from irk.util.storage import resolv
from irk.util.storage.database import search_entry, delete_entry, write_database

def remove(package, specific_resolver=None, dry_run=False, force=False):
    entry = search_entry(package)
    if entry is None:
        if not force:
            print('ERR: That package is not installed. Run with -f/--force to bypass this (you will need to specify a resolver with -r)')
            return 1
    if force and specific_resolver is None:
        print('ERR: You must specify a resolver if forcefully removing a package')
        return 1
    else:
        if entry is not None:
            if specific_resolver is None:
                specific_resolver = entry[0][1]
        for resolver in resolv.get_matching_resolvers(package):
            if specific_resolver is None or resolver.get_resolver_name() == specific_resolver:
                print(f"Using resolver {resolver.get_resolver_name()}")
                code = resolver.resolve_to_installer(package).remove(dry_run)
                if code == InstallerState.OK:
                    print('Removed {}'.format(package))
                    if entry is not None:
                        delete_entry(package)
                    write_database()
                    return 0
                if code == InstallerState.INVALID_NAME:
                    return 1
                if code == InstallerState.FAILED:
                    return 1
                if code == InstallerState.NEEDS_SUDO:
                    print('ERR: You probably need to run me as sudo!')
                    elevate()
                    return 1

        print('ERR: Invalid package!')
        return 2