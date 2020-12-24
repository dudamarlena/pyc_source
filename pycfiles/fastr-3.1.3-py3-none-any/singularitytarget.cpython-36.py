# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/targetplugins/singularitytarget.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 3666 bytes
"""
The module containing the classes describing the targets.
"""
import os, subprocess, fastr
from fastr import exceptions
from fastr.core.target import SubprocessBasedTarget

class SingularityTarget(SubprocessBasedTarget):
    __doc__ = '\n    A tool target that is run using a singularity container,\n    see the `singulary website <http://singularity.lbl.gov/>`_\n\n    * ``binary (required)``: the name of the binary/script to call, can also be called ``bin``\n      for backwards compatibility.\n    * ``container (required)``: the singularity container to run, this can be in url form for singularity\n                                pull or as a path to a local container\n\n    * ``interpreter``: the interpreter to use to call the binary e.g. ``python``\n\n    '
    SINGULARITY_BIN = 'singularity'

    def __init__(self, binary, container, interpreter=None):
        """
        Define a new local binary target. Must be defined either using paths and optionally environment_variables
        and initscripts, or enviroment modules.
        """
        self.binary = binary
        self.container = container
        self.interpreter = interpreter

    def __enter__(self):
        super(SingularityTarget, self).__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleanup the environment
        """
        pass

    @classmethod
    def test(cls):
        """
        Test if singularity is availble on the path
        """
        try:
            subprocess.check_output([cls.SINGULARITY_BIN, '--help'], stderr=(subprocess.STDOUT))
        except OSError:
            raise exceptions.FastrExecutableNotFoundError(cls.SINGULARITY_BIN)

    def run_command(self, command):
        if self.interpreter is not None:
            command = [
             self.interpreter] + command
        mounts = fastr.config.mounts.values()
        binds = []
        for mount in mounts:
            if not os.path.exists(mount):
                pass
            else:
                binds.append('--bind')
                binds.append('{x}:{x}'.format(x=mount))

        fastr.log.info('Singularity binds: {}'.format(binds))
        singularity_command = [
         self.SINGULARITY_BIN, 'exec']
        singularity_command.extend(binds)
        singularity_command.append(self.container)
        singularity_command.extend(command)
        fastr.log.debug('Command: {}'.format(command))
        fastr.log.debug('Singularity command: {}'.format(singularity_command))
        return self.call_subprocess(singularity_command)