# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/path.py
# Compiled at: 2020-04-11 22:12:39
# Size of source mod 2**32: 14644 bytes
"""
Utility methods related to string paths
"""
from __future__ import print_function, division, absolute_import
import os, stat, string, shutil, logging, tempfile, traceback, contextlib, six
from tpDcc.libs.python import name, folder
SEPARATOR = '/'
BAD_SEPARATOR = '\\'
PATH_SEPARATOR = '//'
SERVER_PREFIX = '\\'
RELATIVE_PATH_PREFIX = './'
BAD_RELATIVE_PATH_PREFIX = '../'
WEB_PREFIX = 'https://'
NATIVE_SEPARATOR = (
 SEPARATOR, BAD_SEPARATOR)[(os.name == 'nt')]
LOGGER = logging.getLogger()

class FindUniquePath(name.FindUniqueString, object):

    def __init__(self, directory):
        if not directory:
            directory = folder.get_current_working_directory()
        self.parent_path = self._get_parent_path(directory)
        basename = get_basename(directory=directory)
        super(FindUniquePath, self).__init__(basename)

    def _get_scope_list(self):
        return folder.get_files_and_folders(directory=(self.parent_path))

    def _search(self):
        name = super(FindUniquePath, self)._search()
        return join_path(self.parent_path, name)

    def _get_parent_path(self, directory):
        return get_dirname(directory)


@contextlib.contextmanager
def cd(new_dir, cleanup=lambda : True):
    prev_dir = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(prev_dir)
        cleanup()


@contextlib.contextmanager
def temp_dir():
    dir_path = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dir_path)

    with cd(dir_path, cleanup):
        yield dir_path


def normalize_path(path):
    """
    Normalizes a path to make sure that path only contains forward slashes
    :param path: str, path to normalize
    :return: str, normalized path
    """
    path = path.replace(BAD_SEPARATOR, SEPARATOR).replace(PATH_SEPARATOR, SEPARATOR)
    path = six.u(str(path))
    return path.rstrip('/')


def normalize_paths(paths):
    """
    Normalize all the given paths into a consistent format
    :param paths: list(str)
    :return: list(str)
    """
    return [normalize_path(path) for path in paths]


def clean_path(path):
    """
    Cleans a path. Useful to resolve problems with slashes
    :param path: str
    :return: str, clean path
    """
    path = os.path.expanduser(str(path))
    path = normalize_path(path.strip())
    is_server_path = path.startswith(SERVER_PREFIX)
    while SERVER_PREFIX in path:
        path = path.replace(SERVER_PREFIX, PATH_SEPARATOR)

    if is_server_path:
        path = PATH_SEPARATOR + path
    if not path.find(WEB_PREFIX) > -1:
        path = path.replace(PATH_SEPARATOR, SEPARATOR)
    return path


def real_path(path):
    """
    Returns the given path removing any symbolic link
    :param path: str
    :return: str
    """
    path = os.path.realpath(path)
    path = os.path.expanduser(path)
    return normalize_path(path)


def join_path(dir1, dir2):
    """
    Appends dir2 to the end of dir1
    :param dir1: str
    :param dir2: str
    :return: str, combined directory path
    """
    if not dir1 or not dir2:
        return
    else:
        dir1 = clean_path(dir1)
        dir2 = clean_path(dir2)
        dir_path = '{0}/{1}'.format(dir1, dir2)
        dir_path = clean_path(dir_path)
        return dir_path


def split_path(path):
    """
    Split the given path into directory, basename and extension
    :param path:
    :return: list(str)
    """
    path = normalize_path(path)
    filename, extension = os.path.splitext(path)
    return (
     os.path.dirname(filename), os.path.basename(filename), extension)


def get_relative_path(path, start):
    """
    Gets a relative path from a start path
    :param path: str, path to get relative path
    :param start: str, Start path to calculate the relative path from
    """
    rpath = start
    for i in range(0, 3):
        rpath = os.path.dirname(rpath)
        token = os.path.relpath(rpath, start)
        rpath = normalize_path(rpath)
        token = normalize_path(token)
        if rpath.endswith('/'):
            rpath = rpath[:-1]
        path = path.replace(rpath, token)

    return path


