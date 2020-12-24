# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/updater4pyi/upd_core.py
# Compiled at: 2014-12-07 08:39:53
import re, sys, inspect, os, os.path, stat, collections, zipfile, tarfile, json, glob, subprocess, tempfile, shutil
from . import util
from . import upd_version
from .upd_log import logger
from .upd_defs import RELTYPE_UNKNOWN, RELTYPE_EXE, RELTYPE_ARCHIVE, RELTYPE_BUNDLE_ARCHIVE
from .upd_defs import Updater4PyiError
import upd_downloader
FileToUpdate = collections.namedtuple('FileToUpdate', ('fn', 'reltype', 'executable'))

def determine_file_to_update():
    """
    Inspects the program currently running, and determines the location of the file one
    should replace in the event of a software update.

    Returns a named tuple `FileToUpdate(fn=.., reltype=.., executable=...)`. The values
    are:

        - `fn`: the actual file we should update. This could be a directory in the case of
          a onedir PyInstaller package. For a MAC OS X bundle, it is the `XYZ.app` file.
          
        - `reltype`: the release type we have. This may be one of
          :py:const:`upd_defs.RELTYPE_EXE`, :py:const:`upd_defs.RELTYPE_ARCHIVE`,
          :py:const:`upd_defs.RELTYPE_BUNDLE_ARCHIVE`.

        - `executable`: the actual executable file. This may be different from `fn`, for
          example in Mac OS X bundles, where `executable` is the actual file being
          executed within the bundle.

    .. _PyInstaller: http://www.pyinstaller.org/
    """
    executable = sys.executable
    updatefile = os.path.realpath(sys.executable)
    reltype = None
    logger.debug('trying to determine pyi executable to update. sys.executable=%s; sys._MEIPASS=%s', sys.executable, sys._MEIPASS if hasattr(sys, '_MEIPASS') else '<no sys._MEIPASS>')
    if sys.platform.startswith('darwin'):
        alllastdir, fn = os.path.split(sys.executable)
        allbeforelastdir, lastdir = os.path.split(alllastdir)
        allbeforebeforelastdir, beforelastdir = os.path.split(allbeforelastdir)
        logger.debug('platform is Mac OS X; alllastdir=%s, beforelastdir=%s, lastdir=%s, fn=%s', alllastdir, beforelastdir, lastdir, fn)
        if lastdir == 'MacOS' and beforelastdir == 'Contents':
            reltype = RELTYPE_BUNDLE_ARCHIVE
            updatefile = allbeforebeforelastdir
            logger.debug("We're a bundle: updatefile=%s", updatefile)
    if reltype is None:
        if hasattr(sys, '_MEIPASS'):
            meipass = os.path.realpath(sys._MEIPASS)
            if updatefile.startswith(meipass):
                reltype = RELTYPE_ARCHIVE
                updatefile = meipass
    if reltype is None:
        reltype = RELTYPE_EXE
    logger.debug('got FileToUpdate(fn=%r, reltype=%d, executable=%s)', updatefile, reltype, executable)
    return FileToUpdate(fn=updatefile, reltype=reltype, executable=executable)


_updater = None

def get_updater():
    return _updater


