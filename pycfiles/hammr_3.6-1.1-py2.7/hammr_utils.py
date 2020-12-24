# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/utils/hammr_utils.py
# Compiled at: 2016-12-16 11:09:34
import json, sys, re, traceback
from os.path import expanduser
import os, urllib
from uforge.objects.uforge import *
import ussclicore.utils.download_utils
from ussclicore.utils import printer
from ussclicore.utils import generics_utils

def check_mandatory_stack(stack):
    if 'name' not in stack:
        printer.out('no attribute [name] for [stack]', printer.ERROR)
        return
    if 'version' not in stack:
        printer.out('no attribute [version] for [stack]', printer.ERROR)
        return
    if 'os' not in stack:
        printer.out('no attribute [os] for [stack]', printer.ERROR)
        return
    if 'name' not in stack['os']:
        printer.out('no attribute [name] for [os]', printer.ERROR)
        return
    if 'version' not in stack['os']:
        printer.out('no attribute [version] for [os]', printer.ERROR)
        return
    if 'arch' not in stack['os']:
        printer.out('no attribute [arch] for [os]', printer.ERROR)
        return
    return stack


def check_mandatory_builders(builders):
    return builders


def check_mandatory_generate_scan(builders):
    for builder in builders:
        if 'installation' not in builder:
            printer.out('no attribute installation in builder', printer.ERROR)
            return
        if 'diskSize' not in builder['installation']:
            printer.out('no attribute diskSize in the installation part of builder', printer.ERROR)
            return
        if 'hardwareSettings' not in builder:
            printer.out('no attribute hardwareSettings in builder', printer.ERROR)
            return
        if 'memory' not in builder['hardwareSettings']:
            printer.out('no attribute diskSize in the memory part of hardwareSettings', printer.ERROR)
            return

    return builders


def check_mandatory_create_account(iterables, type):
    for iterable in iterables:
        if type == 'builders':
            if 'account' in iterable:
                if 'type' not in iterable and 'type' not in iterable['account']:
                    printer.out('no attribute type in builder', printer.ERROR)
                    return
                if 'file' in iterable['account']:
                    file = get_file(iterable['account']['file'])
                    if file is None:
                        return 2
                    data = generics_utils.check_json_syntax(file)
                    if data is None:
                        return 2
                    if 'accounts' in data:
                        return check_mandatory_create_account(data['accounts'], 'accounts')
        if type == 'accounts':
            if 'type' not in iterable:
                printer.out('no attribute type in accounts', printer.ERROR)
                return

    return iterables


def validate_json_file(file):
    try:
        data = generics_utils.check_json_syntax(file)
        if data is None:
            return
        if 'stack' in data:
            stack = check_mandatory_stack(data['stack'])
            if stack is None:
                return
        if 'builders' in data:
            check_mandatory_builders(data['builders'])
        return data
    except ValueError as e:
        printer.out('JSON parsing error: ' + str(e), printer.ERROR)
        printer.out('Syntax of template file [' + file + ']: FAILED')
    except IOError as e:
        printer.out('unknown error template json file', printer.ERROR)

    return


def is_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        return True


def get_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        return "UForge Error '" + str(e.args[0].statusCode) + "' with method: " + e.args[0].requestMethod + ' ' + e.args[0].requestUri + '\n' + 'Message:\n\t' + e.args[0].localizedErrorMsg.message


def print_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        printer.out(get_uforge_exception(e), printer.ERROR)
    else:
        traceback.print_exc()


def handle_uforge_exception(e):
    print_uforge_exception(e)
    return 2


def get_uforge_url_from_ws_url(ws_url):
    if ws_url[-1:] != '/':
        return ws_url.rpartition('/')[0]
    else:
        return ws_url[:-1].rpartition('/')[0]


def get_hammr_dir():
    dir = ussclicore.utils.generics_utils.get_home_dir() + os.sep + '.hammr'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return dir


def create_user_ssh_key(api, login, sshKey):
    if 'name' not in sshKey:
        printer.out('sshKey name not found in builder', printer.ERROR)
        return 2
    else:
        if 'publicKey' not in sshKey:
            printer.out('publicKey in sshKey not found in builder', printer.ERROR)
            return 2
        mySshKey = sshKey()
        mySshKey.name = sshKey['name']
        mySshKey.publicKey = sshKey['publicKey']
        key = self.api.Users(login).Sshkeys().Create(mySshKey)
        if key is None:
            printer.out('Impossible to create sshKey [' + mySshKey.name + ']', printer.ERROR)
            return 2
        return key