def get_absolute_path(path, start):
    """
    Gets an absolute path from a start path
    :param path: str, path to get absolute path
    :param start: str, Start path to calculate the absolute path from
    """
    path = path.replace('\\', '/')
    if not os.path.isdir(start):
        start = os.path.dirname(start).replace('\\', '/')
    else:
        start = start.replace('\\', '/')
    return os.path.abspath(os.path.join(start, path)).replace('\\', '/')


def get_absolute_file_paths(root_directory):
    """
    Returns a generator with all absolute paths on a folder (and sub folders)
    :param root_directory: str, directory to start looking
    """
    for root, _, files in os.walk(root_directory):
        for f in files:
            yield os.path.abspath(os.path.join(root, f))


def get_immediate_subdirectories(root_directory):
    """
    Returns a list with intermediate subdirectories of root directory
    :param root_directory: str, directory to start looking
    """
    return [os.path.join(root_directory, name) for name in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, name))]


def get_extension(path):
    """
    Returns the exctension of a file path (wihtout the period)
    :param path: str, valid path to a file
    :return: str
    """
    return os.path.splitext(path)[1][1:]


def exists(directory):
    """
    Returns true if the given path exists
    :param directory: str
    :return: bool
    """
    return os.path.exists(directory)


def has_extension(path, file_extension):
    """
    Checks if a given file path has a specific given file extension
    :param path: str, file path
    :param file_extension: str, valid file extension
    :return: bool, True if the extension of the given path matches the given extension, False otherwise
    """
    if get_extension(path=path) == file_extension:
        return True
    else:
        return False


def get_files(root, file_extension=None, recursive=False, full_path=False, stdout=False):
    """
    Get all files from a given directory
    :param root: str, path to get directories from
    :param file_extension: str, file extension of files to search for
    :param recursive: bool, True if the function will search deeper than one level of files
    :param full_path: str, the output of the path will be the full path if True
    :param stdout: print results in Python output if True
    :return: list<str>, list of files
    """

    def out(data):
        for i in data:
            print(i)
            print('Found {0} files'.format(len(data)))

    if len(root):
        root = clean_path(root)
        directories = [d for d in os.listdir(root) if is_dir(root, d)]
        if file_extension:
            if full_path:
                files = [clean_path(os.path.abspath(os.path.join(root, f))) for f in os.listdir(root) if is_file(root, f) if has_extension(f, file_extension)]
            else:
                files = [f for f in os.listdir(root) if is_file(root, f) if has_extension(f, file_extension)]
        else:
            if full_path:
                files = [clean_path(os.path.abspath(os.path.join(root, f))) for f in os.listdir(root) if is_file(root, f)]
            else:
                files = [f for f in os.listdir(root) if is_file(root, f)]
        if len(directories):
            if recursive:
                more_files = [get_files(os.path.join(root, d), file_extension, recursive, full_path) for d in directories]
                if len(more_files):
                    for chunk in more_files:
                        files.extend(chunk)

        output = [clean_path(p) for p in files]
        if stdout:
            out(output)
        return output


def get_folders_from_path(path):
    """
    Gets a list of sub folders in the given path
    :param path: str
    :return: list<str>
    """
    folders = list()
    while True:
        path, folder = os.path.split(path)
        if folder != '':
            folders.append(folder)
        else:
            if path != '':
                folders.append(path)
            break

    folders.reverse()
    return folders


def get_basename(directory, with_extension=True):
    """
    Get the last part of a directory name
    For example, C:/test/rig.py will return rig.py if with_extension is True of rig if with_extension is False
    :param directory: str
    :param with_extension: bool, Whether to return the file name with extension or not
    :return: variant, str || bool (if fails)
    """
    from tpDcc.libs.python import fileio
    try:
        base_name = os.path.basename(directory)
        if not with_extension:
            base_name = fileio.remove_extension(base_name)
        return base_name
    except Exception:
        return False


def get_dirname(directory):
    """
    Given a directory path, this will return the path above the last child path in the path
    For example, C:/test/rig.py will return C:/test
    :param directory: str,
    :return: variant, str || bool (if fails)
    """
    try:
        return os.path.dirname(directory)
    except Exception:
        return False