class Updater(object):
    """
    The main Updater object.

    This class is responsible for actually checking for updates and performing the
    software update.

    It does not take care of scheduling the checks, however. That's done with an
    UpdaterInterface.

    This class needs to be specified a *source* for updates. See
    :py:class:`upd_source.UpdateSource`.
    """

    def __init__(self, current_version, update_source):
        """
        Instantiates an `Updater`, with updates provided by the source `update_source` (a
        `upd_source.UpdateSource` subclass instance).

        The `current_version` is the current version string of the software, and will
        be provided to the `update_source`.
        """
        if not hasattr(sys, '_MEIPASS'):
            raise Updater4PyiError('This installation is not built with pyinstaller.')
        self._update_source = update_source
        logger.debug('source is %r' % self._update_source)
        self._current_version = current_version
        self._file_to_update = determine_file_to_update()
        super(Updater, self).__init__()

    def update_source(self):
        """
        Return the source given to the constructor.
        """
        return self._update_source

    def current_version(self):
        """
        Return the current version of the running program, as given to the constructor.
        """
        return self._current_version

    def file_to_update(self):
        """
        Return the file one should update. See :py:func:`determine_file_to_update`.
        """
        return self._file_to_update

    def check_for_updates(self):
        """
        Perform an update check.

        Queries the source for possible updates, which matches our system. If a software
        update is found, then a :py:class:`upd_source.BinReleaseInfo` object is returned,
        describing the software update. Otherwise, if no update is available, `None` is
        returned.
        """
        releases = self._update_source.get_releases(newer_than_version=self._current_version)
        logger.debug('releases=%r' % releases)
        if releases is None:
            logger.warning('Software Update Source returned a None release list!')
            return
        else:
            wanted_reltype = self._file_to_update.reltype
            curver = util.parse_version(self._current_version)
            rel_w_parsedversion = [ (r, util.parse_version(r.get_version())) for r in releases ]
            releases2 = sorted([ (rel, relparsedver) for rel, relparsedver in rel_w_parsedversion if rel.get_reltype() == wanted_reltype and rel.get_platform() == util.simple_platform() and relparsedver > curver
                               ], key=lambda r2: r2[1], reverse=True)
            if releases2:
                return releases2[0][0]
            logger.debug('No update found.')
            return

    SPECIAL_ZIP_FILES = (
     '_updater4pyi_metainf.json',
     '_METAINF')

    class _ExtractLocation(object):

        def __init__(self, filetoupdate, needs_sudo, **kwargs):
            self.filetoupdate = filetoupdate
            self.needs_sudo = needs_sudo
            super(Updater._ExtractLocation, self).__init__(**kwargs)

        def findextractto(self, namelist):
            basedir, basefn = os.path.split(self.filetoupdate.fn)
            self.extractto = None
            self.installto = None
            self.extracttotemp = False
            self.extractstodir = True
            if [ True for x in namelist if not x.startswith(basefn) and x not in Updater.SPECIAL_ZIP_FILES ]:
                self.extractstodir = False
                self.extractto = self.filetoupdate.fn
                if not self.needs_sudo:
                    try:
                        os.mkdir(self.filetoupdate.fn)
                    except OSError as e:
                        raise Updater4PyiError('Failed to create directory %s!' % self.filetoupdate.fn)

            else:
                self.extractto = basedir
            if self.needs_sudo:
                self.installto = self.extractto
                self.extracttotemp = True
                self.extractto = tempfile.mkdtemp(suffix='', prefix='upd4pyi_tmp_xtract_', dir=None)
            return self.extractto

    def install_update(self, rel_info):
        """
        Install a given update. `rel_info` should be a
        :py:class:`upd_source.BinReleaseInfo` returned by :py:meth:`check_for_updates`.

        The actual updates are downloaded by calling :py:meth:`download_file`. You may
        overload that function if you need to customize the download process. You may also
        override :py:meth:`verify_download` to implement some download integrity verification.

        This function does not return anything. If an error occurred,
        :py:exc:`upd_defs.Updater4PyiError` is raised.
        """
        tmpfile = tempfile.NamedTemporaryFile(mode='w+b', prefix='upd4pyi_tmp_', dir=None, delete=False)
        url = rel_info.get_url()
        try:
            self.download_file(url, tmpfile)
        except IOError as e:
            if hasattr(e, 'code'):
                raise Updater4PyiError('Got HTTP error: %d %s' % (e.code, e.reason))
            elif hasattr(e, 'reason'):
                raise Updater4PyiError('Connection error: %s' % e.reason)
            else:
                raise Updater4PyiError('Error: %s' % str(e))

        if not self.verify_download(rel_info, tmpfile):
            logger.warning('Failed to download %s : download verification failed.', url)
            os.unlink(tmpfile)
            raise Updater4PyiError('Failed to download software update: verification failed.')
        filetoupdate = self._file_to_update
        needs_sudo = not (util.locationIsWritable(filetoupdate.fn) and util.dirIsWritable(os.path.dirname(filetoupdate.fn)))
        needs_work_in_temp_dir = needs_sudo or util.is_win()
        logger.debug('installation will need sudo? %s', needs_sudo)
        reltype_is_dir = filetoupdate.reltype in (RELTYPE_BUNDLE_ARCHIVE,
         RELTYPE_ARCHIVE)
        extractedfile = None
        installto = None
        extractloc = None

        def cleanuptempfiles():
            if tmpfile.name and os.path.exists(tmpfile.name):
                logger.debug('cleaning up maybe %s', tmpfile.name)
                util.ignore_exc(lambda : os.unlink(tmpfile.name), OSError)
            if extractloc is not None and extractloc.extracttotemp and os.path.exists(extractloc.extractto):
                logger.debug('cleaning up maybe %s', extractloc.extractto)
                util.ignore_exc(lambda : shutil.rmtree(extractloc.extractto), OSError)
            return

        backupfilename = _backupname(filetoupdate.fn)
        if not needs_work_in_temp_dir:
            try:
                os.rename(filetoupdate.fn, backupfilename)
            except OSError as e:
                cleanuptempfiles()
                raise Updater4PyiError('Failed to rename file %s!' % str(e))

        def failure_cleanupandrestorebackup():
            cleanuptempfiles()
            if extractedfile and os.path.exists(extractedfile):
                logger.debug('cleaning up maybe %s', extractedfile)
                util.ignore_exc(lambda : shutil.rmtree(extractedfile), OSError)
            if needs_work_in_temp_dir:
                return
            logger.debug('cleaning up maybe %s', filetoupdate.fn)
            util.ignore_exc(lambda : shutil.rmtree(filetoupdate.fn), OSError)
            try:
                logger.debug('restoring backup %s -> %s', backupfilename, filetoupdate.fn)
                shutil.move(backupfilename, filetoupdate.fn)
            except OSError as e:
                logger.error('Software Update Error: Failed to restore backup %s of %s! %s\n' % (
                 backupfilename, filetoupdate.fn, str(e)))

        try:
            if reltype_is_dir:
                extractloc = Updater._ExtractLocation(filetoupdate=filetoupdate, needs_sudo=needs_work_in_temp_dir)
                logger.debug('extractloc: %r', extractloc.__dict__)
                if zipfile.is_zipfile(tmpfile.name):
                    thezipfile = zipfile.ZipFile(tmpfile.name, 'r')
                    extractloc.findextractto(namelist=thezipfile.namelist())
                    extractto = extractloc.extractto
                    permdata = None
                    if '_updater4pyi_metainf.json' in thezipfile.namelist():
                        try:
                            permdata = json.load(thezipfile.open('_updater4pyi_metainf.json'))
                        except ValueError as e:
                            logger.warning('Invalid JSON data in metainf file _updater4pyi_metainf.json: %s' % str(e))

                    for zinfo in thezipfile.infolist():
                        if zinfo.filename in Updater.SPECIAL_ZIP_FILES:
                            continue
                        thezipfile.extract(zinfo, extractto)
                        os.chmod(os.path.join(extractto, zinfo.filename), 493)

                    thezipfile.close()
                    if permdata and 'permissions' in permdata:
                        for pattern, perm in permdata['permissions'].iteritems():
                            logger.debug('pattern: %s to perms=%s' % (pattern, perm))
                            iperm = int(perm, 0)
                            for it in glob.iglob(os.path.join(filetoupdate.fn, pattern)):
                                logger.debug('Changing permissions of %s to %#o' % (it, iperm))
                                try:
                                    os.chmod(it, iperm)
                                except OSError:
                                    logger.warning('Failed to set permissions to file %s. Ignoring.' % it)

                    os.unlink(tmpfile.name)
                elif tarfile.is_tarfile(tmpfile.name):
                    thetarfile = tarfile.open(tmpfile.name, 'r')
                    extractloc.findextractto(namelist=thetarfile.getnames())
                    extractto = extractloc.extractto
                    thezipfile.extractall(extractto)
                    thezipfile.close()
                    os.unlink(tmpfile.name)
                else:
                    raise Updater4PyiError('Downloaded file %s is not a recognized archive.' % os.path.basename(tmpfile.name))
                extractedfile = os.path.join(extractto, os.path.basename(filetoupdate.fn))
                installto = extractloc.installto
                fnreltoextract = os.path.relpath(filetoupdate.executable, start=filetoupdate.fn)
                if not os.path.exists(os.path.join(extractedfile, fnreltoextract)):
                    logger.error("Update package doesn't contain file %s in %s", fnreltoextract, extractedfile)
                    raise Updater4PyiError("Update package is malformed: can't find executable")
            else:
                os.chmod(tmpfile.name, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                if not needs_work_in_temp_dir:
                    shutil.move(tmpfile.name, filetoupdate.fn)
                else:
                    extractedfile = tmpfile.name
                    installto = filetoupdate.fn
            if needs_work_in_temp_dir:
                if util.is_linux() or util.is_macosx():
                    res = util.run_as_admin([util.which('bash'),
                     util.resource_path('updater4pyi/installers/unix/do_install.sh'),
                     filetoupdate.fn, backupfilename, extractedfile, installto])
                    if res != 0:
                        raise Updater4PyiError("Can't install the update to the final location %s!" % installto)
                elif util.is_win():
                    doinstalldirname = tempfile.mkdtemp(prefix='upd4pyi_tmp_')
                    doinstallzipfile = zipfile.ZipFile(util.resource_path('updater4pyi/installers/win/do_install.exe.zip'), 'r')
                    doinstallzipfile.extractall(doinstalldirname)
                    manage_install_cmd = [
                     os.path.join(doinstalldirname, 'manage_install.exe'),
                     str(os.getpid()),
                     '1' if needs_sudo else '0',
                     filetoupdate.fn,
                     backupfilename,
                     extractedfile,
                     installto,
                     doinstalldirname,
                     filetoupdate.executable]
                    logger.debug('Running %r as %s', manage_install_cmd, 'admin' if needs_sudo else 'normal user')
                    util.run_win(argv=manage_install_cmd, needs_sudo=False, wait=False, cwd=os.path.expanduser('~'))
                    sys.exit(0)
                else:
                    logger.error("I don't know your platform to run sudo install on: %s", util.simple_platform())
                    raise RuntimeError('Unknown platform for sudo install: %s' % util.simple_platform())
        except Exception:
            logger.error('Software Update Error: %s\n' % str(sys.exc_info()[1]))
            failure_cleanupandrestorebackup()
            raise

        logger.debug('cleaning up temp files')
        cleanuptempfiles()
        if not needs_work_in_temp_dir:
            if reltype_is_dir:
                logger.debug('removing backup directory %s', backupfilename)
                try:
                    shutil.rmtree(backupfilename)
                except (OSError, IOError):
                    logger.warning('Failed to remove backup directory %s !', backupfilename)

            else:
                logger.debug('removing backup file %s', backupfilename)
                try:
                    os.unlink(backupfilename)
                except (OSError, IOError):
                    logger.warning('Failed to remove backup file %s !', backupfilename)

        return

    def download_file(self, theurl, fdst):
        """
        Download the file given at location `theurl` to the destination file `fdst`.

        You may reimplement this function to customize the download process. Check out
        `upd_downloader.url_opener` if you want to download stuff from an HTTPS url, it
        may be useful.

        The default implementation downloads the file with the `upd_downloader` utility
        which provides secure downloads with certificate validation for HTTPS downloads.

        This function should return nothing. If an error occurs, this function should
        raise an `IOError`.
        """
        logger.debug('fetching URL %s to temp file %s ...', theurl, util.ignore_exc(lambda : fdst.name))
        fdata = upd_downloader.url_opener.open(theurl)
        shutil.copyfileobj(fdata, fdst)
        fdata.close()
        fdst.close()
        logger.debug('... done.')

    def verify_download(self, rel_info, tmpfile):
        """
        Verify the integrity of the downloaded file. Return `True` if the download
        succeeded or `False` if not.

        Arguments:

            - `rel_info` is the release information as a
              :py:class:`upd_source.BinReleaseInfo` instance, as given to
              :py:meth:`install_update`.

            - `tmpfile` is a python :py:class:`tempfile.NamedTemporaryFile` instance
              where the file was downloaded. This function should in principle check
              the validity of the contents of this file.

        You may reimplement this function to implement integrity check. The default
        implementation does nothing and returns `True`.

        Don't raise arbitrary exceptions here because they might not be caught. You may
        raise :py:exc:`upd_defs.Updater4PyiError` for serious errors, though.
        """
        return True

    def restart_app(self):
        """
        Utility to restart the application. This is meant for graphical applications which
        start in the background.

        The application exit is done by calling ``sys.exit(0)``.
        """
        exe = self._file_to_update.executable
        if util.is_macosx() or util.is_linux():
            exe_cmd = util.bash_quote(exe)
            if util.is_macosx() and exe == self._file_to_update.executable and self._file_to_update.fn.lower().endswith('.app'):
                exe_cmd = 'open ' + util.bash_quote(self._file_to_update.fn)
            this_pid = os.getpid()
            subprocess.Popen('while ps -p %d >/dev/null; do sleep 1; done; ( %s & )' % (
             this_pid, exe_cmd), shell=True)
            sys.exit(0)
        elif util.is_win():
            raise RuntimeError("Can't use restart_app on windows. The manage_install.exe process already takes care of that.")
        else:
            logger.warning("I don't know about your platform. You'll have to restart this program by yourself like a grown-up. I'm exiting now! Have fun.")
            sys.exit(0)


def _backupname(filename):
    try_suffix = '.bkp'
    n = 1
    while n < 999 and os.path.exists(filename + try_suffix):
        try_suffix = '.' + str(n) + '.bkp'
        n += 1

    if os.path.exists(filename + try_suffix):
        raise Updater4PyiError("Can't figure out a backup name for file %s!!" % filename)
    logger.debug('Got backup name: %s' % (filename + try_suffix))
    return filename + try_suffix