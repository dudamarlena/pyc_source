# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/cli/aws.py
# Compiled at: 2017-04-11 07:05:33
# Size of source mod 2**32: 3707 bytes
"""Admin Cell CLI module"""
from __future__ import absolute_import
import logging, treadmill, os, click, errno
from ansible.cli.playbook import PlaybookCLI
from distutils.dir_util import copy_tree
_LOGGER = logging.getLogger(__name__)

def init():
    """Admin Cell CLI module"""

    @click.group()
    def aws():
        """Manage treadmill on AWS"""
        pass

    def _get_from_treadmill_egg(obj):
        return os.path.join(treadmill.TREADMILL_DEPLOY_PACKAGE, obj)

    @aws.command(name='init')
    def init():
        """Initialise ansible files for AWS deployment"""
        destination_dir = os.getcwd() + '/deploy'
        try:
            os.makedirs(destination_dir)
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('AWS "deploy" directory already exists in this folder\n                \n', destination_dir)

        copy_tree(_get_from_treadmill_egg('../deploy'), destination_dir)

    @aws.command(name='cell')
    @click.option('--create', required=False, is_flag=True, help='Create a new treadmill cell on AWS')
    @click.option('--destroy', required=False, is_flag=True, help='Destroy treadmill cell on AWS')
    @click.option('--playbook', help='Playbok file')
    @click.option('--inventory', default=_get_from_treadmill_egg('controller.inventory'), help='Inventory file')
    @click.option('--key-file', default='key.pem', help='AWS ssh pem file')
    @click.option('--aws-config', default=_get_from_treadmill_egg('aws.yml'), help='AWS config file')
    def cell(create, destroy, playbook, inventory, key_file, aws_config):
        """Manage treadmill cell on AWS"""
        playbook_args = [
         'ansible-playbook',
         '-i',
         inventory,
         '-e',
         'aws_config={}'.format(aws_config)]
        if create:
            playbook_args.extend([
             playbook or _get_from_treadmill_egg('cell.yml'),
             '--key-file',
             key_file])
        else:
            if destroy:
                playbook_args.append(playbook or _get_from_treadmill_egg('destroy-cell.yml'))
            else:
                return
        playbook_cli = PlaybookCLI(playbook_args)
        playbook_cli.parse()
        playbook_cli.run()

    @aws.command(name='node')
    @click.option('--create', required=False, is_flag=True, help='Create a new treadmill node')
    @click.option('--playbook', default=_get_from_treadmill_egg('node.yml'), help='Playbok file')
    @click.option('--inventory', default=_get_from_treadmill_egg('controller.inventory'), help='Inventory file')
    @click.option('--key-file', default='key.pem', help='AWS ssh pem file')
    @click.option('--aws-config', default=_get_from_treadmill_egg('aws.yml'), help='AWS config file')
    def node(create, playbook, inventory, key_file, aws_config):
        """Manage treadmill node"""
        if create:
            playbook_cli = PlaybookCLI([
             'ansible-playbook',
             '-i',
             inventory,
             playbook,
             '--key-file',
             key_file,
             '-e',
             'aws_config={}'.format(aws_config)])
            playbook_cli.parse()
            playbook_cli.run()

    del cell
    del node
    return aws