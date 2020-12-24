# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/req/req_uninstall.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 23734 bytes
from __future__ import absolute_import
import csv, functools, logging, os, sys, sysconfig
from pip._vendor import pkg_resources
from pip._internal.exceptions import UninstallationError
from pip._internal.locations import bin_py, bin_user
from pip._internal.utils.compat import WINDOWS, cache_from_source, uses_pycache
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import FakeFile, ask, dist_in_usersite, dist_is_local, egg_link_path, is_local, normalize_path, renames, rmtree
from pip._internal.utils.temp_dir import AdjacentTempDirectory, TempDirectory
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Set, Tuple
    from pip._vendor.pkg_resources import Distribution
logger = logging.getLogger(__name__)

def _script_names(dist, script_name, is_gui):
    """Create the fully qualified name of the files created by
    {console,gui}_scripts for the given ``dist``.
    Returns the list of file names
    """
    if dist_in_usersite(dist):
        bin_dir = bin_user
    else:
        bin_dir = bin_py
    exe_name = os.path.join(bin_dir, script_name)
    paths_to_remove = [exe_name]
    if WINDOWS:
        paths_to_remove.append(exe_name + '.exe')
        paths_to_remove.append(exe_name + '.exe.manifest')
        if is_gui:
            paths_to_remove.append(exe_name + '-script.pyw')
        else:
            paths_to_remove.append(exe_name + '-script.py')
    return paths_to_remove


def _unique(fn):

    @functools.wraps(fn)
    def unique(*args, **kw):
        seen = set()
        for item in fn(*args, **kw):
            if item not in seen:
                seen.add(item)
                yield item

    return unique


@_unique
def uninstallation_paths(dist):
    """
    Yield all the uninstallation paths for dist based on RECORD-without-.py[co]

    Yield paths to all the files in RECORD. For each .py file in RECORD, add
    the .pyc and .pyo in the same directory.

    UninstallPathSet.add() takes care of the __pycache__ .py[co].
    """
    r = csv.reader(FakeFile(dist.get_metadata_lines('RECORD')))
    for row in r:
        path = os.path.join(dist.location, row[0])
        yield path
        if path.endswith('.py'):
            dn, fn = os.path.split(path)
            base = fn[:-3]
            path = os.path.join(dn, base + '.pyc')
            yield path
            path = os.path.join(dn, base + '.pyo')
            yield path


def compact(paths):
    """Compact a path set to contain the minimal number of paths
    necessary to contain all paths in the set. If /a/path/ and
    /a/path/to/a/file.txt are both in the set, leave only the
    shorter path."""
    sep = os.path.sep
    short_paths = set()
    for path in sorted(paths, key=len):
        should_skip = any((path.startswith(shortpath.rstrip('*')) and path[len(shortpath.rstrip('*').rstrip(sep))] == sep for shortpath in short_paths))
        if not should_skip:
            short_paths.add(path)

    return short_paths


def compress_for_rename(paths):
    """Returns a set containing the paths that need to be renamed.

    This set may include directories when the original sequence of paths
    included every file on disk.
    """
    case_map = dict(((os.path.normcase(p), p) for p in paths))
    remaining = set(case_map)
    unchecked = sorted((set((os.path.split(p)[0] for p in case_map.values()))),
      key=len)
    wildcards = set()

    def norm_join(*a):
        return os.path.normcase((os.path.join)(*a))

    for root in unchecked:
        if any((os.path.normcase(root).startswith(w) for w in wildcards)):
            continue
        all_files = set()
        all_subdirs = set()
        for dirname, subdirs, files in os.walk(root):
            all_subdirs.update((norm_join(root, dirname, d) for d in subdirs))
            all_files.update((norm_join(root, dirname, f) for f in files))

        if not all_files - remaining:
            remaining.difference_update(all_files)
            wildcards.add(root + os.sep)

    return set(map(case_map.__getitem__, remaining)) | wildcards


def compress_for_output_listing(paths):
    """Returns a tuple of 2 sets of which paths to display to user

    The first set contains paths that would be deleted. Files of a package
    are not added and the top-level directory of the package has a '*' added
    at the end - to signify that all it's contents are removed.

    The second set contains files that would have been skipped in the above
    folders.
    """
    will_remove = set(paths)
    will_skip = set()
    folders = set()
    files = set()
    for path in will_remove:
        if path.endswith('.pyc'):
            continue
        if not path.endswith('__init__.py'):
            if '.dist-info' in path:
                folders.add(os.path.dirname(path))
            files.add(path)

    _normcased_files = set(map(os.path.normcase, files))
    folders = compact(folders)
    for folder in folders:
        for dirpath, _, dirfiles in os.walk(folder):
            for fname in dirfiles:
                if fname.endswith('.pyc'):
                    continue
                file_ = os.path.join(dirpath, fname)
                if os.path.isfile(file_) and os.path.normcase(file_) not in _normcased_files:
                    will_skip.add(file_)

    will_remove = files | {os.path.join(folder, '*') for folder in folders}
    return (
     will_remove, will_skip)


