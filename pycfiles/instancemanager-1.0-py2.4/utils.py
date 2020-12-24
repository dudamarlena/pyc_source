# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/utils.py
# Compiled at: 2007-12-17 05:32:50
import config, logging, os, os.path, shutil, sys, popen2
log = logging.getLogger('utils')

def makeDir(directoryName):
    log.debug("Checking presence of directory '%s'.", directoryName)
    if not os.path.exists(directoryName):
        os.mkdir(directoryName)
        log.info("Created directory '%s'.", directoryName)


def initLog():
    """Initialise the logger.
    """
    log = logging.getLogger()
    userDir = os.path.expanduser('~')
    configDir = os.path.join(userDir, config.CONFIGDIR)
    if os.path.exists(configDir):
        filename = os.path.join(configDir, config.LOGFILE)
    else:
        filename = config.LOGFILE
    hdlr = logging.FileHandler(filename, 'w')
    formatter = logging.Formatter('%(name)-10s %(levelname)-5s %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)


def addConsoleLogging(level=logging.INFO):
    """Add logging to the console.
    """
    log = logging.getLogger()
    hdlr = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)-5s %(message)s')
    hdlr.setLevel(level)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)


def adaptiveUnarchive(source):
    """Untar or unzip a file to the current directory.
       TODO: is using "not in gzip format" an i18n issue?
       NOTE: using extensions to decide whether a file is tar or tgz format
         is very unreliable for Plone product archives.
       We do not test for or return overall success.
       The next step in the operation will look for unpacked items.
    """
    if source.endswith('zip'):
        zipExtract(source)
    else:
        tarExtract(source)


import zipfile

def zipExtract(filename, extract_dir='.'):
    cwd = os.getcwd()
    os.chdir(extract_dir)
    zf = zipfile.ZipFile(filename, 'r')
    for zipinfo in zf.infolist():
        fn = zipinfo.filename
        if fn[(-1)] == '/':
            os.mkdir(fn)
        else:
            data = zf.read(fn)
            f = open(fn, 'wb')
            f.write(data)
            f.close()

    zf.close()
    os.chdir(cwd)


import tarfile

def tarExtract(filename, extract_dir='.'):
    ext_types = {'gz': 'gz', 'tgz': 'gz', 'bz2': 'bz2', 'tbz': 'bz2'}
    ext_type = ext_types.get(filename.split('.')[(-1)], '')
    cwd = os.getcwd()
    os.chdir(extract_dir)
    tgz = tarfile.open(filename, (':').join(['r', ext_type]))
    for tarinfo in tgz:
        tgz.extract(tarinfo)

    tgz.close()
    os.chdir(cwd)


def symlink(source, target, conf):
    useSvnExport = conf.configData['use_svn_export']
    if not useSvnExport:
        if conf.configData['is_windows']:
            log.debug('Copying %s -> %s.', source, target)
            shutil.copytree(source, target)
        else:
            log.debug('Symlinking %s -> %s.', source, target)
            os.symlink(source, target)
    else:
        if conf.configData['is_windows']:
            source = '"%s"' % source
            log.debug('windows svn export: source is now [%s]', source)
            target = '"%s"' % target
            log.debug('windows svn export: target is now [%s]', target)
        command = (' ').join(['svn export', '-q', source, target])
        log.debug('Svn exporting: %s.', command)
        os.system(command)


def isZope3(conf):
    zope_version = conf.configData['zope_version']
    if zope_version[0] == '3':
        return True
    return False