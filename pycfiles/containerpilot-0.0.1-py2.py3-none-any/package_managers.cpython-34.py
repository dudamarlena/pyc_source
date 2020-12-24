# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/containerdiff/package_managers.py
# Compiled at: 2016-05-23 00:59:59
# Size of source mod 2**32: 4386 bytes
__doc__ = 'Add support for different package managers.\n\nIt is also possible to add support to another package mangers. To be\nable to use tests in modules with the new package manager it is\nnecessary to implement it as a class which provides functions:\nget_installed_packages and get_unowned_files .\n'
import docker, tempfile, os, shutil, logging, containerdiff
logger = logging.getLogger(__name__)

def get_output_from_container(image, command):
    """Run 'command' in shell in container based on 'image'. Get its
    output by redirecting STDOUT to mounted file.

    Return list o lines from the 'command' output.
    """
    logger.info("Running '%s' in image '%s'", command, image)
    cli = docker.AutoVersionClient(base_url=containerdiff.docker_socket)
    volume_dir = tempfile.mkdtemp(dir='/tmp')
    logger.debug('Container output volume: %s', volume_dir)
    container = cli.create_container(image, volumes=[volume_dir], host_config=cli.create_host_config(binds=[volume_dir + ':/mnt/containerdiff-volume:Z']), command="/bin/sh -c 'set -m; touch /mnt/containerdiff-volume/output; chmod a+rw /mnt/containerdiff-volume/output; exec 1>/mnt/containerdiff-volume/output; " + command + "'", user=os.geteuid())
    cli.start(container)
    error = cli.logs(container)
    if error != '':
        logger.error(error)
    cli.stop(container)
    cli.remove_container(container)
    output = open(os.path.join(volume_dir, 'output')).read()
    shutil.rmtree(volume_dir, ignore_errors=True)
    return output


class RPM:
    """RPM"""

    def _get_owned_files(self, ID, root):
        """Get list files installed by rpms in image 'ID' which is
        expanded into 'root'. It runs "rpm -qal" command in the image
        and removes symbolic links in directories in the result.
        """
        filelist = get_output_from_container(ID, 'rpm -qal | grep -v \\(contains\\ no\\ files\\)').split('\n')
        filelist = [os.sep.join(['', os.path.relpath(os.path.realpath(os.sep.join([root, os.path.dirname(filepath)])), start=root), os.path.basename(filepath)]) for filepath in filelist]
        return filelist

    def get_unowned_files(self, ID, metadata, root):
        """Return the list of files that are listed in 'metadata' dict
        (result from extracting the image) and are not installed by
        rpm packages in image 'ID'.
        """
        owned_files = self._get_owned_files(ID, root)
        return list(set(metadata.keys()) - set(owned_files))

    def get_installed_packages(self, ID):
        """Return list of installed packages in image 'ID'. Each
        element of the list is a tuple (<package name>, <version>).
        """
        packages = get_output_from_container(ID, 'rpm -qa').split()
        name_version = []
        for package in packages:
            elements = package.split('-')
            name_version.append(('-'.join(elements[:-2]), '-'.join(elements[-2:])))

        return name_version