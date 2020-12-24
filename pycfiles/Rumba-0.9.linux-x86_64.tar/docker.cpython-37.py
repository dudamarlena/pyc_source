# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/executors/docker.py
# Compiled at: 2018-06-07 06:37:46
# Size of source mod 2**32: 2640 bytes
from rumba import model as mod
import tempfile, tarfile, os
from rumba import log
logger = log.get_logger(__name__)

class DockerException(Exception):
    pass


class DockerExecutor(mod.Executor):

    def __init__(self, testbed):
        self.testbed = testbed
        self.running_containers = testbed.running_containers

    def execute_command(self, node, command, sudo=False, time_out=3):
        logger.debug('%s >> %s' % (node.name, command))
        c, o = self.running_containers[node.name].exec_run(['sh', '-c',
         command])
        if c:
            raise DockerException('A remote command returned an error. Output:\n\n\t' + o.decode('utf-8'))
        return o.decode('utf-8')

    def fetch_file(self, node, path, destination, as_root=False):
        if not path.startswith('/'):
            workingdir = self.running_containers[node.name].attrs['Config']['WorkingDir']
            path = os.path.join(workingdir, path)
        try:
            with tempfile.NamedTemporaryFile() as (tmp):
                archive, _ = self.running_containers[node.name].get_archive(path)
                for c in archive:
                    tmp.write(c)

                tmp.seek(0)
                tarball = tarfile.TarFile(fileobj=tmp, mode='r')
                tarball.extract(os.path.basename(path), destination)
        except:
            logger.error('Error when extracting %s' % path)

    def copy_file(self, node, path, destination):
        pass