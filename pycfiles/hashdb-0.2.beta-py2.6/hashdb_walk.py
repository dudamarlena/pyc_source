# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_walk.py
# Compiled at: 2011-01-06 01:42:59
from hashdb_output import log
import re, fnmatch, os, stat, platform
from collections import namedtuple, deque
from hashdb_mntent_wrapper import MountEntries, MountEntry
PREFIX_ROOT = 'root '
PREFIX_SKIP = 'skip '
PREFIX_REG = 'file '
PREFIX_DIR = 'dir  '
PREFIX_SYM = 'syml '
PREFIX_HARD = 'hard '
PREFIX_BIND = 'bind '

class Walker(object):
    Target = namedtuple('Target', 'true user stat')

    def __init__(self):
        object.__init__(self)
        self._targets = []
        self._skip_fstypes = []
        self._skip_paths = []
        self._skip_names = []
        self._skip_dirnames = []
        self._skip_filenames = []
        self._skip_binds = True
        self._walk_depth = True

    @property
    def walk_depth(self):
        return self._walk_depth

    @walk_depth.setter
    def walk_depth(self, value):
        self._walk_depth = value

    def add_target(self, root):
        try:
            root_user = root
            root_true = MountEntries().truepath(root)
            root_stat = os.lstat(root_true)
            self._targets.append(Walker.Target(root_true, root_user, root_stat))
        except OSError, ex:
            log.warning('warning: unable to stat %r: %s' % (root, ex))

    def add_targets(self, roots):
        for root in roots:
            self.add_target(root)

    def add_skip_fstype(self, name):
        self._skip_fstypes.append(name)

    def add_skip_fstypes(self, names):
        self._skip_fstypes.extend(names)

    def add_skip_path(self, name):
        self._skip_paths.append(name)

    def add_skip_paths(self, names):
        self._skip_paths.extend(names)

    def add_skip_name(self, name):
        self._skip_names.append(name)

    def add_skip_names(self, names):
        self._skip_names.extend(names)

    def add_skip_dirname(self, name):
        self._skip_dirnames.append(name)

    def add_skip_dirnames(self, names):
        self._skip_dirnames.extend(names)

    def add_skip_filename(self, name):
        self._skip_filenames.append(name)

    def add_skip_filenames(self, names):
        self._skip_filenames.extend(names)

    def set_skip_binds(self, skip=True):
        self._skip_binds = skip

    def build_fskip_globs(self, globs):
        if len(globs) == 0:
            return None
        else:

            def fskip(name):
                return exp.match(name) != None

            fskip.func_globals['exp'] = re.compile(('|').join('(?:%s)' % fnmatch.translate(glob) for glob in globs))
            return fskip

    def walk(self):
        targets = set(self._targets)
        fskip_fstype = self.build_fskip_globs(self._skip_fstypes)
        fskip_path = self.build_fskip_globs(self._skip_paths)
        fskip_name = self.build_fskip_globs(self._skip_names)
        fskip_dirname = self.build_fskip_globs(self._skip_dirnames)
        fskip_filename = self.build_fskip_globs(self._skip_filenames)
        fskip_access = None
        skip_binds = self._skip_binds
        mounts = MountEntries()
        if platform.system() != 'Windows':

            def skip_access(target):
                access = stat.S_IMODE(target.stat.st_mode)
                if access & (stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH) == 0:
                    return True
                if target.stat.st_uid == euid:
                    if access & stat.S_IRUSR == 0:
                        return True
                else:
                    if access & (stat.S_IRGRP | stat.S_IROTH) == 0:
                        return True
                    if target.stat.st_gid in groups:
                        if access & stat.S_IRGRP == 0:
                            return True
                    elif access & stat.S_IROTH == 0:
                        return True
                return False

            skip_access.func_globals['uid'] = os.getuid()
            skip_access.func_globals['euid'] = os.geteuid()
            skip_access.func_globals['gid'] = os.getgid()
            skip_access.func_globals['egid'] = os.getegid()
            skip_access.func_globals['groups'] = os.getgroups()
            fskip_access = skip_access
        try:
            todo = deque()
            dirs = deque()
            if self.walk_depth:
                fappend = dirs.appendleft

                def fdone():
                    todo.extendleft(dirs)
                    dirs.clear()

            else:
                fappend = todo.append

                def fdone():
                    pass

            for target in targets:
                log.verbose(PREFIX_ROOT + '%s (root)' % target.user)
                if stat.S_ISREG(target.stat.st_mode):
                    result = yield target
                if stat.S_ISDIR(target.stat.st_mode):
                    result = not (yield target)
                    if not result:
                        if log.is_debug:
                            log.debug(PREFIX_SKIP + '%s (yield returned true)' % child.user)
                        continue
                    todo.clear()
                    todo.append(target)
                    while True:
                        try:
                            target = todo.popleft()
                        except IndexError, _:
                            break

                        try:
                            filelist = os.listdir(target.true)
                            filelist.sort()
                        except OSError, ex:
                            log.warning('warning: Unable to list target %r: %s' % (target.user, ex))
                            continue

                        for name in filelist:
                            child = Walker.Target(os.path.join(target.true, name), os.path.join(target.user, name), None)
                            if fskip_name:
                                if fskip_name(name):
                                    if log.is_debug:
                                        log.debug(PREFIX_SKIP + '%s (skip_name)' % child.user)
                                    continue
                                if fskip_path and fskip_path(child.user):
                                    pass
                                elif log.is_debug:
                                    log.debug(PREFIX_SKIP + '%s (skip_path)' % child.user)
                                continue
                            try:
                                child = child._replace(stat=os.lstat(child.true))
                            except OSError, ex:
                                log.warning('warning: Unable to lstat %r: %s' % (child.user, ex))
                                if log.is_debug:
                                    log.debug(PREFIX_SKIP + '%r (failed lstat)' % child.user)
                                continue

                            if fskip_access != None and fskip_access(child):
                                log.debug(PREFIX_SKIP + '%r (no access)' % child.user)
                                continue
                            if stat.S_ISLNK(child.stat.st_mode):
                                pass
                            else:
                                log.debug(PREFIX_SYM + '%s (sym link)' % child.user)
                                try:
                                    child = child._replace(true=mounts.truepath(child.true))
                                    child = child._replace(stat=os.lstat(child.true))
                                except OSError, ex:
                                    log.warning('warning: Unable to read symlink %r: %s' % (child.user, ex))
                                    if log.is_debug:
                                        log.debug(PREFIX_SKIP + '%r (failed to read symlink)' % child.user)
                                    continue

                                if fskip_access != None:
                                    if fskip_access(child):
                                        log.debug(PREFIX_SKIP + '%r (no access)' % child.user)
                                        continue
                                if stat.S_ISREG(child.stat.st_mode):
                                    if fskip_filename:
                                        if fskip_filename(child.user):
                                            if log.is_debug:
                                                log.debug(PREFIX_SKIP + '%s (skip_filename)' % child.user)
                                            continue
                                        if log.is_verbose:
                                            log.verbose(PREFIX_REG + '%s (regular file)' % child.user)
                                        result = yield child
                                        continue
                                    if stat.S_ISDIR(child.stat.st_mode):
                                        if fskip_dirname:
                                            if fskip_dirname(child.user):
                                                if log.is_debug:
                                                    log.debug(PREFIX_SKIP + '%s (skip_dirname)' % child.user)
                                                continue
                                            keep = None
                                            if target.stat.st_dev != child.stat.st_dev or target.stat.st_ino == child.stat.st_ino:
                                                if mounts.is_bind(child.true):
                                                    if skip_binds:
                                                        pass
                                                    elif log.is_debug:
                                                        log.debug(PREFIX_SKIP + '%s (skip_binds)' % child.user)
                                                    continue
                                                log.debug(PREFIX_BIND + '%s (bind mount)' % child.user)
                                                try:
                                                    child = child._replace(true=mounts.truepath(child.true))
                                                    child = child._replace(stat=os.lstat(child.true))
                                                except OSError, ex:
                                                    log.warning('warning: Unable to read bind target %r: %s' % (child.user, ex))
                                                    if log.is_debug:
                                                        log.debug(PREFIX_SKIP + '%r (failed to read bind target)' % (child.user, ex))
                                                    continue
                                                else:
                                                    if fskip_access != None and fskip_access(child):
                                                        log.debug(PREFIX_SKIP + '%r (no access)' % child.user)
                                                        continue
                                                    keep = True
                                            if fskip_fstype:
                                                fstype = mounts.get_fstype(child.true)
                                                if fstype == None:
                                                    mounts = MountEntries()
                                                    fstype = mounts.get_fstype(child.true)
                                                if fstype == None:
                                                    log.warning('warning: Unable to resolve mount fstype %r' % child.user)
                                                    log.debug(PREFIX_SKIP + '%s (failed to resolve mount fstype)' % child.user)
                                                    continue
                                                mounts = mounts
                                                if fskip_fstype(fstype.type):
                                                    pass
                                                elif log.is_debug:
                                                    log.debug(PREFIX_SKIP + '%s (skip_fstype)' % child.user)
                                                continue
                                        if keep == True:
                                            fappend(child)
                                            continue
                                    if log.is_verbose:
                                        log.verbose(PREFIX_DIR + '%s (directory)' % child.user)
                                    result = not (yield child)
                                    if result:
                                        fappend(child)
                                        continue
                                    else:
                                        if log.is_debug:
                                            log.debug(PREFIX_SKIP + '%s (yield returned true)' % child.user)
                                        continue
                                if log.is_debug:
                                    log.debug(PREFIX_SKIP + '%s (unknown st_mode %r)' % (child.user, child.stat))

                        fdone()

        except Exception, ex:
            log.exception('Unexpected exception!')

        return