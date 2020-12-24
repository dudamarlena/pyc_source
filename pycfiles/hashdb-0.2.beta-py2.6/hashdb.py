# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb.py
# Compiled at: 2011-01-06 01:19:27
from hashdb_output import log, VERBOSE, QUIET, DEBUG, DEFAULT
from hashdb_config_base import CombineDB
from hashdb_walk import Walker, PREFIX_SKIP
from hashdb_db import HashDatabase
from hashdb_hash import build_hash
from hashdb_config import parse_config, display_settings
from hashdb_mntent_wrapper import MountEntries, MountEntry
import stat, time, locale, os
locale.setlocale(locale.LC_ALL, '')
from collections import namedtuple
HashRowData = namedtuple('HashRowData', 'path hash mark size time')

def setting(name, default, canset=True, doc=None):

    def fget(self):
        return self._settings.get(name, default)

    def fset(self, value):
        self._settings[name] = value

    fget.default = default
    fget.settingname = name
    return property(fget=fget, fset=fset if canset else None, doc=doc)


class AppHashDB(object):
    _defaults = {}

    def __init__(self, use_cmdline=False, use_configfile=False):
        object.__init__(self)
        if use_cmdline:
            self._settings = parse_config()
        elif use_configfile:
            self._settings = parse_config({})
        else:
            self._settings = {}

    setting_verbosity = setting('verbosity', DEFAULT)
    setting_database = setting('database', '/var/lib/hashdb/hashdb.db')
    setting_combine = setting('combine', [])
    setting_walk_depth = setting('walk_depth', True)
    setting_skip_binds = setting('skip_binds', False)
    setting_skip_fstypes = setting('skip_fstypes', [])
    setting_skip_paths = setting('skip_paths', [])
    setting_skip_names = setting('skip_names', [])
    setting_skip_dirnames = setting('skip_dirnames', [])
    setting_skip_filenames = setting('skip_filenames', [])
    setting_cmd = setting('cmd', 'hash')
    setting_hash_definitive = setting('hash_definitive', False)
    setting_hash_force = setting('hash_force', False)
    setting_match_check = setting('match_check', True)
    setting_match_any = setting('match_any', True)
    setting_targets = setting('targets', [''])

    @property
    def settings(self):
        results = {}
        for name in dir(self.__class__):
            if name.startswith('setting_'):
                results[getattr(self.__class__, name).fget.settingname] = getattr(self.__class__, name).fget.default

        results.update(self._settings)
        return results

    @settings.setter
    def settings(self, value):
        self._settings = value

    def add_skip_fstype(self, fstype):
        self.setting_skip_fstype = self.setting_skip_fstype + [fstype]

    def add_skip_fstypes(self, fstypes):
        self.setting_skip_fstype = self.setting_skip_fstype + fstypes

    def add_skip_path(self, path):
        self.setting_skip_paths = self.setting_skip_paths + [path]

    def add_skip_paths(self, paths):
        self.setting_skip_paths = self.setting_skip_paths + paths

    def add_skip_name(self, name):
        self.setting_skip_names = self.setting_skip_names + [name]

    def add_skip_names(self, names):
        self.setting_skip_names = self.setting_skip_names + names

    def add_skip_dirname(self, dirname):
        self.setting_skip_dirnames = self.setting_skip_dirnames + [dirname]

    def add_skip_dirnames(self, dirnames):
        self.setting_skip_dirnames = self.setting_skip_dirnames + dirnames

    def add_skip_filename(self, filename):
        self.setting_skip_filenames = self.setting_skip_filenames + [filename]

    def add_skip_filenames(self, filenames):
        self.setting_skip_filenames = self.setting_skip_filenames + filenames

    def add_target(self, target):
        self.setting_targets = self.setting_targets + [target]

    def add_targets(self, targets):
        self.setting_targets = self.setting_targets + targets

    def add_combine(self, database, local=None, remote=None):
        self.setting_combine = self.setting_combine + [CombineDB(local, database, remote)]

    def run(self):
        if self.setting_cmd == 'hash':
            return self.run_hash()
        if self.setting_cmd == 'match':
            return self.run_match()
        if self.setting_cmd == 'view':
            return self.run_view()

    def run_hash(self):
        for (target, hash, db) in self.hash():
            log.default('%s  %s' % (hash, target.user))

    def run_match(self):
        for (target, target_data, matches, db) in self.match():
            log.default('* %s' % target.user)
            log.default('  %s' % target_data.path)
            for (match, stat) in matches:
                log.default('  %s' % match.path)

    def run_view(self):
        timeformat = locale.nl_langinfo(locale.D_T_FMT)
        numpadd = len(locale.format('%d', 2147483648, True))
        for (row, db) in self.view():
            m = '*' if row.mark == 0 else ' '
            h = row.hash
            s = locale.format('%d', row.size, True)
            t = time.strftime(timeformat, time.localtime(row.time))
            p = row.path
            log.default('%s%s %s  %*s  %s' % (
             h,
             m,
             t,
             numpadd,
             s,
             p))

    def view(self):
        log.setLevel(self.setting_verbosity)
        display_settings(self.settings, log.debug)
        log.debug("* setup database's...")
        db = HashDatabase(self.setting_database)
        db.add_combines(self.setting_combine)
        if not db.open():
            return
        mounts = MountEntries()
        targets = [ mounts.truepath(t) for t in self.setting_targets ]
        qfilters = []
        qargmap = {}
        if '/' not in targets:
            for (i, target) in enumerate(targets):
                target = mounts.truepath(target)
                qfilters.append("(path = :%(name)s) OR (substr(path, 1, :%(name)s_len + 1) = :%(name)s || '/')" % {'name': 't%02d' % i})
                qargmap.update({'t%02d' % i: target, 
                   't%02d_len' % i: len(target)})

        qfilter = 'WHERE ' + (' OR ').join(qfilters) if len(qfilters) != 0 else ''
        qorder = '\n            ORDER BY\n                path,\n                mark DESC\n        ' if self.setting_walk_depth else '\n            ORDER BY\n                count_components(path),\n                path,\n                mark DESC\n        '
        query = '\n            SELECT\n                *\n            FROM\n                combinedtab\n        ' + qfilter + qorder
        for row in db.connection.execute(query, qargmap):
            yield (
             HashRowData(path=row['path'], hash=row['hash'], mark=row['mark'], time=row['time'], size=row['size']), db)

    def hash(self):
        log.setLevel(self.setting_verbosity)
        display_settings(self.settings, log.debug)
        log.debug("* setup database's...")
        db = HashDatabase(self.setting_database)
        db.add_combines(self.setting_combine)
        if not db.open():
            return
        else:
            log.debug('* setup walker...')
            walker = Walker()
            walker.walk_depth = self.setting_walk_depth
            walker.add_targets(self.setting_targets)
            walker.add_skip_fstypes(self.setting_skip_fstypes)
            walker.add_skip_paths(self.setting_skip_paths)
            walker.add_skip_names(self.setting_skip_names)
            walker.add_skip_dirnames(self.setting_skip_dirnames)
            walker.add_skip_filenames(self.setting_skip_filenames)
            log.debug('* walk...')
            walk = walker.walk()
            try:
                target = walk.next()
                while True:
                    if stat.S_ISDIR(target.stat.st_mode):
                        if db.path_dirdone(target.true):
                            target = walk.send(True)
                            continue
                    elif stat.S_ISREG(target.stat.st_mode):
                        hash = db.path_hash(target.true, target.stat)
                        if hash == None:
                            hash = build_hash(target)
                            if hash != None:
                                db.path_insert(target.true, target.stat, hash)
                        if hash != None:
                            yield (
                             target, hash, db)
                        else:
                            log.debug(PREFIX_SKIP + '%s (unable to hash file)' % target.user)
                    target = walk.next()

            except StopIteration, _:
                pass

            return

    def match(self):
        matches_done = set()
        for (target, hash, db) in self.hash():
            matches = []
            row = db.connection.execute('SELECT * FROM hashtab WHERE path=?', (target.true,)).fetchone()
            if not row:
                log.debug(PREFIX_SKIP + '%r (unable to get row)' % target.user)
                continue
            target_data = HashRowData(path=row['path'], hash=row['hash'], mark=row['mark'], time=row['time'], size=row['size'])
            if (
             target_data.hash, target_data.size) in matches_done:
                log.debug(PREFIX_SKIP + '%r (already reported match)' % target.user)
                continue
            matches_done.add((target_data.hash, target_data.size))
            for row in db.connection.execute('\n                        SELECT\n                            *\n                        FROM\n                            hashtab\n                        WHERE\n                            (hash =  :hash) AND\n                            (path <> :path) AND\n                            (size =  :size)\n                    UNION\n                        SELECT\n                            *\n                        FROM\n                            combinedtab\n                        WHERE\n                            (hash =  :hash) AND\n                            (path <> :path) AND\n                            (size =  :size)\n                    ORDER BY\n                        path,\n                        mark DESC\n                ', {'path': target_data.path, 'size': target_data.size, 'hash': target_data.hash}):
                match_data = HashRowData(path=row['path'], hash=row['hash'], mark=row['mark'], time=row['time'], size=row['size'])
                log.verbose('comp %s (found match in db)' % match_data.path)
                try:
                    match_stat = os.lstat(match_data.path)
                except OSError, _:
                    log.debug(PREFIX_SKIP + '%r (unable to lstat match): %s' % (match_data.path, ex))
                    continue
                except IOError, _:
                    log.debug(PREFIX_SKIP + '%r (unable to lstat match): %s' % (match_data.path, ex))
                    continue

                if not stat.S_ISREG(match_stat.st_mode):
                    log.debug(PREFIX_SKIP + '%r (not a regular file)' % match_data.path)
                    continue
                match_hash = db.path_hash(match_data.path, match_stat)
                if match_hash == None:
                    match_hash = build_hash(match_data.path)
                    if hash != None:
                        db.path_insert(match_data.path, match_stat, match_hash)
                if match_hash == None:
                    log.debug(PREFIX_SKIP + '%r (unable to determine hash)' % match_data.path)
                    continue
                match_data = match_data._replace(hash=match_hash, size=match_stat.st_size, time=match_stat.st_mtime, mark=db.mark)
                if match_data.hash != target_data.hash or match_data.size != target_data.size:
                    log.debug(PREFIX_SKIP + '%r (files no longer match)' % match_data.path)
                    continue
                matches.append((match_data, match_stat))

            if len(matches) != 0:
                yield (
                 target, target_data, matches, db)

        return


def main():
    app = AppHashDB(True)
    exit(app.run())


if __name__ == '__main__':
    main()