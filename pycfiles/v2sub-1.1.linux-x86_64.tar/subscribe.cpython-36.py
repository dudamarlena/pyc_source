# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/v2sub/subscribe.py
# Compiled at: 2019-11-03 23:22:20
# Size of source mod 2**32: 4247 bytes
import base64, json, os, sys
from urllib.request import urlopen, Request
from urllib.error import URLError
import click
from v2sub import BASE_PATH
from v2sub import DEFAULT_SUBSCRIBE
from v2sub import SERVER_CONFIG
from v2sub import SUBSCRIBE_CONFIG
from v2sub import utils

def init():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    else:
        if not os.path.exists(SUBSCRIBE_CONFIG):
            os.mknod(SUBSCRIBE_CONFIG)
        if not os.path.exists(SERVER_CONFIG):
            os.mknod(SERVER_CONFIG)


def add_subscribe(url, name=DEFAULT_SUBSCRIBE):
    subscribe = utils.read_from_json(SUBSCRIBE_CONFIG)
    subscribe.update({name: url})
    utils.write_to_json(subscribe, SUBSCRIBE_CONFIG)
    click.echo('Added subscribe: %s' % url)


def list_subscribe():
    subscribe = utils.read_from_json(SUBSCRIBE_CONFIG)
    click.echo('Subscribes:')
    for name, url in subscribe.items():
        click.echo('%s: %s' % (name, url))


def _remove_subscribe(name=DEFAULT_SUBSCRIBE, all_subs=False):
    all_subscribes = utils.read_from_json(SUBSCRIBE_CONFIG)
    if all_subs:
        all_subscribes.clear()
    else:
        all_subscribes.pop(name, None)
    utils.write_to_json(all_subscribes, SUBSCRIBE_CONFIG)


def _remove_servers(name=DEFAULT_SUBSCRIBE, all_subs=False):
    all_servers = utils.read_from_json(SERVER_CONFIG)
    if all_subs:
        all_servers.clear()
    else:
        all_servers.pop(name, None)
    utils.write_to_json(all_servers, SERVER_CONFIG)


def remove_subscribe(name=DEFAULT_SUBSCRIBE, all_subs=False):
    _remove_subscribe(name=name, all_subs=all_subs)
    _remove_servers(name=name, all_subs=all_subs)
    if all_subs:
        click.echo('Removed all subscribes.')
    else:
        click.echo('Removed subscribe: %s' % name)


def parser_subscribe(url, name=DEFAULT_SUBSCRIBE):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urlopen(req)
    except URLError:
        click.echo("Can't parse the url, please check your network or make sure you entered the correct URL!")
        sys.exit(1)

    nodes = base64.b64decode(resp.read()).splitlines()
    servers = []
    for node in nodes:
        node = utils.byte2str(node).replace('vmess://', '')
        node = utils.byte2str(base64.b64decode(node))
        servers.append(json.loads(node))

    all_servers = utils.read_from_json(SERVER_CONFIG)
    all_servers.update({name: servers})
    utils.write_to_json(all_servers, SERVER_CONFIG)


def _update_all_subscribe(subscribes: dict):
    for name, url in subscribes.items():
        parser_subscribe(url, name=name)


def update_subscribe(name=DEFAULT_SUBSCRIBE, all_subs=False):
    all_subscribe = utils.read_from_json(SUBSCRIBE_CONFIG)
    if all_subs:
        _update_all_subscribe(all_subscribe)
    else:
        try:
            url = all_subscribe[name]
        except KeyError:
            click.echo('No subscribe named %s found!' % name)
            sys.exit(1)

        parser_subscribe(url, name=name)
    list_servers(name=name, all_subs=all_subs)


def _list_server(name, nodes):
    click.echo('=' * 50)
    click.echo('SUBSCRIBE: %s' % name)
    click.echo('=' * 50)
    for index, node in enumerate(nodes, start=1):
        utils.echo_node(index, node)


def list_servers(name=DEFAULT_SUBSCRIBE, all_subs=False):
    all_servers = utils.read_from_json(SERVER_CONFIG)
    if not all_servers:
        click.echo('No servers found, please add and update subscribe first!')
        sys.exit(1)
    else:
        if all_subs:
            for name, nodes in all_servers.items():
                _list_server(name, nodes)

        else:
            _list_server(name, all_servers[name])


def get_node(index, name=DEFAULT_SUBSCRIBE):
    all_servers = utils.read_from_json(SERVER_CONFIG)
    try:
        servers = all_servers[name]
    except KeyError:
        click.echo('No subscribe named %s found!' % name)
        sys.exit(1)

    try:
        utils.check_index(index)
        node = servers[(index - 1)]
        click.echo('switch to node:')
        utils.ping(name=name, index=index, all_servers=all_servers)
    except IndexError:
        click.echo('Invalid index: %s, please check it.' % index)
        sys.exit(1)

    return node