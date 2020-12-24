# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mdt/main.py
# Compiled at: 2019-09-10 14:32:03
# Size of source mod 2**32: 5401 bytes
"""MDT - The Mendel Development Tool

This is the main CLI dispatch routine that teases out the command line and runs
the appropriate command.

Copyright 2019 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import socket, sys
try:
    import paramiko, zeroconf
except ImportError:
    sys.stderr.write("Couldn't load paramiko or zeroconf -- perhaps you need to install them?\r\n")
    sys.stderr.write("On Debian derivatives, 'apt-get install python3-paramiko python3-zeroconf'.\r\n")
    sys.exit(1)

from mdt import config
from mdt import devices
from mdt import files
from mdt import keys
from mdt import shell
import mdt, warnings
warnings.filterwarnings(action='ignore',
  message='.*signer and verifier have been deprecated.*',
  module='.*paramiko.rsakey')
warnings.filterwarnings(action='ignore',
  message='.*encode_point has been deprecated on EllipticCurvePublicNumbers.*',
  module='.*paramiko.kex_ecdh_nist')
warnings.filterwarnings(action='ignore',
  message='.*Support for unsafe construction of public numbers.*',
  module='.*paramiko.kex_ecdh_nist')
MDT_USAGE_HELP = '\nUsage: mdt <subcommand> [<options>]\n\nWhere <subcommand> may be one of the following:\n    help              - this command, gets help on another command.\n    devices           - lists all detected devices.\n    wait-for-device   - waits for a device to be discovered on the network\n    get               - gets an MDT variable value\n    set               - sets an MDT variable value\n    clear             - clears an MDT variable\n    genkey            - generates an SSH key for connecting to a device\n    pushkey           - pushes an SSH public key to a device\n    setkey            - imports a PEM-format SSH private key into the MDT\n                        keystore\n    resetkeys         - removes all keys from the given board and resets key\n                        authentication to factory defaults\n    shell             - opens an interactive shell to a device\n    exec              - runs a shell command and returns the output and the\n                        exit code\n    install           - installs a Debian package using mdt-install-package on\n                        the device\n    push              - pushes a file (or files) to the device\n    pull              - pulls a file (or files) from the device\n    reboot            - reboots a device\n    reboot-bootloader - reboots a device into the bootloader\n    version           - prints which version of MDT this is\n\nUse "mdt help <subcommand>" for more details.\n'

class HelpCommand:
    __doc__ = 'Usage: mdt help [<subcommand>]\n\nGets additional information about a given subcommand, or returns a summary\nof subcommands available.\n'

    def run(self, args):
        if len(args) <= 1:
            print(MDT_USAGE_HELP)
            return 1
        else:
            subcommand = args[1].lower()
            if subcommand in COMMANDS:
                command = COMMANDS[subcommand]
                if command.__doc__:
                    print(command.__doc__)
                else:
                    print("No help is available for subcommand '{0}' -- please yell at the developers. :)".format(subcommand))
            else:
                print("Unknown subcommand '{0}' -- try 'mdt help' for a list".format(subcommand))


class VersionCommand:
    __doc__ = 'Usage: mdt version\n\nPrints the MDT version.\n'

    def run(self, args):
        print('MDT version {0}'.format(mdt.__version__))


COMMANDS = {'clear':config.ClearCommand(), 
 'devices':devices.DevicesCommand(), 
 'exec':shell.ExecCommand(), 
 'genkey':keys.GenKeyCommand(), 
 'get':config.GetCommand(), 
 'help':HelpCommand(), 
 'install':files.InstallCommand(), 
 'pull':files.PullCommand(), 
 'push':files.PushCommand(), 
 'pushkey':shell.PushKeyCommand(), 
 'reboot':shell.RebootCommand(), 
 'reboot-bootloader':shell.RebootBootloaderCommand(), 
 'resetkeys':shell.ResetKeysCommand(), 
 'set':config.SetCommand(), 
 'setkey':keys.SetKeyCommand(), 
 'shell':shell.ShellCommand(), 
 'wait-for-device':devices.DevicesWaitCommand(), 
 'version':VersionCommand()}

def main():
    try:
        if len(sys.argv) <= 1:
            exit(COMMANDS['help'].run([]))
        else:
            command = sys.argv[1].lower()
        if command == '--help':
            command = 'help'
        if command in COMMANDS:
            command = COMMANDS[command]
            exit(command.run(sys.argv[1:]))
        print("Unknown command '{0}': try 'mdt help'".format(command))
        return 1
    except KeyboardInterrupt:
        print()
        exit(1)


if __name__ == '__main__':
    main()