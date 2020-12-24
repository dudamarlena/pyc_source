# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mdt/config.py
# Compiled at: 2019-09-10 14:32:03
# Size of source mod 2**32: 6190 bytes
"""
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
import os, sys
CONFIG_BASEDIR = os.path.join(os.path.expanduser('~'), '.config', 'mdt')
CONFIG_ATTRDIR = os.path.join(CONFIG_BASEDIR, 'attribs')
DEFAULT_USERNAME = 'mendel'
DEFAULT_PASSWORD = 'mendel'
DEFAULT_DISABLE_PASSWD_AUTH = 'true'
DEFAULT_ENV_WHITELIST = 'TERM LANG LC_*'

class Config:

    def __init__(self):
        self.ensureConfigDirExists()

    def ensureConfigDirExists(self):
        if not os.path.exists(CONFIG_BASEDIR):
            os.makedirs(CONFIG_BASEDIR, mode=448)
        if not os.path.exists(CONFIG_ATTRDIR):
            os.makedirs(CONFIG_ATTRDIR, mode=448)

    def getAllAttributes(self):
        vars = {}
        for name in os.listdir(CONFIG_ATTRDIR):
            vars[name] = self.getAttribute(name)

        return vars

    def getAttribute(self, name, default=None):
        path = os.path.join(CONFIG_ATTRDIR, name)
        if os.path.exists(path):
            with open(path, 'r') as (fp):
                return fp.readline().rstrip()
        return default

    def setAttribute(self, name, value):
        path = os.path.join(CONFIG_ATTRDIR, name)
        with open(path, 'w') as (fp):
            fp.write(value + '\n')

    def clearAttribute(self, name):
        path = os.path.join(CONFIG_ATTRDIR, name)
        if os.path.exists(path):
            os.unlink(path)

    def preferredDevice(self, devicename=None):
        if not devicename:
            return self.getAttribute('preferred-device')
        self.setAttribute('preferred-device', devicename)

    def username(self, username=None):
        if not username:
            return self.getAttribute('username', DEFAULT_USERNAME)
        self.setAttribute('username', username)

    def password(self, password=None):
        if not password:
            return self.getAttribute('password', DEFAULT_PASSWORD)
        self.setAttribute('password', password)

    def envWhitelist(self, whitelist=None):
        if not whitelist:
            return self.getAttribute('env-whitelist', DEFAULT_ENV_WHITELIST)
        self.setAttribute('env-whitelist', whitelist)

    def shouldDisablePasswordAuth(self, disablePasswdAuth=None):
        if disablePasswdAuth == None:
            return self.getAttribute('disable-password-auth', DEFAULT_DISABLE_PASSWD_AUTH)
        self.setAttribute('disable-password-auth', disablePasswdAuth)


class GetCommand:
    __doc__ = "Usage: mdt get [<variablename>]\n\nReturns the value currently set for a given variable name. Some useful\nnvariables are:\n\n    preferred-device    - set this to your preferred device name to default\n                          most commands to manipulating this specific device.\n                          This can be set to an IPv4 address to bypass the mDNS\n                          lookup.\n    username            - set this to the username that should be used to\n                          connect to a device with. Defaults to 'mendel'.\n    password            - set this to the password to use to login to a new\n                          device with. Defaults to 'mendel'. Only used\n                          during the initial setup phase of pushing an SSH\n                          key to the board.\n\nIf no variable name is provided, 'mdt get' will print out the list of all\nknown stored variables and their values. Note: default values are not printed.\n"

    def __init__(self):
        self.config = Config()

    def run(self, args):
        if len(args) == 2:
            value = self.config.getAttribute(args[1])
            if value == None:
                print('{0} is unset'.format(args[1]))
            else:
                print('{0} is {1}'.format(args[1], self.config.getAttribute(args[1])))
        else:
            vars = self.config.getAllAttributes()
            if not vars:
                print('No variables are set.')
                return True
            else:
                for name, value in vars.items():
                    print('{0} is {1}'.format(name, value))

                return True


class SetCommand:
    __doc__ = "Usage: mdt set <variablename> <value>\n\nSets the value for a given variable name. Some useful variables are:\n\n    preferred-device    - set this to your preferred device name to default\n                          most commands to manipulating this specific device.\n                          This can be set to an IPv4 address to bypass the mDNS\n                          lookup.\n    username            - set this to the username that should be used to\n                          connect to a device with. Defaults to 'mendel'.\n    password            - set this to the password to use to login to a new\n                          device with. Defaults to 'mendel'. Only used\n                          during the initial setup phase of pushing an SSH\n                          key to the board.\n\nNote that setting a variable to the empty string does not clear it back to\nthe default value! Use 'mdt clear' for that.\n"

    def __init__(self):
        self.config = Config()

    def run(self, args):
        if len(args) != 3:
            print('Usage: mdt set <variablename> <value>')
            return 1
        self.config.setAttribute(args[1], args[2])
        print('Set {0} to {1}'.format(args[1], args[2]))


class ClearCommand:
    __doc__ = 'Usage: mdt clear <variablename>\n\nClears the value for a given variable name, resetting it back to its\ndefault value.\n'

    def __init__(self):
        self.config = Config()

    def run(self, args):
        if args:
            self.config.clearAttribute(args[1])
            print('Cleared {0}'.format(args[1]))