class StashedUninstallPathSet(object):
    __doc__ = 'A set of file rename operations to stash files while\n    tentatively uninstalling them.'

    def __init__(self):
        self._save_dirs = {}
        self._moves = []

    def _get_directory_stash(self, path):
        """Stashes a directory.

        Directories are stashed adjacent to their original location if
        possible, or else moved/copied into the user's temp dir."""
        try:
            save_dir = AdjacentTempDirectory(path)
        except OSError:
            save_dir = TempDirectory(kind='uninstall')

        self._save_dirs[os.path.normcase(path)] = save_dir
        return save_dir.path

    def _get_file_stash(self, path):
        """Stashes a file.

        If no root has been provided, one will be created for the directory
        in the user's temp directory."""
        path = os.path.normcase(path)
        head, old_head = os.path.dirname(path), None
        save_dir = None
        while 1:
            if head != old_head:
                try:
                    save_dir = self._save_dirs[head]
                    break
                except KeyError:
                    pass

                head, old_head = os.path.dirname(head), head
        else:
            head = os.path.dirname(path)
            save_dir = TempDirectory(kind='uninstall')
            self._save_dirs[head] = save_dir

        relpath = os.path.relpath(path, head)
        if relpath:
            if relpath != os.path.curdir:
                return os.path.join(save_dir.path, relpath)
        return save_dir.path

    def stash(self, path):
        """Stashes the directory or file and returns its new location.
        Handle symlinks as files to avoid modifying the symlink targets.
        """
        path_is_dir = os.path.isdir(path) and not os.path.islink(path)
        if path_is_dir:
            new_path = self._get_directory_stash(path)
        else:
            new_path = self._get_file_stash(path)
        self._moves.append((path, new_path))
        if path_is_dir:
            if os.path.isdir(new_path):
                os.rmdir(new_path)
        renames(path, new_path)
        return new_path

    def commit(self):
        """Commits the uninstall by removing stashed files."""
        for _, save_dir in self._save_dirs.items():
            save_dir.cleanup()

        self._moves = []
        self._save_dirs = {}

    def rollback(self):
        """Undoes the uninstall by moving stashed files back."""
        for p in self._moves:
            (logger.info)(*('Moving to %s\n from %s', ), *p)

        for new_path, path in self._moves:
            try:
                logger.debug('Replacing %s from %s', new_path, path)
                if os.path.isfile(new_path) or os.path.islink(new_path):
                    os.unlink(new_path)
                else:
                    if os.path.isdir(new_path):
                        rmtree(new_path)
                renames(path, new_path)
            except OSError as ex:
                try:
                    logger.error('Failed to restore %s', new_path)
                    logger.debug('Exception: %s', ex)
                finally:
                    ex = None
                    del ex

        self.commit()

    @property
    def can_rollback(self):
        return bool(self._moves)


