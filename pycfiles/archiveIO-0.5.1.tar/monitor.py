# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/archivedb/monitor.py
# Compiled at: 2011-12-26 16:31:26
import os, sys, logging, re, time, archivedb.config as config, archivedb.sql as sql
from archivedb.common import md5sum, split_path
from archivedb.logger import log_traceback
log = logging.getLogger(__name__)
args = config.args

class EmptyClass:

    def __init__(self):
        pass


if os.name == 'posix':
    try:
        import pyinotify
        from pyinotify import ProcessEvent, IN_CLOSE_WRITE, IN_DELETE, IN_MOVED_FROM, IN_MOVED_TO, IN_ISDIR, IN_CREATE
    except ImportError:
        log.warning("module 'pyinotify' not found. disabling inotify monitoring")
        del args['threads'][args['threads'].index('inotify')]
        ProcessEvent = EmptyClass

def is_ignored_file(f):
    for regex in args['ignore_files']:
        if regex == '':
            continue
        if re.search(regex, f, re.I):
            log.debug(("file '{0}' matched '{1}', skipping.").format(f, regex))
            return True

    return False


def is_ignored_directory(full_path):
    for d in args['ignore_dirs']:
        if d == '':
            continue
        if d in full_path:
            log.debug(("directory '{0}' matched ignore_dir '{1}', skipping").format(full_path, d))
            return True

    return False


def add_file(db, full_path):
    if not os.path.isfile(full_path) or os.path.islink(full_path):
        return
        mtime = os.stat(full_path).st_mtime
        size = os.stat(full_path).st_size
        (watch_dir, path, filename) = split_path(args['watch_dirs'], full_path)
        data = db.get_fields(watch_dir, path, filename, ['mtime', 'size'])
        data or log.info(('generating checksum for {0} ...').format(filename))
        md5 = md5sum(full_path)
        if md5:
            log.info(('inserting {0} into the database.').format(filename))
            db.insert_file(watch_dir, path, filename, md5, mtime, size)
        else:
            log.warn(("file '{0}' was moved/deleted during md5sum creation. not being added to database").format(full_path))
    else:
        old_mtime = data[0][0]
        old_size = data[0][1]
        if int(old_mtime) != int(mtime) or int(old_size) != int(size):
            log.debug(('old_mtime = {0}').format(old_mtime))
            log.debug(('mtime = {0}').format(mtime))
            log.debug(('old_size = {0}').format(old_size))
            log.debug(('size = {0}').format(size))
            log.info(('generating checksum for {0} ...').format(filename))
            md5 = md5sum(full_path)
            if md5:
                log.info(('updating {0} in the database.').format(filename))
                rows_changed = db.update_file(watch_dir, path, filename, md5, mtime, size)
                log.debug(('rows_changed = {0}').format(rows_changed))
            else:
                log.warn(("file '{0}' was moved/deleted during md5sum creation. not being added to database").format(full_path))


def scan_dir(db, d):
    if not os.path.isdir(d):
        log.warning(("'{0}' does not exist, skipping.").format(d))
        return
    log.info(("scanning directory: '{0}'").format(d))
    for (root, dirs, files) in os.walk(d):
        for f in files:
            full_path = os.path.join(root, f)
            if not is_ignored_file(f) and not is_ignored_directory(full_path):
                add_file(db, full_path)


def run_oswalk():
    log.info('oswalk thread: start')
    while True:
        db = sql.DatabaseConnection(args['db_host'], args['db_user'], args['db_pass'], args['db_name'], args['db_port'], 'archive')
        try:
            for watch_dir in args['watch_dirs']:
                scan_dir(db, watch_dir)

        except:
            log_traceback(sys.exc_info(), 'Exception raised in run_oswalk():')

        log.info('oswalk thread: sleeping')
        time.sleep(args['scan_interval'] * 3600)


