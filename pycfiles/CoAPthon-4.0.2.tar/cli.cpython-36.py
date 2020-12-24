# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jik/.virtualenvs/coal-mine/lib/python3.6/site-packages/coal_mine/cli.py
# Compiled at: 2018-10-31 12:52:28
# Size of source mod 2**32: 11687 bytes
__doc__ = '\nCoal Mine CLI\n'
import argparse
from configparser import SafeConfigParser
import copy, os, pprint, re, requests
try:
    from simplejson.errors import JSONDecodeError as JSONError
except ImportError:
    JSONError = ValueError

import sys
config_file = '~/.coal-mine.ini'
config_section = 'coal-mine'

def doit(args, config_file):
    config = SafeConfigParser()
    config.read([config_file])
    try:
        section = config[config_section]
    except KeyError:
        config['coal-mine'] = {}
        section = config['coal-mine']

    connect_parser = argparse.ArgumentParser(add_help=False)
    host_default = section.get('host', 'localhost')
    connect_parser.add_argument('--host', action='store', help=('Server host name or URL (default {})'.format(host_default)),
      default=host_default)
    port_default = section.get('port', None)
    connect_parser.add_argument('--port', action='store', type=int, help='Server port',
      default=port_default)
    auth_key_group = connect_parser.add_mutually_exclusive_group()
    auth_key_default = section.get('auth-key', None)
    auth_key_group.add_argument('--auth-key', action='store', help=('Authentication key (default {})'.format('<hidden>' if auth_key_default else None)),
      default=auth_key_default)
    auth_key_group.add_argument('--no-auth-key', action='store_true', help='Disable authentication',
      default=False)
    parser = argparse.ArgumentParser(description="CLI wrapper for Coal Mine's HTTP API")
    subparsers = parser.add_subparsers()
    configure_parser = subparsers.add_parser('configure', help=('Save configuration from command line to ' + config_file),
      parents=[
     connect_parser])
    configure_parser.set_defaults(func=handle_configure, config_parser=config,
      config_file=config_file)
    create_parser = subparsers.add_parser('create', help='Create canary', parents=[
     connect_parser])
    create_parser.add_argument('--name', action='store', required=True)
    create_parser.add_argument('--periodicity', action='store', type=periodicity,
      required=True)
    create_parser.add_argument('--description', action='store')
    create_parser.add_argument('--email', action='append')
    create_parser.add_argument('--paused', action='store_true', default=False)
    create_parser.set_defaults(func=handle_create)
    id_parser = argparse.ArgumentParser(add_help=False)
    id_parser_group = id_parser.add_mutually_exclusive_group(required=True)
    id_parser_group.add_argument('--name', action='store')
    id_parser_group.add_argument('--slug', action='store')
    id_parser_group.add_argument('--id', action='store')
    delete_parser = subparsers.add_parser('delete', help='Delete canary', parents=[
     connect_parser, id_parser])
    delete_parser.set_defaults(func=handle_delete)
    update_parser = subparsers.add_parser('update', help='Update canary', parents=[
     connect_parser])
    update_parser.add_argument('--name', action='store')
    update_parser_group = update_parser.add_mutually_exclusive_group()
    update_parser_group.add_argument('--slug', action='store')
    update_parser_group.add_argument('--id', action='store')
    update_parser.add_argument('--no-history', '--terse', action='store_true', help='Omit history in output')
    update_parser.add_argument('--periodicity', action='store', type=periodicity)
    update_parser.add_argument('--description', action='store')
    update_parser.add_argument('--email', action='append', help='Specify "-" to clear existing email(s)')
    update_parser.set_defaults(func=handle_update)
    get_parser = subparsers.add_parser('get', help='Get canary', parents=[
     connect_parser, id_parser])
    get_parser.add_argument('--no-history', '--terse', action='store_true', help='Omit history in output')
    get_parser.set_defaults(func=handle_get)
    list_parser = subparsers.add_parser('list', help='List canaries', parents=[
     connect_parser])
    list_parser.add_argument('--verbose', action='store_true', default=None)
    list_parser.add_argument('--no-history', '--terse', action='store_true', help='Omit history in output')
    paused_group = list_parser.add_mutually_exclusive_group()
    paused_group.add_argument('--paused', action='store_true', default=None)
    paused_group.add_argument('--no-paused', dest='paused', action='store_false',
      default=None)
    late_group = list_parser.add_mutually_exclusive_group()
    late_group.add_argument('--late', action='store_true', default=None)
    late_group.add_argument('--no-late', dest='late', action='store_false',
      default=None)
    list_parser.add_argument('--search', action='store', default=None, help='Regular expression to match against name, slug, identifier, and email addresses')
    list_parser.set_defaults(func=handle_list)
    trigger_parser = subparsers.add_parser('trigger', help='Trigger canary', parents=[
     connect_parser, id_parser])
    trigger_parser.add_argument('--comment', action='store')
    trigger_parser.set_defaults(func=handle_trigger)
    pause_parser = subparsers.add_parser('pause', help='Pause canary', parents=[
     connect_parser, id_parser])
    pause_parser.add_argument('--no-history', '--terse', action='store_true', help='Omit history in output')
    pause_parser.add_argument('--comment', action='store')
    pause_parser.set_defaults(func=handle_pause)
    unpause_parser = subparsers.add_parser('unpause', help='Unpause canary', parents=[
     connect_parser, id_parser])
    unpause_parser.add_argument('--no-history', '--terse', action='store_true', help='Omit history in output')
    unpause_parser.add_argument('--comment', action='store')
    unpause_parser.set_defaults(func=handle_unpause)
    args = parser.parse_args(args)
    if 'func' not in args:
        parser.error('No command specified')
    url = ''
    if not re.match('^https?:', args.host):
        url += 'http://'
    url += args.host
    if args.port:
        url += ':{}'.format(args.port)
    url += '/coal-mine/v1/canary/'
    args.url = url
    if args.no_auth_key:
        args.auth_key = None
    if args.func is not handle_configure:
        del args.no_auth_key
    args.func(args)


