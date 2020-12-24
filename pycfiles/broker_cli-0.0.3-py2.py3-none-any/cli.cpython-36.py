# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/diogo.munaro/workspace/brokerpackager/brokerpackager/cli.py
# Compiled at: 2017-08-16 15:13:13
# Size of source mod 2**32: 2169 bytes
import os, re, click
from .managers.python import PyManager
from .managers.r import RManager
from .broker import BrokerConnector

@click.group()
def bus():
    pass


@bus.command()
@click.option('--language', '-l', help='Language name', type=(click.Choice(['python', 'r'])), required=True)
@click.option('--name', '-n', help='Package Name', required=True)
@click.option('--version', '-v', help='Package Version', default='')
@click.option('--git', '-g', help='Install from git', default=False, is_flag=True)
@click.option('--pip_paths', '-i', help='Pip paths', multiple=True, default=['pip'])
@click.option('--log_file', '-f', help='LogFile')
def install(language, name, version, git, pip_paths, log_file):
    if language == 'python':
        installer = PyManager(log_file)
        arg_list = [name, version, git, pip_paths]
    else:
        if language == 'r':
            installer = RManager(log_file)
            arg_list = [name, version, git]
        else:
            click.echo('No installer selected')
            exit(1)
    (installer.install)(*arg_list)


@bus.command()
@click.option('--endpoint', '-e', help='Bus Endpoint', default='localhost')
@click.option('--port', '-p', help='Bus Port', type=(click.INT), default=61613)
@click.option('--destination', '-d', help='Bus Destination', required=True)
@click.option('--selector', '-s', help='Bus Header Selector')
@click.option('--python_json_path', '-p', help='Python packages json list path', default='')
@click.option('--pip_paths', '-i', help='Pip paths', multiple=True, default=['pip'])
@click.option('--r_json_path', '-r', help='R packages json list path', default='')
@click.option('--log_file', '-f', help='LogFile')
def monitor(endpoint, port, destination, selector, python_json_path, pip_paths, r_json_path, log_file):
    installer_configs = {'python':{'json':python_json_path, 
      'pip_paths':pip_paths, 
      'log_file':log_file}, 
     'r':{'json':r_json_path, 
      'log_file':log_file}}
    BrokerConnector(endpoint, port, destination, selector, installer_configs)


installer = click.CommandCollection(sources=[bus])