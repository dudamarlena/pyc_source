# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/provisioners/ansibleDriver.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 2119 bytes
import logging, os, subprocess
from toil.provisioners.abstractProvisioner import AbstractProvisioner
logger = logging.getLogger(__name__)

class AnsibleDriver(AbstractProvisioner):
    __doc__ = '\n    Wrapper class for Ansible calls.\n    '

    def __init__(self, playbooks, clusterName, zone, nodeStorage):
        self.playbooks = playbooks
        super(AnsibleDriver, self).__init__(clusterName, zone, nodeStorage)

    def callPlaybook(self, playbook, ansibleArgs, wait=True, tags=['all']):
        """
        Run a playbook.

        :param playbook: An Ansible playbook to run.
        :param ansibleArgs: Arguments to pass to the playbook.
        :param wait: Wait for the play to finish if true.
        :param tags: Control tags for the play.
        """
        playbook = os.path.join(self.playbooks, playbook)
        verbosity = '-vvvvv' if logger.isEnabledFor(logging.DEBUG) else '-v'
        command = ['ansible-playbook', verbosity, '--tags', ','.join(tags), '--extra-vars']
        command.append(' '.join(['='.join(i) for i in ansibleArgs.items()]))
        command.append(playbook)
        logger.debug('Executing Ansible call `%s`', ' '.join(command))
        p = subprocess.Popen(command)
        if wait:
            p.communicate()
            if p.returncode != 0:
                raise RuntimeError('Ansible reported an error when executing playbook %s' % playbook)