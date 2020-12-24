# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/driver.py
# Compiled at: 2016-07-18 22:40:47
import sys, argparse, pkg_resources
from difflib import get_close_matches
from .iaas_client.actions import ActionManager as IaaSActionManager
from .qs_client.actions import ActionManager as QSActionManager
SERVICES = ('iaas', 'qs')
INDENT = '  '
NEWLINE = '\n' + INDENT

def exit_due_to_invalid_service(suggest_services=None):
    usage = NEWLINE + '%(prog)s <service> <action> [parameters]\n\n' + 'Here are valid services:\n\n' + INDENT + NEWLINE.join(SERVICES)
    if suggest_services:
        usage += '\n\nInvalid service, maybe you meant:\n  ' + (',').join(suggest_services)
    parser = argparse.ArgumentParser(prog='qingcloud', usage=usage)
    parser.print_help()
    sys.exit(-1)


def exit_due_to_invalid_action(service, suggest_actions=None):
    usage = NEWLINE + '%(prog)s <action> [parameters]\n\n' + 'Here are valid actions:\n\n' + INDENT + NEWLINE.join(get_valid_actions(service))
    if suggest_actions:
        usage += '\n\nInvalid action, maybe you meant:\n  ' + NEWLINE.join(suggest_actions)
    parser = argparse.ArgumentParser(prog='qingcloud %s' % service, usage=usage)
    parser.print_help()
    sys.exit(-1)


def get_valid_actions(service):
    if service == 'iaas':
        return IaaSActionManager.get_valid_actions()
    if service == 'qs':
        return QSActionManager.get_valid_actions()


def get_action(service, action):
    if service == 'iaas':
        return IaaSActionManager.get_action(action)
    if service == 'qs':
        return QSActionManager.get_action(action)


def check_argument(args):
    if len(args) < 2:
        exit_due_to_invalid_service()
    if args[1].lower() in ('--version', '-v'):
        version = pkg_resources.require('qingcloud-cli')[0].version
        print 'qingcloud-cli version %s' % version
        sys.exit(0)
    service = args[1]
    if service not in SERVICES:
        suggest_services = get_close_matches(service, SERVICES)
        exit_due_to_invalid_service(suggest_services)
    if len(args) < 3:
        exit_due_to_invalid_action(service)
    valid_actions = get_valid_actions(service)
    if args[2] not in valid_actions:
        suggest_actions = get_close_matches(args[2], valid_actions)
        exit_due_to_invalid_action(service, suggest_actions)


def main():
    args = sys.argv
    check_argument(args)
    action = get_action(args[1], args[2])
    action.main(args[3:])