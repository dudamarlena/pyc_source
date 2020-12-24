# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/column/runner.py
# Compiled at: 2017-08-02 01:06:09
import abc, six

@six.add_metaclass(abc.ABCMeta)
class Runner(object):

    def __init__(self, inventory_file=None, **kwargs):
        self.inventory_file = inventory_file
        self.custom_opts = kwargs or {}

    @abc.abstractmethod
    def run_playbook(self, playbook_file, inventory_file=None, **kwargs):
        """Runs playbook specified in playbook_file, with inventory from
            inventory_file, as a remote_user. All other ansible parameters
            are passed using kwargs. see ansible-playbook --help or
            lib/ansible/constants.py in ansible source code for details
            of what parameters can be specified.

        :param playbook_file: str: absolute path to playbook file
        :param inventory_file: str: absolute path to inventory file
        :param kwargs: dict: Dictionary for optional parameters
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def run_module(self, module_name='ping', module_args=None, hosts='all', inventory_file=None, **kwargs):
        """Runs ansible module on hosts as remote_user, with optional
            inventory_file, module_name, and module_args
            All other ansible parameters
            are passed using kwargs. see ansible --help or
            lib/ansible/constants.py in ansible source code for details
            of what parameters can be specified.

        :param module_name: str: ansible module to execute
        :param module_args: str: ansible module arguments
        :param hosts: str: hosts filter, all by default
        :param inventory_file: str: absolute path to inventory file
        :param kwargs: dict: Dictionary for optional parameters
        """
        raise NotImplementedError()