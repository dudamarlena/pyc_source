# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/EMS/utils/ZipUtils.py
# Compiled at: 2015-07-29 09:03:36
import logging, os, zipfile, tarfile, subprocess, shutil
log = logging.getLogger('exaManagementSystem')

def myZip(directory, destZipFile, zipPrefix='.'):
    """Zips a directory recursively to the destination zipfile"""
    log.debug('Zipping directory: ' + directory + ' to ' + destZipFile)
    if len(os.listdir(directory)) == 0:
        return
    zippedDir = zipfile.ZipFile(destZipFile, 'w')

    def zipTreeWalker(args, dirname, fnames):
        theZipArch = args[0]
        root = args[1]
        prefix = args[2]
        fnames.sort()
        for file in fnames:
            file = os.path.join(dirname, file)
            archiveName = file[len(os.path.commonprefix((root, file))) + 1:]
            archiveName = os.path.join(prefix, archiveName)
            if not os.path.isdir(file):
                theZipArch.write(file, archiveName)

    for root, dirs, files in os.walk(directory):
        zipTreeWalker([zippedDir, directory, zipPrefix], root, files)


def myTar(directory, destTarFile, tarPrefix='.'):
    """Creates a tar.gz file of a directory to destTarFile"""

    def isSvn(f):
        return f.endswith('.svn')

    log.debug('Tar.gz - ing ' + directory + ' to ' + destTarFile + '. Using python tar')
    containingFolder = os.path.basename(destTarFile)[:os.path.basename(destTarFile).find('.')]
    tarTempName = '/tmp/tmp.tar.gz'
    files = os.listdir(directory)
    if len(files) == 0:
        return
    tarArchive = tarfile.open(tarTempName, 'w:gz')
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, directory))
    for file in files:
        tarArchive.add(file, containingFolder + '/' + file, exclude=isSvn)

    os.chdir(cwd)
    if len(tarArchive.getmembers()) == 0:
        return
    tarArchive.close()
    shutil.move(tarTempName, destTarFile)
    return destTarFile


def sysTar(directory, destTarFile, tarPrefix='.'):
    cwd = os.getcwd()
    log.debug('Tar.gz - ing ' + directory + ' to ' + destTarFile + '. Using system tar')
    tarTempName = '/tmp/tmp.tar.gz'
    basename = os.path.basename(directory)
    dirname = os.path.dirname(directory)
    os.chdir(os.path.join(cwd, dirname))
    subprocess.call(['tar -czf ' + tarTempName + " --exclude='\\.svn' " + basename], shell=True, cwd='./', stdout=open('/dev/stdout', 'w'))
    os.chdir(cwd)
    shutil.move(tarTempName, destTarFile)