def unique_path_name(directory, padding=0):
    """
    Add padding to the given path name if it is not unique
    :param directory: str, diretory name including path
    :param padding: int, where the padding should start
    :return: str, new unique directory with path
    """
    unique_path = FindUniquePath(directory)
    unique_path.set_padding(padding)
    return unique_path.get()


def get_common_path(path1, path2):
    """
    Returns path that is common in both given paths
    :param path1: str
    :param path2: str
    :return: str, common path shared by both given paths
    """
    path1 = clean_path(path1)
    path2 = clean_path(path2)
    split_path1 = path1.split('/')
    split_path2 = path2.split('/')
    first_list = split_path1
    second_list = split_path2
    found = list()
    for i in range(len(first_list)):
        if len(second_list) <= i:
            break
        else:
            if first_list[i] == second_list[i]:
                found.append(first_list[i])
            if first_list[i] != second_list[i]:
                break

    found = string.join(found, '/')
    return found


def remove_common_path(path1, path2):
    """
    Removes path that is common in both given paths
    :param path1: str
    :param path2: str
    :return: str, path without the path shared by both given paths
    """
    path1 = clean_path(path1)
    path2 = clean_path(path2)
    split_path1 = path1.split('/')
    split_path2 = path2.split('/')
    skip = True
    new_path = list()
    for i in range(len(split_path2)):
        if skip:
            if len(split_path1) > i:
                if split_path1[i] != split_path2[i]:
                    skip = False
            if len(split_path1) - 1 < i:
                skip = False
            if not skip:
                new_path.append(split_path2[i])

    new_path = string.join(new_path, '/')
    return new_path


def remove_common_path_at_beginning(path1, path2):
    """
    Removes path that is similar on both given paths at the beginning of both of them
    :param path1: str
    :param path2: str
    :return: str
    """
    value = path2.find(path1)
    sub_part = None
    if value > -1:
        if value == 0:
            sub_part = path2[len(path1):]
    if sub_part:
        if sub_part.startswith('/'):
            sub_part = sub_part[1:]
    return sub_part


def is_dir(directory, path=None):
    """
    Checks if the given directory is a directory or not
    :param directory: str
    :return: bool
    """
    if not directory:
        return False
    else:
        if path is not None:
            directory = join_path(directory, path)
        try:
            mode = os.stat(directory)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                return True
        except Exception:
            return False

        return False


def is_file(file_path, path=None):
    """
    Checks if the given path is an existing file
    :param file_path: str
    :return: bool
    """
    if not file_path:
        return False
    else:
        if path is not None:
            file_path = join_path(file_path, path)
        try:
            mode = os.stat(file_path)[stat.ST_MODE]
            if stat.S_ISREG(mode):
                return True
        except Exception:
            return False

        return False


def move(path1, path2):
    """
    Move the folder or file pointed by path1 under the directory path2
    :param path1: str, file or folder including path
    :param path2: str, path where path1 should move to
    :return: bool, Whether the move operation was successful
    """
    try:
        shutil.move(path1, path2)
    except Exception:
        LOGGER.warning('Failed to move {0} to {1}'.format(path1, path2))
        return False
    else:
        return True


def rename(directory, name, make_unique=False):
    """
    Renames given with a new name
    :param directory: str, full path to the diretory we want to rename
    :param name: str, new name of the folder we want to rename
    :param make_unique: bool, Whether to add a number to the folder name to make it unique
    :return: str, path of the renamed folder
    """
    base_name = get_basename(directory=directory)
    if base_name == name:
        return
    parent_path = get_dirname(directory=directory)
    rename_path = join_path(parent_path, name)
    if make_unique:
        rename_path = unique_path_name(directory=rename_path)
    if is_dir(rename_path) or is_file(rename_path):
        return False
    try:
        os.chmod(directory, 511)
        message = 'rename: {0} >> {1}'.format(directory, rename_path)
        LOGGER.info(message)
        os.rename(directory, rename_path)
    except Exception:
        LOGGER.error('{}'.format(traceback.format_exc()))
        return False
    else:
        return rename_path