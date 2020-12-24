# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/containerdiff/modules/packages.py
# Compiled at: 2016-05-23 00:53:11
# Size of source mod 2**32: 2896 bytes
__doc__ = 'Show diff in container image packages.'
import os, difflib, logging, magic, logging, containerdiff.package_managers
logger = logging.getLogger(__name__)
package_manager = containerdiff.package_managers.RPM()

def test_packages(ID1, ID2):
    """Test changes in packages installed by package manager.

    Result contains a dict {"added":.., "removed":.., "modified"}. Each
    key has a list value. Values for first two keys contain tuples
    ("<package_name>,<version>") for added/removed packages. Key
    "modified" contains tuples (<package_name>, <old_version>,
    <new_version>).
    """
    packages1, versions1 = zip(*package_manager.get_installed_packages(ID1))
    packages2, versions2 = zip(*package_manager.get_installed_packages(ID2))
    removed = [(package, versions1[packages1.index(package)]) for package in list(set(packages1) - set(packages2))]
    added = [(package, versions2[packages2.index(package)]) for package in list(set(packages2) - set(packages1))]
    modified = [(package, versions1[packages1.index(package)], versions2[packages2.index(package)]) for package in list(set(packages2).intersection(set(packages1))) if versions1[packages1.index(package)] != versions2[packages2.index(package)]]
    return {'added': added,  'removed': removed,  'modified': modified}


def run(image1, image2):
    """Test packages in the image.

    Adds one key to the output of the diff tool:
    "packages" - dict containing information about changed files (see
                 output of "test_packages" function in this module)
    """
    ID1, metadata1, output_dir1 = image1
    ID2, metadata2, output_dir2 = image2
    logger.info('Testing packages in the image')
    result = {}
    result['packages'] = test_packages(ID1, ID2)
    return result