def handle_configure(args):
    section = args.config_parser[config_section]
    section['host'] = args.host
    if args.port:
        section['port'] = str(args.port)
    if args.auth_key:
        section['auth-key'] = args.auth_key
    else:
        if args.no_auth_key:
            section.pop('auth-key', None)
    with open(args.config_file, 'w') as (configfile):
        args.config_parser.write(configfile)


def handle_create(args):
    call('create', args)


def handle_delete(args):
    call('delete', args)


def get_no_history_filter(d):
    if 'canary' in d:
        d = copy.deepcopy(d)
        del d['canary']['history']
        return d
    else:
        if 'canaries' in d:
            d = copy.deepcopy(d)
            for canary in d['canaries']:
                del canary['history']

            return d
        return d


def handle_update(args):
    if not (args.name or args.id or args.slug):
        sys.exit('Must specify --name, --id, or --slug')
    else:
        if args.name:
            if not (args.id or args.slug):
                found = call('get', args, {'name': args.name}, action='return')
                del args.name
                args.id = found['canary']['id']
        if vars(args).pop('no_history', None):
            filter = get_no_history_filter
        else:
            filter = None
    call('update', args, filter=filter)


def handle_get(args):
    if vars(args).pop('no_history', None):
        filter = get_no_history_filter
    else:
        filter = None
    call('get', args, filter=filter)


def handle_list(args):
    if args.paused is None:
        del args.paused
    else:
        if args.late is None:
            del args.late
        if args.search is None:
            del args.search
        if vars(args).pop('no_history', None):
            filter = get_no_history_filter
        else:
            filter = None
    call('list', args, filter=filter)


def handle_trigger(args):
    del args.auth_key
    call('trigger', args)


def handle_pause(args):
    if vars(args).pop('no_history', None):
        filter = get_no_history_filter
    else:
        filter = None
    call('pause', args, filter=filter)


def handle_unpause(args):
    if vars(args).pop('no_history', None):
        filter = get_no_history_filter
    else:
        filter = None
    call('unpause', args, filter=filter)


def call(command, args, payload=None, action='print', filter=None):
    url = args.url + command
    if payload:
        if args.auth_key:
            payload['auth_key'] = args.auth_key
        else:
            payload = {key:(getattr(args, key) if key == 'email' else str(getattr(args, key))) for key in dir(args) if not (key == 'email' and getattr(args, key) == [])}
        response = requests.get(url, params=payload)
        if response.status_code != 200:
            sys.stderr.write('{} {}\n'.format(response.status_code, response.reason))
            try:
                sys.exit(pprint.pformat(response.json()).strip())
            except JSONError:
                sys.exit(response.text)

    else:
        if action == 'print':
            try:
                content = response.json()
                if filter:
                    content = filter(content)
                pprint.pprint(content)
            except BrokenPipeError:
                pass

        else:
            if action == 'return':
                return response.json()
            raise Exception('Unrecognized action: {}'.format(action))


def periodicity(str):
    if re.match('[0-9.]+$', str):
        return float(str)
    else:
        return str


def main():
    doit(sys.argv[1:], os.path.expanduser(config_file))


if __name__ == '__main__':
    main()