class UninstallPathSet(object):
    __doc__ = 'A set of file paths to be removed in the uninstallation of a\n    requirement.'

    def __init__(self, dist):
        self.paths = set()
        self._refuse = set()
        self.pth = {}
        self.dist = dist
        self._moved_paths = StashedUninstallPathSet()

    def _permitted(self, path):
        """
        Return True if the given path is one we are permitted to
        remove/modify, False otherwise.

        """
        return is_local(path)

    def add(self, path):
        head, tail = os.path.split(path)
        path = os.path.join(normalize_path(head), os.path.normcase(tail))
        if not os.path.exists(path):
            return
        elif self._permitted(path):
            self.paths.add(path)
        else:
            self._refuse.add(path)
        if os.path.splitext(path)[1] == '.py':
            if uses_pycache:
                self.add(cache_from_source(path))

    def add_pth(self, pth_file, entry):
        pth_file = normalize_path(pth_file)
        if self._permitted(pth_file):
            if pth_file not in self.pth:
                self.pth[pth_file] = UninstallPthEntries(pth_file)
            self.pth[pth_file].add(entry)
        else:
            self._refuse.add(pth_file)

    def remove(self, auto_confirm=False, verbose=False):
        """Remove paths in ``self.paths`` with confirmation (unless
        ``auto_confirm`` is True)."""
        if not self.paths:
            logger.info("Can't uninstall '%s'. No files were found to uninstall.", self.dist.project_name)
            return
        dist_name_version = self.dist.project_name + '-' + self.dist.version
        logger.info('Uninstalling %s:', dist_name_version)
        with indent_log():
            if auto_confirm or self._allowed_to_proceed(verbose):
                moved = self._moved_paths
                for_rename = compress_for_rename(self.paths)
                for path in sorted(compact(for_rename)):
                    moved.stash(path)
                    logger.debug('Removing file or directory %s', path)

                for pth in self.pth.values():
                    pth.remove()

                logger.info('Successfully uninstalled %s', dist_name_version)

    def _allowed_to_proceed(self, verbose):
        """Display which files would be deleted and prompt for confirmation
        """

        def _display(msg, paths):
            if not paths:
                return
            logger.info(msg)
            with indent_log():
                for path in sorted(compact(paths)):
                    logger.info(path)

        if not verbose:
            will_remove, will_skip = compress_for_output_listing(self.paths)
        else:
            will_remove = set(self.paths)
            will_skip = set()
        _display('Would remove:', will_remove)
        _display('Would not remove (might be manually added):', will_skip)
        _display('Would not remove (outside of prefix):', self._refuse)
        if verbose:
            _display('Will actually move:', compress_for_rename(self.paths))
        return ask('Proceed (y/n)? ', ('y', 'n')) == 'y'

    def rollback(self):
        """Rollback the changes previously made by remove()."""
        if not self._moved_paths.can_rollback:
            logger.error("Can't roll back %s; was not uninstalled", self.dist.project_name)
            return
        logger.info('Rolling back uninstall of %s', self.dist.project_name)
        self._moved_paths.rollback()
        for pth in self.pth.values():
            pth.rollback()

    def commit(self):
        """Remove temporary save dir: rollback will no longer be possible."""
        self._moved_paths.commit()

    @classmethod
    def from_dist--- This code section failed: ---

 L. 455         0  LOAD_GLOBAL              normalize_path
                2  LOAD_FAST                'dist'
                4  LOAD_ATTR                location
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  STORE_FAST               'dist_path'

 L. 456        10  LOAD_GLOBAL              dist_is_local
               12  LOAD_FAST                'dist'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  POP_JUMP_IF_TRUE     46  'to 46'

 L. 457        18  LOAD_GLOBAL              logger
               20  LOAD_METHOD              info

 L. 458        22  LOAD_STR                 'Not uninstalling %s at %s, outside environment %s'

 L. 459        24  LOAD_FAST                'dist'
               26  LOAD_ATTR                key

 L. 460        28  LOAD_FAST                'dist_path'

 L. 461        30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                prefix
               34  CALL_METHOD_4         4  '4 positional arguments'
               36  POP_TOP          

 L. 463        38  LOAD_FAST                'cls'
               40  LOAD_FAST                'dist'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  RETURN_VALUE     
             46_0  COME_FROM            16  '16'

 L. 465        46  LOAD_FAST                'dist_path'
               48  LOAD_SETCOMP             '<code_object <setcomp>>'
               50  LOAD_STR                 'UninstallPathSet.from_dist.<locals>.<setcomp>'
               52  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               54  LOAD_GLOBAL              sysconfig
               56  LOAD_METHOD              get_path
               58  LOAD_STR                 'stdlib'
               60  CALL_METHOD_1         1  '1 positional argument'

 L. 466        62  LOAD_GLOBAL              sysconfig
               64  LOAD_METHOD              get_path
               66  LOAD_STR                 'platstdlib'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  BUILD_SET_2           2 
               72  GET_ITER         
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE   104  'to 104'

 L. 468        80  LOAD_GLOBAL              logger
               82  LOAD_METHOD              info

 L. 469        84  LOAD_STR                 'Not uninstalling %s at %s, as it is in the standard library.'

 L. 470        86  LOAD_FAST                'dist'
               88  LOAD_ATTR                key

 L. 471        90  LOAD_FAST                'dist_path'
               92  CALL_METHOD_3         3  '3 positional arguments'
               94  POP_TOP          

 L. 473        96  LOAD_FAST                'cls'
               98  LOAD_FAST                'dist'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  RETURN_VALUE     
            104_0  COME_FROM            78  '78'

 L. 475       104  LOAD_FAST                'cls'
              106  LOAD_FAST                'dist'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  STORE_FAST               'paths_to_remove'

 L. 476       112  LOAD_GLOBAL              egg_link_path
              114  LOAD_FAST                'dist'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  STORE_FAST               'develop_egg_link'

 L. 477       120  LOAD_STR                 '{}.egg-info'
              122  LOAD_METHOD              format

 L. 478       124  LOAD_GLOBAL              pkg_resources
              126  LOAD_METHOD              to_filename
              128  LOAD_FAST                'dist'
              130  LOAD_ATTR                project_name
              132  CALL_METHOD_1         1  '1 positional argument'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  STORE_FAST               'develop_egg_link_egg_info'

 L. 479       138  LOAD_FAST                'dist'
              140  LOAD_ATTR                egg_info
              142  JUMP_IF_FALSE_OR_POP   156  'to 156'
              144  LOAD_GLOBAL              os
              146  LOAD_ATTR                path
              148  LOAD_METHOD              exists
              150  LOAD_FAST                'dist'
              152  LOAD_ATTR                egg_info
              154  CALL_METHOD_1         1  '1 positional argument'
            156_0  COME_FROM           142  '142'
              156  STORE_FAST               'egg_info_exists'

 L. 481       158  LOAD_GLOBAL              getattr
              160  LOAD_FAST                'dist'
              162  LOAD_ATTR                _provider
              164  LOAD_STR                 'path'
              166  LOAD_CONST               None
              168  CALL_FUNCTION_3       3  '3 positional arguments'
              170  STORE_FAST               'distutils_egg_info'

 L. 485       172  LOAD_FAST                'egg_info_exists'
          174_176  POP_JUMP_IF_FALSE   442  'to 442'
              178  LOAD_FAST                'dist'
              180  LOAD_ATTR                egg_info
              182  LOAD_METHOD              endswith
              184  LOAD_STR                 '.egg-info'
              186  CALL_METHOD_1         1  '1 positional argument'
          188_190  POP_JUMP_IF_FALSE   442  'to 442'

 L. 486       192  LOAD_FAST                'dist'
              194  LOAD_ATTR                egg_info
              196  LOAD_METHOD              endswith
              198  LOAD_FAST                'develop_egg_link_egg_info'
              200  CALL_METHOD_1         1  '1 positional argument'
          202_204  POP_JUMP_IF_TRUE    442  'to 442'

 L. 489       206  LOAD_FAST                'paths_to_remove'
              208  LOAD_METHOD              add
              210  LOAD_FAST                'dist'
              212  LOAD_ATTR                egg_info
              214  CALL_METHOD_1         1  '1 positional argument'
              216  POP_TOP          

 L. 490       218  LOAD_FAST                'dist'
              220  LOAD_METHOD              has_metadata
              222  LOAD_STR                 'installed-files.txt'
              224  CALL_METHOD_1         1  '1 positional argument'
          226_228  POP_JUMP_IF_FALSE   290  'to 290'

 L. 491       230  SETUP_LOOP          438  'to 438'
              232  LOAD_FAST                'dist'
              234  LOAD_METHOD              get_metadata

 L. 492       236  LOAD_STR                 'installed-files.txt'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  LOAD_METHOD              splitlines
              242  CALL_METHOD_0         0  '0 positional arguments'
              244  GET_ITER         
              246  FOR_ITER            286  'to 286'
              248  STORE_FAST               'installed_file'

 L. 493       250  LOAD_GLOBAL              os
              252  LOAD_ATTR                path
              254  LOAD_METHOD              normpath

 L. 494       256  LOAD_GLOBAL              os
              258  LOAD_ATTR                path
              260  LOAD_METHOD              join
              262  LOAD_FAST                'dist'
              264  LOAD_ATTR                egg_info
              266  LOAD_FAST                'installed_file'
              268  CALL_METHOD_2         2  '2 positional arguments'
              270  CALL_METHOD_1         1  '1 positional argument'
              272  STORE_FAST               'path'

 L. 496       274  LOAD_FAST                'paths_to_remove'
              276  LOAD_METHOD              add
              278  LOAD_FAST                'path'
              280  CALL_METHOD_1         1  '1 positional argument'
              282  POP_TOP          
              284  JUMP_BACK           246  'to 246'
              286  POP_BLOCK        
              288  JUMP_FORWARD        752  'to 752'
            290_0  COME_FROM           226  '226'

 L. 500       290  LOAD_FAST                'dist'
              292  LOAD_METHOD              has_metadata
              294  LOAD_STR                 'top_level.txt'
              296  CALL_METHOD_1         1  '1 positional argument'
          298_300  POP_JUMP_IF_FALSE   752  'to 752'

 L. 501       302  LOAD_FAST                'dist'
              304  LOAD_METHOD              has_metadata
              306  LOAD_STR                 'namespace_packages.txt'
              308  CALL_METHOD_1         1  '1 positional argument'
          310_312  POP_JUMP_IF_FALSE   326  'to 326'

 L. 502       314  LOAD_FAST                'dist'
              316  LOAD_METHOD              get_metadata
              318  LOAD_STR                 'namespace_packages.txt'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  STORE_DEREF              'namespaces'
              324  JUMP_FORWARD        330  'to 330'
            326_0  COME_FROM           310  '310'

 L. 504       326  BUILD_LIST_0          0 
              328  STORE_DEREF              'namespaces'
            330_0  COME_FROM           324  '324'

 L. 505       330  SETUP_LOOP          438  'to 438'

 L. 506       332  LOAD_CLOSURE             'namespaces'
              334  BUILD_TUPLE_1         1 
              336  LOAD_LISTCOMP            '<code_object <listcomp>>'
              338  LOAD_STR                 'UninstallPathSet.from_dist.<locals>.<listcomp>'
              340  MAKE_FUNCTION_8          'closure'

 L. 507       342  LOAD_FAST                'dist'
              344  LOAD_METHOD              get_metadata
              346  LOAD_STR                 'top_level.txt'
              348  CALL_METHOD_1         1  '1 positional argument'
              350  LOAD_METHOD              splitlines
              352  CALL_METHOD_0         0  '0 positional arguments'
              354  GET_ITER         
              356  CALL_FUNCTION_1       1  '1 positional argument'
              358  GET_ITER         
              360  FOR_ITER            436  'to 436'
              362  STORE_FAST               'top_level_pkg'

 L. 509       364  LOAD_GLOBAL              os
              366  LOAD_ATTR                path
              368  LOAD_METHOD              join
              370  LOAD_FAST                'dist'
              372  LOAD_ATTR                location
              374  LOAD_FAST                'top_level_pkg'
              376  CALL_METHOD_2         2  '2 positional arguments'
              378  STORE_FAST               'path'

 L. 510       380  LOAD_FAST                'paths_to_remove'
              382  LOAD_METHOD              add
              384  LOAD_FAST                'path'
              386  CALL_METHOD_1         1  '1 positional argument'
              388  POP_TOP          

 L. 511       390  LOAD_FAST                'paths_to_remove'
              392  LOAD_METHOD              add
              394  LOAD_FAST                'path'
              396  LOAD_STR                 '.py'
              398  BINARY_ADD       
              400  CALL_METHOD_1         1  '1 positional argument'
              402  POP_TOP          

 L. 512       404  LOAD_FAST                'paths_to_remove'
              406  LOAD_METHOD              add
              408  LOAD_FAST                'path'
              410  LOAD_STR                 '.pyc'
              412  BINARY_ADD       
              414  CALL_METHOD_1         1  '1 positional argument'
              416  POP_TOP          

 L. 513       418  LOAD_FAST                'paths_to_remove'
              420  LOAD_METHOD              add
              422  LOAD_FAST                'path'
              424  LOAD_STR                 '.pyo'
              426  BINARY_ADD       
              428  CALL_METHOD_1         1  '1 positional argument'
              430  POP_TOP          
          432_434  JUMP_BACK           360  'to 360'
              436  POP_BLOCK        
            438_0  COME_FROM_LOOP      330  '330'
            438_1  COME_FROM_LOOP      230  '230'
          438_440  JUMP_FORWARD        752  'to 752'
            442_0  COME_FROM           202  '202'
            442_1  COME_FROM           188  '188'
            442_2  COME_FROM           174  '174'

 L. 515       442  LOAD_FAST                'distutils_egg_info'
          444_446  POP_JUMP_IF_FALSE   468  'to 468'

 L. 516       448  LOAD_GLOBAL              UninstallationError

 L. 517       450  LOAD_STR                 'Cannot uninstall {!r}. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.'
              452  LOAD_METHOD              format

 L. 520       454  LOAD_FAST                'dist'
              456  LOAD_ATTR                project_name
              458  CALL_METHOD_1         1  '1 positional argument'
              460  CALL_FUNCTION_1       1  '1 positional argument'
              462  RAISE_VARARGS_1       1  'exception instance'
          464_466  JUMP_FORWARD        752  'to 752'
            468_0  COME_FROM           444  '444'

 L. 524       468  LOAD_FAST                'dist'
              470  LOAD_ATTR                location
              472  LOAD_METHOD              endswith
              474  LOAD_STR                 '.egg'
              476  CALL_METHOD_1         1  '1 positional argument'
          478_480  POP_JUMP_IF_FALSE   554  'to 554'

 L. 528       482  LOAD_FAST                'paths_to_remove'
              484  LOAD_METHOD              add
              486  LOAD_FAST                'dist'
              488  LOAD_ATTR                location
              490  CALL_METHOD_1         1  '1 positional argument'
              492  POP_TOP          

 L. 529       494  LOAD_GLOBAL              os
              496  LOAD_ATTR                path
              498  LOAD_METHOD              split
              500  LOAD_FAST                'dist'
              502  LOAD_ATTR                location
              504  CALL_METHOD_1         1  '1 positional argument'
              506  LOAD_CONST               1
              508  BINARY_SUBSCR    
              510  STORE_FAST               'easy_install_egg'

 L. 530       512  LOAD_GLOBAL              os
              514  LOAD_ATTR                path
              516  LOAD_METHOD              join
              518  LOAD_GLOBAL              os
              520  LOAD_ATTR                path
              522  LOAD_METHOD              dirname
              524  LOAD_FAST                'dist'
              526  LOAD_ATTR                location
              528  CALL_METHOD_1         1  '1 positional argument'

 L. 531       530  LOAD_STR                 'easy-install.pth'
              532  CALL_METHOD_2         2  '2 positional arguments'
              534  STORE_FAST               'easy_install_pth'

 L. 532       536  LOAD_FAST                'paths_to_remove'
              538  LOAD_METHOD              add_pth
              540  LOAD_FAST                'easy_install_pth'
              542  LOAD_STR                 './'
              544  LOAD_FAST                'easy_install_egg'
              546  BINARY_ADD       
              548  CALL_METHOD_2         2  '2 positional arguments'
              550  POP_TOP          
              552  JUMP_FORWARD        752  'to 752'
            554_0  COME_FROM           478  '478'

 L. 534       554  LOAD_FAST                'egg_info_exists'
          556_558  POP_JUMP_IF_FALSE   606  'to 606'
              560  LOAD_FAST                'dist'
              562  LOAD_ATTR                egg_info
              564  LOAD_METHOD              endswith
              566  LOAD_STR                 '.dist-info'
              568  CALL_METHOD_1         1  '1 positional argument'
          570_572  POP_JUMP_IF_FALSE   606  'to 606'

 L. 535       574  SETUP_LOOP          752  'to 752'
              576  LOAD_GLOBAL              uninstallation_paths
              578  LOAD_FAST                'dist'
              580  CALL_FUNCTION_1       1  '1 positional argument'
              582  GET_ITER         
              584  FOR_ITER            602  'to 602'
              586  STORE_FAST               'path'

 L. 536       588  LOAD_FAST                'paths_to_remove'
              590  LOAD_METHOD              add
              592  LOAD_FAST                'path'
              594  CALL_METHOD_1         1  '1 positional argument'
              596  POP_TOP          
          598_600  JUMP_BACK           584  'to 584'
              602  POP_BLOCK        
              604  JUMP_FORWARD        752  'to 752'
            606_0  COME_FROM           570  '570'
            606_1  COME_FROM           556  '556'

 L. 538       606  LOAD_FAST                'develop_egg_link'
          608_610  POP_JUMP_IF_FALSE   736  'to 736'

 L. 540       612  LOAD_GLOBAL              open
              614  LOAD_FAST                'develop_egg_link'
              616  LOAD_STR                 'r'
              618  CALL_FUNCTION_2       2  '2 positional arguments'
              620  SETUP_WITH          648  'to 648'
              622  STORE_FAST               'fh'

 L. 541       624  LOAD_GLOBAL              os
              626  LOAD_ATTR                path
              628  LOAD_METHOD              normcase
              630  LOAD_FAST                'fh'
              632  LOAD_METHOD              readline
              634  CALL_METHOD_0         0  '0 positional arguments'
              636  LOAD_METHOD              strip
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  CALL_METHOD_1         1  '1 positional argument'
              642  STORE_FAST               'link_pointer'
              644  POP_BLOCK        
              646  LOAD_CONST               None
            648_0  COME_FROM_WITH      620  '620'
              648  WITH_CLEANUP_START
              650  WITH_CLEANUP_FINISH
              652  END_FINALLY      

 L. 542       654  LOAD_FAST                'link_pointer'
              656  LOAD_FAST                'dist'
              658  LOAD_ATTR                location
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_TRUE    688  'to 688'
              666  LOAD_ASSERT              AssertionError

 L. 543       668  LOAD_STR                 'Egg-link {} does not match installed location of {} (at {})'
              670  LOAD_METHOD              format

 L. 545       672  LOAD_FAST                'link_pointer'
              674  LOAD_FAST                'dist'
              676  LOAD_ATTR                project_name
              678  LOAD_FAST                'dist'
              680  LOAD_ATTR                location
              682  CALL_METHOD_3         3  '3 positional arguments'
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  RAISE_VARARGS_1       1  'exception instance'
            688_0  COME_FROM           662  '662'

 L. 547       688  LOAD_FAST                'paths_to_remove'
              690  LOAD_METHOD              add
              692  LOAD_FAST                'develop_egg_link'
              694  CALL_METHOD_1         1  '1 positional argument'
              696  POP_TOP          

 L. 548       698  LOAD_GLOBAL              os
              700  LOAD_ATTR                path
              702  LOAD_METHOD              join
              704  LOAD_GLOBAL              os
              706  LOAD_ATTR                path
              708  LOAD_METHOD              dirname
              710  LOAD_FAST                'develop_egg_link'
              712  CALL_METHOD_1         1  '1 positional argument'

 L. 549       714  LOAD_STR                 'easy-install.pth'
              716  CALL_METHOD_2         2  '2 positional arguments'
              718  STORE_FAST               'easy_install_pth'

 L. 550       720  LOAD_FAST                'paths_to_remove'
              722  LOAD_METHOD              add_pth
              724  LOAD_FAST                'easy_install_pth'
              726  LOAD_FAST                'dist'
              728  LOAD_ATTR                location
              730  CALL_METHOD_2         2  '2 positional arguments'
              732  POP_TOP          
              734  JUMP_FORWARD        752  'to 752'
            736_0  COME_FROM           608  '608'

 L. 553       736  LOAD_GLOBAL              logger
              738  LOAD_METHOD              debug

 L. 554       740  LOAD_STR                 'Not sure how to uninstall: %s - Check: %s'

 L. 555       742  LOAD_FAST                'dist'
              744  LOAD_FAST                'dist'
              746  LOAD_ATTR                location
              748  CALL_METHOD_3         3  '3 positional arguments'
              750  POP_TOP          
            752_0  COME_FROM           734  '734'
            752_1  COME_FROM           604  '604'
            752_2  COME_FROM_LOOP      574  '574'
            752_3  COME_FROM           552  '552'
            752_4  COME_FROM           464  '464'
            752_5  COME_FROM           438  '438'
            752_6  COME_FROM           298  '298'

 L. 559       752  LOAD_FAST                'dist'
              754  LOAD_METHOD              has_metadata
              756  LOAD_STR                 'scripts'
              758  CALL_METHOD_1         1  '1 positional argument'
          760_762  POP_JUMP_IF_FALSE   868  'to 868'
              764  LOAD_FAST                'dist'
              766  LOAD_METHOD              metadata_isdir
              768  LOAD_STR                 'scripts'
              770  CALL_METHOD_1         1  '1 positional argument'
          772_774  POP_JUMP_IF_FALSE   868  'to 868'

 L. 560       776  SETUP_LOOP          868  'to 868'
              778  LOAD_FAST                'dist'
              780  LOAD_METHOD              metadata_listdir
              782  LOAD_STR                 'scripts'
              784  CALL_METHOD_1         1  '1 positional argument'
              786  GET_ITER         
            788_0  COME_FROM           834  '834'
              788  FOR_ITER            866  'to 866'
              790  STORE_FAST               'script'

 L. 561       792  LOAD_GLOBAL              dist_in_usersite
              794  LOAD_FAST                'dist'
              796  CALL_FUNCTION_1       1  '1 positional argument'
          798_800  POP_JUMP_IF_FALSE   808  'to 808'

 L. 562       802  LOAD_GLOBAL              bin_user
              804  STORE_FAST               'bin_dir'
              806  JUMP_FORWARD        812  'to 812'
            808_0  COME_FROM           798  '798'

 L. 564       808  LOAD_GLOBAL              bin_py
              810  STORE_FAST               'bin_dir'
            812_0  COME_FROM           806  '806'

 L. 565       812  LOAD_FAST                'paths_to_remove'
              814  LOAD_METHOD              add
              816  LOAD_GLOBAL              os
              818  LOAD_ATTR                path
              820  LOAD_METHOD              join
              822  LOAD_FAST                'bin_dir'
              824  LOAD_FAST                'script'
              826  CALL_METHOD_2         2  '2 positional arguments'
              828  CALL_METHOD_1         1  '1 positional argument'
              830  POP_TOP          

 L. 566       832  LOAD_GLOBAL              WINDOWS
          834_836  POP_JUMP_IF_FALSE   788  'to 788'

 L. 567       838  LOAD_FAST                'paths_to_remove'
              840  LOAD_METHOD              add
              842  LOAD_GLOBAL              os
              844  LOAD_ATTR                path
              846  LOAD_METHOD              join
              848  LOAD_FAST                'bin_dir'
              850  LOAD_FAST                'script'
              852  CALL_METHOD_2         2  '2 positional arguments'
              854  LOAD_STR                 '.bat'
              856  BINARY_ADD       
              858  CALL_METHOD_1         1  '1 positional argument'
              860  POP_TOP          
          862_864  JUMP_BACK           788  'to 788'
              866  POP_BLOCK        
            868_0  COME_FROM_LOOP      776  '776'
            868_1  COME_FROM           772  '772'
            868_2  COME_FROM           760  '760'

 L. 570       868  BUILD_LIST_0          0 
              870  STORE_FAST               '_scripts_to_remove'

 L. 571       872  LOAD_FAST                'dist'
              874  LOAD_ATTR                get_entry_map
              876  LOAD_STR                 'console_scripts'
              878  LOAD_CONST               ('group',)
              880  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              882  STORE_FAST               'console_scripts'

 L. 572       884  SETUP_LOOP          922  'to 922'
              886  LOAD_FAST                'console_scripts'
              888  LOAD_METHOD              keys
              890  CALL_METHOD_0         0  '0 positional arguments'
              892  GET_ITER         
              894  FOR_ITER            920  'to 920'
              896  STORE_FAST               'name'

 L. 573       898  LOAD_FAST                '_scripts_to_remove'
              900  LOAD_METHOD              extend
              902  LOAD_GLOBAL              _script_names
              904  LOAD_FAST                'dist'
              906  LOAD_FAST                'name'
              908  LOAD_CONST               False
              910  CALL_FUNCTION_3       3  '3 positional arguments'
              912  CALL_METHOD_1         1  '1 positional argument'
              914  POP_TOP          
          916_918  JUMP_BACK           894  'to 894'
              920  POP_BLOCK        
            922_0  COME_FROM_LOOP      884  '884'

 L. 575       922  LOAD_FAST                'dist'
              924  LOAD_ATTR                get_entry_map
              926  LOAD_STR                 'gui_scripts'
              928  LOAD_CONST               ('group',)
              930  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              932  STORE_FAST               'gui_scripts'

 L. 576       934  SETUP_LOOP          972  'to 972'
              936  LOAD_FAST                'gui_scripts'
              938  LOAD_METHOD              keys
              940  CALL_METHOD_0         0  '0 positional arguments'
              942  GET_ITER         
              944  FOR_ITER            970  'to 970'
              946  STORE_FAST               'name'

 L. 577       948  LOAD_FAST                '_scripts_to_remove'
              950  LOAD_METHOD              extend
              952  LOAD_GLOBAL              _script_names
              954  LOAD_FAST                'dist'
              956  LOAD_FAST                'name'
              958  LOAD_CONST               True
              960  CALL_FUNCTION_3       3  '3 positional arguments'
              962  CALL_METHOD_1         1  '1 positional argument'
              964  POP_TOP          
          966_968  JUMP_BACK           944  'to 944'
              970  POP_BLOCK        
            972_0  COME_FROM_LOOP      934  '934'

 L. 579       972  SETUP_LOOP          998  'to 998'
              974  LOAD_FAST                '_scripts_to_remove'
              976  GET_ITER         
              978  FOR_ITER            996  'to 996'
              980  STORE_FAST               's'

 L. 580       982  LOAD_FAST                'paths_to_remove'
              984  LOAD_METHOD              add
              986  LOAD_FAST                's'
              988  CALL_METHOD_1         1  '1 positional argument'
              990  POP_TOP          
          992_994  JUMP_BACK           978  'to 978'
              996  POP_BLOCK        
            998_0  COME_FROM_LOOP      972  '972'

 L. 582       998  LOAD_FAST                'paths_to_remove'
             1000  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 438_1