class InotifyHandler(ProcessEvent):

    def my_init(self):
        log.debug('calling my_init()')
        self.db = sql.DatabaseConnection(args['db_host'], args['db_user'], args['db_pass'], args['db_name'], args['db_port'], 'archive')
        self.last_moved = None
        return

    def check_last_moved(self, event):
        """
            This is my solution for recognizing when files are moved
            outside of the given watch directories which should be deleted:
            
            When moving a file within the given watch directories, it is
            assumed that immediately after the IN_MOVED_FROM event,
            an IN_MOVED_TO event follows. So if there is no IN_MOVED_TO
            event, it's assumed that the file was moved outside 
            of the watch directories
            
            process_IN_MOVED_FROM sets self.last_moved to the latest
            moved file
            
            This function will check event.src_pathname with self.last_moved,
            if they're equal, then the file is moved within the watch_dirs
            
            This function should be called at the top of ALL process_* functions
            
        """
        del_last_moved = False
        if self.last_moved:
            log.debug(('self.last_moved = {0}').format(self.last_moved))
            if 'IN_MOVED_TO' in event.maskname.split('|'):
                if not hasattr(event, 'src_pathname'):
                    del_last_moved = True
                log.debug(('event.src_pathname = {0}').format(event.src_pathname))
                log.debug(('self.last_moved.pathname = {0}').format(self.last_moved.pathname))
                if event.src_pathname == self.last_moved.pathname:
                    self.last_moved = None
                else:
                    del_last_moved = True
            else:
                del_last_moved = True
        if del_last_moved:
            log.debug('it is assumed file was moved outside watch_dirs, deleting.')
            log.info(("deleting '{0}'").format(self.last_moved.pathname))
            if self.last_moved.dir:
                self.db.delete_directory(self.last_moved.pathname)
            else:
                self.db.delete_file(self.last_moved)
            self.last_moved = None
        return

    def process_IN_CLOSE_WRITE(self, event):
        log.debug(event)
        self.check_last_moved(event)
        full_path = event.pathname
        f = event.name
        if not is_ignored_file(f) and not is_ignored_directory(full_path):
            add_file(self.db, full_path)

    def process_IN_DELETE(self, event):
        log.debug(event)
        self.check_last_moved(event)
        if event.dir:
            self.db.delete_directory(event.pathname)
        else:
            self.db.delete_file(event.pathname)

    def process_IN_MOVED_FROM(self, event):
        """
            Used to delete files from database that have been moved out of
            the program's watch_dirs
        """
        log.debug(event)
        self.check_last_moved(event)
        self.last_moved = event

    def process_IN_MOVED_TO(self, event):
        """
            Note about how the IN_MOVED_TO event works:
            when a dir/file is moved, if it's source location is being monitored
            by inotify, there will be an attribute in the event called src_pathname.
            if the dir/file was moved from somewhere outside of pyinotify's watch,
            the src_pathname attribute won't exist.
        """
        log.debug(event)
        self.check_last_moved(event)
        try:
            src_full_path = event.src_pathname
        except AttributeError:
            src_full_path = None

        dest_full_path = event.pathname
        dest_filename = event.name
        if not is_ignored_file(dest_filename) and not is_ignored_directory(dest_full_path):
            if src_full_path:
                if event.dir:
                    src_full_path += os.sep
                    dest_full_path += os.sep
                src_split_path = split_path(args['watch_dirs'], src_full_path)
                dest_split_path = split_path(args['watch_dirs'], dest_full_path)
                log.debug(('src_split_path    = {0}').format(src_split_path))
                log.debug(('dest_split_path    = {0}').format(dest_split_path))
                if event.dir:
                    log.info(("directory '{0}' has been moved to '{1}', updating.").format(src_full_path, dest_full_path))
                    rows_changed = self.db.move_directory(src_split_path, dest_split_path)
                else:
                    log.info(('{0} has been moved to {1}, updating.').format(src_full_path, dest_full_path))
                    rows_changed = self.db.move_file(src_split_path, dest_split_path)
                log.debug(('rows_changed = {0}').format(rows_changed))
                if rows_changed == 0:
                    log.debug(('no rows were changed during UPDATE, inserting {0} into database.').format(dest_full_path))
                    if event.dir:
                        scan_dir(self.db, dest_full_path)
                    else:
                        add_file(self.db, dest_full_path)
            elif event.dir:
                scan_dir(self.db, dest_full_path)
            else:
                add_file(self.db, dest_full_path)
        elif src_full_path:
            self.db.delete_file(src_full_path)
        return


def run_inotify():
    masks = IN_CLOSE_WRITE | IN_DELETE | IN_MOVED_FROM | IN_MOVED_TO | IN_ISDIR | IN_CREATE
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, default_proc_fun=InotifyHandler())
    log.info('initializing inotify monitoring')
    for watch_dir in args['watch_dirs']:
        log.info(("now monitoring: '{0}'").format(watch_dir))
        wm.add_watch(watch_dir, masks, rec=True, auto_add=True)

    log.info('starting inotify monitoring')
    try:
        notifier.loop()
    except:
        log_traceback(sys.exc_info(), 'Exception raised in run_inotify():')