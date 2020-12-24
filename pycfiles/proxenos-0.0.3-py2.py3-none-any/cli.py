# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/cli.py
# Compiled at: 2017-01-22 19:48:17
"""Provides the proxenos command line interface."""
from __future__ import absolute_import
import re, click, stevedore.driver, proxenos.mappers, proxenos.rendezvous
__all__ = ('main', )
DEFAULT_PORTS = {'consul': 8500, 
   'etcd': 4001}
HASH_METHODS = proxenos.rendezvous.HashMethod.__members__

@click.group()
@click.pass_context
def main(ctx):
    """proxenos-cli: Consistently select nodes from service discovery."""
    pass


@main.command('select')
@click.option('-b', '--backend', default='consul', help='Service discovery backend.', type=click.Choice(proxenos.mappers.available_backends))
@click.option('-f', '--filter-pattern', help='Regex pattern to filter socket address strings.')
@click.option('-h', '--host', default='localhost', help='Service discovery host.')
@click.option('-p', '--port', help='Service discovery port.')
@click.option('-H', '--hash-method', callback=lambda _, __, v: getattr(proxenos.rendezvous.HashMethod, v.upper()), default='SIPHASH', envvar='PROXENOS_PRF', help='Hash method. Defaults to SipHash.', type=click.Choice(HASH_METHODS))
@click.argument('key')
def cmd_select(backend, filter_pattern, host, port, hash_method, key):
    """Selects a node from a cluster."""
    if port is None:
        port = DEFAULT_PORTS[backend]
    driver_manager = stevedore.driver.DriverManager(namespace=proxenos.mappers.NAMESPACE, name=backend, invoke_on_load=False)
    mapper = driver_manager.driver(host=host, port=port)
    mapper.update()
    cluster = mapper.cluster.copy()
    if filter_pattern:
        pattern = re.compile(filter_pattern)
        cluster = {addr for addr in cluster if pattern.match(str(addr))}
    addr = proxenos.rendezvous.select_node(cluster, key, hash_method=hash_method)
    click.echo(str(addr))
    return