class UninstallPthEntries(object):

    def __init__(self, pth_file):
        self.file = pth_file
        self.entries = set()
        self._saved_lines = None

    def add(self, entry):
        entry = os.path.normcase(entry)
        if WINDOWS:
            if not os.path.splitdrive(entry)[0]:
                entry = entry.replace('\\', '/')
        self.entries.add(entry)

    def remove(self):
        logger.debug('Removing pth entries from %s:', self.file)
        if not os.path.isfile(self.file):
            logger.warning('Cannot remove entries from nonexistent file {}'.format(self.file))
            return
        else:
            with open(self.file, 'rb') as (fh):
                lines = fh.readlines()
                self._saved_lines = lines
            if any((b'\r\n' in line for line in lines)):
                endline = '\r\n'
            else:
                endline = '\n'
        if lines:
            if not lines[(-1)].endswith(endline.encode('utf-8')):
                lines[-1] = lines[(-1)] + endline.encode('utf-8')
        for entry in self.entries:
            try:
                logger.debug('Removing entry: %s', entry)
                lines.remove((entry + endline).encode('utf-8'))
            except ValueError:
                pass

        with open(self.file, 'wb') as (fh):
            fh.writelines(lines)

    def rollback(self):
        if self._saved_lines is None:
            logger.error('Cannot roll back changes to %s, none were made', self.file)
            return False
        logger.debug('Rolling %s back to previous state', self.file)
        with open(self.file, 'wb') as (fh):
            fh.writelines(self._saved_lines)
        return True