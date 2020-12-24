# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simo/Projects/pygmount/pygmount/bin/mount_smb_shares.py
# Compiled at: 2014-04-03 06:36:36
from __future__ import unicode_literals, absolute_import
import sys, optparse
from pygmount.utils.mount import MountSmbShares

def main():
    description_msg = b'Mount samba shares into Samba Domain'
    p = optparse.OptionParser(description=description_msg, prog=b'mount-smb-shares', version=b'0.1.1', usage=b'%prog [options]')
    p.add_option(b'--verbose', b'-v', action=b'store_true', default=False, help=b'Enables verbose output')
    p.add_option(b'--file', b'-f', action=b'store', default=None, help=b"Path's mount shares file")
    p.add_option(b'--dry-run', b'-n', action=b'store_true', default=False, dest=b'dry_run', help=b'Perform a trial run with no changes made')
    p.add_option(b'--shell-mode', b'-s', action=b'store_true', default=False, dest=b'shell_mode', help=b'Run commands without Zenity support')
    options, arguments = p.parse_args()
    MountSmbShares(verbose=options.verbose, file=options.file, dry_run=options.dry_run, shell_mode=options.shell_mode).run()
    sys.exit(0)
    return


if __name__ == b'__main__':
    main()