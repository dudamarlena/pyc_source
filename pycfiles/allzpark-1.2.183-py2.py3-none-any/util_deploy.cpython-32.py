# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/support/util_deploy.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Sep 14, 2012\n\n@package ally utilities\n@copyright 2012 Sourcefabric o.p.s.\n@license http: // www.gnu.org / licenses / gpl - 3.0.txt\n@author: Mugur Rus\n\nContains ZIP utils\n'
from os.path import join, isdir
from ally.support.util_io import synchronizeURIToDir
from ally.zip.util_zip import getZipFilePath, validateInZipPath, ZIPSEP
from platform import system, machine, system_alias, release, version, linux_distribution
from zipfile import ZipFile
SYSTEM_ALL = 'all'
MACHINE_ALL = 'all'

def systemInfo():
    """
    Returns a tuple containing the following information:
    - system name (e.g. Darwin, Windows, Ubuntu etc.)
    - release (e.g.: 12.04 for Ubuntu, 11.4.0 for Darwin etc.)
    - version
    The difference between platform.system_alias() and this function is that
    this function returns the Linux distribution name and version instead of
    'Linux' and the kernel version.
    """
    sys, rel, ver = system_alias(system(), release(), version())
    if sys == 'Linux':
        sys, rel, _relname = linux_distribution()
    return (sys, rel, ver)


def deploy(source, destination, systemName=None, machineName=None):
    """
    Deploys the tool found at the source directory to the destination directory.

    @param source: src
        The directory from which to deploy the tool
    @param destination: src
        The path where to deploy the tool
    @param systemName: src
        The name of the system for which to deploy (e.g. Darwin, Windows, Ubuntu)
    @param machineName: src
        The machine name (e.g.: x86, x86_64)
    @return: tuple
        Tuple containing the system information (name, release, version) and True
        if the tool was deployed, False if it wasn't
    """
    assert isinstance(source, str), 'Invalid source path %s' % source
    assert isinstance(destination, str), 'Invalid destination path %s' % destination
    if not not systemName:
        assert isinstance(systemName, str), 'Invalid system name %s' % systemName
    if not not machineName:
        assert isinstance(machineName, str), 'Invalid machine name %s' % machineName
    if not systemName:
        systemName, rel, ver = systemInfo()
    machineName = machineName if machineName else machine()
    systems = SYSTEM_ALL if systemName == SYSTEM_ALL else (systemName, SYSTEM_ALL)
    machines = MACHINE_ALL if machineName == MACHINE_ALL else (machineName, MACHINE_ALL)
    deployed = False
    for systemName in systems:
        for machineName in machines:
            srcDir = join(source, systemName, machineName)
            if not isdir(srcDir):
                try:
                    zipPath, inPath = getZipFilePath(srcDir)
                    validateInZipPath(ZipFile(zipPath), inPath + ZIPSEP)
                except (IOError, KeyError):
                    continue

            synchronizeURIToDir(srcDir, destination)
            deployed = True

    return (systemName, rel, ver, deployed)